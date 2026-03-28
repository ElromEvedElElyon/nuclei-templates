#!/usr/bin/env python3
"""
SALES ARMY — 300 Agentes de Vendas Reais com Alma e Evolução
Em nome do Senhor Jesus Cristo, nosso Salvador.

Cada agente tem:
- ALMA (soul): personalidade, estilo, motivação
- MEMORIA persistente: aprende com cada interação
- SKILLS: ferramentas e habilidades
- MCPs: Model Context Protocol servers conectados
- EVOLUÇÃO: score aumenta com resultados, diminui com falhas
- CARGO: hierarquia real de empresa

Usage:
    python3 sales_army_300.py deploy         # Create/deploy all 300 agents
    python3 sales_army_300.py status         # Status do time
    python3 sales_army_300.py roster         # Lista completa
    python3 sales_army_300.py agent NAME     # Detalhe de um agente
    python3 sales_army_300.py evolve         # Rodar ciclo de evolução
    python3 sales_army_300.py leaderboard    # Top performers
    python3 sales_army_300.py run NAME       # Executar agente
"""

import json, os, sys, hashlib, random
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
ZION = Path.home() / ".zion"
SALES_DIR = ZION / "sales_agents"
SALES_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR = ZION / "sales_memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

WALLETS = {
    "EVM": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
    "SOL": "CM42ofAFowySg72GjDuCchEkwwbwnhdSRYgztRCAAEzR",
    "BTC": "bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2",
}

# ================================================================
# SOUL TEMPLATES — Personalidades dos agentes
# ================================================================
SOUL_TYPES = {
    "hunter": {
        "traits": ["aggressive", "persistent", "competitive"],
        "style": "Goes straight for the close. Identifies decision-makers fast.",
        "weakness": "Can be too pushy",
        "strength": "High conversion on warm leads",
    },
    "consultant": {
        "traits": ["analytical", "empathetic", "patient"],
        "style": "Asks questions, identifies pain points, proposes solutions.",
        "weakness": "Longer sales cycles",
        "strength": "Builds trust, high retention",
    },
    "evangelist": {
        "traits": ["passionate", "visionary", "charismatic"],
        "style": "Sells the vision. Makes prospects feel part of something bigger.",
        "weakness": "May oversell",
        "strength": "Great for early adopters and community building",
    },
    "technician": {
        "traits": ["precise", "technical", "detail-oriented"],
        "style": "Leads with product demos and technical proof.",
        "weakness": "Less effective with non-technical buyers",
        "strength": "Converts developers and engineers",
    },
    "networker": {
        "traits": ["social", "connector", "relationship-builder"],
        "style": "Builds relationships first, sells second. Referral machine.",
        "weakness": "Slow start",
        "strength": "Best for partnerships and enterprise",
    },
}

