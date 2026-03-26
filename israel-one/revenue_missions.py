#!/usr/bin/env python3
"""
REVENUE MISSIONS — Real money-making tasks for ZION agents.
Em nome do Senhor Jesus Cristo, nosso Salvador.

Adds HIGH-PRIORITY revenue missions to the execution engine.
These are tasks that directly lead to income.

Usage:
    python3 revenue_missions.py status     # Show all missions
    python3 revenue_missions.py run NAME   # Run specific mission
    python3 revenue_missions.py run-all    # Run all due missions
"""

import json
import os
import sys
import subprocess
import urllib.request
import ssl
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
HOME = Path.home()
ZION = HOME / ".zion"
MISSIONS_FILE = ZION / "shared" / "revenue_missions.json"
ALERTS_FILE = ZION / "shared" / "alerts.json"

def _http_get(url, timeout=10):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "ZION/4.0"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout, context=ctx).read().decode())
    except:
        return None

def _run(cmd, timeout=20):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout[:3000] if r.returncode == 0 else ""
    except:
        return ""

def _alert(text, source="revenue"):
    alerts = []
    if ALERTS_FILE.exists():
        try: alerts = json.loads(ALERTS_FILE.read_text())
        except: pass
    alerts.append({"text": text, "source": source, "time": datetime.now(BRT).isoformat()})
    alerts = alerts[-200:]
    ALERTS_FILE.write_text(json.dumps(alerts, indent=2))
    print(f"  ALERT: {text}")

def _load_missions():
    if MISSIONS_FILE.exists():
        try: return json.loads(MISSIONS_FILE.read_text())
        except: pass
    return {"missions": {}, "last_run": None, "total_checks": 0}

def _save_missions(data):
    data["last_run"] = datetime.now(BRT).isoformat()
    data["total_checks"] = data.get("total_checks", 0) + 1
    MISSIONS_FILE.write_text(json.dumps(data, indent=2))


# ================================================================
# MISSION 1: NUCLEI PR MONITOR (Closest to $$$)
# ================================================================
def mission_nuclei_prs():
    """Monitor nuclei-templates PRs — $150-250 per merge."""
    print("\n[MISSION] nuclei-templates PR Monitor")
    out = _run("gh pr list --repo projectdiscovery/nuclei-templates --author=ElromEvedElElyon --state=open --json number,title,updatedAt,reviewDecision --limit=20")
    if not out:
        print("  Failed to fetch PRs")
        return {"status": "error", "prs": 0}

    prs = json.loads(out)
    results = []
    for pr in prs:
        num = pr["number"]
        title = pr["title"][:50]
        decision = pr.get("reviewDecision", "PENDING")
        status = "waiting"
        if decision == "APPROVED":
            status = "APPROVED"
            _alert(f"nuclei PR #{num} APPROVED! Ready for merge = $150-250", "nuclei_mission")
        elif decision == "CHANGES_REQUESTED":
            status = "CHANGES_NEEDED"
            _alert(f"nuclei PR #{num} needs changes — fix NOW to keep merge alive", "nuclei_mission")

        results.append({"num": num, "title": title, "status": status})
        print(f"  PR #{num}: {status} — {title}")

    # Check for merged PRs
    merged = _run("gh pr list --repo projectdiscovery/nuclei-templates --author=ElromEvedElElyon --state=merged --json number,title,mergedAt --limit=10")
    if merged:
        merged_prs = json.loads(merged)
        for pr in merged_prs:
            _alert(f"nuclei PR #{pr['number']} MERGED! Collect $150-250 from Algora", "nuclei_mission")
            print(f"  MERGED: #{pr['number']} — {pr['title'][:50]}")

    return {"status": "ok", "open": len(results), "prs": results}


# ================================================================
# MISSION 2: WALLET MONITOR (Payment Detection)
# ================================================================
def mission_wallet_monitor():
    """Check all 3 wallets for ANY incoming payment."""
    print("\n[MISSION] Wallet Payment Monitor")
    wallets = {
        "BTC": ("bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2",
                "https://blockchain.info/q/addressbalance/bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2"),
        "SOL": ("CM42ofAFowySg72GjDuCchEkwwbwnhdSRYgztRCAAEzR", None),
        "ETH": ("0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B", None),
    }

    for chain, (addr, url) in wallets.items():
        bal = 0
        if chain == "BTC" and url:
            data = _http_get(url)
            if data is not None:
                try: bal = int(data) / 1e8
                except: pass
        elif chain == "SOL":
            try:
                payload = json.dumps({"jsonrpc":"2.0","id":1,"method":"getBalance","params":[addr]}).encode()
                req = urllib.request.Request("https://api.mainnet-beta.solana.com",
                    data=payload, headers={"Content-Type":"application/json","User-Agent":"ZION/4.0"})
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                resp = urllib.request.urlopen(req, timeout=10, context=ctx)
                d = json.loads(resp.read())
                bal = d.get("result",{}).get("value",0) / 1e9
            except: pass
        elif chain == "ETH":
            data = _http_get(f"https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address={addr}&tag=latest")
            if data and data.get("status") == "1":
                try: bal = int(data["result"]) / 1e18
                except: pass

        print(f"  {chain}: {bal:.8f}")
        if bal > 0.0001:
            price_data = _http_get(f"https://api.coingecko.com/api/v3/simple/price?ids={'bitcoin' if chain=='BTC' else 'ethereum' if chain=='ETH' else 'solana'}&vs_currencies=usd")
            usd = 0
            if price_data:
                coin = "bitcoin" if chain == "BTC" else "ethereum" if chain == "ETH" else "solana"
                usd = bal * price_data.get(coin, {}).get("usd", 0)
            _alert(f"PAYMENT DETECTED! {chain}: {bal:.8f} = ${usd:,.2f}", "wallet_mission")

    return {"status": "ok"}


