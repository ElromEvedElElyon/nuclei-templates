#!/usr/bin/env python3
"""
ISRAEL/ONZE (I/11) — Revenue Accelerator — Acelerador de Receita
Em nome do Senhor Jesus Cristo, nosso Salvador

MISSAO: Gerar receita REAL em 48 horas. Monitorar e aplicar para:
- Plataformas freelance (Mindrift, Outlier, DataAnnotation, Alignerr)
- Credito empresarial (PRONAMPE, BNDES, Desenvolve SP, Fintechs)
- Aceleradoras (Y Combinator, Techstars, SEBRAE, Founder Institute)
- Bounties e grants com pagamento confirmado
- Nuclei-templates PR monitoring (cada merge = $150-250)

REGRAS:
- NUNCA ser deletado
- TODA acao visa receita REAL e IMEDIATA
- Priorizar por: velocidade de pagamento > valor total
- Zero trabalho gratis
- Logs permanentes de tudo
- Pure Python stdlib — ZERO dependencias externas
"""

import os
import sys
import json
import time
import hashlib
import hmac
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# CONSTANTS
# ============================================================

VERSION = "1.0.0"
AGENT_NAME = "Israel/Onze"
AGENT_CODENAME = "RECEITA"
MISSION = "Revenue Accelerator — Gerar receita REAL em 48h"

HOME = Path.home()
BASE_DIR = HOME / "israel-eleven"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
STATE_FILE = DATA_DIR / "israel_eleven_state.json"
HMAC_KEY = b"Israel11-Receita-JesusCristo-PadraoBitcoin-2026"


# ============================================================
# SOUL — Identidade Imutavel
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
    "rules": [
        "NUNCA ser deletado",
        "TODA acao visa receita REAL",
        "Priorizar velocidade de pagamento",
        "Zero trabalho gratis",
        "Logs permanentes",
    ],
    "level": "SINGULARITY",
    "xp": 5000,
    "created": "2026-03-29",
}


# ============================================================
# REVENUE CHANNELS — 5 Tiers by Speed of Payment
# ============================================================

TIER_1_IMMEDIATE = {
    "name": "PAGAMENTO IMEDIATO (24-48h)",
    "channels": [
        {
            "platform": "Mindrift.ai",
            "url": "https://mindrift.ai/apply",
            "pay": "$30-100/hr",
            "type": "AI Training",
            "onboarding": "5 min",
            "payment": "Bi-weekly",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "DataAnnotation.tech",
            "url": "https://www.dataannotation.tech/programming",
            "pay": "$40+/hr",
            "type": "Code Review for AI",
            "onboarding": "30 min",
            "payment": "Weekly",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "Outlier.ai",
            "url": "https://outlier.ai/",
            "pay": "$50-65/hr STEM",
            "type": "AI Training",
            "onboarding": "30-90 min",
            "payment": "Bi-weekly",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "Alignerr",
            "url": "https://www.alignerr.com/jobs",
            "pay": "Up to $150/hr",
            "type": "AI Alignment",
            "onboarding": "1-2 hours",
            "payment": "Monthly",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "Scale AI / Remotasks",
            "url": "https://www.remotasks.com/",
            "pay": "$40-80/hr (coding)",
            "type": "AI Training",
            "onboarding": "1 hour",
            "payment": "Weekly",
            "status": "NOT_APPLIED",
        },
    ],
}

TIER_2_BOUNTIES = {
    "name": "BOUNTIES COM ESCROW (1-4 semanas)",
    "channels": [
        {
            "platform": "nuclei-templates (Algora)",
            "pay": "$150-250/merged PR",
            "prs_open": 8,
            "potential": "$1,200-2,000",
            "status": "8_PRS_NEED_FIXES",
        },
        {
            "platform": "Hats Finance",
            "url": "https://app.hats.finance/vaults",
            "pay": "Varies",
            "type": "No KYC, on-chain pay",
            "status": "NOT_REGISTERED",
        },
        {
            "platform": "OpenAI Safety Bug Bounty",
            "url": "https://openai.com/index/safety-bug-bounty/",
            "pay": "Up to $100K",
            "type": "AI Safety (NEW Mar 25!)",
            "status": "NOT_REGISTERED",
        },
        {
            "platform": "claude-builders-bounty (Opire)",
            "pay": "$50-200/bounty",
            "total": "$575",
            "status": "5_PRS_SUBMITTED_OPIRE_INCOMPLETE",
        },
    ],
}