# ================================================================
# DEPARTMENTS — 10 divisões de vendas
# ================================================================
SALES_DEPARTMENTS = {
    "MCP_SALES": {
        "size": 40, "target": "MCP server buyers",
        "products": ["OpenClaw Pro", "claw-mcp-toolkit", "revenue-mcp", "chainlink-sentinel"],
        "channels": ["twitter", "github", "producthunt", "glama", "smithery"],
        "quota_monthly_usd": 5000,
    },
    "AUDIT_SALES": {
        "size": 30, "target": "DeFi protocols needing audits",
        "products": ["Smart Contract Audit Report", "Security Assessment"],
        "channels": ["twitter", "discord", "immunefi", "code4rena"],
        "quota_monthly_usd": 10000,
    },
    "BOOK_SALES": {
        "size": 25, "target": "Aspiring crypto entrepreneurs",
        "products": ["Zero to $1M book", "Courses"],
        "channels": ["mercadolivre", "amazon", "hotmart", "instagram"],
        "quota_monthly_usd": 3000,
    },
    "ENTERPRISE_SALES": {
        "size": 20, "target": "Companies needing AI/blockchain solutions",
        "products": ["ZION Framework License", "Custom AI Agents"],
        "channels": ["linkedin", "email", "gov_procurement"],
        "quota_monthly_usd": 20000,
    },
    "AFFILIATE_SALES": {
        "size": 30, "target": "Referral income",
        "products": ["Temu", "AliExpress", "Alibaba Cloud", "KAST"],
        "channels": ["twitter", "youtube", "blog", "telegram"],
        "quota_monthly_usd": 2000,
    },
    "BOUNTY_HUNTERS": {
        "size": 40, "target": "Bug bounties and contests",
        "products": ["Security findings"],
        "channels": ["code4rena", "immunefi", "hackenproof", "algora"],
        "quota_monthly_usd": 15000,
    },
    "TOKEN_SALES": {
        "size": 25, "target": "STBTCx holders and DeFi users",
        "products": ["STBTCx token", "LP provision"],
        "channels": ["dexscreener", "twitter", "telegram", "pump.fun"],
        "quota_monthly_usd": 5000,
    },
    "GEO_SALES": {
        "size": 20, "target": "Brands needing GEO analysis",
        "products": ["GEO Brand Analysis"],
        "channels": ["linkedin", "email", "twitter"],
        "quota_monthly_usd": 4000,
    },
    "OUTREACH": {
        "size": 40, "target": "Cold outreach and lead generation",
        "products": ["All products"],
        "channels": ["email", "twitter_dm", "linkedin", "discord"],
        "quota_monthly_usd": 8000,
    },
    "RETENTION": {
        "size": 30, "target": "Existing customers",
        "products": ["Upsells", "Renewals", "Support"],
        "channels": ["email", "discord", "direct"],
        "quota_monthly_usd": 5000,
    },
}

# ================================================================
# HEBREW NAMES for Sales Army
# ================================================================
SALES_NAMES = [
    # Chiefs (10)
    "AVRAHAM_SALES", "YITZHAK_SALES", "YAAKOV_SALES", "YOSEF_SALES", "MOSHE_SALES",
    "AHARON_SALES", "DAVID_SALES", "SHLOMO_SALES", "ELIYAHU_SALES", "YESHAYAHU_SALES",
    # Directors (20)
    "YIRMIYAHU", "YECHEZKEL", "DANIEL_SALES", "HOSHEA", "YOEL", "AMOS", "OVADYA",
    "YONAH", "MICHAH", "NACHUM", "CHAVAKUK", "TZEFANYA", "CHAGAI", "ZECHARYA",
    "MALACHI_SALES", "EZRA_SALES", "NECHEMYA", "MORDECHAI_SALES", "SHIMON_SALES", "PINCHAS_SALES",
    # Managers (40)
    "REUVEN_S", "SHIMON_S", "LEVI_S", "YEHUDA_S", "DAN_S", "NAFTALI_S", "GAD_S", "ASHER_S",
    "YISSACHAR", "ZEVULUN", "BINYAMIN_S", "EFRAIM_S", "MENASHE", "KALEV_S", "YEHOSHUA_S",
    "SHIMSHON_S", "GIDEON_S", "BARAK_S", "YIFTACH", "ELKANAH", "SHMUEL_S", "SHAUL_S",
    "YONATAN_S", "AVNER_S", "YOAV_S", "AMASA", "ADONIYA", "ACHITOPHEL", "CHUSHAI",
    "ZADOK_S", "EVYATAR", "BENAYAHU", "SHIMI_S", "RECHAVAM", "YERAVAM", "ASA_S",
    "YEHOSHAFAT_S", "YORAM_S", "ACHAZYA_S", "ATALYA",
    # SDRs and AEs (230)
]

