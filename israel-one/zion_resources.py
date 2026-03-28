#!/usr/bin/env python3
"""
ZION RESOURCES — Distribuição de MCPs, Skills, Tools, Repos, Memórias
para todos os 1001 agentes do exército ZION.

Conecta cada agente aos recursos que precisa:
- MCPs (7 servidores ativos)
- Skills (90+ do everything-claude-code)
- Ferramentas (tools do claw-mcp-toolkit, openclaw-webtools)
- Repositórios Git (121 repos clonados)
- Memórias (memory files compartilhados)
- Feed do X/Twitter (posts alimentam agentes)

Usage:
    python3 zion_resources.py distribute        # Distribui recursos para todos
    python3 zion_resources.py agent NAME        # Mostra recursos do agente
    python3 zion_resources.py dept DEPT         # Mostra recursos do departamento
    python3 zion_resources.py mcps              # Lista todos MCPs
    python3 zion_resources.py repos             # Lista todos repos por categoria
    python3 zion_resources.py skills            # Lista todas skills
    python3 zion_resources.py feed              # Carrega feed do X para agentes
    python3 zion_resources.py update            # Atualiza todos repos git
    python3 zion_resources.py sync              # Sincroniza memórias compartilhadas
"""

import json, os, sys, subprocess, datetime, glob

ZION_DIR = os.path.expanduser("~/.zion")
SHARED_DIR = os.path.join(ZION_DIR, "shared")
AGENTS_DIR = os.path.join(ZION_DIR, "agents")
HOME = os.path.expanduser("~")

for d in [SHARED_DIR, AGENTS_DIR, os.path.join(ZION_DIR, "feeds")]:
    os.makedirs(d, exist_ok=True)

# ============================================================
# MCP SERVERS (7 configurados)
# ============================================================
MCPS = {
    "claw-mcp-toolkit": {
        "path": f"{HOME}/claw-mcp-toolkit/dist/index.js",
        "tools": [
            "crypto_price", "crypto_trending", "crypto_fear_greed", "crypto_market_overview",
            "crypto_price_history", "crypto_search",
            "web_fetch", "web_extract_links", "web_dns_lookup", "web_ssl_check", "web_seo_check",
            "social_generate_tweet", "social_thread_builder", "social_content_calendar",
            "social_hashtag_research", "social_engagement_analyzer",
            "finance_stock_price", "finance_forex_rate", "finance_portfolio_tracker",
            "finance_expense_log", "finance_invoice_generator",
            "productivity_pomodoro", "productivity_task_breakdown", "productivity_note",
            "productivity_calendar_event", "productivity_reminder",
            "buy_stbtcx", "stbtcx_price", "list_products",
        ],
        "departments": ["ALL"],  # All departments have access
    },
    "mcp-crypto-prices": {
        "path": f"{HOME}/mcp-crypto-prices/dist/index.js",
        "tools": ["get_crypto_price", "get_market_overview", "get_trending",
                  "search_coin", "get_price_history", "get_defi_overview"],
        "departments": ["CRYPTO_MARKETS", "DEFI_PROTOCOLS", "TREASURY", "MARKET_INTEL", "SOCIAL_MEDIA"],
    },
    "openclaw-webtools": {
        "path": f"{HOME}/openclaw-mcp-server/dist/index.js",
        "tools": ["seo_analyze", "dns_lookup", "http_headers", "ssl_check",
                  "perf_check", "robots_txt", "tech_detect", "domain_info"],
        "departments": ["SEO", "SECURITY_AUDIT", "OSINT", "GROWTH_HACKING", "DEVOPS", "BRAND"],
    },
    "firefox-devtools": {
        "path": "npx firefox-devtools-mcp@latest",
        "tools": ["browser_navigate", "browser_click", "browser_type", "browser_screenshot"],
        "departments": ["SOCIAL_MEDIA", "OSINT", "GROWTH_HACKING", "SEO"],
    },
    "twitter": {
        "path": f"{HOME}/twitter-mcp-server/build/index.js",
        "tools": ["post_tweet", "search_tweets", "get_timeline", "get_mentions"],
        "departments": ["SOCIAL_MEDIA", "CONTENT", "BRAND", "GROWTH_HACKING"],
    },
    "filesystem": {
        "path": "npx -y @modelcontextprotocol/server-filesystem",
        "tools": ["read_file", "write_file", "list_directory", "search_files"],
        "departments": ["ALL"],
    },
    "sequential-thinking": {
        "path": "npx -y @modelcontextprotocol/server-sequential-thinking",
        "tools": ["sequentialthinking"],
        "departments": ["COMMAND", "SECURITY_AUDIT", "BOUNTY_HUNTING", "AI_ML"],
    },
}