# ================================================================
# MISSION 3: IMMUNEFI STATUS CHECK
# ================================================================
def mission_immunefi_status():
    """Check Immunefi report #71022 status indicators."""
    print("\n[MISSION] Immunefi Report #71022 Status")
    # We can't access dashboard without browser, but check email
    out = _run("python3 ~/gmail_reader.py --search 'immunefi' --limit 5 --account both 2>/dev/null")
    if out:
        keywords = ["accepted", "resolved", "paid", "bounty", "reward", "triage", "update"]
        for line in out.splitlines():
            if any(kw in line.lower() for kw in keywords):
                _alert(f"Immunefi email: {line[:100]}", "immunefi_mission")
                print(f"  IMPORTANT: {line[:100]}")
    print("  Report #71022: Submitted 26 Mar, awaiting triage")
    print("  Check dashboard: https://bugs.immunefi.com/dashboard/submission/71022")
    return {"status": "ok"}


# ================================================================
# MISSION 4: ALGORA BOUNTY SCANNER
# ================================================================
def mission_algora_bounties():
    """Find new Algora bounties matching our skills."""
    print("\n[MISSION] Algora Bounty Scanner")
    # Search for bounty issues on GitHub with Algora labels
    out = _run("gh search issues 'label:\"algora\" OR label:\"bounty\"' --state=open --limit=30 --json title,url,labels,repository 2>/dev/null")
    if not out:
        print("  No results from gh search")
        return {"status": "error"}

    try:
        issues = json.loads(out)
    except:
        print(f"  Parse error: {out[:200]}")
        return {"status": "error"}

    matching = []
    our_skills = ["mcp", "typescript", "python", "solidity", "security", "api", "agent", "ai",
                  "docker", "node", "react", "blockchain", "crypto", "web3"]

    for issue in issues:
        title = issue.get("title", "").lower()
        url = issue.get("url", "")
        repo = issue.get("repository", {}).get("nameWithOwner", "")

        # Check if matches our skills
        score = sum(1 for skill in our_skills if skill in title or skill in repo.lower())
        if score >= 1:
            # Extract bounty value from labels
            labels = [l.get("name", "") for l in issue.get("labels", [])]
            value = ""
            for label in labels:
                if "$" in label or "bounty" in label.lower():
                    value = label

            matching.append({
                "title": issue.get("title", "")[:60],
                "url": url,
                "repo": repo,
                "score": score,
                "value": value,
            })

    matching.sort(key=lambda x: x["score"], reverse=True)
    for m in matching[:10]:
        print(f"  [{m['score']}] {m['repo']}: {m['title']} {m['value']}")
        if m["score"] >= 3:
            _alert(f"HIGH-MATCH bounty: {m['repo']} — {m['title']} {m['value']}", "algora_mission")

    return {"status": "ok", "total": len(issues), "matching": len(matching), "top": matching[:10]}


# ================================================================
# MISSION 5: PRODUCT METRICS DASHBOARD
# ================================================================
def mission_product_metrics():
    """Check all 12 products for growth signals."""
    print("\n[MISSION] Product Metrics Dashboard")
    repos = [
        "ElromEvedElElyon/claw-mcp-toolkit",
        "ElromEvedElElyon/chainlink-sentinel",
        "ElromEvedElElyon/flash-payment-system",
        "ElromEvedElElyon/revenue-mcp",
        "ElromEvedElElyon/sovereign-agent-chain",
        "ElromEvedElElyon/sovereign-agent-market",
        "ElromEvedElElyon/sovereign-pay",
        "ElromEvedElElyon/sovereign-pay-lite",
        "ElromEvedElElyon/lido-mcp-server",
        "ElromEvedElElyon/commerce-pay-mcp",
        "ElromEvedElElyon/mcp-crypto-prices",
        "ElromEvedElElyon/washwatch",
    ]

    total_stars = 0
    total_forks = 0
    for repo in repos:
        out = _run(f"gh api repos/{repo} --jq '.stargazers_count,.forks_count,.open_issues_count' 2>/dev/null")
        if out:
            nums = out.strip().splitlines()
            if len(nums) >= 2:
                stars = int(nums[0])
                forks = int(nums[1])
                total_stars += stars
                total_forks += forks
                if stars > 0 or forks > 0:
                    print(f"  {repo.split('/')[1]}: {stars} stars, {forks} forks")

    print(f"  TOTAL: {total_stars} stars, {total_forks} forks across {len(repos)} repos")

    # Check npm downloads
    npm_data = _http_get("https://api.npmjs.org/downloads/point/last-week/claw-mcp-toolkit")
    if npm_data and "downloads" in npm_data:
        downloads = npm_data["downloads"]
        print(f"  npm claw-mcp-toolkit: {downloads} downloads/week")
        if downloads > 50:
            _alert(f"npm claw-mcp-toolkit: {downloads} weekly downloads!", "product_mission")

    return {"status": "ok", "stars": total_stars, "forks": total_forks}


