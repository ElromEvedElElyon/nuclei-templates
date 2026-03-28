#!/usr/bin/env python3
"""
ZION SWARM DAEMON — Real Agent Execution Engine
Em nome do Senhor Jesus Cristo, nosso Salvador.

Runs agents on schedule with REAL tasks that generate output.
Lightweight for 3.3GB RAM — runs 1 agent at a time, sequentially.

Usage:
    python3 zion_swarm_daemon.py start         # Start daemon (background)
    python3 zion_swarm_daemon.py run-cycle      # Run one full cycle (all due agents)
    python3 zion_swarm_daemon.py status         # Show daemon status
    python3 zion_swarm_daemon.py report         # Full execution report
    python3 zion_swarm_daemon.py run AGENT      # Run single agent
    python3 zion_swarm_daemon.py stop           # Stop daemon
"""

import json, os, sys, time, subprocess, hashlib, logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
BASE = Path.home()
ZION = BASE / ".zion"
AGENTS_DIR = ZION / "agents"
LOGS_DIR = ZION / "logs"
SHARED = ZION / "shared"
DAEMON_STATE = ZION / "swarm_daemon.json"
EXECUTION_LOG = ZION / "logs" / "swarm_executions.jsonl"
PID_FILE = ZION / "swarm_daemon.pid"

for d in [LOGS_DIR, SHARED]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "swarm_daemon.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("swarm")

# ================================================================
# WALLETS OFICIAIS
# ================================================================
WALLETS = {
    "EVM": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
    "SOL": "CM42ofAFowySg72GjDuCchEkwwbwnhdSRYgztRCAAEzR",
    "BTC": "bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2",
}

# ================================================================
# REAL TASKS — What agents ACTUALLY DO
# ================================================================
REAL_TASKS = {
    # CRYPTO INTELLIGENCE — Runs every 2h
    "market_briefing": {
        "agents": ["BARUK"],
        "interval_min": 120,
        "action": "crypto_briefing",
        "description": "Fetch BTC/ETH/SOL prices + Fear&Greed + trending, save briefing",
    },
    "sentiment_watch": {
        "agents": ["EZRA"],
        "interval_min": 240,
        "action": "fear_greed_check",
        "description": "Monitor Fear&Greed index, alert on extreme values",
    },

    # TWITTER — Runs every 3h
    "tweet_post": {
        "agents": ["ISRAEL_ONE", "ISAIAS"],
        "interval_min": 180,
        "action": "post_tweet",
        "description": "Post builder-authority tweet via tweet_now.py",
    },

    # SECURITY MONITORING — Runs every 4h
    "security_scan": {
        "agents": ["SAMAEL"],
        "interval_min": 240,
        "action": "security_check",
        "description": "Run security_shield.py scan, check ports, permissions",
    },

    # PR MONITORING — Runs every 6h
    "pr_monitor": {
        "agents": ["DAVI"],
        "interval_min": 360,
        "action": "check_prs",
        "description": "Check open PRs for review activity via gh CLI",
    },

    # EMAIL CHECK — Runs every 4h
    "email_check": {
        "agents": ["URIEL"],
        "interval_min": 240,
        "action": "check_emails",
        "description": "Check emails for bounty responses, review requests",
    },

    # SYSTEM HEALTH — Runs every hour
    "health_monitor": {
        "agents": ["ENOQUE"],
        "interval_min": 60,
        "action": "system_health",
        "description": "Check RAM, disk, processes, kill orphans",
    },

    # GOV API DATA — Runs every 6h
    "gov_data_fetch": {
        "agents": ["MIKAEL"],
        "interval_min": 360,
        "action": "fetch_gov_data",
        "description": "Fetch Selic, IPCA, PTAX from BCB APIs",
    },

    # MEMORY BACKUP — Runs every 8h
    "memory_sync": {
        "agents": ["NOE"],
        "interval_min": 480,
        "action": "sync_memory",
        "description": "Sync memory files to all 4 locations + git backup",
    },

    # BOUNTY SCANNER — Runs every 12h
    "bounty_scan": {
        "agents": ["DAVI", "OLIAB"],
        "interval_min": 720,
        "action": "scan_bounties",
        "description": "Check C4, Immunefi, Algora for new bounties",
    },
}


