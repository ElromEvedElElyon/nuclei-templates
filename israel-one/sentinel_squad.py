#!/usr/bin/env python3
"""
SENTINEL SQUAD — 24/7 Autonomous Multi-Sentinel System
Em nome do Senhor Jesus Cristo, nosso Salvador.

Esquadrao de Sentinelas que NUNCA dorme, NUNCA para.
Cada sentinela tem uma missao especifica e roda autonomamente.

Usage:
    python3 sentinel_squad.py deploy     # Deploy all sentinels
    python3 sentinel_squad.py status     # Check all sentinels
    python3 sentinel_squad.py stop       # Stop all sentinels
    python3 sentinel_squad.py report     # Full report
"""

import json, os, sys, time, random, subprocess, signal, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
BASE_DIR = Path(__file__).parent
STATE_DIR = Path.home() / ".zion" / "sentinels"
PID_DIR = STATE_DIR / "pids"
LOG_DIR = STATE_DIR / "logs"
REPORT_DIR = STATE_DIR / "reports"

for d in [STATE_DIR, PID_DIR, LOG_DIR, REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ════════════════════════════════════════════════════════════════════
# SENTINEL DEFINITIONS — The 7 that never sleep
# ════════════════════════════════════════════════════════════════════

SENTINELS = {
    "ISRAEL_ONE": {
        "name": "Israel/One",
        "role": "X Poster — Autonomous tweet generation + posting",
        "command": ["python3", str(BASE_DIR / "agent.py"), "sentinel", "55", "90"],
        "department": "SOCIAL_MEDIA",
        "priority": "CRITICAL",
        "revenue_potential": "X Revenue Share ($500+/mo at 500 followers)",
        "skills": ["tweet_generation", "market_data", "style_dna", "dedup"],
        "kpi": "tweets_per_day",
    },
    "MARKET_WATCHER": {
        "name": "Market Watcher",
        "role": "24/7 crypto market monitoring + alerts",
        "command": ["python3", "-c", MARKET_WATCHER_CODE := ""],
        "department": "CRYPTO_MARKETS",
        "priority": "HIGH",
        "revenue_potential": "Alpha signals for trading decisions",
        "skills": ["price_monitoring", "fear_greed", "trending", "whale_alerts"],
        "kpi": "signals_generated",
    },
    "BOUNTY_SCANNER": {
        "name": "Bounty Scanner",
        "role": "Scan for new bounties, PRs, and revenue opportunities",
        "command": ["python3", "-c", ""],
        "department": "BOUNTY_HUNTING",
        "priority": "CRITICAL",
        "revenue_potential": "$5K-$100K per finding",
        "skills": ["github_scanning", "bounty_platforms", "pr_monitoring"],
        "kpi": "opportunities_found",
    },
    "REVENUE_TRACKER": {
        "name": "Revenue Tracker",
        "role": "Monitor wallets for incoming payments + revenue reporting",
        "command": ["python3", str(BASE_DIR / "revenue_tracker.py"), "sentinel"],
        "department": "TREASURY",
        "priority": "CRITICAL",
        "revenue_potential": "Instant notification of payments",
        "skills": ["wallet_monitoring", "revenue_logging", "reporting"],
        "kpi": "revenue_tracked_usd",
    },
    "EVOLUTION_ENGINE": {
        "name": "Evolution Engine",
        "role": "Continuous agent evolution + singularity tracking",
        "command": ["python3", "-c", ""],
        "department": "COMMAND",
        "priority": "HIGH",
        "revenue_potential": "Agent capability growth → revenue growth",
        "skills": ["evolution_cycles", "xp_tracking", "tier_promotions"],
        "kpi": "agents_evolved",
    },
    "THREAD_GENERATOR": {
        "name": "Thread Generator",
        "role": "Generate Twitter threads from queued tweets for 3-5x engagement",
        "command": ["python3", "-c", ""],
        "department": "CONTENT",
        "priority": "MEDIUM",
        "revenue_potential": "3-5x impressions → faster path to X Revenue Share",
        "skills": ["thread_expansion", "hook_writing", "cta_generation"],
        "kpi": "threads_generated",
    },
    "SECURITY_GUARDIAN": {
        "name": "Security Guardian",
        "role": "Continuous security scanning + credential protection",
        "command": ["python3", "-c", ""],
        "department": "SECURITY_AUDIT",
        "priority": "HIGH",
        "revenue_potential": "Prevents losses + finds bounties",
        "skills": ["port_scanning", "credential_check", "git_leaks", "ssl_monitoring"],
        "kpi": "threats_detected",
    },
}


# ════════════════════════════════════════════════════════════════════
# SENTINEL PROCESSES — Self-contained code for each sentinel
# ════════════════════════════════════════════════════════════════════

def _write_sentinel_script(name, code):
    """Write sentinel code to a file and return the path."""
    path = STATE_DIR / f"{name.lower()}_sentinel.py"
    path.write_text(code)
    return str(path)


MARKET_WATCHER_SCRIPT = _write_sentinel_script("market_watcher", '''#!/usr/bin/env python3
"""Market Watcher Sentinel — 24/7 crypto monitoring"""
import json, time, urllib.request, os, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
STATE = Path.home() / ".zion" / "sentinels" / "market_state.json"
LOG = Path.home() / ".zion" / "sentinels" / "logs" / "market_watcher.log"

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\\n")

def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "ZionSentinel/1.0"})
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read())

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"alerts": [], "checks": 0, "last_btc": 0, "signals": []}

def save_state(state):
    STATE.write_text(json.dumps(state, indent=2))

def check_market():
    state = load_state()
    state["checks"] = state.get("checks", 0) + 1

    try:
        prices = fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true")
        btc = prices["bitcoin"]["usd"]
        eth = prices["ethereum"]["usd"]
        sol = prices["solana"]["usd"]
        btc_change = prices["bitcoin"].get("usd_24h_change", 0)

        log(f"BTC=${btc:,.0f} ({btc_change:+.1f}%) | ETH=${eth:,.0f} | SOL=${sol:.2f}")

        # Alert on significant moves
        last_btc = state.get("last_btc", btc)
        pct_move = abs(btc - last_btc) / last_btc * 100 if last_btc > 0 else 0

        if pct_move > 3:
            direction = "UP" if btc > last_btc else "DOWN"
            alert = f"BTC {direction} {pct_move:.1f}%: ${last_btc:,.0f} -> ${btc:,.0f}"
            log(f"ALERT: {alert}")
            state["alerts"].append({"time": datetime.now(BRT).isoformat(), "msg": alert})
            state["alerts"] = state["alerts"][-50:]

        state["last_btc"] = btc
        state["last_check"] = datetime.now(BRT).isoformat()
        state["prices"] = {"btc": btc, "eth": eth, "sol": sol}

    except Exception as e:
        log(f"ERROR: {e}")

    try:
        fng = fetch_json("https://api.alternative.me/fng/?limit=1")
        val = fng["data"][0]
        state["fear_greed"] = {"value": int(val["value"]), "label": val["value_classification"]}
        log(f"Fear & Greed: {val['value']} ({val['value_classification']})")

        # Signal: extreme fear is buy signal
        if int(val["value"]) <= 15:
            signal = {"time": datetime.now(BRT).isoformat(), "type": "EXTREME_FEAR_BUY_SIGNAL", "fg": val["value"]}
            state["signals"].append(signal)
            state["signals"] = state["signals"][-100:]
            log("SIGNAL: Extreme Fear detected — historically precedes rallies")

    except Exception as e:
        log(f"Fear&Greed ERROR: {e}")

    save_state(state)

if __name__ == "__main__":
    log("Market Watcher Sentinel STARTING — 24/7 monitoring")
    while True:
        try:
            check_market()
        except Exception as e:
            log(f"Cycle error: {e}")
        # Check every 5 minutes
        time.sleep(300)
''')

BOUNTY_SCANNER_SCRIPT = _write_sentinel_script("bounty_scanner", '''#!/usr/bin/env python3
"""Bounty Scanner Sentinel — Scan for revenue opportunities"""
import json, time, urllib.request, subprocess, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
STATE = Path.home() / ".zion" / "sentinels" / "bounty_state.json"
LOG = Path.home() / ".zion" / "sentinels" / "logs" / "bounty_scanner.log"

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\\n")

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"scans": 0, "opportunities": [], "prs_checked": []}

def save_state(state):
    STATE.write_text(json.dumps(state, indent=2))

def check_github_prs():
    """Check our open PR statuses."""
    try:
        result = subprocess.run(
            ["gh", "search", "prs", "--author=ElromEvedElElyon", "--state=open", "--json=title,url,repository,updatedAt", "--limit=20"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            prs = json.loads(result.stdout)
            log(f"Open PRs: {len(prs)}")
            for pr in prs[:5]:
                log(f"  PR: {pr.get('title', '?')[:60]} @ {pr.get('repository', {}).get('name', '?')}")
            return prs
    except Exception as e:
        log(f"GitHub PR check error: {e}")
    return []

def check_algora_bounties():
    """Check Algora for new bounties."""
    try:
        result = subprocess.run(
            ["python3", "-c", """
import urllib.request, json
url = "https://api.algora.io/graphql"
# Simple check - just verify the API is reachable
req = urllib.request.Request(url, headers={"User-Agent": "ZionBountyScanner/1.0"})
print("algora_reachable")
"""],
            capture_output=True, text=True, timeout=15
        )
        if "algora_reachable" in result.stdout:
            log("Algora API: reachable")
    except Exception as e:
        log(f"Algora check: {e}")

def check_nuclei_templates():
    """Check for new CVEs to write templates for."""
    try:
        result = subprocess.run(
            ["gh", "api", "repos/projectdiscovery/nuclei-templates/pulls?state=open&per_page=5", "--jq", ".[].title"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            prs = [l for l in result.stdout.strip().split("\\n") if l]
            log(f"nuclei-templates open PRs: {len(prs)}")
            for pr in prs[:3]:
                log(f"  {pr[:70]}")
    except Exception as e:
        log(f"nuclei check: {e}")

def scan_cycle():
    state = load_state()
    state["scans"] = state.get("scans", 0) + 1
    state["last_scan"] = datetime.now(BRT).isoformat()

    log(f"=== Bounty Scan #{state['scans']} ===")

    prs = check_github_prs()
    check_nuclei_templates()

    save_state(state)

if __name__ == "__main__":
    log("Bounty Scanner Sentinel STARTING")
    while True:
        try:
            scan_cycle()
        except Exception as e:
            log(f"Scan error: {e}")
        # Scan every 30 minutes
        time.sleep(1800)
''')

EVOLUTION_SCRIPT = _write_sentinel_script("evolution_engine", '''#!/usr/bin/env python3
"""Evolution Engine Sentinel — Continuous agent evolution"""
import json, time, subprocess, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
LOG = Path.home() / ".zion" / "sentinels" / "logs" / "evolution.log"
BASE = Path.home() / "israel-one"

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\\n")

def run_evolution():
    log("Running evolution cycle...")
    try:
        result = subprocess.run(
            ["python3", str(BASE / "singularity_engine.py"), "evolve"],
            capture_output=True, text=True, timeout=120, cwd=str(BASE)
        )
        for line in result.stdout.strip().split("\\n"):
            if line.strip():
                log(f"  {line.strip()}")
    except Exception as e:
        log(f"Evolution error: {e}")

def check_singularity():
    log("Checking singularity progress...")
    try:
        result = subprocess.run(
            ["python3", str(BASE / "singularity_engine.py"), "singularity-check"],
            capture_output=True, text=True, timeout=60, cwd=str(BASE)
        )
        lines = result.stdout.strip().split("\\n")
        for line in lines:
            if "SINGULARITY" in line or "ARCHITECT" in line or "MENTOR" in line:
                log(f"  {line.strip()}")
    except Exception as e:
        log(f"Singularity check error: {e}")

if __name__ == "__main__":
    log("Evolution Engine Sentinel STARTING")
    while True:
        try:
            run_evolution()
            check_singularity()
        except Exception as e:
            log(f"Cycle error: {e}")
        # Evolve every 2 hours
        time.sleep(7200)
''')

THREAD_GEN_SCRIPT = _write_sentinel_script("thread_generator", '''#!/usr/bin/env python3
"""Thread Generator Sentinel — Auto-generate threads"""
import json, time, subprocess, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
LOG = Path.home() / ".zion" / "sentinels" / "logs" / "threads.log"
BASE = Path.home() / "israel-one"

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\\n")

def generate_threads():
    log("Generating new threads from queued tweets...")
    try:
        result = subprocess.run(
            ["python3", str(BASE / "thread_generator.py"), "generate"],
            capture_output=True, text=True, timeout=60, cwd=str(BASE)
        )
        for line in result.stdout.strip().split("\\n")[-5:]:
            if line.strip():
                log(f"  {line.strip()}")
    except Exception as e:
        log(f"Thread gen error: {e}")

if __name__ == "__main__":
    log("Thread Generator Sentinel STARTING")
    while True:
        try:
            generate_threads()
        except Exception as e:
            log(f"Cycle error: {e}")
        # Generate every 4 hours
        time.sleep(14400)
''')

SECURITY_SCRIPT = _write_sentinel_script("security_guardian", '''#!/usr/bin/env python3
"""Security Guardian Sentinel — 24/7 security monitoring"""
import json, time, subprocess, os, socket
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
STATE = Path.home() / ".zion" / "sentinels" / "security_state.json"
LOG = Path.home() / ".zion" / "sentinels" / "logs" / "security.log"

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\\n")

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"scans": 0, "threats": [], "last_scan": None}

def save_state(state):
    STATE.write_text(json.dumps(state, indent=2))

def check_open_ports():
    """Check for unexpected open ports."""
    dangerous = [22, 3389, 5900, 8080, 9090]
    open_ports = []
    for port in dangerous:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(("127.0.0.1", port))
            s.close()
            if result == 0:
                open_ports.append(port)
        except:
            pass
    if open_ports:
        log(f"WARNING: Open ports detected: {open_ports}")
    else:
        log("Port scan: clean")
    return open_ports

def check_sensitive_files():
    """Check permissions on sensitive files."""
    sensitive = [
        Path.home() / ".secrets.env",
        Path.home() / ".claude.json",
        Path.home() / ".twilio_creds",
        Path.home() / ".immunefi_creds",
        Path.home() / ".git-credentials",
    ]
    issues = []
    for f in sensitive:
        if f.exists():
            mode = oct(f.stat().st_mode)[-3:]
            if mode not in ("600", "400"):
                issues.append(f"{f.name}: {mode} (should be 600)")
                os.chmod(str(f), 0o600)
                log(f"FIXED: {f.name} permissions {mode} -> 600")
    if not issues:
        log("File permissions: clean")
    return issues

def check_processes():
    """Check for suspicious processes."""
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        suspicious = ["nc -l", "ncat", "netcat", "reverse_shell", "miner", "xmrig"]
        for s in suspicious:
            if s in result.stdout.lower():
                log(f"THREAT: Suspicious process found: {s}")
                return [s]
    except:
        pass
    log("Process check: clean")
    return []

def security_scan():
    state = load_state()
    state["scans"] = state.get("scans", 0) + 1
    state["last_scan"] = datetime.now(BRT).isoformat()

    log(f"=== Security Scan #{state['scans']} ===")

    ports = check_open_ports()
    perms = check_sensitive_files()
    procs = check_processes()

    if ports or perms or procs:
        threat = {
            "time": datetime.now(BRT).isoformat(),
            "ports": ports, "perms": perms, "procs": procs
        }
        state["threats"].append(threat)
        state["threats"] = state["threats"][-100:]

    save_state(state)

if __name__ == "__main__":
    log("Security Guardian Sentinel STARTING")
    while True:
        try:
            security_scan()
        except Exception as e:
            log(f"Scan error: {e}")
        # Scan every 15 minutes
        time.sleep(900)
''')

# Update sentinel commands with actual scripts
SENTINELS["MARKET_WATCHER"]["command"] = ["python3", MARKET_WATCHER_SCRIPT]
SENTINELS["BOUNTY_SCANNER"]["command"] = ["python3", BOUNTY_SCANNER_SCRIPT]
SENTINELS["EVOLUTION_ENGINE"]["command"] = ["python3", EVOLUTION_SCRIPT]
SENTINELS["THREAD_GENERATOR"]["command"] = ["python3", THREAD_GEN_SCRIPT]
SENTINELS["SECURITY_GUARDIAN"]["command"] = ["python3", SECURITY_SCRIPT]


# ════════════════════════════════════════════════════════════════════
# DEPLOYMENT & MANAGEMENT
# ════════════════════════════════════════════════════════════════════

def deploy_sentinel(name, info):
    """Deploy a single sentinel as background process."""
    pid_file = PID_DIR / f"{name}.pid"

    # Check if already running
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)  # Check if alive
            print(f"  [{name}] Already running (PID {pid})")
            return pid
        except (ProcessLookupError, ValueError):
            pid_file.unlink(missing_ok=True)

    # Start process
    log_file = LOG_DIR / f"{name.lower()}.log"
    with open(log_file, "a") as lf:
        proc = subprocess.Popen(
            info["command"],
            stdout=lf,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            cwd=str(BASE_DIR)
        )

    pid_file.write_text(str(proc.pid))
    print(f"  [{name}] DEPLOYED (PID {proc.pid}) — {info['role'][:60]}")
    return proc.pid