# ============================================================
# GIT REPOS — Categorized by department relevance
# ============================================================
REPOS = {
    # === CRYPTO & DEFI ===
    "CRYPTO_MARKETS": [
        "chainlink-sentinel", "whale-tracker-mcp", "mcp-crypto-prices",
        "crypto-feargreed-mcp", "etf-flow-mcp", "stocks-mcp",
        "dexpaprika-mcp", "debank-mcp-server", "hyperliquid-mcp-server",
        "polymarket-mcp-server", "whalescope",
    ],
    "DEFI_PROTOCOLS": [
        "goat", "solana-agent-kit", "Solana-MCP", "solana-vault-standard",
        "debridge-mcp", "onchain-mcp", "evm-mcp-server", "v4lend",
        "limitbreak-amm", "mcp-free-usdc-transfer", "pump.fun7",
        "sxt-proof-of-sql",
    ],
    "TREASURY": [
        "Clone-Standard-Bitcoin", "Standard-STBCTX-v", "STBTC-X-CLONEX",
        "flash-payment-system", "privacylayer-withdraw",
    ],

    # === SECURITY & BOUNTIES ===
    "SECURITY_AUDIT": [
        "israel-one", "contractscan-ai", "2026-03-chainlink",
        "washwatch", "PrivacyLayer", "rustchain-bounties-2303",
    ],
    "BOUNTY_HUNTING": [
        "dn-institute", "awesome-mcp-servers", "awesome-blockchain-mcps",
        "awesome-crypto-mcp-servers", "awesome-x402", "stop-slop",
    ],

    # === SOFTWARE & MCP DEV ===
    "SOFTWARE_DEV": [
        "claw-mcp-toolkit", "openclaw-mcp-server", "revenue-mcp",
        "rustchain-mcp", "hub-mcp", "mcpGOTAS", "MCPHub-Desktop",
        "MCP-Orchestrator-Framework", "github-mcp-server",
        "DesktopCommanderMCP", "servers",
    ],
    "MCP_DEVELOPMENT": [
        "claw-mcp-toolkit", "openclaw-mcp-server", "revenue-mcp",
        "chainlink-sentinel", "mcp-crypto-prices", "dappier-mcp",
        "goldrush-mcp-server", "heurist-mesh-mcp-server",
        "esim-mcp-server",
    ],
    "FRONTEND": [
        "bitcoinbrasil", "bitcoinbrasil-seo", "frontend-correto",
        "sintex-ai-production", "Sintex.Ai", "Sintex.Claude.1",
    ],
    "BACKEND": [
        "backend", "flash-payment-system",
    ],

    # === MARKETING & CONTENT ===
    "CONTENT": [
        "twitter-mcp-server", "twitter-scraper-mcp",
        "awesome-chatgpt-prompts", "culturabot",
    ],
    "SOCIAL_MEDIA": [
        "twitter-mcp-server", "twitter-scraper-mcp", "israel-one",
    ],
    "SEO": [
        "bitcoinbrasil-seo", "openclaw-mcp-server",
    ],
    "BRAND": [
        "pitchcraft-ai", "invoicecraft-ai",
    ],

    # === INTELLIGENCE ===
    "MARKET_INTEL": [
        "system-prompts-and-models-of-ai-tools", "awesome-llm-apps",
        "500-AI-Agents-Projects",
    ],
    "OSINT": [
        "system-prompts-and-models-of-ai-tools", "dn-institute",
    ],
    "GOVERNMENT_DATA": [],  # Uses APIs, not repos

    # === AI & LEARNING ===
    "AI_ML": [
        "awesome-llm-apps", "llm-course", "agency-agents",
        "agenticSeek", "claude-code-is-programmable",
        "everything-claude-code", "archestra", "fish-speech",
        "500-AI-Agents-Projects", "BitNet", "context-hub",
    ],
    "KNOWLEDGE": [
        "everything-claude-code", "claude-code-is-programmable",
        "claude-mem", "context-hub", "awesome-chatgpt-prompts",
        "agency-agents", "system-prompts-and-models-of-ai-tools",
    ],

    # === FINANCE ===
    "FISCAL": [],  # Uses Gov APIs
    "INVOICING": ["invoicecraft-ai"],
    "LEGAL": [],

    # === OTHER ===
    "SALES": ["pitchcraft-ai"],
    "MARKETPLACE": [],
    "PARTNERSHIPS": ["awesome-mcp-servers"],
    "ENTERPRISE": [],
    "GROWTH_HACKING": ["bitcoinbrasil-seo"],
    "DEVOPS": ["DesktopCommanderMCP"],
    "COMMAND": ["israel-one", "everything-claude-code"],
    "QUALITY": ["everything-claude-code"],
    "TREND_ANALYSIS": ["awesome-llm-apps", "system-prompts-and-models-of-ai-tools"],
}