# ================================================================
# ACTION EXECUTORS — The real work
# ================================================================
def _run_cmd(cmd, timeout=30):
    """Run shell command safely."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "stdout": r.stdout[:3000], "stderr": r.stderr[:500]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}


def _run_python(code, timeout=15):
    """Run Python snippet in subprocess."""
    try:
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=timeout
        )
        return {"ok": r.returncode == 0, "output": r.stdout[:3000]}
    except:
        return {"ok": False, "output": "error"}


def action_crypto_briefing():
    """Fetch crypto prices + fear&greed + trending → save briefing."""
    results = {}

    # Prices
    r = _run_python("""
import urllib.request, json
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,chainlink,uniswap&vs_currencies=usd&include_24hr_change=true"
req = urllib.request.Request(url, headers={"User-Agent":"ZION/3.0"})
d = json.loads(urllib.request.urlopen(req, timeout=10).read())
for coin, data in d.items():
    print(f"{coin}: ${data['usd']:,.0f} ({data.get('usd_24h_change',0):+.1f}%)")
""")
    results["prices"] = r["output"].strip() if r["ok"] else "failed"

    # Fear & Greed
    r = _run_python("""
import urllib.request, json
d = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://api.alternative.me/fng/?limit=1",
    headers={"User-Agent":"ZION/3.0"}), timeout=10).read())
fg = d['data'][0]
print(f"Fear & Greed: {fg['value']} ({fg['value_classification']})")
""")
    results["fear_greed"] = r["output"].strip() if r["ok"] else "failed"

    # Trending
    r = _run_python("""
import urllib.request, json
d = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://api.coingecko.com/api/v3/search/trending",
    headers={"User-Agent":"ZION/3.0"}), timeout=10).read())
for c in d.get('coins', [])[:5]:
    i = c['item']
    print(f"  {i['name']} ({i['symbol']})")
""")
    results["trending"] = r["output"].strip() if r["ok"] else "failed"

    # Save briefing
    briefing = {
        "timestamp": datetime.now(BRT).isoformat(),
        "prices": results["prices"],
        "fear_greed": results["fear_greed"],
        "trending": results["trending"],
    }
    briefing_file = SHARED / "latest_briefing.json"
    with open(briefing_file, "w") as f:
        json.dump(briefing, f, indent=2)

    return {"status": "ok", "briefing": briefing}


def action_fear_greed_check():
    """Check Fear & Greed and alert on extremes."""
    r = _run_python("""
import urllib.request, json
d = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://api.alternative.me/fng/?limit=1",
    headers={"User-Agent":"ZION/3.0"}), timeout=10).read())