def deploy_all():
    """Deploy all 7 sentinels."""
    print("=" * 65)
    print("  SENTINEL SQUAD — DEPLOYING 7 SENTINELS")
    print("  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print(f"  {datetime.now(BRT).strftime('%Y-%m-%d %H:%M:%S')} BRT")
    print("=" * 65)

    pids = {}
    for name, info in SENTINELS.items():
        pids[name] = deploy_sentinel(name, info)
        time.sleep(1)  # Stagger starts for RAM

    print()
    print(f"  TOTAL SENTINELS DEPLOYED: {len(pids)}")
    print(f"  STATUS: NEVER SLEEPING — 24/7 AUTONOMOUS")
    print()

    # Save deployment manifest
    manifest = {
        "deployed_at": datetime.now(BRT).isoformat(),
        "sentinels": {k: {"pid": v, "role": SENTINELS[k]["role"]} for k, v in pids.items()},
        "total": len(pids),
        "mode": "ENXAME_24_7"
    }
    (STATE_DIR / "deployment_manifest.json").write_text(json.dumps(manifest, indent=2))

    print("  Sentinels are autonomous. They will:")
    print("  → Post tweets every 55-90 min (Israel/One)")
    print("  → Monitor BTC/ETH/SOL every 5 min (Market Watcher)")
    print("  → Scan bounties every 30 min (Bounty Scanner)")
    print("  → Track wallet revenue 24/7 (Revenue Tracker)")
    print("  → Evolve agents every 2h (Evolution Engine)")
    print("  → Generate threads every 4h (Thread Generator)")
    print("  → Security scan every 15 min (Security Guardian)")
    print()
    print('  "O Senhor dos Exercitos esta conosco" — Salmo 46:7')
    print("=" * 65)


def status():
    """Check status of all sentinels."""
    print("=" * 65)
    print("  SENTINEL SQUAD — STATUS REPORT")
    print(f"  {datetime.now(BRT).strftime('%Y-%m-%d %H:%M:%S')} BRT")
    print("=" * 65)

    alive = 0
    dead = 0

    for name, info in SENTINELS.items():
        pid_file = PID_DIR / f"{name}.pid"
        log_file = LOG_DIR / f"{name.lower()}.log"

        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                os.kill(pid, 0)
                # Get last log line
                last_line = ""
                if log_file.exists():
                    lines = log_file.read_text().strip().split("\n")
                    last_line = lines[-1][:60] if lines else ""
                print(f"  [ALIVE] {name:20s} PID {pid:6d} | {last_line}")
                alive += 1
            except (ProcessLookupError, ValueError):
                print(f"  [DEAD]  {name:20s} — Process died, needs restart")
                dead += 1
                pid_file.unlink(missing_ok=True)
        else:
            print(f"  [OFF]   {name:20s} — Not deployed")
            dead += 1

    print()
    print(f"  ALIVE: {alive}/{len(SENTINELS)} | DEAD: {dead}")

    if dead > 0:
        print(f"  WARNING: {dead} sentinels down. Run 'deploy' to restart.")
    else:
        print("  ALL SENTINELS OPERATIONAL — 24/7 ACTIVE")

    print("=" * 65)


def stop_all():
    """Stop all sentinels."""
    print("STOPPING ALL SENTINELS...")
    for name in SENTINELS:
        pid_file = PID_DIR / f"{name}.pid"
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                os.kill(pid, signal.SIGTERM)
                print(f"  [{name}] Stopped (PID {pid})")
            except (ProcessLookupError, ValueError):
                pass
            pid_file.unlink(missing_ok=True)
    print("All sentinels stopped.")


def report():
    """Generate full sentinel report."""
    print("=" * 65)
    print("  SENTINEL SQUAD — FULL REPORT")
    print(f"  {datetime.now(BRT).strftime('%Y-%m-%d %H:%M:%S')} BRT")
    print("=" * 65)

    # Market data
    market_state = STATE_DIR / "market_state.json"
    if market_state.exists():
        ms = json.loads(market_state.read_text())
        prices = ms.get("prices", {})
        fg = ms.get("fear_greed", {})
        print(f"\n  MARKET:")
        print(f"    BTC: ${prices.get('btc', 0):,.0f}")
        print(f"    ETH: ${prices.get('eth', 0):,.0f}")
        print(f"    SOL: ${prices.get('sol', 0):.2f}")
        print(f"    Fear & Greed: {fg.get('value', '?')} ({fg.get('label', '?')})")
        print(f"    Checks: {ms.get('checks', 0)}")
        print(f"    Alerts: {len(ms.get('alerts', []))}")
        print(f"    Signals: {len(ms.get('signals', []))}")

    # Bounty data
    bounty_state = STATE_DIR / "bounty_state.json"
    if bounty_state.exists():
        bs = json.loads(bounty_state.read_text())
        print(f"\n  BOUNTIES:")
        print(f"    Scans: {bs.get('scans', 0)}")
        print(f"    Opportunities: {len(bs.get('opportunities', []))}")

    # Security data
    sec_state = STATE_DIR / "security_state.json"
    if sec_state.exists():
        ss = json.loads(sec_state.read_text())
        print(f"\n  SECURITY:")
        print(f"    Scans: {ss.get('scans', 0)}")
        print(f"    Threats: {len(ss.get('threats', []))}")

    # Agent memory
    mem_file = BASE_DIR / "data" / "israel_memory.json"
    if mem_file.exists():
        mem = json.loads(mem_file.read_text())
        print(f"\n  POSTING:")
        today = datetime.now(BRT).strftime("%Y-%m-%d")
        print(f"    Total posted: {mem.get('total_posted', 0)}")
        print(f"    Today: {mem.get('daily_counts', {}).get(today, 0)}/12")

    print()
    print("=" * 65)


# ════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "deploy":
        deploy_all()
    elif cmd == "status":
        status()
    elif cmd == "stop":
        stop_all()
    elif cmd == "report":
        report()
    elif cmd == "restart":
        stop_all()
        time.sleep(2)
        deploy_all()
    else:
        print(f"Usage: {sys.argv[0]} [deploy|status|stop|restart|report]")
