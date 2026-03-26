#!/usr/bin/env python3
"""
SENTINEL GUARDIAN — Auto-Restart Service
Em nome do Senhor Jesus Cristo, nosso Salvador.

Monitora os 7 Sentinelas a cada 60 segundos.
Se algum morrer, reinicia automaticamente.
NUNCA para. NUNCA dorme. Vigilia eterna.

Usage:
    python3 sentinel_guardian.py         # Run forever
    python3 sentinel_guardian.py check   # Single check
"""

import json, os, sys, time, subprocess, signal
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
PID_DIR = Path.home() / ".zion" / "sentinels" / "pids"
LOG_FILE = Path.home() / ".zion" / "sentinels" / "logs" / "guardian.log"
GUARDIAN_PID = Path.home() / ".zion" / "sentinels" / "guardian.pid"
BASE_DIR = Path(__file__).parent

# Write our PID
GUARDIAN_PID.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] GUARDIAN: {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def is_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, ValueError):
        return False

def restart_sentinel(name, command, log_file):
    """Restart a dead sentinel."""
    log(f"RESTARTING {name}...")
    with open(log_file, "a") as lf:
        proc = subprocess.Popen(
            command,
            stdout=lf,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            cwd=str(BASE_DIR)
        )
    pid_file = PID_DIR / f"{name}.pid"
    pid_file.write_text(str(proc.pid))
    log(f"RESTARTED {name} — PID {proc.pid}")
    return proc.pid

# Sentinel definitions matching sentinel_squad.py
SENTINELS = {
    "ISRAEL_ONE": {
        "command": ["python3", str(BASE_DIR / "agent.py"), "sentinel", "55", "90"],
    },
    "MARKET_WATCHER": {
        "command": ["python3", str(Path.home() / ".zion" / "sentinels" / "market_watcher_sentinel.py")],
    },
    "BOUNTY_SCANNER": {
        "command": ["python3", str(Path.home() / ".zion" / "sentinels" / "bounty_scanner_sentinel.py")],
    },
    "REVENUE_TRACKER": {
        "command": ["python3", str(BASE_DIR / "revenue_tracker.py"), "sentinel"],
    },
    "EVOLUTION_ENGINE": {
        "command": ["python3", str(Path.home() / ".zion" / "sentinels" / "evolution_engine_sentinel.py")],
    },
    "THREAD_GENERATOR": {
        "command": ["python3", str(Path.home() / ".zion" / "sentinels" / "thread_generator_sentinel.py")],
    },
    "SECURITY_GUARDIAN": {
        "command": ["python3", str(Path.home() / ".zion" / "sentinels" / "security_guardian_sentinel.py")],
    },
}

def check_and_restart():
    """Check all sentinels, restart any that died."""
    alive = 0
    restarted = 0

    for name, info in SENTINELS.items():
        pid_file = PID_DIR / f"{name}.pid"
        log_file = Path.home() / ".zion" / "sentinels" / "logs" / f"{name.lower()}.log"

        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                if is_alive(pid):
                    alive += 1
                    continue
            except ValueError:
                pass

        # Sentinel is dead — restart it
        log(f"DEAD: {name} — initiating restart")
        try:
            restart_sentinel(name, info["command"], log_file)
            restarted += 1
        except Exception as e:
            log(f"FAILED to restart {name}: {e}")

    return alive, restarted

def run_forever():
    """Run guardian loop forever."""
    GUARDIAN_PID.write_text(str(os.getpid()))
    log("=" * 50)
    log("SENTINEL GUARDIAN STARTING — VIGILIA ETERNA")
    log(f"PID: {os.getpid()}")
    log("Monitoring 7 sentinels every 60 seconds")
    log("'Vigiai e orai' — Mateus 26:41")
    log("=" * 50)

    while True:
        try:
            alive, restarted = check_and_restart()
            if restarted > 0:
                log(f"Status: {alive + restarted}/7 alive ({restarted} restarted)")
            # Only log every 10 min when all healthy to save disk
            elif int(time.time()) % 600 < 60:
                log(f"All {alive}/7 sentinels healthy")
        except Exception as e:
            log(f"Guardian error: {e}")

        time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        alive, restarted = check_and_restart()
        print(f"Alive: {alive}/7 | Restarted: {restarted}")
    else:
        run_forever()