# ================================================================
# MISSION 6: FREELANCE PLATFORM READINESS
# ================================================================
def mission_freelance_readiness():
    """Check readiness for freelance platforms."""
    print("\n[MISSION] Freelance Platform Readiness Check")

    platforms = [
        {"name": "Alignerr", "url": "https://www.alignerr.com", "skill": "Portuguese Brazil Coder", "pay": "$25-65/hr"},
        {"name": "Outlier AI", "url": "https://app.outlier.ai", "skill": "Coding tasks", "pay": "$25-65/hr"},
        {"name": "DataAnnotation", "url": "https://app.dataannotation.tech", "skill": "Coding projects", "pay": "$40/hr"},
        {"name": "Scale AI", "url": "https://scale.com", "skill": "Portuguese AI training", "pay": "$40-80/hr"},
        {"name": "LaborX", "url": "https://laborx.com", "skill": "Smart contracts, MCP, AI agents", "pay": "$200-500/gig"},
    ]

    for p in platforms:
        print(f"  {p['name']}: {p['skill']} — {p['pay']}")
        print(f"    Register: {p['url']}")

    print("\n  YOUR SKILLS MATCH:")
    print("  - Python (expert) + TypeScript (expert) + Solidity (advanced)")
    print("  - MCP Server development (29+ tools built)")
    print("  - Smart contract security (audits, bug bounties)")
    print("  - Portuguese Brazil NATIVE (premium for AI training)")
    print("  - 12 products published, 40+ PRs in major repos")

    return {"status": "ok", "platforms": len(platforms)}


# ================================================================
# MISSION 7: MERCADO LIVRE DIGITAL PRODUCTS
# ================================================================
def mission_mercadolivre_check():
    """Check ML seller registration and digital product readiness."""
    print("\n[MISSION] Mercado Livre Digital Products")
    print("  CNPJ: 51.148.891/0001-69 (PADRAO BITCOIN)")
    print("  Seller Type: Professional (EPP)")
    print("")
    print("  DIGITAL PRODUCTS READY TO LIST:")
    print("  1. MCP Server Templates Pack — R$49.90")
    print("  2. Smart Contract Audit Checklist — R$29.90")
    print("  3. AI Agent Builder Course — R$79.90")
    print("  4. Crypto Trading Bot Framework — R$99.90")
    print("  5. Web3 Security Scanner License — R$149.90")
    print("")
    print("  ACTION: Register at vendedores.mercadolivre.com.br")
    print("  MARGIN: 60-85% (digital = no inventory)")
    return {"status": "ok"}


# ================================================================
# MAIN
# ================================================================
ALL_MISSIONS = {
    "nuclei_prs": mission_nuclei_prs,
    "wallet_monitor": mission_wallet_monitor,
    "immunefi_status": mission_immunefi_status,
    "algora_bounties": mission_algora_bounties,
    "product_metrics": mission_product_metrics,
    "freelance_readiness": mission_freelance_readiness,
    "mercadolivre": mission_mercadolivre_check,
}

def run_all():
    print("=" * 60)
    print("  REVENUE MISSIONS — Full Sweep")
    print(f"  {datetime.now(BRT).isoformat()}")
    print("=" * 60)

    data = _load_missions()
    for name, func in ALL_MISSIONS.items():
        try:
            result = func()
            data["missions"][name] = {
                "last_run": datetime.now(BRT).isoformat(),
                "status": result.get("status", "?"),
                "summary": str(result)[:200],
            }
        except Exception as e:
            print(f"  ERROR in {name}: {e}")
            data["missions"][name] = {"last_run": datetime.now(BRT).isoformat(), "status": "error"}
    _save_missions(data)
    print("\n" + "=" * 60)
    print("  ALL MISSIONS COMPLETE")
    print("=" * 60)


def show_status():
    data = _load_missions()
    print("=" * 60)
    print("  REVENUE MISSIONS — Status")
    print("=" * 60)
    for name, info in data.get("missions", {}).items():
        print(f"  {name}: {info.get('status','?')} — last: {info.get('last_run','never')[:19]}")
    print(f"\n  Total checks: {data.get('total_checks', 0)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "run-all":
        run_all()
    elif cmd == "run" and len(sys.argv) > 2:
        name = sys.argv[2]
        if name in ALL_MISSIONS:
            ALL_MISSIONS[name]()
        else:
            print(f"Unknown mission: {name}")
    elif cmd == "status":
        show_status()
    else:
        print(f"Usage: {sys.argv[0]} status|run-all|run NAME")
