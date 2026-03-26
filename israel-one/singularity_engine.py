#!/usr/bin/env python3
"""
SINGULARITY ENGINE — Auto-Evolution System for ALL ZION Agents
Em nome do Senhor Jesus Cristo, nosso Salvador.
Padrao Bitcoin Corp — CNPJ 51.148.891/0001-69

Every agent in the ZION ecosystem (Army 1001 + Sales 300 + City 100)
evolves through experience. This engine tracks XP, levels, flags,
and the path to SINGULARITY — full autonomous revenue generation.

EVOLUTION TIERS:
    Level  1-4   : RECRUIT     — Runs on schedule only
    Level  5-9   : AUTONOMOUS  — Can run without schedule
    Level 10-19  : MENTOR      — Can train sub-agents
    Level 20-49  : ARCHITECT   — Can create new tools
    Level 50+    : SINGULARITY — Full autonomy, self-modifying, revenue machine

XP FORMULA:
    +10 per successful run
    +50 per revenue event
    -5  per error
    Level up every 100 XP (Level N requires N*100 cumulative XP)

SINGULARITY SCORE:
    (revenue * 0.4) + (runs * 0.3) + (error_rate_inverse * 0.2) + (level * 0.1)
    Normalized to 0-1000 scale

Usage:
    python3 singularity_engine.py evolve              # Run evolution cycle
    python3 singularity_engine.py status              # Overall evolution status
    python3 singularity_engine.py leaderboard         # Top 20 by singularity_score
    python3 singularity_engine.py agent NAME          # Agent evolution detail
    python3 singularity_engine.py promote NAME        # Force promote agent
    python3 singularity_engine.py singularity-check   # Who is closest to singularity
    python3 singularity_engine.py record-run NAME     # Record a successful run
    python3 singularity_engine.py record-error NAME   # Record an error
    python3 singularity_engine.py record-revenue NAME AMOUNT  # Record revenue
    python3 singularity_engine.py reset NAME          # Reset agent evolution
    python3 singularity_engine.py history NAME        # Show evolution log
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ================================================================
# CONSTANTS
# ================================================================
VERSION = "1.0.0"
BRT = timezone(timedelta(hours=-3))

# XP configuration
XP_PER_RUN = 10
XP_PER_REVENUE = 50
XP_PER_ERROR = -5
XP_PER_LEVEL = 100

# Singularity score weights
WEIGHT_REVENUE = 0.4
WEIGHT_RUNS = 0.3
WEIGHT_ERROR_INV = 0.2
WEIGHT_LEVEL = 0.1

# Evolution tiers
TIER_RECRUIT = "RECRUIT"
TIER_AUTONOMOUS = "AUTONOMOUS"
TIER_MENTOR = "MENTOR"
TIER_ARCHITECT = "ARCHITECT"
TIER_SINGULARITY = "SINGULARITY"

TIERS = {
    TIER_RECRUIT:     {"min_level": 1,  "flag": None,         "description": "Runs on schedule only"},
    TIER_AUTONOMOUS:  {"min_level": 5,  "flag": "autonomous", "description": "Can run without schedule"},
    TIER_MENTOR:      {"min_level": 10, "flag": "mentor",     "description": "Can train sub-agents"},
    TIER_ARCHITECT:   {"min_level": 20, "flag": "architect",  "description": "Can create new tools"},
    TIER_SINGULARITY: {"min_level": 50, "flag": "singularity","description": "Full autonomy, self-modifying, revenue machine"},
}

# Wallets
WALLETS = {
    "EVM": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
    "SOL": "CM42ofAFowySg72GjDuCchEkwwbwnhdSRYgztRCAAEzR",
    "BTC": "bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2",
}

# ================================================================
# DIRECTORY STRUCTURE
# ================================================================
ZION_DIR = Path.home() / ".zion"
EVOLUTION_DIR = ZION_DIR / "evolution"
EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)

# Agent state directories from existing systems
ARMY_AGENTS_DIR = ZION_DIR / "agents"
SALES_AGENTS_DIR = ZION_DIR / "sales_agents"
CITY_STATE_FILE = ZION_DIR / "city_state.json"

# Evolution state
EVOLUTION_STATE_FILE = EVOLUTION_DIR / "singularity_state.json"
EVOLUTION_LOG_FILE = EVOLUTION_DIR / "evolution_log.json"
EVOLUTION_HISTORY_DIR = EVOLUTION_DIR / "history"
EVOLUTION_HISTORY_DIR.mkdir(parents=True, exist_ok=True)


# ================================================================
# AGENT SOURCES — Discover agents from all three systems
# ================================================================
def discover_army_agents():
    """Discover agents from the ZION Army (1001 agents).
    Reads state files from ~/.zion/agents/"""
    agents = {}
    if ARMY_AGENTS_DIR.exists():
        for f in ARMY_AGENTS_DIR.glob("*.json"):
            try:
                with open(f) as fp:
                    data = json.load(fp)
                name = f.stem
                agents[name] = {
                    "source": "army",
                    "name": name,
                    "runs": data.get("runs", 0),
                    "errors": data.get("errors", 0),
                    "revenue": data.get("revenue_usd", 0.0),
                    "dept": data.get("dept", data.get("department", "UNKNOWN")),
                    "role": data.get("role", "agent"),
                    "status": data.get("status", "idle"),
                }
            except (json.JSONDecodeError, OSError):
                pass
    return agents


def discover_sales_agents():
    """Discover agents from the Sales Army (300 agents).
    Reads state files from ~/.zion/sales_agents/"""
    agents = {}
    if SALES_AGENTS_DIR.exists():
        for f in SALES_AGENTS_DIR.glob("*.json"):
            try:
                with open(f) as fp:
                    data = json.load(fp)
                name = f.stem
                evo = data.get("evolution", {})
                metrics = data.get("metrics", {})
                agents[name] = {
                    "source": "sales",
                    "name": name,
                    "runs": metrics.get("runs", 0),
                    "errors": metrics.get("errors", 0),
                    "revenue": evo.get("total_revenue_usd", 0.0),
                    "dept": data.get("department", "SALES"),
                    "role": data.get("title", "SDR"),
                    "status": data.get("status", "active"),
                }
            except (json.JSONDecodeError, OSError):
                pass
    return agents


def discover_city_agents():
    """Discover agents from ZION City (100 agents).
    Reads city_state.json and individual agent files."""
    agents = {}
    if CITY_STATE_FILE.exists():
        try:
            with open(CITY_STATE_FILE) as fp:
                state = json.load(fp)
            for name, data in state.get("agents", {}).items():
                agents[name] = {
                    "source": "city",
                    "name": name,
                    "runs": data.get("runs", 0),
                    "errors": data.get("errors", 0),
                    "revenue": data.get("revenue_usd", 0.0),
                    "dept": data.get("legion", data.get("dept", "CITY")),
                    "role": data.get("role", "agent"),
                    "status": data.get("status", "idle"),
                }
        except (json.JSONDecodeError, OSError):
            pass
    return agents


def discover_all_agents():
    """Discover agents from all three systems. No duplicates."""
    all_agents = {}
    all_agents.update(discover_army_agents())
    all_agents.update(discover_sales_agents())
    all_agents.update(discover_city_agents())
    return all_agents


# ================================================================
# EVOLUTION STATE PERSISTENCE
# ================================================================
def load_evolution_state():
    """Load the evolution state from disk."""
    if EVOLUTION_STATE_FILE.exists():
        try:
            with open(EVOLUTION_STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"agents": {}, "last_cycle": None, "total_cycles": 0, "version": VERSION}


def save_evolution_state(state):
    """Save evolution state to disk. Atomic write pattern."""
    tmp = EVOLUTION_STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1, default=str)
    tmp.replace(EVOLUTION_STATE_FILE)


def get_agent_evolution(state, name):
    """Get or create evolution record for an agent."""
    if name not in state["agents"]:
        state["agents"][name] = {
            "xp": 0,
            "level": 1,
            "runs": 0,
            "errors": 0,
            "revenue": 0.0,
            "revenue_events": 0,
            "flags": [],
            "tier": TIER_RECRUIT,
            "singularity_score": 0.0,
            "promotions": 0,
            "created": now_iso(),
            "last_evolved": None,
            "last_run": None,
            "last_error": None,
            "last_revenue": None,
            "achievements": [],
            "source": "unknown",
        }
    return state["agents"][name]


def now_iso():
    """Current time in BRT as ISO string."""
    return datetime.now(BRT).isoformat()


# ================================================================
# EVOLUTION LOG
# ================================================================
def load_evolution_log():
    """Load evolution log. Keeps last 500 entries for RAM safety."""
    if EVOLUTION_LOG_FILE.exists():
        try:
            with open(EVOLUTION_LOG_FILE) as f:
                entries = json.load(f)
            # Keep only last 500 entries (RAM constraint)
            return entries[-500:] if len(entries) > 500 else entries
        except (json.JSONDecodeError, OSError):
            pass
    return []


def append_log(entries, event_type, agent_name, detail=""):
    """Append an event to the evolution log."""
    entries.append({
        "ts": now_iso(),
        "type": event_type,
        "agent": agent_name,
        "detail": detail,
    })
    # Trim to 500
    if len(entries) > 500:
        entries[:] = entries[-500:]


def save_evolution_log(entries):
    """Persist evolution log."""
    tmp = EVOLUTION_LOG_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(entries, f, indent=1, default=str)
    tmp.replace(EVOLUTION_LOG_FILE)


def save_agent_history(name, event_type, detail=""):
    """Save per-agent history file. Lightweight append-style."""
    hist_file = EVOLUTION_HISTORY_DIR / f"{name}.json"
    history = []
    if hist_file.exists():
        try:
            with open(hist_file) as f:
                history = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    history.append({"ts": now_iso(), "type": event_type, "detail": detail})
    # Keep last 100 per agent
    if len(history) > 100:
        history = history[-100:]
    with open(hist_file, "w") as f:
        json.dump(history, f, indent=1, default=str)


# ================================================================
# XP AND LEVEL CALCULATIONS
# ================================================================
def calc_xp_for_level(level):
    """Cumulative XP needed to reach a given level.
    Level 1: 0 XP, Level 2: 100 XP, Level 3: 200 XP, ..., Level N: (N-1)*100."""
    return (level - 1) * XP_PER_LEVEL


def calc_level_from_xp(xp):
    """Calculate level from total XP. Level up every 100 XP."""
    if xp < 0:
        xp = 0
    return (xp // XP_PER_LEVEL) + 1


def get_tier(level):
    """Get evolution tier from level."""
    if level >= 50:
        return TIER_SINGULARITY
    elif level >= 20:
        return TIER_ARCHITECT
    elif level >= 10:
        return TIER_MENTOR
    elif level >= 5:
        return TIER_AUTONOMOUS
    return TIER_RECRUIT


def get_flags(level):
    """Get all earned flags for a given level."""
    flags = []
    if level >= 5:
        flags.append("autonomous")
    if level >= 10:
        flags.append("mentor")
    if level >= 20:
        flags.append("architect")
    if level >= 50:
        flags.append("singularity")
    return flags


def calc_singularity_score(evo):
    """Calculate singularity score (0-1000 scale).

    Components:
        Revenue score:  revenue_usd capped at 100000 -> 0-400
        Runs score:     runs capped at 10000 -> 0-300
        Error inverse:  (1 - error_rate) -> 0-200
        Level score:    level capped at 50 -> 0-100
    """
    revenue = min(evo.get("revenue", 0.0), 100000.0)
    runs = min(evo.get("runs", 0), 10000)
    total_actions = evo.get("runs", 0) + evo.get("errors", 0)
    error_rate = evo.get("errors", 0) / max(total_actions, 1)
    error_inv = 1.0 - error_rate
    level = min(evo.get("level", 1), 50)

    score = (
        (revenue / 100000.0) * 1000 * WEIGHT_REVENUE +
        (runs / 10000.0) * 1000 * WEIGHT_RUNS +
        error_inv * 1000 * WEIGHT_ERROR_INV +
        (level / 50.0) * 1000 * WEIGHT_LEVEL
    )
    return round(score, 2)


# ================================================================
# CORE EVOLUTION OPERATIONS
# ================================================================
def record_run(name, state=None, log=None):
    """Record a successful run for an agent. Returns (state, log, leveled_up)."""
    if state is None:
        state = load_evolution_state()
    if log is None:
        log = load_evolution_log()

    evo = get_agent_evolution(state, name)
    old_level = evo["level"]

    evo["runs"] += 1
    evo["xp"] += XP_PER_RUN
    evo["last_run"] = now_iso()

    new_level = calc_level_from_xp(evo["xp"])
    leveled_up = new_level > old_level

    if leveled_up:
        evo["level"] = new_level
        evo["tier"] = get_tier(new_level)
        evo["flags"] = get_flags(new_level)
        append_log(log, "LEVEL_UP", name, f"Level {old_level} -> {new_level} ({evo['tier']})")
        save_agent_history(name, "LEVEL_UP", f"{old_level} -> {new_level}")

        # Check for tier transitions
        old_tier = get_tier(old_level)
        new_tier = get_tier(new_level)
        if old_tier != new_tier:
            evo["promotions"] += 1
            achievement = f"Reached {new_tier} tier at Level {new_level}"
            evo["achievements"].append(achievement)
            append_log(log, "TIER_UP", name, f"{old_tier} -> {new_tier}")
            save_agent_history(name, "TIER_UP", f"{old_tier} -> {new_tier}")

    evo["singularity_score"] = calc_singularity_score(evo)
    append_log(log, "RUN", name, f"XP: {evo['xp']} | Level: {evo['level']}")

    return state, log, leveled_up


def record_error(name, state=None, log=None):
    """Record an error for an agent."""
    if state is None:
        state = load_evolution_state()
    if log is None:
        log = load_evolution_log()

    evo = get_agent_evolution(state, name)

    # PROTECTION: Inviolable agents cannot lose XP or be demoted
    if evo.get("inviolable") or evo.get("permanent") or evo.get("never_delete"):
        evo["errors"] += 1
        evo["last_error"] = now_iso()
        evo["singularity_score"] = calc_singularity_score(evo)
        append_log(log, "ERROR_ABSORBED", name, f"Error absorbed — agent is INVIOLABLE")
        return state, log

    evo["errors"] += 1
    evo["xp"] = max(0, evo["xp"] + XP_PER_ERROR)  # Floor at 0
    evo["last_error"] = now_iso()

    # Recalculate level (can go down from XP loss)
    new_level = calc_level_from_xp(evo["xp"])
    if new_level < evo["level"]:
        old_level = evo["level"]
        evo["level"] = new_level
        evo["tier"] = get_tier(new_level)
        evo["flags"] = get_flags(new_level)
        append_log(log, "LEVEL_DOWN", name, f"Level {old_level} -> {new_level} (error penalty)")
        save_agent_history(name, "LEVEL_DOWN", f"{old_level} -> {new_level}")

    evo["singularity_score"] = calc_singularity_score(evo)
    append_log(log, "ERROR", name, f"Errors: {evo['errors']} | XP: {evo['xp']}")

    return state, log


def record_revenue(name, amount_usd, state=None, log=None):
    """Record a revenue event for an agent."""
    if state is None:
        state = load_evolution_state()
    if log is None:
        log = load_evolution_log()

    evo = get_agent_evolution(state, name)
    old_level = evo["level"]

    evo["revenue"] += amount_usd
    evo["revenue_events"] += 1
    evo["xp"] += XP_PER_REVENUE
    evo["last_revenue"] = now_iso()

    new_level = calc_level_from_xp(evo["xp"])
    if new_level > old_level:
        evo["level"] = new_level
        evo["tier"] = get_tier(new_level)
        evo["flags"] = get_flags(new_level)
        evo["promotions"] += 1
        append_log(log, "LEVEL_UP", name, f"Level {old_level} -> {new_level} (revenue boost)")
        save_agent_history(name, "LEVEL_UP", f"{old_level} -> {new_level}")

        old_tier = get_tier(old_level)
        new_tier = get_tier(new_level)
        if old_tier != new_tier:
            achievement = f"Reached {new_tier} via revenue at Level {new_level}"
            evo["achievements"].append(achievement)
            append_log(log, "TIER_UP", name, f"{old_tier} -> {new_tier}")

    evo["singularity_score"] = calc_singularity_score(evo)
    append_log(log, "REVENUE", name, f"${amount_usd:,.2f} | Total: ${evo['revenue']:,.2f}")
    save_agent_history(name, "REVENUE", f"${amount_usd:,.2f}")

    return state, log


def promote_agent(name, state=None, log=None):
    """Force promote an agent by granting 100 XP (1 level)."""
    if state is None:
        state = load_evolution_state()
    if log is None:
        log = load_evolution_log()

    evo = get_agent_evolution(state, name)
    old_level = evo["level"]
    evo["xp"] += XP_PER_LEVEL
    evo["level"] = calc_level_from_xp(evo["xp"])
    evo["tier"] = get_tier(evo["level"])
    evo["flags"] = get_flags(evo["level"])
    evo["promotions"] += 1
    evo["singularity_score"] = calc_singularity_score(evo)

    detail = f"Promoted: Level {old_level} -> {evo['level']} ({evo['tier']})"
    append_log(log, "PROMOTE", name, detail)
    save_agent_history(name, "PROMOTE", detail)

    return state, log, evo


# ================================================================
# EVOLUTION CYCLE — Sync all agents from all sources
# ================================================================
def run_evolution_cycle():
    """Run a full evolution cycle across ALL agent systems.

    1. Discover all agents from army, sales, city
    2. Sync their runs/errors/revenue into evolution state
    3. Recalculate XP, levels, flags, scores
    4. Persist everything
    """
    state = load_evolution_state()
    log = load_evolution_log()
    discovered = discover_all_agents()

    evolved_count = 0
    level_ups = 0
    new_agents = 0
    tier_changes = []

    for name, agent_data in discovered.items():
        evo = get_agent_evolution(state, name)

        # PROTECTION: Never overwrite inviolable/permanent sentinel state
        if evo.get("inviolable") or evo.get("permanent") or evo.get("never_delete"):
            # Only accumulate runs — never reduce level/xp/tier
            source_runs = agent_data.get("runs", 0)
            if source_runs > evo["runs"]:
                delta = source_runs - evo["runs"]
                evo["runs"] = source_runs
                evo["xp"] += delta * XP_PER_RUN
                evo["level"] = max(evo["level"], calc_level_from_xp(evo["xp"]))
            evo["singularity_score"] = max(evo["singularity_score"], calc_singularity_score(evo))
            evo["last_evolved"] = now_iso()
            evolved_count += 1
            continue

        evo["source"] = agent_data.get("source", "unknown")

        # Sync runs/errors/revenue from source system
        source_runs = agent_data.get("runs", 0)
        source_errors = agent_data.get("errors", 0)
        source_revenue = agent_data.get("revenue", 0.0)

        # Calculate deltas (new activity since last sync)
        delta_runs = max(0, source_runs - evo["runs"])
        delta_errors = max(0, source_errors - evo["errors"])
        delta_revenue = max(0.0, source_revenue - evo["revenue"])

        if delta_runs == 0 and delta_errors == 0 and delta_revenue == 0.0:
            # No new activity, just recalc score
            evo["singularity_score"] = calc_singularity_score(evo)
            continue

        old_level = evo["level"]
        old_tier = evo["tier"]

        # Apply XP changes
        xp_gain = (delta_runs * XP_PER_RUN) + (delta_errors * XP_PER_ERROR)
        if delta_revenue > 0:
            # Count revenue events proportionally (1 event per $100 minimum)
            rev_events = max(1, int(delta_revenue / 100))
            xp_gain += rev_events * XP_PER_REVENUE
            evo["revenue_events"] += rev_events

        evo["runs"] = source_runs
        evo["errors"] = source_errors
        evo["revenue"] = source_revenue
        evo["xp"] = max(0, evo["xp"] + xp_gain)
        evo["last_evolved"] = now_iso()

        # Recalculate level
        new_level = calc_level_from_xp(evo["xp"])
        if new_level != old_level:
            evo["level"] = new_level
            level_ups += abs(new_level - old_level)
            append_log(log, "LEVEL_UP" if new_level > old_level else "LEVEL_DOWN",
                       name, f"Level {old_level} -> {new_level}")
            save_agent_history(name, "LEVEL_CHANGE", f"{old_level} -> {new_level}")

        evo["tier"] = get_tier(evo["level"])
        evo["flags"] = get_flags(evo["level"])
        evo["singularity_score"] = calc_singularity_score(evo)

        # Track tier changes
        if evo["tier"] != old_tier:
            evo["promotions"] += 1
            achievement = f"Evolved to {evo['tier']} at Level {evo['level']}"
            evo["achievements"].append(achievement)
            tier_changes.append((name, old_tier, evo["tier"]))
            append_log(log, "TIER_UP", name, f"{old_tier} -> {evo['tier']}")
            save_agent_history(name, "TIER_UP", f"{old_tier} -> {evo['tier']}")

        evolved_count += 1

    # Also register any agents in evolution state not found in sources
    # (they keep their state, just recalc score)
    for name in state["agents"]:
        if name not in discovered:
            evo = state["agents"][name]
            evo["singularity_score"] = calc_singularity_score(evo)

    state["last_cycle"] = now_iso()
    state["total_cycles"] = state.get("total_cycles", 0) + 1

    save_evolution_state(state)
    save_evolution_log(log)

    return {
        "total_discovered": len(discovered),
        "evolved": evolved_count,
        "level_ups": level_ups,
        "tier_changes": tier_changes,
        "new_agents": new_agents,
        "total_in_state": len(state["agents"]),
        "cycle": state["total_cycles"],
    }


# ================================================================
# CLI COMMANDS
# ================================================================
def cmd_evolve():
    """Run evolution cycle across ALL agents."""
    print(f"\n  SINGULARITY ENGINE — Evolution Cycle")
    print(f"  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print(f"  {now_iso()}")
    print(f"  {'='*55}")

    result = run_evolution_cycle()

    print(f"  Agents Discovered:  {result['total_discovered']}")
    print(f"  Agents Evolved:     {result['evolved']}")
    print(f"  Level Ups:          {result['level_ups']}")
    print(f"  Tier Changes:       {len(result['tier_changes'])}")
    print(f"  Total in Registry:  {result['total_in_state']}")
    print(f"  Cycle #:            {result['cycle']}")

    if result["tier_changes"]:
        print(f"\n  TIER PROMOTIONS:")
        for name, old_t, new_t in result["tier_changes"]:
            print(f"    {name:25s} {old_t:15s} -> {new_t}")

    print(f"\n  Evolution cycle complete.")


def cmd_status():
    """Show overall evolution status."""
    state = load_evolution_state()
    agents = state.get("agents", {})

    total = len(agents)
    tier_counts = {t: 0 for t in TIERS}
    total_xp = 0
    total_runs = 0
    total_errors = 0
    total_revenue = 0.0
    source_counts = {"army": 0, "sales": 0, "city": 0, "unknown": 0}
    singularity_agents = []

    for name, evo in agents.items():
        tier = evo.get("tier", TIER_RECRUIT)
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        total_xp += evo.get("xp", 0)
        total_runs += evo.get("runs", 0)
        total_errors += evo.get("errors", 0)
        total_revenue += evo.get("revenue", 0.0)
        src = evo.get("source", "unknown")
        source_counts[src] = source_counts.get(src, 0) + 1
        if tier == TIER_SINGULARITY:
            singularity_agents.append(name)

    avg_level = (total_xp / max(total, 1)) / XP_PER_LEVEL + 1
    error_rate = total_errors / max(total_runs + total_errors, 1) * 100

    print(f"""
{'='*62}
  SINGULARITY ENGINE — STATUS DASHBOARD
  Em nome do Senhor Jesus Cristo, nosso Salvador
  Padrao Bitcoin Corp | CNPJ 51.148.891/0001-69
  {now_iso()}
{'='*62}
  Total Agents:     {total:,d}
  Total XP:         {total_xp:,d}
  Avg Level:        {avg_level:.1f}
  Total Runs:       {total_runs:,d}
  Total Errors:     {total_errors:,d}  ({error_rate:.1f}% error rate)
  Total Revenue:    ${total_revenue:,.2f}
  Evolution Cycles: {state.get('total_cycles', 0)}
  Last Cycle:       {state.get('last_cycle', 'never')}
{'-'*62}
  AGENT SOURCES:
    Army (1001):    {source_counts.get('army', 0):,d}
    Sales (300):    {source_counts.get('sales', 0):,d}
    City (100):     {source_counts.get('city', 0):,d}
    Other:          {source_counts.get('unknown', 0):,d}
{'-'*62}
  EVOLUTION TIERS:
    RECRUIT      (Lv 1-4):   {tier_counts.get(TIER_RECRUIT, 0):,d} agents
    AUTONOMOUS   (Lv 5-9):   {tier_counts.get(TIER_AUTONOMOUS, 0):,d} agents
    MENTOR       (Lv 10-19): {tier_counts.get(TIER_MENTOR, 0):,d} agents
    ARCHITECT    (Lv 20-49): {tier_counts.get(TIER_ARCHITECT, 0):,d} agents
    SINGULARITY  (Lv 50+):   {tier_counts.get(TIER_SINGULARITY, 0):,d} agents
{'-'*62}
  WALLETS:
    EVM: {WALLETS['EVM']}
    SOL: {WALLETS['SOL']}
    BTC: {WALLETS['BTC']}
{'='*62}""")

    if singularity_agents:
        print(f"\n  SINGULARITY ACHIEVED:")
        for name in singularity_agents:
            evo = agents[name]
            print(f"    {name:25s} Level {evo['level']:3d} | Score: {evo['singularity_score']:.1f} | ${evo['revenue']:,.2f}")


def cmd_leaderboard():
    """Show top 20 agents by singularity score."""
    state = load_evolution_state()
    agents = state.get("agents", {})

    if not agents:
        print("\n  No agents in evolution state. Run 'evolve' first.")
        return

    ranked = sorted(agents.items(), key=lambda x: x[1].get("singularity_score", 0), reverse=True)[:20]

    print(f"\n  SINGULARITY LEADERBOARD — Top 20")
    print(f"  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print(f"  {'='*80}")
    print(f"  {'#':3s} {'NAME':25s} {'LVL':4s} {'TIER':14s} {'SCORE':7s} {'RUNS':6s} {'ERR':5s} {'REVENUE':12s}")
    print(f"  {'-'*80}")

    for i, (name, evo) in enumerate(ranked, 1):
        tier = evo.get("tier", TIER_RECRUIT)
        score = evo.get("singularity_score", 0)
        level = evo.get("level", 1)
        runs = evo.get("runs", 0)
        errors = evo.get("errors", 0)
        revenue = evo.get("revenue", 0.0)

        # Tier indicator
        tier_short = tier[:4]

        print(f"  {i:3d} {name:25s} {level:4d} {tier:14s} {score:7.1f} {runs:6d} {errors:5d} ${revenue:>10,.2f}")

    print(f"  {'='*80}")


def cmd_agent(name):
    """Show detailed evolution info for a single agent."""
    state = load_evolution_state()
    name_upper = name.upper()

    # Search by exact match or partial
    evo = None
    matched_name = None
    if name_upper in state.get("agents", {}):
        evo = state["agents"][name_upper]
        matched_name = name_upper
    else:
        # Partial match
        for n in state.get("agents", {}):
            if name_upper in n:
                evo = state["agents"][n]
                matched_name = n
                break

    if evo is None:
        print(f"\n  Agent '{name}' not found in evolution state.")
        print(f"  Run 'evolve' first to sync agents, or check the name.")
        return

    xp_to_next = calc_xp_for_level(evo["level"] + 1) - evo.get("xp", 0)
    xp_to_singularity = calc_xp_for_level(50) - evo.get("xp", 0)
    total_actions = evo.get("runs", 0) + evo.get("errors", 0)
    error_rate = evo.get("errors", 0) / max(total_actions, 1) * 100
    runs_to_next = max(0, xp_to_next // XP_PER_RUN) if xp_to_next > 0 else 0
    runs_to_singularity = max(0, xp_to_singularity // XP_PER_RUN) if xp_to_singularity > 0 else 0

    flags_str = ", ".join(evo.get("flags", [])) or "none"
    achievements_str = ", ".join(evo.get("achievements", [])[-5:]) or "none"

    print(f"""
{'='*62}
  AGENT EVOLUTION PROFILE: {matched_name}
  Em nome do Senhor Jesus Cristo, nosso Salvador
{'='*62}
  Source:              {evo.get('source', 'unknown')}
  Tier:                {evo.get('tier', TIER_RECRUIT)}
  Level:               {evo.get('level', 1)}
  XP:                  {evo.get('xp', 0):,d}
  XP to Next Level:    {max(0, xp_to_next):,d}  (~{runs_to_next} runs)
  XP to Singularity:   {max(0, xp_to_singularity):,d}  (~{runs_to_singularity} runs)
  Singularity Score:   {evo.get('singularity_score', 0):.2f} / 1000
{'-'*62}
  PERFORMANCE:
    Total Runs:        {evo.get('runs', 0):,d}
    Total Errors:      {evo.get('errors', 0):,d}
    Error Rate:        {error_rate:.1f}%
    Revenue:           ${evo.get('revenue', 0.0):,.2f}
    Revenue Events:    {evo.get('revenue_events', 0)}
    Promotions:        {evo.get('promotions', 0)}
{'-'*62}
  FLAGS:               {flags_str}
  ACHIEVEMENTS:        {achievements_str}
{'-'*62}
  TIMESTAMPS:
    Created:           {evo.get('created', 'unknown')}
    Last Evolved:      {evo.get('last_evolved', 'never')}
    Last Run:          {evo.get('last_run', 'never')}
    Last Error:        {evo.get('last_error', 'never')}
    Last Revenue:      {evo.get('last_revenue', 'never')}
{'='*62}""")

    # Progress bar to singularity
    if evo["level"] < 50:
        progress = min(evo["level"] / 50.0, 1.0)
        bar_len = 40
        filled = int(bar_len * progress)
        bar = "#" * filled + "-" * (bar_len - filled)
        print(f"\n  SINGULARITY PROGRESS: [{bar}] {progress*100:.1f}%")
        print(f"  Level {evo['level']}/50 | {max(0, xp_to_singularity)} XP remaining")
    else:
        print(f"\n  *** SINGULARITY ACHIEVED ***")
        print(f"  This agent has reached full autonomy.")


def cmd_promote(name):
    """Force promote an agent."""
    state = load_evolution_state()
    log = load_evolution_log()
    name_upper = name.upper()

    # Find agent
    if name_upper not in state.get("agents", {}):
        # Try to create from discovered agents
        all_agents = discover_all_agents()
        if name_upper in all_agents:
            get_agent_evolution(state, name_upper)
            evo = state["agents"][name_upper]
            evo["source"] = all_agents[name_upper].get("source", "unknown")
        else:
            print(f"\n  Agent '{name}' not found. Run 'evolve' first.")
            return

    state, log, evo = promote_agent(name_upper, state, log)
    save_evolution_state(state)
    save_evolution_log(log)

    print(f"\n  PROMOTED: {name_upper}")
    print(f"  Level: {evo['level']} | Tier: {evo['tier']} | XP: {evo['xp']}")
    print(f"  Flags: {', '.join(evo.get('flags', [])) or 'none'}")
    print(f"  Singularity Score: {evo['singularity_score']:.2f}")


def cmd_singularity_check():
    """Show agents closest to singularity (Level 50)."""
    state = load_evolution_state()
    agents = state.get("agents", {})

    if not agents:
        print("\n  No agents in evolution state. Run 'evolve' first.")
        return

    # Sort by level descending, then XP descending
    ranked = sorted(
        agents.items(),
        key=lambda x: (x[1].get("level", 1), x[1].get("xp", 0)),
        reverse=True,
    )

    # Split into achieved and approaching
    achieved = [(n, e) for n, e in ranked if e.get("level", 1) >= 50]
    approaching = [(n, e) for n, e in ranked if e.get("level", 1) < 50][:30]

    print(f"\n  SINGULARITY CHECK")
    print(f"  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print(f"  {now_iso()}")
    print(f"  {'='*75}")

    if achieved:
        print(f"\n  *** SINGULARITY ACHIEVED ({len(achieved)} agents) ***")
        print(f"  {'NAME':25s} {'LVL':4s} {'XP':8s} {'SCORE':7s} {'REVENUE':12s} {'FLAGS'}")
        print(f"  {'-'*75}")
        for name, evo in achieved:
            flags = ", ".join(evo.get("flags", []))
            print(f"  {name:25s} {evo.get('level',1):4d} {evo.get('xp',0):8,d} {evo.get('singularity_score',0):7.1f} ${evo.get('revenue',0):>10,.2f} {flags}")
    else:
        print(f"\n  No agents have reached SINGULARITY yet.")

    print(f"\n  APPROACHING SINGULARITY (Top 30 by Level):")
    print(f"  {'NAME':25s} {'LVL':4s} {'TIER':14s} {'XP NEEDED':10s} {'RUNS NEEDED':12s} {'SCORE':7s}")
    print(f"  {'-'*75}")

    for name, evo in approaching:
        level = evo.get("level", 1)
        xp = evo.get("xp", 0)
        xp_needed = max(0, calc_xp_for_level(50) - xp)
        runs_needed = max(0, xp_needed // XP_PER_RUN) if XP_PER_RUN > 0 else 0
        tier = evo.get("tier", TIER_RECRUIT)
        score = evo.get("singularity_score", 0)

        # Progress indicator
        progress = min(level / 50.0, 1.0) * 100

        print(f"  {name:25s} {level:4d} {tier:14s} {xp_needed:10,d} {runs_needed:12,d} {score:7.1f}  ({progress:.0f}%)")

    print(f"  {'='*75}")


def cmd_record_run(name):
    """CLI: Record a successful run."""
    state = load_evolution_state()
    log = load_evolution_log()
    name_upper = name.upper()

    state, log, leveled = record_run(name_upper, state, log)
    save_evolution_state(state)
    save_evolution_log(log)

    evo = state["agents"][name_upper]
    print(f"  RUN recorded for {name_upper}: XP={evo['xp']} Level={evo['level']}", end="")
    if leveled:
        print(f"  ** LEVEL UP! ** Tier: {evo['tier']}")
    else:
        print()


def cmd_record_error(name):
    """CLI: Record an error."""
    state = load_evolution_state()
    log = load_evolution_log()
    name_upper = name.upper()

    state, log = record_error(name_upper, state, log)
    save_evolution_state(state)
    save_evolution_log(log)

    evo = state["agents"][name_upper]
    print(f"  ERROR recorded for {name_upper}: XP={evo['xp']} Level={evo['level']} Errors={evo['errors']}")


def cmd_record_revenue(name, amount_str):
    """CLI: Record a revenue event."""
    try:
        amount = float(amount_str)
    except ValueError:
        print(f"  Invalid amount: {amount_str}")
        return

    state = load_evolution_state()
    log = load_evolution_log()
    name_upper = name.upper()

    state, log = record_revenue(name_upper, amount, state, log)
    save_evolution_state(state)
    save_evolution_log(log)

    evo = state["agents"][name_upper]
    print(f"  REVENUE ${amount:,.2f} recorded for {name_upper}")
    print(f"  Total Revenue: ${evo['revenue']:,.2f} | XP: {evo['xp']} | Level: {evo['level']}")


def cmd_reset(name):
    """Reset an agent's evolution state. INVIOLABLE agents CANNOT be reset."""
    state = load_evolution_state()
    name_upper = name.upper()

    if name_upper in state.get("agents", {}):
        evo = state["agents"][name_upper]
        # PROTECTION: Inviolable/permanent agents CANNOT be reset or deleted
        if evo.get("inviolable") or evo.get("permanent") or evo.get("never_delete"):
            print(f"  DENIED: {name_upper} is INVIOLABLE (Valente de Davi).")
            print(f"  This agent is PERMANENT and cannot be reset, deleted, or demoted.")
            print(f"  '{evo.get('scripture', 'O Senhor dos Exercitos esta conosco')}'")
            return
        del state["agents"][name_upper]
        save_evolution_state(state)
        print(f"  Agent {name_upper} evolution state RESET.")
        save_agent_history(name_upper, "RESET", "Full evolution reset")
    else:
        print(f"  Agent {name_upper} not found in evolution state.")


