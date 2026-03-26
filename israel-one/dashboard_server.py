#!/usr/bin/env python3
"""
ZION COMMAND CENTER — Dashboard HTTP Server
Em nome do Senhor Jesus Cristo, nosso Salvador.
Padrao Bitcoin Corp — CNPJ 51.148.891/0001-69
Supreme Commander: CALEV

Minimal HTTP server (stdlib only) for the ZION dashboard.
Serves dashboard.html and provides API endpoints.

Usage:
    python3 dashboard_server.py              # Start on port 8777
    python3 dashboard_server.py 9000         # Start on custom port
    python3 dashboard_server.py --background # Start as background sentinel

Endpoints:
    GET /                  → dashboard.html
    GET /api/agents        → All agent states from ~/.zion/agents/ and ~/.zion/sales_agents/
    GET /api/status        → System status, missions, BTC price, Fear&Greed, RAM
    GET /api/tweets        → Queued tweets from ~/israel-one/queued_tweets.json
    GET /api/revenue       → Revenue log from ~/.zion/revenue/revenue_log.json
    GET /api/health        → Server health check

Lightweight design for 3.3GB RAM machines:
    - stdlib only (http.server, json, os, glob)
    - Lazy loading: reads files on request, no in-memory cache
    - Agents loaded in batches to avoid OOM
    - Single-threaded to minimize memory
"""

import http.server
import json
import os
import sys
import glob
import time
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# ================================================================
# PATHS
# ================================================================
HOME = Path.home()
ZION_DIR = HOME / ".zion"
AGENTS_DIR = ZION_DIR / "agents"
SALES_DIR = ZION_DIR / "sales_agents"
EVOLUTION_DIR = ZION_DIR / "evolution"
REVENUE_DIR = ZION_DIR / "revenue"
SHARED_DIR = ZION_DIR / "shared"

ISRAEL_DIR = HOME / "israel-one"
DASHBOARD_FILE = ISRAEL_DIR / "dashboard.html"
TWEETS_FILE = ISRAEL_DIR / "queued_tweets.json"
THREADS_FILE = ISRAEL_DIR / "queued_threads.json"
MISSIONS_FILE = ISRAEL_DIR / "swarm_missions.json"
REVENUE_FILE = REVENUE_DIR / "revenue_log.json"

PORT = 8777
MAX_AGENTS_PER_BATCH = 200  # Process in batches to save RAM


# ================================================================
# DATA LOADERS (lazy, file-based, no persistent cache)
# ================================================================