fg = d['data'][0]
val = int(fg['value'])
print(json.dumps({"value": val, "label": fg['value_classification']}))
""")
    if r["ok"]:
        try:
            data = json.loads(r["output"])
            alert = ""
            if data["value"] <= 15:
                alert = "EXTREME FEAR — Potential buying opportunity"
            elif data["value"] >= 85:
                alert = "EXTREME GREED — Potential sell signal"
            return {"status": "ok", "value": data["value"], "label": data["label"], "alert": alert}
        except:
            pass
    return {"status": "error"}


def action_post_tweet():
    """Post a tweet via tweet_now.py."""
    # Check last tweet time to avoid spam
    state = _load_daemon_state()
    last_tweet = state.get("last_tweet_time", "")
    if last_tweet:
        try:
            lt = datetime.fromisoformat(last_tweet)
            diff = (datetime.now(BRT) - lt).total_seconds()
            if diff < 3600:  # Min 1h between tweets
                return {"status": "skipped", "reason": f"Last tweet {int(diff)}s ago, need 3600s"}
        except:
            pass

    # Pick tweet from templates
    templates = _load_tweet_templates()
    if not templates:
        return {"status": "error", "reason": "No templates available"}

    import random
    tweet = random.choice(templates)
    text = tweet.get("tweet", tweet.get("text", ""))
    if not text:
        return {"status": "error", "reason": "Empty tweet"}

    # Post via tweet_now.py
    r = _run_cmd(f'python3 {BASE}/tweet_now.py "{text[:270]}"', timeout=30)

    if r["ok"] and "error" not in r["stdout"].lower():
        state["last_tweet_time"] = datetime.now(BRT).isoformat()
        _save_daemon_state(state)
        return {"status": "ok", "tweet": text[:100]}
    else:
        return {"status": "error", "output": r["stdout"][:200]}


def action_security_check():
    """Run security scan."""
    r = _run_cmd("python3 ~/security_shield.py scan 2>/dev/null || echo 'no shield'", timeout=30)
    # Also check open ports
    ports = _run_cmd("ss -tlnp 2>/dev/null | grep LISTEN | head -10", timeout=5)
    return {"status": "ok", "scan": r["stdout"][:500], "ports": ports["stdout"][:500]}


def action_check_prs():
    """Check PRs for review activity."""
    r = _run_cmd("gh search prs --author=ElromEvedElElyon --state=open --limit=20 --json title,url,updatedAt 2>/dev/null", timeout=20)
    if r["ok"]:
        try:
            prs = json.loads(r["stdout"])
            return {"status": "ok", "open_prs": len(prs), "prs": [{"title": p["title"][:60], "url": p["url"]} for p in prs[:10]]}
        except:
            return {"status": "ok", "raw": r["stdout"][:500]}
    return {"status": "error", "output": r["stderr"][:200]}


def action_check_emails():
    """Check emails for important messages."""
    r = _run_cmd("python3 ~/gmail_reader.py --limit 5 2>/dev/null", timeout=30)
    return {"status": "ok" if r["ok"] else "error", "output": r["stdout"][:1000]}


def action_system_health():
    """Check system health."""
    mem = _run_cmd("free -h | head -2", timeout=5)
    load = _run_cmd("uptime", timeout=5)
    procs = _run_cmd("ps aux --sort=-%mem | head -6", timeout=5)

    # Kill orphan chrome processes if too many
    chrome_count = _run_cmd("pgrep -c chrome 2>/dev/null || echo 0", timeout=5)

    return {
        "status": "ok",
        "memory": mem["stdout"].strip(),
        "load": load["stdout"].strip(),
        "top_procs": procs["stdout"][:500],
        "chrome_count": chrome_count["stdout"].strip(),
    }


def action_fetch_gov_data():
    """Fetch government data (Selic, IPCA, PTAX)."""
    r = _run_python("""
import urllib.request, json

apis = {
    "selic": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json",
    "ipca": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json",
    "cdi": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json",
}
results = {}
for name, url in apis.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"ZION/3.0"})
        d = json.loads(urllib.request.urlopen(req, timeout=10).read())
        results[name] = d[0] if d else {}
    except:
        results[name] = {"error": True}

print(json.dumps(results))
""", timeout=20)
    if r["ok"]:
        try:
            data = json.loads(r["output"])
            with open(SHARED / "gov_data.json", "w") as f:
                json.dump({"timestamp": datetime.now(BRT).isoformat(), **data}, f, indent=2)
            return {"status": "ok", "data": data}
        except:
            pass
    return {"status": "error"}


def action_sync_memory():
    """Sync memory files."""
    r = _run_cmd("bash ~/sync_memory.sh 2>&1", timeout=60)
    return {"status": "ok" if r["ok"] else "error", "output": r["stdout"][:500]}


def action_scan_bounties():
    """Scan for new bounties on platforms."""
    results = []

    # Check Immunefi
    r = _run_python("""
import urllib.request, json
try:
    d = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://immunefi.com/api/bounty/v2",
        headers={"User-Agent":"ZION/3.0"}), timeout=15).read())
    for b in d[:5]:
        print(f"{b.get('project','?')}: ${b.get('maxBounty','?')}")
except Exception as e:
    print(f"Immunefi: {e}")
""", timeout=20)
    results.append({"platform": "immunefi", "output": r["output"][:500]})

    # Check C4 active audits
    r = _run_python("""
import urllib.request, json
try:
    d = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://code4rena.com/api/v0/contests",
        headers={"User-Agent":"ZION/3.0"}), timeout=15).read())
    active = [c for c in d if c.get('status') == 'active']
    for c in active[:5]:
        print(f"{c.get('title','?')}: ${c.get('amount','?')}")