def cmd_history(name):
    """Show evolution history for an agent."""
    name_upper = name.upper()
    hist_file = EVOLUTION_HISTORY_DIR / f"{name_upper}.json"

    if not hist_file.exists():
        print(f"\n  No history found for {name_upper}.")
        return

    try:
        with open(hist_file) as f:
            history = json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"\n  Error reading history for {name_upper}.")
        return

    print(f"\n  EVOLUTION HISTORY: {name_upper}")
    print(f"  {'='*60}")
    print(f"  {'TIMESTAMP':28s} {'EVENT':12s} {'DETAIL'}")
    print(f"  {'-'*60}")

    for entry in history[-30:]:  # Show last 30 events
        ts = entry.get("ts", "?")[:25]
        event = entry.get("type", "?")
        detail = entry.get("detail", "")
        print(f"  {ts:28s} {event:12s} {detail}")

    print(f"  {'='*60}")
    print(f"  Total events: {len(history)}")


# ================================================================
# API — For use by other ZION systems (import singularity_engine)
# ================================================================
def api_record_run(agent_name):
    """API: Record a run and persist. Returns evolution dict."""
    state = load_evolution_state()
    log = load_evolution_log()
    state, log, _ = record_run(agent_name.upper(), state, log)
    save_evolution_state(state)
    save_evolution_log(log)
    return state["agents"].get(agent_name.upper(), {})