# Global repos that ALL agents can access
GLOBAL_REPOS = [
    "israel-one", "claw-mcp-toolkit", "everything-claude-code",
    "padrao-bitcoin-backup",
]

# ============================================================
# SKILLS — From everything-claude-code + custom
# ============================================================
SKILLS = {
    # Engineering skills
    "ENGINEERING": [
        "tdd", "code-review", "build-fix", "refactor", "plan",
        "e2e-test", "api-design", "database-migration", "docker-deploy",
        "security-review", "rust-review", "python-review", "go-review",
    ],
    # AI/ML skills
    "AI_ML": [
        "autonomous-loops", "continuous-learning", "prompt-optimizer",
        "agentic-engineering", "agent-harness", "enterprise-agent-ops",
        "deep-research", "mcp-server-patterns", "rag-pipeline",
    ],
    # Business skills
    "BUSINESS": [
        "investor-materials", "investor-outreach", "market-research",
        "content-engine", "article-writing", "pitch-deck",
    ],
    # Security skills
    "SECURITY": [
        "smart-contract-audit", "slither-analysis", "foundry-fuzzing",
        "nuclei-template", "cve-research", "pentest-report",
    ],
    # Marketing skills
    "MARKETING": [
        "seo-optimization", "twitter-growth", "content-calendar",
        "thread-building", "hashtag-strategy", "engagement-analysis",
    ],
    # Finance skills
    "FINANCE": [
        "das-calculation", "fator-r-optimization", "crypto-tax-br",
        "invoice-generation", "expense-tracking", "ptax-conversion",
    ],
    # Command skills
    "COMMAND": [
        "orchestrate", "multi-plan", "multi-execute", "quality-gate",
        "loop-start", "devfleet", "skill-create", "learn",
    ],
}

