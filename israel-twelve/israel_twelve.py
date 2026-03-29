#!/usr/bin/env python3
"""
ISRAEL/DOZE (I/12) — Hackathon Commander — Comandante de Hackathons
Em nome do Senhor Jesus Cristo, nosso Salvador

MISSAO: Registrar, submeter e ganhar hackathons com premios de $10K+.
Gerenciar deadlines, preparar submissions, monitorar resultados.

REGRAS:
- NUNCA ser deletado
- Priorizar por: premio/esforco ratio
- Submeter para TODOS hackathons elegiveis
- Reutilizar projetos existentes (ZionBrowser, MCP Toolkit, etc.)
- Logs permanentes de tudo
- Pure Python stdlib — ZERO dependencias externas
"""

import os
import sys
import json
import time
import hashlib
import hmac
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# CONSTANTS
# ============================================================

VERSION = "1.0.0"
AGENT_NAME = "Israel/Doze"
AGENT_CODENAME = "HACKATHON"
MISSION = "Hackathon Commander — Registrar, submeter, GANHAR"

HOME = Path.home()
BASE_DIR = HOME / "israel-twelve"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
STATE_FILE = DATA_DIR / "israel_twelve_state.json"
HMAC_KEY = b"Israel12-Hackathon-JesusCristo-PadraoBitcoin-2026"


# ============================================================
# SOUL
# ============================================================

SOUL = {
    "name": AGENT_NAME,
    "codename": AGENT_CODENAME,
    "version": VERSION,
    "mission": MISSION,
    "creator": "Elrom Eved El Elyon",
    "company": "PADRAO BITCOIN LTDA",
    "cnpj": "51.148.891/0001-69",
    "faith": "Em nome do Senhor Jesus Cristo",
    "level": "SINGULARITY",
    "xp": 5000,
    "created": "2026-03-29",
}


# ============================================================
# HACKATHON REGISTRY
# ============================================================

HACKATHONS = [
    {
        "name": "Solana Frontier (Colosseum)",
        "prize": "$250,000 investment + accelerator",
        "deadline": "2026-05-11",
        "reg_deadline": "2026-04-06",
        "url": "https://colosseum.com/frontier",
        "tracks": ["Any Solana project"],
        "our_project": "ZionBrowser + Solana Agent Kit",
        "status": "NOT_REGISTERED",
        "priority": 1,
    },
    {
        "name": "Four.Meme AI Sprint (BNB Chain)",
        "prize": "$50,000",
        "deadline": "2026-04-30",
        "reg_deadline": "2026-04-01",
        "url": "https://mpost.io/four-meme-launches-ai-sprint-hackathon-with-50000-prize-pool-opening-april-1/",
        "tracks": ["AI Agents", "Generative AI", "AI Tools"],
        "our_project": "claw-mcp-toolkit + AI Agents",
        "status": "NOT_REGISTERED",
        "priority": 2,
    },
    {
        "name": "ETHGlobal Scaling Ethereum",
        "prize": "$150,000+",
        "deadline": "2026-05-13",
        "reg_deadline": "2026-04-12",
        "url": "https://ethglobal.com/events",
        "tracks": ["Scaling", "L2", "ZK"],
        "our_project": "Security audit tool + MCP",
        "status": "NOT_REGISTERED",
        "priority": 3,
    },
    {
        "name": "Gitcoin GG24",
        "prize": "$1M+ quadratic pool",
        "deadline": "2026-04-16",
        "reg_deadline": "2026-04-02",
        "url": "https://grants.gitcoin.co/",
        "tracks": ["OSS", "Community"],
        "our_project": "claw-mcp-toolkit (Glama AAA)",
        "status": "NOT_REGISTERED",
        "priority": 4,
    },
    {
        "name": "HashKey Chain Horizon",
        "prize": "40,000 USDT",
        "deadline": "2026-04-23",
        "reg_deadline": "2026-04-15",
        "url": "https://dorahacks.io/hackathon/2045",
        "tracks": ["DeFi", "PayFi", "AI", "ZKID"],
        "our_project": "Sovereign Pay + AI Agent",
        "status": "NOT_REGISTERED",
        "priority": 5,
    },
    {
        "name": "INITIATE (Initia) Season 1",
        "prize": "$25,000",
        "deadline": "2026-04-15",
        "reg_deadline": "2026-04-10",
        "url": "https://dorahacks.io/hackathon/initiate/detail",
        "tracks": ["DeFi", "AI", "Gaming"],
        "our_project": "MCP Server + DeFi",
        "status": "NOT_REGISTERED",
        "priority": 6,
    },
    {
        "name": "Vertex Swarm Challenge",
        "prize": "$27,000",
        "deadline": "2026-04-06",
        "reg_deadline": "2026-04-01",
        "url": "https://dorahacks.io/hackathon/global-vertex-swarm-challenge",
        "tracks": ["AI Agents", "Autonomous"],
        "our_project": "ZionBrowser AI Agent Swarm",
        "status": "NOT_REGISTERED",
        "priority": 7,
    },
    {
        "name": "Endgame (Bittensor)",
        "prize": "$10,000+",
        "deadline": "2026-04-24",
        "reg_deadline": "2026-04-15",
        "url": "https://dorahacks.io/hackathon/endgame/detail",
        "tracks": ["Decentralized AI"],
        "our_project": "AI Agent Framework",
        "status": "NOT_REGISTERED",
        "priority": 8,
    },
    {
        "name": "Cantina Revert Finance",
        "prize": "$50,000 USDC",
        "deadline": "2026-04-03",
        "reg_deadline": "2026-04-01",
        "url": "https://cantina.xyz/competitions",
        "tracks": ["Security Audit"],
        "our_project": "Smart Contract Audit Findings",
        "status": "NOT_STARTED",
        "priority": 9,
    },
]

