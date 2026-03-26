#!/usr/bin/env python3
"""
ZION EXECUTION ENGINE — Real Agent Orchestrator for 300 Valentes.
Em nome do Senhor Jesus Cristo, nosso Salvador.
Padrao Bitcoin Corp — CNPJ 51.148.891/0001-69

The engine that makes 300 agents REAL. Each agent executes REAL work
on a round-robin schedule. 1-3 tasks run per cycle. Each agent accumulates
XP, memory, and output from ACTUAL execution.

AGENTS ARE IMMORTAL: permanent=True, inviolable=True, never_delete=True.
No agent is ever killed, deleted, or demoted. They only grow.

Usage:
    python3 zion_execution_engine.py start [interval_sec]
    python3 zion_execution_engine.py stop
    python3 zion_execution_engine.py status
    python3 zion_execution_engine.py report
    python3 zion_execution_engine.py run-group GROUP_NAME
    python3 zion_execution_engine.py run-agent AGENT_NAME
    python3 zion_execution_engine.py dry-run
"""

import json
import os
import sys
import time
import signal
import logging
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

BRT = timezone(timedelta(hours=-3))
HOME = Path.home()
ZION = HOME / ".zion"
VALENTES_DIR = ZION / "valentes"
AGENTS_DIR = ZION / "agents"
LOGS_DIR = ZION / "logs"
SHARED = ZION / "shared"
ENGINE_STATE = ZION / "engine_state.json"
ENGINE_PID = ZION / "engine.pid"
EXEC_LOG = LOGS_DIR / "engine_executions.jsonl"

for d in [LOGS_DIR, SHARED]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "engine.log"),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger("engine")

# Import task functions
try:
    from task_functions import get_task_function, TASK_REGISTRY
except ImportError:
    log.error("task_functions.py not found — engine cannot run tasks")
    TASK_REGISTRY = {}
    def get_task_function(g, s): return None


# ================================================================
# GROUP CONFIG — must match agent_roster.py
# ================================================================
GROUP_CONFIG = {
    "bounty_hunter":     {"interval_min": 120, "agents_per_cycle": 3},
    "pr_monitor":        {"interval_min": 240, "agents_per_cycle": 2},
    "revenue_watcher":   {"interval_min": 60,  "agents_per_cycle": 2},
    "market_intel":      {"interval_min": 120, "agents_per_cycle": 3},
    "tweet_army":        {"interval_min": 180, "agents_per_cycle": 2},
    "security_squad":    {"interval_min": 240, "agents_per_cycle": 2},
    "product_evangelist":{"interval_min": 360, "agents_per_cycle": 2},
    "git_warrior":       {"interval_min": 360, "agents_per_cycle": 2},
}


# ================================================================
# STATE MANAGEMENT
# ================================================================
def _load_state():
    if ENGINE_STATE.exists():
        try:
            return json.loads(ENGINE_STATE.read_text())
        except:
            pass
    return {
        "started_at": None,
        "cycles": 0,
        "total_executions": 0,
        "total_errors": 0,
        "groups": {},
    }


def _save_state(state):
    ENGINE_STATE.write_text(json.dumps(state, indent=2))