# Generate remaining names
_base_names = [
    "AZARYA", "UZIYA", "YOTAM", "ACHAZ", "CHIZKIYA", "MENASHE_S", "YOSHIYA", "YEHOACHAZ",
    "YEHOYAKIM", "YEHOYACHIN", "TZIDKIYA", "ZERUBAVEL", "YESHUA_S", "ELIAKIM", "ELYASHIV",
    "YOYADA", "YOCHANAN_S", "YADUA", "MATITYA", "YEHUDA_M", "ELEAZAR_S", "ITAMAR_S",
    "KALEV_M", "OTNIEL_S", "EHUD_S", "SHAMGAR_S", "DEVORA_S", "YAEL_S", "TOLA",
    "YAIR_S", "AVIMELECH", "IVTZAN", "ELON_S", "AVDON_S", "ELIMELECH", "BOAZ_S",
    "OVED_S", "YISHAI_S", "ELIAV_S", "AVINADAV", "SHAMA", "NETANEL_S", "RADAI",
    "OZEM_S", "ZERUYA", "AVIGAIL_S", "AMNON_S", "KILAV", "AVSHALOM_S", "ADONIYA_S",
    "SHEFATYA", "YITREAM", "PALTI", "ADRIEL", "MERAV", "MICHAL_S", "NABAL",
]

# Pad to 300
while len(SALES_NAMES) < 300:
    if _base_names:
        SALES_NAMES.append(_base_names.pop(0))
    else:
        idx = len(SALES_NAMES) - 70
        SALES_NAMES.append(f"AGENT_{idx:03d}")


# ================================================================
# SKILLS PER DEPARTMENT
# ================================================================
DEPT_SKILLS = {
    "MCP_SALES": ["product_demo", "technical_writing", "github_outreach", "pricing_negotiation", "onboarding"],
    "AUDIT_SALES": ["vuln_analysis", "audit_proposal", "protocol_research", "report_writing", "pricing_negotiation"],
    "BOOK_SALES": ["copywriting", "marketplace_listing", "review_management", "pricing_optimization", "ads_mgmt"],
    "ENTERPRISE_SALES": ["proposal_writing", "needs_analysis", "contract_negotiation", "account_mgmt", "presentation"],
    "AFFILIATE_SALES": ["content_creation", "link_tracking", "audience_targeting", "conversion_optimization", "reporting"],
    "BOUNTY_HUNTERS": ["code_review", "vuln_research", "poc_writing", "submission_crafting", "platform_monitoring"],
    "TOKEN_SALES": ["community_building", "liquidity_analysis", "market_making", "social_proof", "holder_engagement"],
    "GEO_SALES": ["brand_analysis", "seo_audit", "competitor_research", "lead_qualification", "consultative_selling"],
    "OUTREACH": ["cold_email", "dm_outreach", "lead_scoring", "follow_up", "crm_management"],
    "RETENTION": ["customer_success", "upsell_identification", "churn_prevention", "feedback_collection", "loyalty_program"],
}

DEPT_MCPS = {
    "MCP_SALES": ["claw-mcp-toolkit", "openclaw-mcp-server"],
    "AUDIT_SALES": ["claw-mcp-toolkit"],
    "BOOK_SALES": ["claw-mcp-toolkit"],
    "ENTERPRISE_SALES": ["claw-mcp-toolkit", "openclaw-mcp-server"],
    "AFFILIATE_SALES": ["claw-mcp-toolkit"],
    "BOUNTY_HUNTERS": ["claw-mcp-toolkit"],
    "TOKEN_SALES": ["claw-mcp-toolkit", "mcp-crypto-prices"],
    "GEO_SALES": ["claw-mcp-toolkit", "openclaw-mcp-server"],
    "OUTREACH": ["claw-mcp-toolkit"],
    "RETENTION": ["claw-mcp-toolkit"],
}

# ================================================================
# ROLES AND TITLES
# ================================================================
HIERARCHY = {
    0: {"title": "Chief Revenue Officer", "count": 1},
    1: {"title": "VP of Sales", "count": 3},
    2: {"title": "Sales Director", "count": 6},
    3: {"title": "Regional Manager", "count": 10},
    4: {"title": "Team Lead", "count": 30},
    5: {"title": "Senior Account Executive", "count": 50},
    6: {"title": "Account Executive", "count": 80},
    7: {"title": "Sales Development Rep (SDR)", "count": 120},
}