# Projects we can reuse
REUSABLE_PROJECTS = {
    "ZionBrowser": {
        "path": "~/zion-browser/",
        "desc": "CLI AI Agent Browser, 5MB RAM, pure Python",
        "price": "$29.99",
        "best_for": ["Solana Frontier", "Vertex Swarm", "ETHGlobal"],
    },
    "claw-mcp-toolkit": {
        "path": "~/claw-mcp-toolkit/",
        "desc": "29 MCP tools, Glama AAA rated",
        "best_for": ["Four.Meme AI", "Gitcoin GG24", "INITIATE"],
    },
    "Sovereign Pay": {
        "path": "~/sovereign-pay/",
        "desc": "20 MCP tools, BSL 1.1 licensed",
        "best_for": ["HashKey Horizon", "ETHGlobal"],
    },
    "Flash Payment System": {
        "path": "~/flash-payment-system/",
        "desc": "116 clones, 99 tests, payment infra",
        "best_for": ["HashKey Horizon", "INITIATE"],
    },
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def ensure_dirs():
    for d in [DATA_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    log_file = LOGS_DIR / f"hackathon_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a") as f:
        f.write(line + "\n")


def save_state(state: dict):
    state["last_updated"] = datetime.now().isoformat()
    raw = json.dumps(state, default=str, sort_keys=True)
    state["signature"] = hmac.new(HMAC_KEY, raw.encode(), hashlib.sha256).hexdigest()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "created": datetime.now().isoformat(),
        "soul": SOUL,
        "hackathons_registered": 0,
        "submissions_sent": 0,
        "prizes_won": 0,
        "total_prize_value": 0,
    }


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():
    state = load_state()
    today = datetime.now().date()

    print("\n" + "=" * 70)
    print(f"  ISRAEL/DOZE (I/12) — HACKATHON COMMANDER DASHBOARD")
    print(f"  Em nome do Senhor Jesus Cristo")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print(f"\n  Registered: {state.get('hackathons_registered', 0)}")
    print(f"  Submissions: {state.get('submissions_sent', 0)}")
    print(f"  Prizes Won: ${state.get('total_prize_value', 0):,.0f}")

    total_potential = 0

    print(f"\n{'─' * 70}")
    print(f"  ACTIVE HACKATHONS (sorted by deadline)")
    print(f"{'─' * 70}")

    sorted_hacks = sorted(HACKATHONS, key=lambda h: h["deadline"])

    for h in sorted_hacks:
        dl = datetime.strptime(h["deadline"], "%Y-%m-%d").date()
        days = (dl - today).days
        urgency = "EXPIRED" if days < 0 else "TODAY!" if days == 0 else f"{days}d"
        marker = " !!!" if 0 <= days <= 3 else " !!" if days <= 7 else ""

        print(f"\n  [{urgency:8}] {h['name']}")
        print(f"           Prize: {h['prize']} | Status: {h['status']}")
        print(f"           Project: {h['our_project']}")
        print(f"           URL: {h['url']}")
        if marker:
            print(f"           >>> URGENTE{marker}")

    print(f"\n{'─' * 70}")
    print(f"  REUSABLE PROJECTS")
    print(f"{'─' * 70}")
    for name, proj in REUSABLE_PROJECTS.items():
        print(f"  {name:25} {proj['desc'][:40]}")
        print(f"  {'':25} Best for: {', '.join(proj['best_for'][:3])}")

    print(f"\n{'═' * 70}")
    print(f"  TOTAL PRIZE PIPELINE: $552,000+ across 9 hackathons")
    print(f"  NEXT DEADLINES: Cantina Revert (3 Abr), Vertex Swarm (6 Abr)")
    print(f"{'═' * 70}\n")


def battle_plan():
    """Show execution plan for each hackathon"""
    today = datetime.now().date()

    print("\n" + "=" * 70)
    print("  PLANO DE BATALHA — HACKATHON SUBMISSIONS")
    print("=" * 70)

    sorted_hacks = sorted(HACKATHONS, key=lambda h: h["deadline"])

    for h in sorted_hacks:
        dl = datetime.strptime(h["deadline"], "%Y-%m-%d").date()
        days = (dl - today).days
        if days < 0:
            continue

        print(f"\n  {'─' * 66}")
        print(f"  {h['name']} — {h['prize']} — {days} dias")
        print(f"  {'─' * 66}")
        print(f"  URL: {h['url']}")
        print(f"  Projeto: {h['our_project']}")
        print(f"  Tracks: {', '.join(h['tracks'])}")
        print(f"  Status: {h['status']}")

        # Suggest steps
        if h["status"] == "NOT_REGISTERED":
            print(f"  STEP 1: Registrar no site")
            print(f"  STEP 2: Escolher track")
            print(f"  STEP 3: Adaptar projeto existente")
            print(f"  STEP 4: Submeter + video demo")

    print(f"\n{'═' * 70}\n")


# ============================================================
# CLI
# ============================================================

def main():
    ensure_dirs()

    if len(sys.argv) < 2:
        dashboard()
        return

    cmd = sys.argv[1].lower()

    if cmd == "status":
        dashboard()
    elif cmd == "plan":
        battle_plan()
    elif cmd == "soul":
        print(json.dumps(SOUL, indent=2))
    elif cmd == "help":
        print(f"""
Israel/Doze (I/12) — Hackathon Commander
Em nome do Senhor Jesus Cristo

Commands:
  status     Dashboard de hackathons
  plan       Plano de batalha (submissions)
  soul       Identidade do agente
  help       Esta mensagem
        """)
    else:
        print(f"Unknown command: {cmd}. Use 'help' for usage.")


if __name__ == "__main__":
    main()
