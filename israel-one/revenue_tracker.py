#!/usr/bin/env python3
"""
Revenue Tracker — Padrao Bitcoin
Em nome do Senhor Jesus Cristo, nosso Salvador

Real-time revenue tracking system.
Monitors wallet balances (BTC, ETH, SOL) via free public APIs.
Tracks bounty payments, product sales, grant payments.
Generates daily/weekly/monthly revenue reports.

Usage:
    python3 revenue_tracker.py check      — Check all wallet balances NOW
    python3 revenue_tracker.py log        — Show all revenue events
    python3 revenue_tracker.py add SOURCE AMOUNT_USD DESCRIPTION
    python3 revenue_tracker.py report     — Full revenue report
    python3 revenue_tracker.py pipeline   — Show pending revenue pipeline
    python3 revenue_tracker.py sentinel   — Continuous balance checking (30 min)

stdlib only — lightweight for 3.3GB RAM.
"""

import json
import os
import sys
import time
import signal
import ssl
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WALLETS = {
    "EVM": {
        "address": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
        "chain": "Ethereum",
        "symbol": "ETH",
    },
    "SOL": {
        "address": "CM42ofAFowySg72GjDuCchEkwwbwnhdSRYgztRCAAEzR",
        "chain": "Solana",
        "symbol": "SOL",
    },
    "BTC": {
        "address": "bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2",
        "chain": "Bitcoin",
        "symbol": "BTC",
    },
}

REVENUE_DIR = Path.home() / ".zion" / "revenue"
REVENUE_LOG = REVENUE_DIR / "revenue_log.json"
BALANCE_HISTORY = REVENUE_DIR / "balance_history.json"
PIPELINE_FILE = REVENUE_DIR / "pipeline.json"
SENTINEL_PID = REVENUE_DIR / "sentinel.pid"

SENTINEL_INTERVAL = 1800  # 30 minutes

# Prices API (CoinGecko free, no key required)
PRICES_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum,solana&vs_currencies=usd"
)

# Default pipeline items (known pending revenue)
DEFAULT_PIPELINE = [
    {
        "source": "ZKsync OS Bug",
        "platform": "Immunefi",
        "amount_usd_min": 5000,
        "amount_usd_max": 50000,
        "status": "report_ready",
        "deadline": "2026-04-01",
        "description": "Callstack off-by-one ee_trait_impl.rs:351",
    },
    {
        "source": "Golem Cloud MCP",
        "platform": "Algora",
        "amount_usd_min": 3500,
        "amount_usd_max": 3500,
        "status": "in_escrow",
        "deadline": "2026-04-15",
        "description": "Algora escrow — payment guaranteed",
    },
    {
        "source": "NEAR Intents",
        "platform": "HackenProof",
        "amount_usd_min": 1000,
        "amount_usd_max": 300000,
        "status": "hunting",
        "deadline": "2026-06-01",
        "description": "Bridge vulnerabilities research",
    },
    {
        "source": "C4 Chainlink",
        "platform": "Code4rena",
        "amount_usd_min": 5000,
        "amount_usd_max": 65000,
        "status": "submitted",
        "deadline": "2026-03-27",
        "description": "H-01 critical finding submitted",
    },
    {
        "source": "Guardian LimitBreak",
        "platform": "Guardian Audits",
        "amount_usd_min": 10000,
        "amount_usd_max": 150000,
        "status": "findings_ready",
        "deadline": "2026-04-09",
        "description": "8 findings ready, KYC pending",
    },
]


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _now_iso():
    """Current time as ISO string with timezone."""
    return datetime.now(timezone(timedelta(hours=-3))).isoformat()


def _now_dt():
    """Current datetime object (BRT)."""
    return datetime.now(timezone(timedelta(hours=-3)))


def _ensure_dirs():
    """Create revenue directory if needed."""
    REVENUE_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path, default=None):
    """Load JSON file, return default if missing or corrupt."""
    if default is None:
        default = {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(path, data):
    """Save data as JSON."""
    _ensure_dirs()
    tmp = str(path) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, default=str)
    os.replace(tmp, str(path))