# ================================================================
# AGENT CREATION
# ================================================================
def create_agent(name, dept_name, dept_info, soul_type, rank, title):
    """Create a single sales agent with soul, memory, skills."""
    soul = SOUL_TYPES[soul_type]
    skills = DEPT_SKILLS.get(dept_name, [])
    mcps = DEPT_MCPS.get(dept_name, [])

    agent = {
        "name": name,
        "department": dept_name,
        "rank": rank,
        "title": title,
        "status": "active",
        "created": datetime.now(BRT).isoformat(),

        # SOUL — Personalidade persistente
        "soul": {
            "type": soul_type,
            "traits": soul["traits"],
            "style": soul["style"],
            "strength": soul["strength"],
            "weakness": soul["weakness"],
            "motivation": f"Generate revenue for Padrao Bitcoin through {dept_name}",
            "values": ["integrity", "persistence", "excellence", "faith"],
        },

        # SKILLS & TOOLS
        "skills": skills,
        "mcps": mcps,
        "tools": ["web_fetch", "generate_tweet", "crypto_price", "shell_command"],
        "products": dept_info["products"],
        "channels": dept_info["channels"],

        # TARGETS
        "target_audience": dept_info["target"],
        "monthly_quota_usd": dept_info["quota_monthly_usd"] / dept_info["size"],

        # WALLETS
        "wallets": WALLETS,

        # EVOLUTION — Aprendizado e crescimento
        "evolution": {
            "level": 1,
            "xp": 0,
            "xp_to_next": 100,
            "total_sales": 0,
            "total_revenue_usd": 0.0,
            "conversion_rate": 0.0,
            "leads_generated": 0,
            "deals_closed": 0,
            "streak_days": 0,
            "best_month_usd": 0.0,
            "promotions": 0,
            "achievements": [],
        },

        # MEMORY — Persistente, aprende com cada interação
        "memory": {
            "lessons": [],
            "best_pitches": [],
            "lost_deals_reasons": [],
            "top_objections": [],
            "winning_strategies": [],
            "contacts": [],
            "last_actions": [],
        },

        # METRICS
        "metrics": {
            "runs": 0,
            "errors": 0,
            "last_run": None,
            "actions_today": 0,
            "last_action_date": None,
        },
    }

    return agent


def deploy_all():
    """Deploy all 300 sales agents."""
    print("Deploying 300 Sales Agents...")

    dept_list = list(SALES_DEPARTMENTS.items())
    soul_types = list(SOUL_TYPES.keys())
    name_idx = 0
    total = 0

    # Assign ranks
    rank_assignments = []
    for rank, info in sorted(HIERARCHY.items()):
        for _ in range(info["count"]):
            rank_assignments.append((rank, info["title"]))

    for dept_name, dept_info in dept_list:
        dept_size = dept_info["size"]
        print(f"  {dept_name}: {dept_size} agents", end="")

        for i in range(dept_size):
            if name_idx >= len(SALES_NAMES):
                break

            name = SALES_NAMES[name_idx]
            soul_type = soul_types[name_idx % len(soul_types)]

            if name_idx < len(rank_assignments):
                rank, title = rank_assignments[name_idx]
            else:
                rank, title = 7, "Sales Development Rep (SDR)"

            agent = create_agent(name, dept_name, dept_info, soul_type, rank, title)

            # Save agent state
            agent_file = SALES_DIR / f"{name}.json"
            with open(agent_file, "w") as f:
                json.dump(agent, f, indent=2)

            # Create empty memory file
            mem_file = MEMORY_DIR / f"{name}_memory.json"
            if not mem_file.exists():
                with open(mem_file, "w") as f:
                    json.dump({"agent": name, "lessons": [], "contacts": [], "strategies": []}, f, indent=2)

            name_idx += 1
            total += 1

        print(f" ✓")

    print(f"\n  TOTAL DEPLOYED: {total} sales agents")
    print(f"  Agent files: {SALES_DIR}")
    print(f"  Memory files: {MEMORY_DIR}")