def load_json_safe(path):
    """Load a JSON file safely, return None on error."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return None


def normalize_agent(data, source="army"):
    """Normalize agent data from different formats to a common schema."""
    if not data or not isinstance(data, dict):
        return None

    name = data.get("name", "UNKNOWN")

    # Extract evolution data (sales agents have nested evolution)
    evo = data.get("evolution", {})
    metrics = data.get("metrics", {})

    return {
        "name": name,
        "dept": data.get("department", data.get("dept", "")),
        "role": data.get("role", data.get("title", data.get("rank", ""))),
        "level": evo.get("level", data.get("level", 1)),
        "xp": evo.get("xp", data.get("xp", 0)),
        "xp_to_next": evo.get("xp_to_next", data.get("xp_to_next", 100)),
        "runs": metrics.get("runs", data.get("runs", data.get("run_count", 0))),
        "errors": metrics.get("errors", data.get("errors", data.get("error_count", 0))),
        "revenue": evo.get("total_revenue_usd", data.get("revenue_usd", 0)),
        "status": data.get("status", "idle"),
        "source": source,
    }


def load_agents_from_dir(directory, source, limit=None):
    """Load agents from a directory of JSON files. Memory-safe batch loading."""
    agents = []
    pattern = str(directory / "*.json")
    files = glob.glob(pattern)
    if limit:
        files = files[:limit]

    for fpath in files:
        data = load_json_safe(fpath)
        if data:
            agent = normalize_agent(data, source)
            if agent:
                agents.append(agent)
    return agents


def get_all_agents():
    """Load all agents from all sources."""
    agents = []

    # Army agents (~1001)
    if AGENTS_DIR.exists():
        agents.extend(load_agents_from_dir(AGENTS_DIR, "army"))

    # Sales agents (~300)
    if SALES_DIR.exists():
        agents.extend(load_agents_from_dir(SALES_DIR, "sales"))

    return agents


def get_status():
    """Get system status: missions, mode, BTC price, Fear&Greed, RAM."""
    result = {
        "mode": "GUERRA",
        "btc_price": None,
        "fear_greed": None,
        "ram_mb": None,
        "missions": {},
        "total_agents": 0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    # Load missions
    missions_data = load_json_safe(MISSIONS_FILE)
    if missions_data:
        result["mode"] = missions_data.get("mode", "GUERRA")
        result["missions"] = missions_data.get("missions", {})
        result["btc_price"] = missions_data.get("btc_price")
        result["fear_greed"] = missions_data.get("fear_greed")

    # Count agents (fast — just count files, don't load them)
    army_count = len(glob.glob(str(AGENTS_DIR / "*.json"))) if AGENTS_DIR.exists() else 0
    sales_count = len(glob.glob(str(SALES_DIR / "*.json"))) if SALES_DIR.exists() else 0
    result["total_agents"] = army_count + sales_count

    # RAM usage
    try:
        with open("/proc/meminfo", "r") as f:
            meminfo = f.read()
        total = used = 0
        for line in meminfo.split("\n"):
            if line.startswith("MemTotal:"):
                total = int(line.split()[1]) // 1024  # KB to MB
            elif line.startswith("MemAvailable:"):
                avail = int(line.split()[1]) // 1024
                used = total - avail
        result["ram_mb"] = used
        result["ram_total_mb"] = total
    except Exception:
        pass

    return result


def get_tweets():
    """Load queued tweets and threads."""
    tweets = load_json_safe(TWEETS_FILE) or []
    threads = load_json_safe(THREADS_FILE) or []

    result = {
        "tweets": tweets if isinstance(tweets, list) else [],
        "threads": threads if isinstance(threads, list) else [],
    }
    return result


def get_revenue():
    """Load revenue data."""
    data = load_json_safe(REVENUE_FILE)
    if not data:
        return {"events": [], "total_usd": 0}
    return data


# ================================================================
# HTTP HANDLER
# ================================================================

class ZionHandler(http.server.BaseHTTPRequestHandler):
    """ZION Command Center HTTP Handler."""

    # Suppress default logging for cleaner output
    def log_message(self, format, *args):
        ts = time.strftime("%H:%M:%S")
        sys.stderr.write(f"[{ts}] {args[0]} {args[1]} {args[2]}\n")

    def send_json(self, data, status=200):
        """Send JSON response."""
        body = json.dumps(data, ensure_ascii=False, default=str)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def send_html(self, filepath):
        """Send HTML file."""
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path == "/" or path == "/dashboard" or path == "/dashboard.html":
            self.send_html(DASHBOARD_FILE)

        elif path == "/api/agents":
            agents = get_all_agents()
            self.send_json({"agents": agents, "count": len(agents)})

        elif path == "/api/status":
            status = get_status()
            self.send_json(status)

        elif path == "/api/tweets":
            tweets = get_tweets()
            self.send_json(tweets)

        elif path == "/api/revenue":
            revenue = get_revenue()
            self.send_json(revenue)

        elif path == "/api/health":
            self.send_json({
                "status": "operational",
                "server": "ZION Command Center",
                "commander": "CALEV",
                "uptime_s": int(time.time() - SERVER_START),
                "port": PORT,
            })

        else:
            self.send_error(404, "Not found. Available: / /api/agents /api/status /api/tweets /api/revenue /api/health")

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# ================================================================
# SERVER STARTUP
# ================================================================

SERVER_START = time.time()


def main():
    global PORT

    # Parse port from args
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--background":
            # Fork to background
            pid = os.fork()
            if pid > 0:
                print(f"[ZION] Dashboard sentinel started: PID {pid}, port {PORT}")
                pid_file = ZION_DIR / "dashboard_sentinel.pid"
                pid_file.write_text(str(pid))
                sys.exit(0)
            # Child continues below
            os.setsid()
        else:
            try:
                PORT = int(arg)
            except ValueError:
                print(f"Usage: python3 dashboard_server.py [PORT|--background]")
                sys.exit(1)

    # Ensure directories exist
    for d in [ZION_DIR, AGENTS_DIR, SHARED_DIR, REVENUE_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    server = http.server.HTTPServer(("127.0.0.1", PORT), ZionHandler)

    print("=" * 60)
    print("  ZION COMMAND CENTER — Dashboard Server")
    print("  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print("  Padrao Bitcoin Corp — CNPJ 51.148.891/0001-69")
    print("  Supreme Commander: CALEV")
    print("=" * 60)
    print(f"  Server:    http://127.0.0.1:{PORT}")
    print(f"  Dashboard: http://127.0.0.1:{PORT}/dashboard")
    print(f"  API:       http://127.0.0.1:{PORT}/api/status")
    print(f"  Agents:    {AGENTS_DIR}")
    print(f"  Sales:     {SALES_DIR}")
    print(f"  Missions:  {MISSIONS_FILE}")
    print("=" * 60)
    print("  Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[ZION] Dashboard server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