def _fetch_url(url, timeout=15):
    """Fetch URL content, return parsed JSON or None."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        "User-Agent": "RevenueTracker/1.0",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
        return None


def _format_usd(amount):
    """Format number as USD string."""
    if amount >= 1_000_000:
        return f"${amount:,.2f}"
    elif amount >= 1000:
        return f"${amount:,.2f}"
    else:
        return f"${amount:.4f}"


def _print_header(title):
    """Print a section header."""
    line = "=" * 60
    print(f"\n{line}")
    print(f"  {title}")
    print(f"{line}")


def _print_row(label, value, indent=2):
    """Print a key-value row."""
    pad = " " * indent
    print(f"{pad}{label:<30} {value}")


# ---------------------------------------------------------------------------
# Revenue log management
# ---------------------------------------------------------------------------

def _load_revenue_log():
    """Load the revenue log, preserving existing entries."""
    data = _load_json(REVENUE_LOG, {"events": [], "total_usd": 0.0})
    if "events" not in data:
        data["events"] = []
    if "total_usd" not in data:
        data["total_usd"] = 0.0
    return data


def _save_revenue_log(data):
    """Save revenue log and recalculate total."""
    data["total_usd"] = sum(e.get("amount_usd", 0) for e in data["events"])
    data["last_updated"] = _now_iso()
    _save_json(REVENUE_LOG, data)


def add_revenue_event(source, amount_usd, description, agent="revenue_tracker"):
    """Add a new revenue event to the log."""
    log = _load_revenue_log()
    event = {
        "source": source,
        "amount_usd": float(amount_usd),
        "description": description,
        "agent": agent,
        "timestamp": _now_iso(),
    }
    log["events"].append(event)
    _save_revenue_log(log)
    return event


# ---------------------------------------------------------------------------
# Wallet balance checking
# ---------------------------------------------------------------------------

def _get_prices():
    """Fetch current BTC, ETH, SOL prices in USD."""
    data = _fetch_url(PRICES_URL)
    if not data:
        return {"bitcoin": 0, "ethereum": 0, "solana": 0}
    return {
        "bitcoin": data.get("bitcoin", {}).get("usd", 0),
        "ethereum": data.get("ethereum", {}).get("usd", 0),
        "solana": data.get("solana", {}).get("usd", 0),
    }


def _check_btc_balance():
    """Check BTC balance via blockchain.info API."""
    addr = WALLETS["BTC"]["address"]
    url = f"https://blockchain.info/q/addressbalance/{addr}"
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "RevenueTracker/1.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            satoshis = int(resp.read().decode("utf-8").strip())
            return satoshis / 1e8
    except Exception:
        return None


def _check_eth_balance():
    """Check ETH balance via public Ethereum RPC (eth_getBalance)."""
    addr = WALLETS["EVM"]["address"]
    # Try free Cloudflare Ethereum RPC
    rpc_url = "https://cloudflare-eth.com"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [addr, "latest"],
        "id": 1,
    }).encode("utf-8")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        rpc_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "RevenueTracker/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hex_balance = data.get("result", "0x0")
            wei = int(hex_balance, 16)
            return wei / 1e18
    except Exception:
        return None


def _check_sol_balance():
    """Check SOL balance via public Solana RPC."""
    addr = WALLETS["SOL"]["address"]
    rpc_url = "https://api.mainnet-beta.solana.com"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [addr],
    }).encode("utf-8")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        rpc_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "RevenueTracker/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            lamports = data.get("result", {}).get("value", 0)
            return lamports / 1e9
    except Exception:
        return None


def check_all_balances():
    """Check all wallet balances and return structured data."""
    print("\n  Fetching prices...")
    prices = _get_prices()

    print("  Checking BTC balance...")
    btc_bal = _check_btc_balance()

    print("  Checking ETH balance...")
    eth_bal = _check_eth_balance()

    print("  Checking SOL balance...")
    sol_bal = _check_sol_balance()

    balances = {
        "BTC": {
            "balance": btc_bal,
            "price_usd": prices.get("bitcoin", 0),
            "value_usd": (btc_bal or 0) * prices.get("bitcoin", 0),
            "address": WALLETS["BTC"]["address"],
        },
        "ETH": {
            "balance": eth_bal,
            "price_usd": prices.get("ethereum", 0),
            "value_usd": (eth_bal or 0) * prices.get("ethereum", 0),
            "address": WALLETS["EVM"]["address"],
        },
        "SOL": {
            "balance": sol_bal,
            "price_usd": prices.get("solana", 0),
            "value_usd": (sol_bal or 0) * prices.get("solana", 0),
            "address": WALLETS["SOL"]["address"],
        },
    }

    total_usd = sum(b["value_usd"] for b in balances.values())
    balances["total_usd"] = total_usd
    balances["timestamp"] = _now_iso()
    balances["prices"] = prices

    # Save to balance history
    history = _load_json(BALANCE_HISTORY, {"snapshots": []})
    history["snapshots"].append({
        "timestamp": balances["timestamp"],
        "total_usd": total_usd,
        "btc": btc_bal,
        "eth": eth_bal,
        "sol": sol_bal,
        "prices": prices,
    })
    # Keep last 1000 snapshots to save disk
    if len(history["snapshots"]) > 1000:
        history["snapshots"] = history["snapshots"][-1000:]
    _save_json(BALANCE_HISTORY, history)

    return balances


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_check():
    """Check all wallet balances NOW."""
    _print_header("WALLET BALANCE CHECK")
    print(f"  Time: {_now_iso()}")

    balances = check_all_balances()

    print()
    for symbol in ["BTC", "ETH", "SOL"]:
        b = balances[symbol]
        bal_str = f"{b['balance']:.8f}" if b["balance"] is not None else "ERROR"
        price_str = _format_usd(b["price_usd"])
        val_str = _format_usd(b["value_usd"])
        print(f"  {symbol:<5} {bal_str:>18} {symbol}  @ {price_str:>12}  =  {val_str:>12}")
        print(f"        {b['address']}")
        print()

    total = balances["total_usd"]
    print(f"  {'TOTAL WALLET VALUE':<30} {_format_usd(total)}")

    # Also show revenue log total
    log = _load_revenue_log()
    logged_total = log.get("total_usd", 0)
    print(f"  {'TOTAL LOGGED REVENUE':<30} {_format_usd(logged_total)}")
    print(f"  {'COMBINED':<30} {_format_usd(total + logged_total)}")
    print()

    # Detect new funds since last check
    history = _load_json(BALANCE_HISTORY, {"snapshots": []})
    snapshots = history.get("snapshots", [])
    if len(snapshots) >= 2:
        prev = snapshots[-2]
        curr = snapshots[-1]
        diff = curr["total_usd"] - prev["total_usd"]
        if abs(diff) > 0.01:
            direction = "INCREASE" if diff > 0 else "DECREASE"
            print(f"  ** Balance {direction}: {_format_usd(abs(diff))} since last check **")
            if diff > 0:
                print(f"  ** PAYMENT DETECTED — check transaction details **")
            print()

    return balances


def cmd_log():
    """Show all revenue events."""
    log = _load_revenue_log()
    events = log.get("events", [])

    _print_header("REVENUE LOG")
    print(f"  Total events: {len(events)}")
    print(f"  Total revenue: {_format_usd(log.get('total_usd', 0))}")
    print()

    if not events:
        print("  No revenue events recorded yet.")
        print("  Use: revenue_tracker.py add SOURCE AMOUNT DESCRIPTION")
        return

    print(f"  {'#':<4} {'Date':<22} {'Source':<22} {'Amount':>12}  Description")
    print(f"  {'-'*4} {'-'*22} {'-'*22} {'-'*12}  {'-'*30}")

    for i, e in enumerate(events, 1):
        ts = e.get("timestamp", "unknown")[:19]
        src = e.get("source", "unknown")[:22]
        amt = _format_usd(e.get("amount_usd", 0))
        desc = e.get("description", "")[:40]
        print(f"  {i:<4} {ts:<22} {src:<22} {amt:>12}  {desc}")

    print(f"\n  {'TOTAL':>50} {_format_usd(log.get('total_usd', 0)):>12}")
    print()


def cmd_add(source, amount_usd, description):
    """Log a manual revenue event."""
    try:
        amount = float(amount_usd)
    except ValueError:
        print(f"  ERROR: '{amount_usd}' is not a valid number.")
        sys.exit(1)

    event = add_revenue_event(source, amount, description)

    _print_header("REVENUE EVENT LOGGED")
    _print_row("Source:", source)
    _print_row("Amount:", _format_usd(amount))
    _print_row("Description:", description)
    _print_row("Timestamp:", event["timestamp"])
    print()

    log = _load_revenue_log()
    print(f"  New total revenue: {_format_usd(log.get('total_usd', 0))}")
    print()


def cmd_report():
    """Full revenue report — daily/weekly/monthly breakdown."""
    log = _load_revenue_log()
    events = log.get("events", [])
    now = _now_dt()

    _print_header("REVENUE REPORT — PADRAO BITCOIN")
    print(f"  Generated: {_now_iso()}")
    print(f"  Em nome do Senhor Jesus Cristo, nosso Salvador")

    # Overall totals
    total = log.get("total_usd", 0)
    print(f"\n  OVERALL TOTAL: {_format_usd(total)}")
    print(f"  Total events:  {len(events)}")

    # Time-based breakdown
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=now.weekday())
    month_start = today_start.replace(day=1)

    daily_total = 0.0
    weekly_total = 0.0
    monthly_total = 0.0
    by_source = {}

    for e in events:
        amt = e.get("amount_usd", 0)
        src = e.get("source", "unknown")
        ts_str = e.get("timestamp", "")

        # Parse timestamp
        try:
            if "T" in ts_str:
                # Handle ISO format with timezone
                ts_clean = ts_str[:19]
                ts_dt = datetime.strptime(ts_clean, "%Y-%m-%dT%H:%M:%S")
                ts_dt = ts_dt.replace(tzinfo=timezone(timedelta(hours=-3)))
            else:
                ts_dt = now - timedelta(days=365)  # fallback: old
        except (ValueError, TypeError):
            ts_dt = now - timedelta(days=365)

        if ts_dt >= today_start:
            daily_total += amt
        if ts_dt >= week_start:
            weekly_total += amt
        if ts_dt >= month_start:
            monthly_total += amt

        by_source[src] = by_source.get(src, 0) + amt

    _print_header("TIME BREAKDOWN")
    _print_row("Today:", _format_usd(daily_total))
    _print_row("This week:", _format_usd(weekly_total))
    _print_row("This month:", _format_usd(monthly_total))
    _print_row("All time:", _format_usd(total))

    # By source
    if by_source:
        _print_header("REVENUE BY SOURCE")
        sorted_sources = sorted(by_source.items(), key=lambda x: x[1], reverse=True)
        for src, amt in sorted_sources:
            pct = (amt / total * 100) if total > 0 else 0
            bar = "#" * int(pct / 2)
            print(f"  {src:<25} {_format_usd(amt):>12}  ({pct:5.1f}%)  {bar}")

    # Wallet balances
    _print_header("CURRENT WALLET BALANCES")
    balances = check_all_balances()
    for symbol in ["BTC", "ETH", "SOL"]:
        b = balances[symbol]
        bal_str = f"{b['balance']:.8f}" if b["balance"] is not None else "N/A"
        val_str = _format_usd(b["value_usd"])
        print(f"  {symbol:<5}  {bal_str:>18}  =  {val_str:>12}")

    wallet_total = balances["total_usd"]
    print(f"\n  Wallet total:  {_format_usd(wallet_total)}")
    print(f"  Logged total:  {_format_usd(total)}")
    print(f"  GRAND TOTAL:   {_format_usd(wallet_total + total)}")

    # Pipeline preview
    _print_header("PENDING PIPELINE (top 3)")
    pipeline = _load_pipeline()
    items = pipeline.get("items", [])
    sorted_items = sorted(items, key=lambda x: x.get("deadline", "9999"))
    for item in sorted_items[:3]:
        src = item.get("source", "unknown")
        amt_min = item.get("amount_usd_min", 0)
        amt_max = item.get("amount_usd_max", 0)
        status = item.get("status", "unknown")
        deadline = item.get("deadline", "N/A")
        print(f"  {src:<25} {_format_usd(amt_min)}-{_format_usd(amt_max)}  [{status}]  by {deadline}")

    pipeline_total_min = sum(i.get("amount_usd_min", 0) for i in items)
    pipeline_total_max = sum(i.get("amount_usd_max", 0) for i in items)
    print(f"\n  Pipeline range: {_format_usd(pipeline_total_min)} — {_format_usd(pipeline_total_max)}")
    print()


def _load_pipeline():
    """Load pipeline or create default."""
    pipeline = _load_json(PIPELINE_FILE, None)
    if pipeline is None or "items" not in pipeline:
        pipeline = {
            "items": DEFAULT_PIPELINE,
            "created": _now_iso(),
            "last_updated": _now_iso(),
        }
        _save_json(PIPELINE_FILE, pipeline)
    return pipeline


def cmd_pipeline():
    """Show pending revenue pipeline."""
    pipeline = _load_pipeline()
    items = pipeline.get("items", [])

    _print_header("REVENUE PIPELINE — PENDING")
    print(f"  Last updated: {pipeline.get('last_updated', 'unknown')}")
    print()

    if not items:
        print("  No pipeline items.")
        return

    # Status priority order
    status_order = {
        "in_escrow": 1,
        "submitted": 2,
        "report_ready": 3,
        "findings_ready": 4,
        "hunting": 5,
        "research": 6,
    }
    sorted_items = sorted(items, key=lambda x: (
        status_order.get(x.get("status", ""), 99),
        x.get("deadline", "9999"),
    ))

    # Status labels
    status_labels = {
        "in_escrow": "[ESCROW]  ",
        "submitted": "[SENT]    ",
        "report_ready": "[READY]   ",
        "findings_ready": "[FINDINGS]",
        "hunting": "[HUNTING] ",
        "research": "[RESEARCH]",
    }

    total_min = 0
    total_max = 0

    print(f"  {'Source':<22} {'Range':>25}  {'Status':<12} {'Deadline':<12} Platform")
    print(f"  {'-'*22} {'-'*25}  {'-'*12} {'-'*12} {'-'*15}")

    for item in sorted_items:
        src = item.get("source", "unknown")[:22]
        amt_min = item.get("amount_usd_min", 0)
        amt_max = item.get("amount_usd_max", 0)
        status = item.get("status", "unknown")
        status_label = status_labels.get(status, f"[{status}]")
        deadline = item.get("deadline", "N/A")
        platform = item.get("platform", "")
        desc = item.get("description", "")

        range_str = f"{_format_usd(amt_min)} — {_format_usd(amt_max)}"
        print(f"  {src:<22} {range_str:>25}  {status_label:<12} {deadline:<12} {platform}")
        if desc:
            print(f"  {'':>22} {desc}")
        print()

        total_min += amt_min
        total_max += amt_max

    print(f"  {'PIPELINE TOTAL':<22} {_format_usd(total_min)} — {_format_usd(total_max)}")
    print()

    # Urgency check
    now_date = _now_dt().date()
    urgent = [i for i in items if i.get("deadline", "9999") <= str(now_date + timedelta(days=7))]
    if urgent:
        print(f"  !! {len(urgent)} item(s) with deadline within 7 days:")
        for u in urgent:
            print(f"     - {u['source']} by {u.get('deadline', 'N/A')}")
        print()


def cmd_sentinel():
    """Run continuous balance checking every 30 minutes."""
    _ensure_dirs()

    # Write PID
    pid = os.getpid()
    with open(SENTINEL_PID, "w") as f:
        f.write(str(pid))

    def _cleanup(signum=None, frame=None):
        print(f"\n  Sentinel stopping (PID {pid})...")
        try:
            SENTINEL_PID.unlink(missing_ok=True)
        except Exception:
            pass
        sys.exit(0)

    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)

    _print_header("REVENUE SENTINEL — ACTIVE")
    print(f"  PID: {pid}")
    print(f"  Interval: {SENTINEL_INTERVAL}s ({SENTINEL_INTERVAL // 60} min)")
    print(f"  Started: {_now_iso()}")
    print(f"  Log: {REVENUE_LOG}")
    print(f"  History: {BALANCE_HISTORY}")
    print(f"  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print()
    print("  Press Ctrl+C to stop.")
    print()

    cycle = 0
    prev_total = None

    while True:
        cycle += 1
        print(f"\n  --- Sentinel cycle {cycle} at {_now_iso()} ---")

        try:
            balances = check_all_balances()
            curr_total = balances["total_usd"]

            for symbol in ["BTC", "ETH", "SOL"]:
                b = balances[symbol]
                if b["balance"] is not None:
                    bal_str = f"{b['balance']:.8f}"
                    val_str = _format_usd(b["value_usd"])
                    print(f"  {symbol}: {bal_str} = {val_str}")
                else:
                    print(f"  {symbol}: ERROR fetching balance")

            print(f"  Total: {_format_usd(curr_total)}")

            # Detect changes
            if prev_total is not None:
                diff = curr_total - prev_total
                if diff > 0.50:  # More than $0.50 increase (account for price fluctuation)
                    print()
                    print("  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"  !! FUNDS INCREASE DETECTED: +{_format_usd(diff)}")
                    print("  !! Check wallet transactions for payment")
                    print("  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print()

                    # Auto-log potential revenue event
                    add_revenue_event(
                        source="wallet_increase",
                        amount_usd=diff,
                        description=f"Wallet balance increase detected (cycle {cycle})",
                        agent="sentinel",
                    )

            prev_total = curr_total

        except Exception as e:
            print(f"  ERROR in cycle {cycle}: {e}")

        print(f"  Next check in {SENTINEL_INTERVAL // 60} minutes...")

        try:
            time.sleep(SENTINEL_INTERVAL)
        except KeyboardInterrupt:
            _cleanup()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def print_usage():
    """Print usage information."""
    _print_header("REVENUE TRACKER — PADRAO BITCOIN")
    print("  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print()
    print("  Commands:")
    print("    check                           Check all wallet balances NOW")
    print("    log                             Show all revenue events")
    print("    add SOURCE AMOUNT DESCRIPTION   Log manual revenue event")
    print("    report                          Full revenue report")
    print("    pipeline                        Show pending revenue pipeline")
    print("    sentinel                        Continuous balance checking (30 min)")
    print()
    print("  Examples:")
    print("    python3 revenue_tracker.py check")
    print("    python3 revenue_tracker.py add bounty 5000 'ZKsync Immunefi payout'")
    print("    python3 revenue_tracker.py add sale 99 'OpenClaw Pro monthly'")
    print("    python3 revenue_tracker.py report")
    print("    python3 revenue_tracker.py sentinel")
    print()
    print(f"  Revenue log: {REVENUE_LOG}")
    print(f"  Wallets:")
    for name, w in WALLETS.items():
        print(f"    {name}: {w['address']}")
    print()


def main():
    _ensure_dirs()

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "check":
        cmd_check()
    elif cmd == "log":
        cmd_log()
    elif cmd == "add":
        if len(sys.argv) < 5:
            print("  Usage: revenue_tracker.py add SOURCE AMOUNT_USD DESCRIPTION")
            print("  Example: revenue_tracker.py add bounty 5000 'Immunefi payout'")
            sys.exit(1)
        source = sys.argv[2]
        amount = sys.argv[3]
        description = " ".join(sys.argv[4:])
        cmd_add(source, amount, description)
    elif cmd == "report":
        cmd_report()
    elif cmd == "pipeline":
        cmd_pipeline()
    elif cmd == "sentinel":
        cmd_sentinel()
    else:
        print(f"  Unknown command: {cmd}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