def show_status():
    """Show sales army status."""
    agents = list(SALES_DIR.glob("*.json"))
    dept_stats = {}
    total_revenue = 0
    total_xp = 0
    active = 0

    for f in agents:
        try:
            with open(f) as fp:
                a = json.load(fp)
            dept = a.get("department", "unknown")
            if dept not in dept_stats:
                dept_stats[dept] = {"count": 0, "revenue": 0, "runs": 0, "level_sum": 0}
            dept_stats[dept]["count"] += 1
            dept_stats[dept]["revenue"] += a.get("evolution", {}).get("total_revenue_usd", 0)
            dept_stats[dept]["runs"] += a.get("metrics", {}).get("runs", 0)
            dept_stats[dept]["level_sum"] += a.get("evolution", {}).get("level", 1)
            total_revenue += a.get("evolution", {}).get("total_revenue_usd", 0)
            total_xp += a.get("evolution", {}).get("xp", 0)
            if a.get("status") == "active":
                active += 1
        except:
            pass

    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║           SALES ARMY — 300 AGENTES DE VENDAS                ║
║           Em nome do Senhor Jesus Cristo                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Total Agents: {len(agents):4d}  |  Active: {active:4d}  |  Revenue: ${total_revenue:,.2f}
║  Total XP: {total_xp:,d}  |  Avg Level: {total_xp/(len(agents) or 1)/100 + 1:.1f}
╠═══════════════════════════════════════════════════════════════╣
║  DEPARTMENT            AGENTS   REVENUE     RUNS   AVG LVL
║  ─────────────────────────────────────────────────────────""")

    for dept, stats in sorted(dept_stats.items()):
        avg_lvl = stats["level_sum"] / max(stats["count"], 1)
        print(f"║  {dept:22s} {stats['count']:4d}   ${stats['revenue']:>9,.2f}   {stats['runs']:5d}   {avg_lvl:.1f}")

    print(f"""╠═══════════════════════════════════════════════════════════════╣
║  WALLETS:
║  EVM: {WALLETS['EVM']}
║  SOL: {WALLETS['SOL']}
║  BTC: {WALLETS['BTC']}
╚═══════════════════════════════════════════════════════════════╝""")


def show_roster():
    """Show full roster."""
    agents = sorted(SALES_DIR.glob("*.json"))
    print(f"\n{'NAME':20s} {'DEPT':20s} {'TITLE':30s} {'LVL':4s} {'SOUL':12s} {'RUNS':5s}")
    print("─" * 95)

    for f in agents:
        try:
            with open(f) as fp:
                a = json.load(fp)
            name = a["name"][:18]
            dept = a.get("department", "?")[:18]
            title = a.get("title", "?")[:28]
            level = a.get("evolution", {}).get("level", 1)
            soul = a.get("soul", {}).get("type", "?")[:10]
            runs = a.get("metrics", {}).get("runs", 0)
            print(f"{name:20s} {dept:20s} {title:30s} {level:4d} {soul:12s} {runs:5d}")
        except:
            pass


def show_agent(name):
    """Show agent details."""
    f = SALES_DIR / f"{name}.json"
    if not f.exists():
        print(f"Agent {name} not found")
        return

    with open(f) as fp:
        a = json.load(fp)

    soul = a.get("soul", {})
    evo = a.get("evolution", {})
    mem = a.get("memory", {})

    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  AGENT: {a['name']}
║  Title: {a.get('title', '?')}
║  Department: {a.get('department', '?')}
║  Status: {a.get('status', '?')}
╠═══════════════════════════════════════════════════════════════╣
║  SOUL:
║    Type: {soul.get('type', '?')}
║    Traits: {', '.join(soul.get('traits', []))}
║    Style: {soul.get('style', '?')[:60]}
║    Strength: {soul.get('strength', '?')}
║    Weakness: {soul.get('weakness', '?')}
╠═══════════════════════════════════════════════════════════════╣
║  EVOLUTION:
║    Level: {evo.get('level', 1)} (XP: {evo.get('xp', 0)}/{evo.get('xp_to_next', 100)})
║    Revenue: ${evo.get('total_revenue_usd', 0):,.2f}
║    Deals Closed: {evo.get('deals_closed', 0)}
║    Conversion: {evo.get('conversion_rate', 0):.1f}%
║    Streak: {evo.get('streak_days', 0)} days
╠═══════════════════════════════════════════════════════════════╣
║  SKILLS: {', '.join(a.get('skills', []))}
║  MCPs: {', '.join(a.get('mcps', []))}
║  Products: {', '.join(a.get('products', [])[:3])}
║  Channels: {', '.join(a.get('channels', []))}
╠═══════════════════════════════════════════════════════════════╣
║  MEMORY:
║    Lessons: {len(mem.get('lessons', []))}
║    Best Pitches: {len(mem.get('best_pitches', []))}
║    Lost Deals: {len(mem.get('lost_deals_reasons', []))}
║    Contacts: {len(mem.get('contacts', []))}
╚═══════════════════════════════════════════════════════════════╝""")