def _log_execution(agent_name, group, spec_name, result, duration_ms):
    """Append to execution log (JSONL)."""
    entry = {
        "time": datetime.now(BRT).isoformat(),
        "agent": agent_name,
        "group": group,
        "spec": spec_name,
        "status": result.get("status", "?"),
        "output": result.get("output", "")[:200],
        "duration_ms": duration_ms,
    }
    with open(EXEC_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Trim to last 2000 entries
    if EXEC_LOG.stat().st_size > 500_000:
        lines = EXEC_LOG.read_text().splitlines()
        EXEC_LOG.write_text("\n".join(lines[-2000:]) + "\n")


# ================================================================
# AGENT LOADING
# ================================================================
def load_group_roster(group_name):
    """Load all valentes in a specific group, sorted by last_run (oldest first)."""
    roster = []
    for f in VALENTES_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            if data.get("task_group") == group_name:
                data["_file"] = str(f)
                roster.append(data)
        except:
            continue

    # Sort: least recently run first (round-robin fairness)
    roster.sort(key=lambda a: a.get("memory", {}).get("last_engine_run", "1970-01-01"))
    return roster


def update_agent_after_run(agent, result, duration_ms):
    """Update agent JSON with run results. NEVER delete data."""
    filepath = agent.get("_file")
    if not filepath:
        return

    try:
        data = json.loads(Path(filepath).read_text())
    except:
        data = agent

    # Update runs counter
    data["runs"] = data.get("runs", 0) + 1

    # Update memory with latest execution
    if "memory" not in data:
        data["memory"] = {}

    data["memory"]["last_engine_run"] = datetime.now(BRT).isoformat()
    data["memory"]["last_output"] = result.get("output", "")[:500]
    data["memory"]["last_status"] = result.get("status", "unknown")
    data["memory"]["total_runs"] = data.get("runs", 0)

    # Track execution history (keep last 20)
    history = data["memory"].get("execution_history", [])
    history.append({
        "time": datetime.now(BRT).isoformat(),
        "status": result.get("status", "?"),
        "output": result.get("output", "")[:100],
        "duration_ms": duration_ms,
    })
    data["memory"]["execution_history"] = history[-20:]

    # Store data results for agent memory growth
    if result.get("data"):
        data["memory"]["last_data"] = result["data"]

    # Handle alerts
    if result.get("alert"):
        alerts = data["memory"].get("alerts", [])
        alerts.append({"time": datetime.now(BRT).isoformat(), "text": result["alert"]})
        data["memory"]["alerts"] = alerts[-10:]

    # Track errors
    if result.get("status") == "error":
        data["errors"] = data.get("errors", 0) + 1
        data["memory"]["last_error"] = result.get("output", "")[:200]

    # Update XP via singularity engine integration
    _update_xp(data, result)

    # NEVER remove permanent/inviolable/never_delete flags
    data["permanent"] = True
    data["inviolable"] = True
    data["never_delete"] = True

    # Save
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log.error(f"Failed to save {filepath}: {e}")


def _update_xp(data, result):
    """Update agent XP based on execution result."""
    xp = data.get("xp", 0)
    if result.get("status") == "ok":
        xp += 10  # Successful run
        if result.get("alert"):
            xp += 25  # Found something important
        if result.get("data", {}).get("high_value"):
            xp += 50  # Found high-value bounty
    elif result.get("status") == "error":
        xp = max(0, xp - 5)

    data["xp"] = xp

    # Level calculation (100 XP per level)
    level = max(1, xp // 100)
    data["level"] = level

    # Tier assignment
    if level >= 50:
        data["tier"] = "SINGULARITY"
    elif level >= 20:
        data["tier"] = "ARCHITECT"
    elif level >= 10:
        data["tier"] = "MENTOR"
    elif level >= 5:
        data["tier"] = "AUTONOMOUS"
    else:
        data["tier"] = "RECRUIT"


# ================================================================
# EXECUTION ENGINE
# ================================================================
def run_single_agent(agent):
    """Execute one agent's task. Returns result dict."""
    group = agent.get("task_group", "")
    spec = agent.get("specialization", {})
    spec_name = spec.get("name", "default")
    name = agent.get("name", "UNKNOWN")

    func = get_task_function(group, spec_name)
    if not func:
        return {"status": "error", "output": f"No function for {group}:{spec_name}"}

    # Build spec dict for the function
    call_spec = {
        "name": name,
        "memory": agent.get("memory", {}),
    }
    # Merge specialization params
    for k, v in spec.items():
        if k != "name":
            call_spec[k] = v

    # Execute with timing
    start = time.time()
    try:
        result = func(call_spec)
    except Exception as e:
        result = {"status": "error", "output": f"Exception: {str(e)[:200]}"}
        log.error(f"Agent {name} ({group}:{spec_name}) exception: {e}")
    duration_ms = int((time.time() - start) * 1000)

    return result, duration_ms


def run_cycle(state, dry_run=False):
    """Run one full engine cycle — check all groups, execute due agents."""
    now = datetime.now(BRT)
    cycle_start = time.time()
    executions = 0
    errors = 0

    for group_name, cfg in GROUP_CONFIG.items():
        # Check if group is due
        group_state = state["groups"].get(group_name, {})
        last_run = group_state.get("last_run", "1970-01-01T00:00:00")
        try:
            last_dt = datetime.fromisoformat(last_run)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=BRT)
            minutes_since = (now - last_dt).total_seconds() / 60
        except:
            minutes_since = 9999

        if minutes_since < cfg["interval_min"]:
            continue  # Not due yet

        # Load roster for this group
        roster = load_group_roster(group_name)
        if not roster:
            continue

        # Pick agents (round-robin — oldest first)
        agents_to_run = roster[:cfg["agents_per_cycle"]]

        for agent in agents_to_run:
            name = agent.get("name", "?")

            if dry_run:
                group = agent.get("task_group", "")
                spec_name = agent.get("specialization", {}).get("name", "default")
                func = get_task_function(group, spec_name)
                log.info(f"[DRY-RUN] {name} ({group}:{spec_name}) -> {'READY' if func else 'NO FUNC'}")
                executions += 1
                continue

            try:
                result, duration_ms = run_single_agent(agent)
                status = result.get("status", "?")
                output = result.get("output", "")[:80]
                log.info(f"[{group_name}] {name}: {status} ({duration_ms}ms) — {output}")

                # Update agent state
                update_agent_after_run(agent, result, duration_ms)

                # Log execution
                spec_name = agent.get("specialization", {}).get("name", "default")
                _log_execution(name, group_name, spec_name, result, duration_ms)

                executions += 1
                if status == "error":
                    errors += 1

            except Exception as e:
                log.error(f"Failed to run {name}: {e}")
                errors += 1

        # Update group last_run
        state["groups"][group_name] = {
            "last_run": now.isoformat(),
            "last_agents": [a.get("name", "?") for a in agents_to_run],
            "roster_size": len(roster),
        }

    # Update state
    state["cycles"] += 1
    state["total_executions"] += executions
    state["total_errors"] += errors
    state["last_cycle"] = now.isoformat()
    state["last_cycle_duration_ms"] = int((time.time() - cycle_start) * 1000)
    state["last_cycle_executions"] = executions

    _save_state(state)
    return executions, errors


def start_engine(interval_sec=300):
    """Start the main engine loop."""
    # Write PID
    ENGINE_PID.write_text(str(os.getpid()))

    # Signal handling
    running = [True]
    def handle_stop(sig, frame):
        running[0] = False
        log.info("Engine stopping (signal received)")
    signal.signal(signal.SIGTERM, handle_stop)
    signal.signal(signal.SIGINT, handle_stop)

    state = _load_state()
    state["started_at"] = datetime.now(BRT).isoformat()
    state["pid"] = os.getpid()
    _save_state(state)

    log.info(f"=== ZION EXECUTION ENGINE STARTED (PID {os.getpid()}, interval {interval_sec}s) ===")
    log.info(f"Groups: {len(GROUP_CONFIG)}, Valentes: {sum(1 for _ in VALENTES_DIR.glob('*.json'))}")

    while running[0]:
        try:
            execs, errs = run_cycle(state)
            if execs > 0:
                log.info(f"Cycle {state['cycles']}: {execs} executions, {errs} errors, {state['last_cycle_duration_ms']}ms")
        except Exception as e:
            log.error(f"Cycle error: {e}")
            traceback.print_exc()

        # Sleep in small increments for responsive shutdown
        for _ in range(interval_sec):
            if not running[0]:
                break
            time.sleep(1)

    # Cleanup
    log.info("Engine stopped")
    if ENGINE_PID.exists():
        ENGINE_PID.unlink()


def stop_engine():
    """Stop the running engine."""
    if ENGINE_PID.exists():
        try:
            pid = int(ENGINE_PID.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            log.info(f"Sent SIGTERM to engine PID {pid}")
            ENGINE_PID.unlink()
        except ProcessLookupError:
            log.info("Engine already stopped")
            ENGINE_PID.unlink()
        except Exception as e:
            log.error(f"Failed to stop: {e}")
    else:
        log.info("No engine PID file found")


def show_status():
    """Show engine status."""
    state = _load_state()
    print("=" * 60)
    print("  ZION EXECUTION ENGINE — STATUS")
    print("  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print(f"  {datetime.now(BRT).isoformat()}")
    print("=" * 60)

    # Check if running
    running = False
    if ENGINE_PID.exists():
        try:
            pid = int(ENGINE_PID.read_text().strip())
            os.kill(pid, 0)
            running = True
            print(f"  Status: RUNNING (PID {pid})")
        except:
            print("  Status: STOPPED (stale PID)")
    else:
        print("  Status: STOPPED")

    print(f"  Started: {state.get('started_at', 'never')}")
    print(f"  Cycles: {state.get('cycles', 0)}")
    print(f"  Total Executions: {state.get('total_executions', 0)}")
    print(f"  Total Errors: {state.get('total_errors', 0)}")
    print(f"  Last Cycle: {state.get('last_cycle', 'never')}")
    print(f"  Last Duration: {state.get('last_cycle_duration_ms', 0)}ms")
    print()

    # Group status
    print("  GROUPS:")
    total_agents = 0
    for group_name, cfg in GROUP_CONFIG.items():
        gs = state.get("groups", {}).get(group_name, {})
        roster_size = gs.get("roster_size", 0)
        total_agents += roster_size
        last_agents = gs.get("last_agents", [])
        last_run = gs.get("last_run", "never")
        print(f"    {group_name}: {roster_size} agents | interval {cfg['interval_min']}min | last: {last_run[:19]}")
        if last_agents:
            print(f"      Last executed: {', '.join(last_agents[:5])}")

    print(f"\n  Total Agents in Roster: {total_agents}")
    print("=" * 60)


def show_report():
    """Show detailed execution report."""
    # Read last 50 executions
    if not EXEC_LOG.exists():
        print("No executions logged yet")
        return

    lines = EXEC_LOG.read_text().strip().splitlines()
    recent = lines[-50:]

    print("=" * 70)
    print("  ZION EXECUTION ENGINE — REPORT (last 50 executions)")
    print("=" * 70)

    group_stats = {}
    for line in recent:
        try:
            entry = json.loads(line)
            group = entry.get("group", "?")
            status = entry.get("status", "?")
            group_stats.setdefault(group, {"ok": 0, "error": 0, "skipped": 0})
            group_stats[group][status] = group_stats[group].get(status, 0) + 1
        except:
            continue

    print("\n  GROUP SUMMARY:")
    for group, stats in sorted(group_stats.items()):
        total = sum(stats.values())
        ok = stats.get("ok", 0)
        print(f"    {group}: {total} runs ({ok} ok, {stats.get('error', 0)} errors)")

    print(f"\n  RECENT EXECUTIONS:")
    for line in recent[-20:]:
        try:
            e = json.loads(line)
            t = e.get("time", "?")[:19]
            print(f"    [{t}] {e.get('agent', '?'):20s} {e.get('group', '?'):18s} {e.get('status', '?'):6s} {e.get('duration_ms', 0):5d}ms | {e.get('output', '')[:50]}")
        except:
            continue


def run_group(group_name):
    """Force-run a specific group."""
    state = _load_state()
    # Reset last_run to force execution
    state["groups"][group_name] = {"last_run": "1970-01-01T00:00:00"}
    _save_state(state)

    # Run one cycle
    execs, errs = run_cycle(state)
    print(f"Group {group_name}: {execs} executions, {errs} errors")


def run_agent(agent_name):
    """Force-run a specific agent."""
    for f in VALENTES_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            if data.get("name", "").upper() == agent_name.upper():
                data["_file"] = str(f)
                result, duration_ms = run_single_agent(data)
                update_agent_after_run(data, result, duration_ms)
                print(f"Agent {agent_name}: {result.get('status')} ({duration_ms}ms)")
                print(f"  Output: {result.get('output', '')[:200]}")
                return
        except:
            continue
    print(f"Agent {agent_name} not found")


def dry_run():
    """Test all groups without executing."""
    log.info("=== DRY RUN — Testing all groups ===")
    state = _load_state()
    # Force all groups due
    for g in GROUP_CONFIG:
        state["groups"][g] = {"last_run": "1970-01-01T00:00:00"}
    _save_state(state)
    execs, errs = run_cycle(state, dry_run=True)
    log.info(f"Dry run complete: {execs} agents would execute")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "start":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        start_engine(interval)
    elif cmd == "stop":
        stop_engine()
    elif cmd == "status":
        show_status()
    elif cmd == "report":
        show_report()
    elif cmd == "run-group":
        if len(sys.argv) < 3:
            print("Usage: run-group GROUP_NAME")
        else:
            run_group(sys.argv[2])
    elif cmd == "run-agent":
        if len(sys.argv) < 3:
            print("Usage: run-agent AGENT_NAME")
        else:
            run_agent(sys.argv[2])
    elif cmd == "dry-run":
        dry_run()
    else:
        print(f"Usage: {sys.argv[0]} start|stop|status|report|run-group|run-agent|dry-run")