# Department-to-skill mapping
DEPT_SKILLS = {
    "CRYPTO_MARKETS": ["BUSINESS"],
    "DEFI_PROTOCOLS": ["ENGINEERING", "SECURITY"],
    "SECURITY_AUDIT": ["SECURITY", "ENGINEERING"],
    "BOUNTY_HUNTING": ["SECURITY", "ENGINEERING"],
    "SOFTWARE_DEV": ["ENGINEERING", "AI_ML"],
    "MCP_DEVELOPMENT": ["ENGINEERING", "AI_ML"],
    "FRONTEND": ["ENGINEERING"],
    "BACKEND": ["ENGINEERING"],
    "DEVOPS": ["ENGINEERING"],
    "AI_ML": ["AI_ML", "ENGINEERING"],
    "SALES": ["BUSINESS"],
    "MARKETPLACE": ["BUSINESS"],
    "PARTNERSHIPS": ["BUSINESS"],
    "ENTERPRISE": ["BUSINESS"],
    "CONTENT": ["MARKETING", "BUSINESS"],
    "SOCIAL_MEDIA": ["MARKETING"],
    "SEO": ["MARKETING"],
    "GROWTH_HACKING": ["MARKETING", "BUSINESS"],
    "BRAND": ["MARKETING"],
    "MARKET_INTEL": ["BUSINESS", "AI_ML"],
    "GOVERNMENT_DATA": ["FINANCE"],
    "OSINT": ["SECURITY"],
    "TREND_ANALYSIS": ["BUSINESS", "AI_ML"],
    "FISCAL": ["FINANCE"],
    "TREASURY": ["FINANCE"],
    "INVOICING": ["FINANCE"],
    "LEGAL": ["FINANCE"],
    "COMMAND": ["COMMAND", "AI_ML"],
    "QUALITY": ["ENGINEERING"],
    "KNOWLEDGE": ["AI_ML", "COMMAND"],
}

# ============================================================
# MEMORY FILES — Shared knowledge base
# ============================================================
MEMORY_DIR = os.path.expanduser("~/.claude/projects/-home-administrador/memory")

MEMORY_FILES = {
    "ALL": [
        "MEMORY.md", "lessons-learned.md",
    ],
    "CRYPTO_MARKETS": ["smart-contract-security.md", "defi-development.md"],
    "DEFI_PROTOCOLS": ["smart-contract-security.md", "defi-development.md"],
    "SECURITY_AUDIT": ["smart-contract-security.md"],
    "BOUNTY_HUNTING": ["bounties-pipeline.md", "smart-contract-security.md", "prs-active.md"],
    "SOFTWARE_DEV": ["git-workflows.md", "machine-optimization.md"],
    "MCP_DEVELOPMENT": ["mcp-servers.md"],
    "SOCIAL_MEDIA": ["twitter-config.md", "x-growth-strategy.md", "jarvis-agent-learnings.md"],
    "CONTENT": ["jarvis-agent-learnings.md", "x-growth-strategy.md"],
    "SEO": [],
    "SALES": ["revenue-status.md", "monetization-playbook.md"],
    "MARKETPLACE": ["revenue-status.md", "marketplace-distribution.md"],
    "FINANCE": ["revenue-status.md"],
    "FISCAL": ["revenue-status.md"],
    "TREASURY": ["revenue-status.md"],
    "INTELLIGENCE": ["network-contacts.md"],
    "MARKET_INTEL": ["network-contacts.md", "ai-ml-knowledge.md"],
    "AI_ML": ["ai-ml-knowledge.md"],
    "KNOWLEDGE": ["zion-army-reference.md"],
    "COMMAND": ["zion-army-reference.md", "revenue-status.md"],
}