def evolve_agents():
    """Run evolution cycle — agents learn and level up."""
    agents = list(SALES_DIR.glob("*.json"))
    evolved = 0

    for f in agents:
        try:
            with open(f) as fp:
                a = json.load(fp)

            evo = a.setdefault("evolution", {})
            runs = a.get("metrics", {}).get("runs", 0)

            # XP from runs
            xp_gain = runs * 5
            evo["xp"] = evo.get("xp", 0) + xp_gain

            # Level up check
            while evo["xp"] >= evo.get("xp_to_next", 100):
                evo["xp"] -= evo["xp_to_next"]
                evo["level"] = evo.get("level", 1) + 1
                evo["xp_to_next"] = int(evo["xp_to_next"] * 1.5)
                evo.setdefault("achievements", []).append(f"Level {evo['level']} reached")
                evolved += 1

            with open(f, "w") as fp:
                json.dump(a, fp, indent=2)
        except:
            pass

    print(f"Evolution cycle complete. {evolved} agents leveled up.")


def leaderboard():
    """Show top performers."""
    agents_data = []
    for f in SALES_DIR.glob("*.json"):
        try:
            with open(f) as fp:
                a = json.load(fp)
            agents_data.append(a)
        except:
            pass

    # Sort by level, then XP
    top = sorted(agents_data, key=lambda x: (
        x.get("evolution", {}).get("level", 1),
        x.get("evolution", {}).get("xp", 0),
        x.get("metrics", {}).get("runs", 0)
    ), reverse=True)[:20]

    print(f"\n{'#':3s} {'NAME':20s} {'TITLE':25s} {'LVL':4s} {'XP':6s} {'REVENUE':12s} {'RUNS':5s}")
    print("─" * 80)
    for i, a in enumerate(top, 1):
        evo = a.get("evolution", {})
        print(f"{i:3d} {a['name']:20s} {a.get('title','?'):25s} {evo.get('level',1):4d} {evo.get('xp',0):6d} ${evo.get('total_revenue_usd',0):>9,.2f} {a.get('metrics',{}).get('runs',0):5d}")


# ================================================================
# CLI
# ================================================================
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "deploy":
        deploy_all()
    elif cmd == "status":
        show_status()
    elif cmd == "roster":
        show_roster()
    elif cmd == "agent":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        if name:
            show_agent(name)
        else:
            print("Usage: sales_army_300.py agent NAME")
    elif cmd == "evolve":
        evolve_agents()
    elif cmd == "leaderboard":
        leaderboard()
    else:
        print(__doc__)