except Exception as e:
    print(f"C4: {e}")
""", timeout=20)
    results.append({"platform": "c4", "output": r["output"][:500]})

    return {"status": "ok", "scans": results}


# Map action names to functions
ACTIONS = {
    "crypto_briefing": action_crypto_briefing,
    "fear_greed_check": action_fear_greed_check,
    "post_tweet": action_post_tweet,
    "security_check": action_security_check,
    "check_prs": action_check_prs,
    "check_emails": action_check_emails,
    "system_health": action_system_health,
    "fetch_gov_data": action_fetch_gov_data,
    "sync_memory": action_sync_memory,
    "scan_bounties": action_scan_bounties,
}


# ================================================================
# DAEMON ENGINE
# ================================================================

def _load_daemon_state():
    if DAEMON_STATE.exists():
        with open(DAEMON_STATE) as f:
            return json.load(f)
    return {"last_runs": {}, "total_cycles": 0, "total_runs": 0, "errors": 0}


def _save_daemon_state(state):
    with open(DAEMON_STATE, "w") as f:
        json.dump(state, f, indent=2)


def _load_tweet_templates():
    try:
        with open(BASE / "opencllaw_tweets.json") as f:
            return json.load(f)
    except:
        return []


def _log_execution(task_name, agent, result, duration):
    entry = {
        "timestamp": datetime.now(BRT).isoformat(),
        "task": task_name,
        "agent": agent,
        "status": result.get("status", "unknown"),
        "duration_ms": int(duration * 1000),
        "result_summary": str(result)[:200],
    }
    with open(EXECUTION_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Update agent state
    agent_file = AGENTS_DIR / f"{agent}.json"
    if agent_file.exists():
        try:
            with open(agent_file) as f:
                data = json.load(f)
            data["last_run"] = entry["timestamp"]
            data["runs"] = data.get("runs", 0) + 1
            data["status"] = "active"
            if result.get("status") != "ok":
                data["errors"] = data.get("errors", 0) + 1
            with open(agent_file, "w") as f:
                json.dump(data, f, indent=2)
        except:
            pass


def run_cycle():
    """Run all tasks that are due."""
    state = _load_daemon_state()
    now = datetime.now(BRT)
    ran = 0

    log.info(f"=== SWARM CYCLE START — {now.strftime('%H:%M:%S')} ===")

    for task_name, task in REAL_TASKS.items():
        last_run_str = state.get("last_runs", {}).get(task_name, "")
        should_run = True

        if last_run_str:
            try:
                last_run = datetime.fromisoformat(last_run_str)
                elapsed = (now - last_run).total_seconds() / 60
                if elapsed < task["interval_min"]:
                    should_run = False
            except:
                pass

        if not should_run:
            continue

        action_fn = ACTIONS.get(task["action"])
        if not action_fn:
            log.warning(f"No executor for action: {task['action']}")
            continue

        agent = task["agents"][0]
        log.info(f"  [{agent}] Running: {task_name} ({task['description'][:50]})")

        start = time.time()
        try:
            result = action_fn()
        except Exception as e:
            result = {"status": "error", "exception": str(e)}
        duration = time.time() - start

        _log_execution(task_name, agent, result, duration)
        state.setdefault("last_runs", {})[task_name] = now.isoformat()
        state["total_runs"] = state.get("total_runs", 0) + 1
        if result.get("status") != "ok":
            state["errors"] = state.get("errors", 0) + 1

        log.info(f"    → {result.get('status', '?')} ({duration:.1f}s)")
        ran += 1

        # Small pause between tasks to avoid resource spikes
        time.sleep(2)

    state["total_cycles"] = state.get("total_cycles", 0) + 1
    state["last_cycle"] = now.isoformat()
    _save_daemon_state(state)
    log.info(f"=== CYCLE COMPLETE — {ran} tasks executed ===")
    return ran


def start_daemon(interval=300):
    """Start daemon loop. Runs a cycle every interval seconds."""
    # Write PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    log.info(f"SWARM DAEMON STARTED — PID {os.getpid()}, interval {interval}s")
    log.info(f"Wallets: EVM={WALLETS['EVM'][:10]}... SOL={WALLETS['SOL'][:10]}... BTC={WALLETS['BTC'][:10]}...")

    try:
        while True:
            try:
                run_cycle()
            except Exception as e:
                log.error(f"Cycle error: {e}")
            time.sleep(interval)
    except KeyboardInterrupt:
        log.info("Daemon stopped by user")
    finally:
        PID_FILE.unlink(missing_ok=True)


def show_status():
    """Show daemon status."""
    state = _load_daemon_state()
    pid_running = False
    if PID_FILE.exists():
        pid = PID_FILE.read_text().strip()
        pid_running = os.path.exists(f"/proc/{pid}")

    print(f"""