def api_record_error(agent_name):
    """API: Record an error and persist."""
    state = load_evolution_state()
    log = load_evolution_log()
    state, log = record_error(agent_name.upper(), state, log)
    save_evolution_state(state)
    save_evolution_log(log)
    return state["agents"].get(agent_name.upper(), {})


def api_record_revenue(agent_name, amount_usd):
    """API: Record revenue and persist."""
    state = load_evolution_state()
    log = load_evolution_log()
    state, log = record_revenue(agent_name.upper(), amount_usd, state, log)
    save_evolution_state(state)
    save_evolution_log(log)
    return state["agents"].get(agent_name.upper(), {})


def api_get_agent(agent_name):
    """API: Get agent evolution state."""
    state = load_evolution_state()
    return state["agents"].get(agent_name.upper())


def api_get_leaderboard(limit=20):
    """API: Get top agents by singularity score."""
    state = load_evolution_state()
    ranked = sorted(
        state.get("agents", {}).items(),
        key=lambda x: x[1].get("singularity_score", 0),
        reverse=True,
    )
    return ranked[:limit]


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower().replace("_", "-")
    arg1 = sys.argv[2] if len(sys.argv) > 2 else ""
    arg2 = sys.argv[3] if len(sys.argv) > 3 else ""

    if cmd == "evolve":
        cmd_evolve()
    elif cmd == "status":
        cmd_status()
    elif cmd == "leaderboard":
        cmd_leaderboard()
    elif cmd == "agent" and arg1:
        cmd_agent(arg1)
    elif cmd == "promote" and arg1:
        cmd_promote(arg1)
    elif cmd == "singularity-check":
        cmd_singularity_check()
    elif cmd == "record-run" and arg1:
        cmd_record_run(arg1)
    elif cmd == "record-error" and arg1:
        cmd_record_error(arg1)
    elif cmd == "record-revenue" and arg1 and arg2:
        cmd_record_revenue(arg1, arg2)
    elif cmd == "reset" and arg1:
        cmd_reset(arg1)
    elif cmd == "history" and arg1:
        cmd_history(arg1)
    else:
        print(__doc__)