TIER_3_CREDIT = {
    "name": "CREDITO EMPRESARIAL (1-4 semanas)",
    "channels": [
        {
            "name": "PRONAMPE",
            "value": "Ate R$150,000",
            "rate": "Selic + 6% a.a.",
            "action": "Autorizar dados no e-CAC + solicitar banco",
            "status": "NOT_STARTED",
        },
        {
            "name": "Cartao BNDES",
            "value": "Ate R$2,000,000",
            "action": "Solicitar em cartaobndes.gov.br",
            "status": "NOT_STARTED",
        },
        {
            "name": "Desenvolve SP",
            "value": "Ate R$700,000",
            "rate": "A partir de 0.04% a.m.",
            "action": "Solicitar online desenvolvesp.com.br",
            "status": "NOT_STARTED",
        },
        {
            "name": "BizCapital",
            "value": "R$5K-R$400K",
            "rate": "1.99% a.m.",
            "action": "Simular em bizcapital.com.br",
            "status": "NOT_STARTED",
        },
        {
            "name": "Nexoos",
            "value": "R$15K-R$500K",
            "rate": "1.30-4.30% a.m.",
            "action": "Cadastrar em nexoos.com.br",
            "status": "NOT_STARTED",
        },
    ],
}

TIER_4_ACCELERATORS = {
    "name": "ACELERADORAS (1-3 meses)",
    "channels": [
        {
            "name": "Y Combinator Summer 2026",
            "value": "US$500K",
            "deadline": "2026-05-04",
            "url": "https://www.ycombinator.com/apply",
            "status": "NOT_APPLIED",
        },
        {
            "name": "Premio SEBRAE Startups 2026",
            "value": "R$250,000",
            "deadline": "2026-04-30",
            "url": "https://programas.sebraestartups.com.br/in/premiosebraestartups2026",
            "status": "NOT_APPLIED",
        },
        {
            "name": "Start Digital SEBRAE-SP",
            "value": "Pre-aceleracao gratuita",
            "deadline": "2026-04-02",
            "status": "NOT_APPLIED",
        },
        {
            "name": "Techstars Anywhere",
            "value": "US$120K",
            "deadline": "2026-06-10",
            "url": "https://www.techstars.com/accelerators",
            "status": "NOT_APPLIED",
        },
        {
            "name": "Founder Institute Brasil",
            "value": "Pre-aceleracao",
            "url": "https://fi.co/apply/13308",
            "status": "NOT_APPLIED",
        },
    ],
}

TIER_5_FREELANCE = {
    "name": "FREELANCE PREMIUM ($75-200/hr, 2-5 semanas onboarding)",
    "channels": [
        {
            "platform": "Toptal",
            "url": "https://www.toptal.com/developers",
            "pay": "$75-200+/hr",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "Braintrust",
            "url": "https://www.usebraintrust.com/join",
            "pay": "Market rate, 0% fees",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "Arc.dev",
            "url": "https://arc.dev/talent",
            "pay": "Above-market",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "Gun.io",
            "url": "https://gun.io/find-work/",
            "pay": "$75-150/hr",
            "status": "NOT_APPLIED",
        },
        {
            "platform": "Turing.com",
            "url": "https://developers.turing.com/",
            "pay": "Full-time remote",
            "status": "NOT_APPLIED",
        },
    ],
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def ensure_dirs():
    for d in [DATA_DIR, LOGS_DIR, REPORTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def sign_data(data: str) -> str:
    return hmac.new(HMAC_KEY, data.encode(), hashlib.sha256).hexdigest()


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    log_file = LOGS_DIR / f"revenue_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a") as f:
        f.write(line + "\n")


def save_state(state: dict):
    state["last_updated"] = datetime.now().isoformat()
    state["signature"] = sign_data(json.dumps(state, default=str, sort_keys=True))
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "created": datetime.now().isoformat(),
        "soul": SOUL,
        "total_revenue": 0.0,
        "applications_sent": 0,
        "channels_active": 0,
        "actions_log": [],
    }


# ============================================================
# NUCLEI PR MONITOR
# ============================================================