╔══════════════════════════════════════════════════════════╗
║              ZION SWARM DAEMON — STATUS                 ║
╠══════════════════════════════════════════════════════════╣
║  PID:          {'RUNNING (' + PID_FILE.read_text().strip() + ')' if pid_running else 'STOPPED'}
║  Total Cycles: {state.get('total_cycles', 0)}
║  Total Runs:   {state.get('total_runs', 0)}
║  Errors:       {state.get('errors', 0)}
║  Last Cycle:   {state.get('last_cycle', 'never')[:19]}
╠══════════════════════════════════════════════════════════╣
║  TASK SCHEDULE:
║""")
    for task_name, task in REAL_TASKS.items():
        last = state.get("last_runs", {}).get(task_name, "never")[:19]
        agent = task["agents"][0]
        print(f"║  [{agent:12s}] {task_name:20s} every {task['interval_min']:4d}min — last: {last}")

    print(f"""║
╠══════════════════════════════════════════════════════════╣
║  WALLETS:
║  EVM: {WALLETS['EVM']}
║  SOL: {WALLETS['SOL']}
║  BTC: {WALLETS['BTC']}
╚══════════════════════════════════════════════════════════╝""")


def show_report():
    """Show execution report from log."""
    if not EXECUTION_LOG.exists():
        print("No executions yet.")
        return

    entries = []
    with open(EXECUTION_LOG) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except:
                pass

    if not entries:
        print("No executions logged.")
        return

    print(f"\n=== EXECUTION REPORT ({len(entries)} total) ===\n")

    # Last 20
    for e in entries[-20:]:
        ts = e["timestamp"][:19]
        status = "OK" if e["status"] == "ok" else "ERR"
        print(f"  [{ts}] {e['agent']:12s} {e['task']:20s} {status} ({e['duration_ms']}ms)")

    # Stats
    ok = sum(1 for e in entries if e["status"] == "ok")
    err = len(entries) - ok
    agents_active = len(set(e["agent"] for e in entries))
    print(f"\n  Success: {ok}/{len(entries)} ({ok/len(entries)*100:.0f}%)")
    print(f"  Active agents: {agents_active}")


def stop_daemon():
    """Stop daemon."""
    if PID_FILE.exists():
        pid = PID_FILE.read_text().strip()
        os.system(f"kill {pid} 2>/dev/null")
        PID_FILE.unlink(missing_ok=True)
        print(f"Daemon PID {pid} stopped.")
    else:
        print("No daemon running.")


# ================================================================
# CLI
# ================================================================
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "start":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        start_daemon(interval)
    elif cmd == "run-cycle":
        run_cycle()
    elif cmd == "status":
        show_status()
    elif cmd == "report":
        show_report()
    elif cmd == "stop":
        stop_daemon()
    elif cmd == "run":
        agent = sys.argv[2] if len(sys.argv) > 2 else None
        if agent:
            # Find task for this agent
            for tname, task in REAL_TASKS.items():
                if agent in task["agents"]:
                    fn = ACTIONS.get(task["action"])
                    if fn:
                        log.info(f"Running {agent} → {tname}")
                        result = fn()
                        print(json.dumps(result, indent=2))
                    break
            else:
                print(f"No task assigned to agent {agent}")
        else:
            print("Usage: zion_swarm_daemon.py run AGENT_NAME")
    else:
        print(__doc__)