# ============================================================
# GOVERNMENT APIs — For relevant departments
# ============================================================
GOV_APIS = {
    "FISCAL": [
        {"name": "BCB_SELIC", "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/5?formato=json"},
        {"name": "BCB_IPCA", "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/5?formato=json"},
        {"name": "BRASIL_API_TAXAS", "url": "https://brasilapi.com.br/api/taxas/v1"},
        {"name": "SEBRAE_NFE", "url": "https://emissornfe.sebrae.com.br/"},
    ],
    "TREASURY": [
        {"name": "BCB_PTAX", "url": "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@d)?@d='{date}'&$format=json"},
        {"name": "BCB_CDI", "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/5?formato=json"},
    ],
    "GOVERNMENT_DATA": [
        {"name": "PORTAL_TRANSPARENCIA", "url": "https://api.portaldatransparencia.gov.br/"},
        {"name": "IBGE_ESTADOS", "url": "https://servicodados.ibge.gov.br/api/v1/localidades/estados"},
        {"name": "CVM_DADOS", "url": "https://dados.cvm.gov.br/"},
        {"name": "OPEN_CNPJ", "url": "https://opencnpj.org/api/cnpj/51148891000169"},
        {"name": "BRASIL_API_CNPJ", "url": "https://brasilapi.com.br/api/cnpj/v1/51148891000169"},
    ],
    "ENTERPRISE": [
        {"name": "PORTAL_TRANSPARENCIA", "url": "https://api.portaldatransparencia.gov.br/"},
    ],
    "INVOICING": [
        {"name": "SEBRAE_NFE", "url": "https://emissornfe.sebrae.com.br/"},
        {"name": "BRASIL_API_CEP", "url": "https://brasilapi.com.br/api/cep/v2/04008010"},
    ],
}

# ============================================================
# X/TWITTER FEED — Posts alimentam agentes
# ============================================================
def load_x_feed():
    """Load recent tweets from Israel/One agent logs to feed back to agents."""
    feed = []

    # Load from agent memory
    memory_path = os.path.expanduser("~/israel-one/memory/posts.json")
    if os.path.exists(memory_path):
        try:
            with open(memory_path) as f:
                posts = json.load(f)
            for p in posts[-20:]:  # Last 20 posts
                feed.append({
                    "text": p.get("text", ""),
                    "time": p.get("timestamp", ""),
                    "type": p.get("template_type", ""),
                    "engagement": p.get("engagement", {}),
                })
        except:
            pass

    # Load from agent log
    log_path = os.path.expanduser("~/israel-one/logs/israel.log")
    if os.path.exists(log_path):
        try:
            with open(log_path) as f:
                lines = f.readlines()
            for line in lines[-100:]:
                if "Posted successfully" in line or "Posting:" in line:
                    feed.append({"log": line.strip()})
        except:
            pass

    # Save feed for agents
    feed_path = os.path.join(ZION_DIR, "feeds", "x_feed.json")
    with open(feed_path, "w") as f:
        json.dump({"updated": datetime.datetime.now().isoformat(), "posts": feed}, f, indent=1)

    return feed


# ============================================================
# RESOURCE DISTRIBUTION ENGINE
# ============================================================
def get_agent_resources(agent_name, agent_data):
    """Get all resources assigned to an agent based on its department."""
    dept = agent_data.get("dept", "")
    resources = {
        "mcps": [],
        "mcp_tools": [],
        "skills": [],
        "repos": [],
        "memory_files": [],
        "gov_apis": [],
        "x_feed": os.path.join(ZION_DIR, "feeds", "x_feed.json"),
    }

    # MCPs — department-specific + global
    for mcp_name, mcp in MCPS.items():
        if "ALL" in mcp["departments"] or dept in mcp["departments"]:
            resources["mcps"].append(mcp_name)
            resources["mcp_tools"].extend(mcp["tools"])

    # Skills — department-specific
    skill_categories = DEPT_SKILLS.get(dept, [])
    for cat in skill_categories:
        resources["skills"].extend(SKILLS.get(cat, []))

    # Repos — department-specific + global
    resources["repos"] = list(set(GLOBAL_REPOS + REPOS.get(dept, [])))

    # Memory files — department-specific + global
    mem_files = MEMORY_FILES.get("ALL", []) + MEMORY_FILES.get(dept, [])
    resources["memory_files"] = list(set(mem_files))

    # Gov APIs
    resources["gov_apis"] = GOV_APIS.get(dept, [])

    return resources