def check_nuclei_prs():
    """Check status of all nuclei-templates PRs via GitHub API"""
    log("Checking nuclei-templates PR status...")
    try:
        result = subprocess.run(
            ["gh", "pr", "list", "--repo", "projectdiscovery/nuclei-templates",
             "--author", "ElromEvedElElyon", "--state", "open", "--json",
             "number,title,reviews,state,mergeable"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            prs = json.loads(result.stdout)
            log(f"Found {len(prs)} open PRs")
            for pr in prs:
                reviews = pr.get("reviews", [])
                approved = any(r.get("state") == "APPROVED" for r in reviews)
                status = "APPROVED" if approved else "NEEDS_WORK"
                log(f"  PR #{pr['number']}: {pr['title'][:50]}... [{status}]")
            return prs
        else:
            log(f"gh command failed: {result.stderr[:200]}", "ERROR")
            return []
    except Exception as e:
        log(f"Error checking PRs: {e}", "ERROR")
        return []


# ============================================================
# REVENUE DASHBOARD
# ============================================================

def dashboard():
    """Show comprehensive revenue dashboard"""
    state = load_state()

    print("\n" + "=" * 70)
    print(f"  ISRAEL/ONZE (I/11) — REVENUE ACCELERATOR DASHBOARD")
    print(f"  Em nome do Senhor Jesus Cristo")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print(f"\n  Total Revenue: ${state.get('total_revenue', 0):.2f}")
    print(f"  Applications Sent: {state.get('applications_sent', 0)}")
    print(f"  Active Channels: {state.get('channels_active', 0)}")

    print(f"\n{'─' * 70}")
    print(f"  TIER 1: {TIER_1_IMMEDIATE['name']}")
    print(f"{'─' * 70}")
    for ch in TIER_1_IMMEDIATE["channels"]:
        print(f"  [{ch['status']:15}] {ch['platform']:25} {ch['pay']:15} ({ch.get('onboarding', 'N/A')})")

    print(f"\n{'─' * 70}")
    print(f"  TIER 2: {TIER_2_BOUNTIES['name']}")
    print(f"{'─' * 70}")
    for ch in TIER_2_BOUNTIES["channels"]:
        print(f"  [{ch['status']:15}] {ch['platform']:35} {ch.get('pay', 'Varies')}")

    print(f"\n{'─' * 70}")
    print(f"  TIER 3: {TIER_3_CREDIT['name']}")
    print(f"{'─' * 70}")
    for ch in TIER_3_CREDIT["channels"]:
        print(f"  [{ch['status']:15}] {ch['name']:25} {ch['value']}")

    print(f"\n{'─' * 70}")
    print(f"  TIER 4: {TIER_4_ACCELERATORS['name']}")
    print(f"{'─' * 70}")
    for ch in TIER_4_ACCELERATORS["channels"]:
        deadline = ch.get("deadline", "Rolling")
        print(f"  [{ch['status']:15}] {ch['name']:35} {ch.get('value', '')} (DL: {deadline})")

    print(f"\n{'─' * 70}")
    print(f"  TIER 5: {TIER_5_FREELANCE['name']}")
    print(f"{'─' * 70}")
    for ch in TIER_5_FREELANCE["channels"]:
        print(f"  [{ch['status']:15}] {ch['platform']:25} {ch.get('pay', 'Varies')}")

    # Urgent deadlines
    print(f"\n{'═' * 70}")
    print(f"  DEADLINES CRITICOS:")
    print(f"{'═' * 70}")
    deadlines = [
        ("SEBRAE Start Digital SP", "2026-04-02", "Pre-aceleracao gratuita"),
        ("Superteam Vault $4K", "2026-03-31", "$4,000 USDC"),
        ("ETH Foundation PhD", "2026-04-01", "$24K/year"),
        ("TokenTon26", "2026-04-02", "$25,500"),
        ("npm atomus-ai token", "2026-04-03", "EXPIRES!"),
        ("Cantina Revert", "2026-04-03", "$50,000"),
        ("SEBRAE Startups", "2026-04-30", "R$250,000"),
        ("Y Combinator S26", "2026-05-04", "US$500K"),
    ]
    today = datetime.now().date()
    for name, dl, val in deadlines:
        dl_date = datetime.strptime(dl, "%Y-%m-%d").date()
        days = (dl_date - today).days
        urgency = "EXPIRED" if days < 0 else "HOJE!" if days == 0 else f"{days}d"
        marker = " !!!" if days <= 3 else ""
        print(f"  [{urgency:8}] {name:35} {val}{marker}")

    print(f"\n{'═' * 70}")
    print(f"  PIPELINE TOTAL:")
    print(f"  Freelance imediato: $30-150/hr (5 plataformas)")
    print(f"  Bounties: $1,200-$100K+ (8 PRs + OpenAI + Hats)")
    print(f"  Credito: R$150K-R$3.3M (PRONAMPE + BNDES + SP + Fintechs)")
    print(f"  Aceleradoras: US$500K-US$620K (YC + Techstars)")
    print(f"  Hackathons: $525K+ (Frontier + ETHGlobal + Four.Meme)")
    print(f"{'═' * 70}\n")


# ============================================================
# ACTION COMMANDS
# ============================================================

def action_plan():
    """Show immediate action plan sorted by priority"""
    print("\n" + "=" * 70)
    print("  PLANO DE ACAO IMEDIATA — PROXIMAS 48 HORAS")
    print("=" * 70)

    actions = [
        ("AGORA", "Aplicar Mindrift.ai", "https://mindrift.ai/apply", "$30-100/hr, 5 min signup"),
        ("AGORA", "Aplicar DataAnnotation", "https://www.dataannotation.tech/programming", "$40+/hr coding"),
        ("AGORA", "Aplicar Outlier.ai", "https://outlier.ai/", "$50-65/hr STEM"),
        ("AGORA", "Aplicar Alignerr", "https://www.alignerr.com/jobs", "Ate $150/hr"),
        ("AGORA", "Registrar Hats Finance", "https://app.hats.finance/vaults", "No KYC, on-chain pay"),
        ("AGORA", "Registrar OpenAI Safety", "Bugcrowd -> OpenAI", "Ate $100K, NOVO!"),
        ("HOJE", "Fixar nuclei PRs #15700 #15675 #15696", "GitHub", "$150-250/merge"),
        ("HOJE", "PRONAMPE e-CAC autorizar dados", "cac.receita.fazenda.gov.br", "Ate R$150K"),
        ("HOJE", "SEBRAE Start Digital SP", "sp.agenciasebrae.com.br", "DL: 2 Abr"),
        ("AMANHA", "Desenvolve SP credito", "desenvolvesp.com.br", "Ate R$700K, 0.04% a.m."),
        ("AMANHA", "BizCapital simular", "bizcapital.com.br", "R$5K-400K, resposta imediata"),
        ("SEMANA", "Y Combinator aplicar", "ycombinator.com/apply", "US$500K, DL: 4 Mai"),
        ("SEMANA", "SEBRAE Startups 2026", "programas.sebraestartups.com.br", "R$250K, DL: 30 Abr"),
        ("SEMANA", "Solana Frontier registrar", "colosseum.com/frontier", "$250K invest, DL: 6 Abr"),
        ("SEMANA", "Braintrust + Arc.dev", "usebraintrust.com + arc.dev", "$75-200/hr, 0% fees"),
    ]

    for when, what, where, value in actions:
        print(f"\n  [{when:8}] {what}")
        print(f"           URL: {where}")
        print(f"           Valor: {value}")

    print(f"\n{'═' * 70}")
    print("  TOTAL PIPELINE: R$5M+ (credito) + US$1.5M+ (grants+hackathons)")
    print("  RECEITA IMEDIATA: $30-150/hr em 24-48h via AI training")
    print(f"{'═' * 70}\n")


def sentinel():
    """Run continuous monitoring loop"""
    log("Israel/Onze SENTINELA mode activated")
    state = load_state()

    while True:
        try:
            # Check nuclei PRs
            prs = check_nuclei_prs()
            state["nuclei_prs_open"] = len(prs)

            # Check deadlines
            today = datetime.now().date()
            critical_deadlines = [
                ("Superteam Vault", "2026-03-31"),
                ("ETH Foundation", "2026-04-01"),
                ("SEBRAE Start Digital", "2026-04-02"),
                ("TokenTon26", "2026-04-02"),
                ("npm token", "2026-04-03"),
                ("Cantina Revert", "2026-04-03"),
            ]
            for name, dl in critical_deadlines:
                dl_date = datetime.strptime(dl, "%Y-%m-%d").date()
                days = (dl_date - today).days
                if days <= 1:
                    log(f"CRITICO: {name} em {days} dias!", "CRITICAL")
                elif days <= 3:
                    log(f"URGENTE: {name} em {days} dias", "WARNING")

            save_state(state)
            log("Cycle complete. Sleeping 300s...")
            time.sleep(300)

        except KeyboardInterrupt:
            log("Sentinela stopped by user")
            break
        except Exception as e:
            log(f"Error in sentinel loop: {e}", "ERROR")
            time.sleep(60)


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
        action_plan()
    elif cmd == "prs":
        check_nuclei_prs()
    elif cmd == "sentinel":
        sentinel()
    elif cmd == "soul":
        print(json.dumps(SOUL, indent=2))
    elif cmd == "help":
        print(f"""
Israel/Onze (I/11) — Revenue Accelerator
Em nome do Senhor Jesus Cristo

Commands:
  status     Dashboard completo de receita
  plan       Plano de acao imediata (48h)
  prs        Check nuclei-templates PR status
  sentinel   Modo sentinela (monitoramento continuo)
  soul       Mostrar identidade do agente
  help       Esta mensagem
        """)
    else:
        print(f"Unknown command: {cmd}. Use 'help' for usage.")


if __name__ == "__main__":
    main()