def distribute_all():
    """Distribute resources to all 1001 agents."""
    # Import the army
    try:
        from zion_army_1001 import ARMY
    except ImportError:
        sys.path.insert(0, os.path.expanduser("~/israel-one"))
        from zion_army_1001 import ARMY

    print(f"\n  DISTRIBUTING RESOURCES TO {len(ARMY)} AGENTS")
    print(f"  {'='*55}")
    print(f"  MCPs: {len(MCPS)}")
    print(f"  Skill categories: {len(SKILLS)}")
    print(f"  Repo categories: {len(REPOS)}")
    print(f"  Memory files: {sum(len(v) for v in MEMORY_FILES.values())}")
    print(f"  Gov API endpoints: {sum(len(v) for v in GOV_APIS.values())}")
    print()

    # Load X feed
    feed = load_x_feed()
    print(f"  X/Twitter feed loaded: {len(feed)} posts")

    # Distribute to each agent
    stats = {"total": 0, "mcps_assigned": 0, "skills_assigned": 0, "repos_assigned": 0}

    for name, agent in ARMY.items():
        resources = get_agent_resources(name, agent)

        # Update agent state with resources
        state_path = os.path.join(AGENTS_DIR, f"{name}.json")
        state = {}
        if os.path.exists(state_path):
            try:
                with open(state_path) as f:
                    state = json.load(f)
            except:
                pass

        state["name"] = name
        state["resources"] = {
            "mcps": resources["mcps"],
            "mcp_tools_count": len(resources["mcp_tools"]),
            "skills": resources["skills"],
            "repos": resources["repos"],
            "memory_files": resources["memory_files"],
            "gov_apis_count": len(resources["gov_apis"]),
            "x_feed": resources["x_feed"],
            "distributed_at": datetime.datetime.now().isoformat(),
        }

        with open(state_path, "w") as f:
            json.dump(state, f, indent=1, default=str)

        stats["total"] += 1
        stats["mcps_assigned"] += len(resources["mcps"])
        stats["skills_assigned"] += len(resources["skills"])
        stats["repos_assigned"] += len(resources["repos"])

    print(f"  Distribution complete:")
    print(f"    Agents processed: {stats['total']}")
    print(f"    MCP assignments: {stats['mcps_assigned']}")
    print(f"    Skill assignments: {stats['skills_assigned']}")
    print(f"    Repo assignments: {stats['repos_assigned']}")

    # Save distribution manifest
    manifest = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agents": stats["total"],
        "mcps": list(MCPS.keys()),
        "skill_categories": list(SKILLS.keys()),
        "total_skills": sum(len(v) for v in SKILLS.values()),
        "total_repos": len(set(r for repos in REPOS.values() for r in repos)),
        "gov_apis": sum(len(v) for v in GOV_APIS.values()),
        "x_feed_posts": len(feed),
    }
    with open(os.path.join(SHARED_DIR, "distribution_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n  Manifest saved to {SHARED_DIR}/distribution_manifest.json")


def show_agent_resources(agent_name):
    """Show resources for a specific agent."""
    try:
        from zion_army_1001 import ARMY
    except ImportError:
        sys.path.insert(0, os.path.expanduser("~/israel-one"))
        from zion_army_1001 import ARMY

    agent_name = agent_name.upper()
    agent = ARMY.get(agent_name)
    if not agent:
        print(f"  Agent '{agent_name}' not found")
        return

    resources = get_agent_resources(agent_name, agent)

    print(f"\n  RESOURCES: {agent_name} — {agent['role']}")
    print(f"  Department: {agent['dept']}")
    print(f"  {'─'*50}")

    print(f"\n  MCPs ({len(resources['mcps'])}):")
    for m in resources["mcps"]:
        print(f"    - {m} ({len(MCPS[m]['tools'])} tools)")

    print(f"\n  MCP Tools ({len(resources['mcp_tools'])}):")
    for t in resources["mcp_tools"][:15]:
        print(f"    - {t}")
    if len(resources["mcp_tools"]) > 15:
        print(f"    ... and {len(resources['mcp_tools'])-15} more")

    print(f"\n  Skills ({len(resources['skills'])}):")
    for s in resources["skills"]:
        print(f"    - {s}")

    print(f"\n  Git Repos ({len(resources['repos'])}):")
    for r in resources["repos"]:
        path = os.path.join(HOME, r)
        exists = "OK" if os.path.isdir(path) else "MISSING"
        print(f"    - ~/{r} [{exists}]")

    print(f"\n  Memory Files ({len(resources['memory_files'])}):")
    for m in resources["memory_files"]:
        path = os.path.join(MEMORY_DIR, m)
        exists = "OK" if os.path.exists(path) else "MISSING"
        print(f"    - {m} [{exists}]")

    if resources["gov_apis"]:
        print(f"\n  Government APIs ({len(resources['gov_apis'])}):")
        for api in resources["gov_apis"]:
            print(f"    - {api['name']}: {api['url'][:60]}")

    print(f"\n  X/Twitter Feed: {resources['x_feed']}")


def show_dept_resources(dept_name):
    """Show resources for an entire department."""
    dept_name = dept_name.upper().replace(" ", "_")

    print(f"\n  DEPARTMENT RESOURCES: {dept_name}")
    print(f"  {'='*50}")

    # MCPs
    mcps = []
    for mcp_name, mcp in MCPS.items():
        if "ALL" in mcp["departments"] or dept_name in mcp["departments"]:
            mcps.append((mcp_name, mcp["tools"]))
    print(f"\n  MCPs ({len(mcps)}):")
    for name, tools in mcps:
        print(f"    {name}: {len(tools)} tools")

    # Skills
    skill_cats = DEPT_SKILLS.get(dept_name, [])
    all_skills = []
    for cat in skill_cats:
        all_skills.extend(SKILLS.get(cat, []))
    print(f"\n  Skills ({len(all_skills)}): {', '.join(all_skills[:10])}")

    # Repos
    repos = GLOBAL_REPOS + REPOS.get(dept_name, [])
    print(f"\n  Git Repos ({len(repos)}):")
    for r in repos:
        print(f"    ~/{r}")

    # Memory
    mems = MEMORY_FILES.get("ALL", []) + MEMORY_FILES.get(dept_name, [])
    print(f"\n  Memory Files ({len(mems)}): {', '.join(mems)}")

    # Gov APIs
    apis = GOV_APIS.get(dept_name, [])
    if apis:
        print(f"\n  Government APIs ({len(apis)}):")
        for api in apis:
            print(f"    {api['name']}")


def update_all_repos():
    """Git pull all cloned repos to get latest changes."""
    print(f"\n  UPDATING ALL GIT REPOS")
    print(f"  {'='*50}")

    all_repos = set()
    for repos in REPOS.values():
        all_repos.update(repos)
    all_repos.update(GLOBAL_REPOS)

    updated = 0
    errors = 0
    for repo in sorted(all_repos):
        path = os.path.join(HOME, repo)
        if not os.path.isdir(os.path.join(path, ".git")):
            continue
        try:
            r = subprocess.run(
                f"cd {path} && git pull --ff-only 2>&1 | tail -1",
                shell=True, capture_output=True, text=True, timeout=30
            )
            status = r.stdout.strip()[:60]
            if "Already up to date" in status:
                print(f"  {repo:35s} [up to date]")
            elif "error" in status.lower() or "fatal" in status.lower():
                print(f"  {repo:35s} [ERROR: {status}]")
                errors += 1
            else:
                print(f"  {repo:35s} [UPDATED: {status}]")
                updated += 1
        except subprocess.TimeoutExpired:
            print(f"  {repo:35s} [TIMEOUT]")
            errors += 1
        except Exception as e:
            print(f"  {repo:35s} [ERROR: {str(e)[:40]}]")
            errors += 1

    print(f"\n  Updated: {updated}, Errors: {errors}, Total: {len(all_repos)}")


def sync_memories():
    """Sync shared memories between agents."""
    print(f"\n  SYNCING SHARED MEMORIES")
    print(f"  {'='*50}")

    # Read all memory files
    knowledge = {}
    if os.path.isdir(MEMORY_DIR):
        for f in os.listdir(MEMORY_DIR):
            if f.endswith(".md"):
                path = os.path.join(MEMORY_DIR, f)
                try:
                    with open(path) as fh:
                        content = fh.read()
                    knowledge[f] = {
                        "size": len(content),
                        "lines": content.count("\n"),
                        "updated": datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
                    }
                    print(f"  {f:40s} {knowledge[f]['lines']:5d} lines")
                except:
                    pass

    # Save knowledge index
    index_path = os.path.join(SHARED_DIR, "knowledge_index.json")
    with open(index_path, "w") as f:
        json.dump({
            "timestamp": datetime.datetime.now().isoformat(),
            "files": knowledge,
            "total_files": len(knowledge),
        }, f, indent=2)

    print(f"\n  Synced {len(knowledge)} memory files to shared index")

    # Load and save X feed
    feed = load_x_feed()
    print(f"  X/Twitter feed: {len(feed)} posts loaded for agent consumption")


def show_all_mcps():
    """Show all MCPs and their tools."""
    print(f"\n  MCP SERVERS ({len(MCPS)})")
    print(f"  {'='*55}")
    total_tools = 0
    for name, mcp in MCPS.items():
        print(f"\n  {name}")
        print(f"    Path: {mcp['path'][:60]}")
        print(f"    Depts: {', '.join(mcp['departments'])}")
        print(f"    Tools ({len(mcp['tools'])}):")
        for t in mcp["tools"]:
            print(f"      - {t}")
        total_tools += len(mcp["tools"])
    print(f"\n  TOTAL: {len(MCPS)} MCPs, {total_tools} tools")


def show_all_repos():
    """Show all repos categorized by department."""
    print(f"\n  GIT REPOSITORIES BY DEPARTMENT")
    print(f"  {'='*55}")
    all_repos = set()
    for dept, repos in sorted(REPOS.items()):
        if not repos:
            continue
        print(f"\n  {dept}:")
        for r in repos:
            path = os.path.join(HOME, r)
            exists = "OK" if os.path.isdir(path) else "MISSING"
            print(f"    ~/{r} [{exists}]")
            all_repos.add(r)
    print(f"\n  GLOBAL (all agents):")
    for r in GLOBAL_REPOS:
        print(f"    ~/{r}")
    print(f"\n  TOTAL: {len(all_repos)} unique repos assigned")


def show_all_skills():
    """Show all skills by category."""
    print(f"\n  SKILLS REGISTRY")
    print(f"  {'='*55}")
    total = 0
    for cat, skills in sorted(SKILLS.items()):
        print(f"\n  {cat} ({len(skills)}):")
        for s in skills:
            print(f"    - {s}")
        total += len(skills)
    print(f"\n  TOTAL: {total} skills across {len(SKILLS)} categories")

    print(f"\n  DEPARTMENT ASSIGNMENTS:")
    for dept, cats in sorted(DEPT_SKILLS.items()):
        skills_count = sum(len(SKILLS.get(c, [])) for c in cats)
        print(f"    {dept:25s}: {', '.join(cats)} ({skills_count} skills)")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    if cmd == "distribute":
        distribute_all()
    elif cmd == "agent" and arg:
        show_agent_resources(arg)
    elif cmd == "dept" and arg:
        show_dept_resources(arg)
    elif cmd == "mcps":
        show_all_mcps()
    elif cmd == "repos":
        show_all_repos()
    elif cmd == "skills":
        show_all_skills()
    elif cmd == "feed":
        feed = load_x_feed()
        print(f"  Loaded {len(feed)} posts from X feed")
        for p in feed[:5]:
            print(f"  - {str(p)[:80]}")
    elif cmd == "update":
        update_all_repos()
    elif cmd == "sync":
        sync_memories()
    else:
        print(__doc__)
