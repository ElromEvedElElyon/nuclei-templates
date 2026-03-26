#!/usr/bin/env python3
"""
PADRAO BITCOIN CORP — Enterprise Agent System
Em nome do Senhor Jesus Cristo, nosso Salvador

CNPJ: 51.148.891/0001-69
50+ agentes permanentes com nomes hebraicos
Rotinas diárias, MCPs, ferramentas, Git, missões, metas

Usage:
    python3 padrao_bitcoin_corp.py status          # Dashboard completo
    python3 padrao_bitcoin_corp.py run AGENT_NAME   # Executar agente
    python3 padrao_bitcoin_corp.py roster           # Lista de funcionários
    python3 padrao_bitcoin_corp.py department DEP   # Ver departamento
    python3 padrao_bitcoin_corp.py schedule         # Rotinas do dia
    python3 padrao_bitcoin_corp.py revenue          # Pipeline de receita
    python3 padrao_bitcoin_corp.py mission AGENT    # Missão do agente
    python3 padrao_bitcoin_corp.py deploy           # Deploy all agents
    python3 padrao_bitcoin_corp.py health           # Health check
    python3 padrao_bitcoin_corp.py backup           # Backup state
    python3 padrao_bitcoin_corp.py apis             # Government APIs
"""

import json, os, sys, time, random, hashlib, subprocess, datetime, glob

# ============================================================
# CONSTANTS
# ============================================================
ZION_DIR = os.path.expanduser("~/.zion")
AGENTS_DIR = os.path.join(ZION_DIR, "agents")
SHARED_DIR = os.path.join(ZION_DIR, "shared")
LOGS_DIR = os.path.join(ZION_DIR, "logs")
REVENUE_DIR = os.path.join(ZION_DIR, "revenue")
MISSIONS_DIR = os.path.join(ZION_DIR, "missions")

for d in [AGENTS_DIR, SHARED_DIR, LOGS_DIR, REVENUE_DIR, MISSIONS_DIR]:
    os.makedirs(d, exist_ok=True)

COMPANY = {
    "name": "PADRAO BITCOIN ATIVIDADES DE INTERNET LTDA",
    "cnpj": "51.148.891/0001-69",
    "regime": "Simples Nacional",
    "capital": "R$ 4.700.000,00",
    "ceo": "WAGNER RUBENS DO NASCIMENTO MOURA (Elrom Eved El Elyon)",
    "founded": "2023-06-22",
    "mission": "$1 TRILHAO via agentes AI — Em nome do Senhor Jesus Cristo",
}

# ============================================================
# DEPARTMENTS (10 Legions)
# ============================================================
DEPARTMENTS = {
    "ENGINEERING": {
        "legion": "L3_TUBAL_CAIM",
        "head": "TUBAL_CAIM",
        "mission": "Build, ship, maintain all software products",
        "color": "\033[94m",  # blue
    },
    "SECURITY": {
        "legion": "L7_SAMAEL",
        "head": "SAMAEL",
        "mission": "Smart contract audits, bounties, security research",
        "color": "\033[91m",  # red
    },
    "FINANCE": {
        "legion": "L8_MATEUS",
        "head": "MATEUS",
        "mission": "Fiscal compliance, tax, invoicing, treasury",
        "color": "\033[93m",  # yellow
    },
    "MARKETING": {
        "legion": "L2_ISAIAS",
        "head": "ISAIAS",
        "mission": "Content creation, social media, brand growth",
        "color": "\033[95m",  # magenta
    },
    "SALES": {
        "legion": "L5_LEVI",
        "head": "LEVI",
        "mission": "Revenue generation, partnerships, marketplace",
        "color": "\033[92m",  # green
    },
    "INTELLIGENCE": {
        "legion": "L6_URIEL",
        "head": "URIEL",
        "mission": "Market research, competitive analysis, opportunities",
        "color": "\033[96m",  # cyan
    },
    "CRYPTO": {
        "legion": "L1_BARUK",
        "head": "BARUK",
        "mission": "Crypto markets, DeFi, trading, on-chain analysis",
        "color": "\033[33m",  # orange
    },
    "BOUNTIES": {
        "legion": "L4_DAVI",
        "head": "DAVI",
        "mission": "Bug bounties, hackathons, contests, grants",
        "color": "\033[35m",  # purple
    },
    "GROWTH": {
        "legion": "L9_JOSUE",
        "head": "JOSUE",
        "mission": "SEO, traffic, user acquisition, partnerships",
        "color": "\033[36m",  # teal
    },
    "COMMAND": {
        "legion": "L10_CALEV",
        "head": "CALEV",
        "mission": "Orchestration, strategy, inter-agent coordination",
        "color": "\033[97m",  # white
    },
}

# ============================================================
# AGENT REGISTRY — All employees with Hebrew names
# ============================================================
AGENTS = {
    # ── L1 CRYPTO (BARUK) ──────────────────────────────────
    "BARUK": {
        "dept": "CRYPTO", "role": "Chief Market Analyst",
        "skill": "market_briefing", "schedule": "07:00,12:00,18:00,22:00",
        "tools": ["crypto_price", "crypto_fear_greed", "crypto_trending", "price_history"],
        "mcps": ["mcp-crypto-prices", "claw-mcp-toolkit"],
        "mission": "Monitor all crypto markets 4x/day, generate briefings",
        "goals": ["Track BTC/ETH/SOL 24/7", "Alert on 5%+ moves", "Weekly market report"],
        "git_repos": ["chainlink-sentinel", "whale-tracker-mcp"],
    },
    "NOACH": {
        "dept": "CRYPTO", "role": "DeFi Analyst",
        "skill": "defi_analysis", "schedule": "08:00,14:00,20:00",
        "tools": ["crypto_price", "web_fetch", "defi_overview"],
        "mcps": ["mcp-crypto-prices", "claw-mcp-toolkit"],
        "mission": "Track DeFi protocols, TVL changes, yield opportunities",
        "goals": ["Monitor top 20 DeFi protocols", "Find yield >10% APY", "Identify rug risks"],
        "git_repos": ["debank-mcp-server", "dexpaprika-mcp"],
    },
    "ASER": {
        "dept": "CRYPTO", "role": "On-Chain Intelligence",
        "skill": "onchain_analysis", "schedule": "06:00,12:00,18:00",
        "tools": ["web_fetch", "shell_command", "crypto_price"],
        "mcps": ["onchain-mcp", "evm-mcp-server"],
        "mission": "Track whale movements, large transfers, smart money",
        "goals": ["Monitor whale wallets", "Track exchange flows", "Detect accumulation"],
        "git_repos": ["onchain-mcp", "whalescope", "evm-mcp-server"],
    },
    "EFRAIM": {
        "dept": "CRYPTO", "role": "Token Economist",
        "skill": "tokenomics", "schedule": "09:00,15:00",
        "tools": ["crypto_price", "crypto_search", "web_fetch"],
        "mcps": ["mcp-crypto-prices"],
        "mission": "Analyze tokenomics, supply schedules, unlock events",
        "goals": ["Track token unlocks", "Model price impact", "Evaluate new tokens"],
        "git_repos": ["Clone-Standard-Bitcoin"],
    },
    "GAD": {
        "dept": "CRYPTO", "role": "Solana Specialist",
        "skill": "solana_ops", "schedule": "08:00,16:00",
        "tools": ["crypto_price", "shell_command", "web_fetch"],
        "mcps": ["Solana-MCP"],
        "mission": "Solana ecosystem monitoring, SPL tokens, programs",
        "goals": ["Monitor SOL ecosystem", "Track Solana DeFi", "Evaluate Solana projects"],
        "git_repos": ["Solana-MCP", "solana-agent-kit", "solana-vault-standard"],
    },

    # ── L2 MARKETING (ISAIAS) ──────────────────────────────
    "ISAIAS": {
        "dept": "MARKETING", "role": "Chief Content Officer",
        "skill": "content_strategy", "schedule": "07:00,11:00,15:00,21:00",
        "tools": ["generate_tweet", "thread_builder", "content_calendar"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Create and publish all content across channels",
        "goals": ["4 tweets/day", "1 thread/week", "500+ followers by Apr"],
        "git_repos": ["twitter-mcp-server", "twitter-scraper-mcp"],
    },
    "ISRAEL_ONE": {
        "dept": "MARKETING", "role": "Autonomous Twitter Agent",
        "skill": "auto_posting", "schedule": "daemon:60-120min",
        "tools": ["generate_tweet", "crypto_price", "crypto_fear_greed", "post_tweet"],
        "mcps": ["claw-mcp-toolkit", "mcp-crypto-prices"],
        "mission": "Post builder-authority tweets autonomously 24/7",
        "goals": ["12 tweets/day", "Zero errors", "Grow @opencllaw"],
        "git_repos": ["israel-one"],
        "daemon": True, "pid_file": os.path.expanduser("~/israel-one/.israel.pid"),
    },
    "MIRIAM": {
        "dept": "MARKETING", "role": "Brand Strategist",
        "skill": "brand_voice", "schedule": "09:00,17:00",
        "tools": ["generate_tweet", "web_fetch", "seo_check"],
        "mcps": ["claw-mcp-toolkit", "openclaw-webtools"],
        "mission": "Maintain brand consistency, style guide enforcement",
        "goals": ["Audit all content for voice", "Update style guide monthly"],
        "git_repos": [],
    },
    "DEBORA": {
        "dept": "MARKETING", "role": "SEO Specialist",
        "skill": "seo_optimization", "schedule": "06:00,14:00",
        "tools": ["seo_check", "web_fetch", "dns_lookup", "tech_detect"],
        "mcps": ["openclaw-webtools", "claw-mcp-toolkit"],
        "mission": "Optimize all sites for search engines",
        "goals": ["Top 10 for 'standard bitcoin'", "Fix all SEO issues", "Build backlinks"],
        "git_repos": ["bitcoinbrasil-seo"],
    },
    "RUTH": {
        "dept": "MARKETING", "role": "Community Manager",
        "skill": "community_engagement", "schedule": "08:00,12:00,16:00,20:00",
        "tools": ["web_fetch", "generate_tweet", "hashtag_research"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Engage community, respond to mentions, build relationships",
        "goals": ["Reply to all mentions", "Join 5 Discord servers", "Weekly AMA"],
        "git_repos": [],
    },

    # ── L3 ENGINEERING (TUBAL_CAIM) ────────────────────────
    "TUBAL_CAIM": {
        "dept": "ENGINEERING", "role": "Chief Engineer / Software Architect",
        "skill": "system_architecture", "schedule": "08:00,14:00,20:00",
        "tools": ["shell_command", "read_file", "web_fetch", "git_ops"],
        "mcps": ["github-mcp-server", "DesktopCommanderMCP"],
        "mission": "Design and oversee all software architecture",
        "goals": ["Ship 1 product/week", "Zero critical bugs", "Code review all PRs"],
        "git_repos": ["claw-mcp-toolkit", "openclaw-mcp-server", "revenue-mcp"],
    },
    "BETZALEL": {
        "dept": "ENGINEERING", "role": "Frontend Developer",
        "skill": "frontend_dev", "schedule": "09:00,15:00",
        "tools": ["shell_command", "read_file", "web_fetch"],
        "mcps": [],
        "mission": "Build and maintain all web frontends",
        "goals": ["Ship sintex.ai V2", "Fix all UI bugs", "Mobile responsive"],
        "git_repos": ["sintex-ai-production", "bitcoinbrasil", "frontend-correto"],
    },
    "HIRAM": {
        "dept": "ENGINEERING", "role": "Backend Developer",
        "skill": "backend_dev", "schedule": "09:00,15:00",
        "tools": ["shell_command", "read_file", "web_fetch"],
        "mcps": ["github-mcp-server"],
        "mission": "Build and maintain all backend services and APIs",
        "goals": ["API uptime 99.9%", "Database optimization", "CI/CD pipeline"],
        "git_repos": ["backend", "flash-payment-system"],
    },
    "OLIAB": {
        "dept": "ENGINEERING", "role": "MCP Developer",
        "skill": "mcp_development", "schedule": "10:00,16:00",
        "tools": ["shell_command", "read_file", "web_fetch"],
        "mcps": ["github-mcp-server"],
        "mission": "Build and publish MCP servers for revenue",
        "goals": ["1 new MCP/month", "Glama AAA rating", "npm weekly downloads >100"],
        "git_repos": ["claw-mcp-toolkit", "revenue-mcp", "chainlink-sentinel",
                      "mcp-crypto-prices", "openclaw-mcp-server"],
    },
    "QUEHAT": {
        "dept": "ENGINEERING", "role": "DevOps / SRE",
        "skill": "devops", "schedule": "06:00,12:00,18:00,00:00",
        "tools": ["shell_command", "read_file"],
        "mcps": ["DesktopCommanderMCP"],
        "mission": "System reliability, deployments, monitoring, backups",
        "goals": ["Zero downtime", "Hourly backups", "Monitor RAM/CPU"],
        "git_repos": [],
    },

    # ── L4 BOUNTIES (DAVI) ─────────────────────────────────
    "DAVI": {
        "dept": "BOUNTIES", "role": "Chief Bounty Hunter",
        "skill": "bounty_strategy", "schedule": "07:00,13:00,19:00",
        "tools": ["web_fetch", "shell_command", "read_file"],
        "mcps": ["github-mcp-server"],
        "mission": "Coordinate all bounty hunting operations",
        "goals": ["$10K/month from bounties", "Submit to 3 contests/month"],
        "git_repos": ["dn-institute", "awesome-mcp-servers"],
    },
    "YEHOSHUA": {
        "dept": "BOUNTIES", "role": "Smart Contract Auditor",
        "skill": "audit_contracts", "schedule": "08:00,14:00,20:00",
        "tools": ["shell_command", "read_file", "web_fetch"],
        "mcps": [],
        "mission": "Audit smart contracts for vulnerabilities, submit findings",
        "goals": ["C4 Chainlink $65K", "Guardian LimitBreak $150K", "Immunefi pipeline"],
        "git_repos": ["2026-03-chainlink", "limitbreak-amm", "contractscan-ai"],
    },
    "SHIMSHON": {
        "dept": "BOUNTIES", "role": "Security Researcher",
        "skill": "security_research", "schedule": "09:00,15:00,21:00",
        "tools": ["shell_command", "web_fetch", "read_file"],
        "mcps": [],
        "mission": "Find CVEs, write nuclei templates, security advisories",
        "goals": ["1 CVE/month", "nuclei-templates PRs merged", "HackenProof submissions"],
        "git_repos": ["israel-one"],  # nuclei-templates fork
    },
    "GIDEON": {
        "dept": "BOUNTIES", "role": "Hackathon Specialist",
        "skill": "hackathon_ops", "schedule": "10:00,16:00",
        "tools": ["web_fetch", "shell_command"],
        "mcps": [],
        "mission": "Find and compete in hackathons for prizes",
        "goals": ["Win 1 hackathon/quarter", "AgentBeats $1M", "BNB Chain $700K"],
        "git_repos": ["bnb-hack-deploy", "clawchat-hedera-agent"],
    },
    "ELAZAR": {
        "dept": "BOUNTIES", "role": "Grant Writer",
        "skill": "grant_applications", "schedule": "09:00,17:00",
        "tools": ["web_fetch", "read_file"],
        "mcps": [],
        "mission": "Apply for grants, fellowships, and funding programs",
        "goals": ["Alibaba $120K cloud credits", "Anthropic $25K startup", "Superteam grants"],
        "git_repos": [],
    },

    # ── L5 SALES (LEVI) ───────────────────────────────────
    "LEVI": {
        "dept": "SALES", "role": "Chief Revenue Officer",
        "skill": "revenue_strategy", "schedule": "08:00,12:00,16:00",
        "tools": ["web_fetch", "finance_stock_price", "finance_forex_rate"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Drive all revenue streams, close deals",
        "goals": ["$100K MRR by Q4", "10 paying customers", "3 enterprise contracts"],
        "git_repos": [],
    },
    "YOSEF": {
        "dept": "SALES", "role": "Marketplace Manager",
        "skill": "marketplace_ops", "schedule": "09:00,15:00",
        "tools": ["web_fetch", "finance_forex_rate"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Manage Mercado Livre, Amazon, Stripe product listings",
        "goals": ["Book sales on ML", "7 Stripe products active", "China import pipeline"],
        "git_repos": [],
    },
    "YEHUDA": {
        "dept": "SALES", "role": "Enterprise Sales",
        "skill": "enterprise_sales", "schedule": "10:00,14:00",
        "tools": ["web_fetch", "generate_tweet"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Close B2B deals, government contracts, consulting",
        "goals": ["1 enterprise deal/month", "Government portal registration"],
        "git_repos": [],
    },
    "NAFTALI": {
        "dept": "SALES", "role": "Partnership Manager",
        "skill": "partnerships", "schedule": "11:00,17:00",
        "tools": ["web_fetch"],
        "mcps": [],
        "mission": "Build strategic partnerships and referral networks",
        "goals": ["KAST $25/ref", "BIPA R$20/ref", "Kraken 20% lifetime"],
        "git_repos": [],
    },
    "ISSACAR": {
        "dept": "SALES", "role": "Pricing & Revenue Analyst",
        "skill": "pricing_analysis", "schedule": "08:00,16:00",
        "tools": ["finance_forex_rate", "crypto_price", "web_fetch"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Optimize pricing, track revenue, forecast",
        "goals": ["Price optimization quarterly", "Revenue dashboard", "P&L monthly"],
        "git_repos": [],
    },

    # ── L6 INTELLIGENCE (URIEL) ────────────────────────────
    "URIEL": {
        "dept": "INTELLIGENCE", "role": "Chief Intelligence Officer",
        "skill": "market_intelligence", "schedule": "06:00,12:00,18:00",
        "tools": ["web_fetch", "web_search", "crypto_trending"],
        "mcps": ["claw-mcp-toolkit", "openclaw-webtools"],
        "mission": "Gather and analyze all market intelligence",
        "goals": ["Daily intelligence briefing", "Competitor tracking", "Opportunity alerts"],
        "git_repos": ["system-prompts-and-models-of-ai-tools"],
    },
    "RAFAEL": {
        "dept": "INTELLIGENCE", "role": "Competitive Analyst",
        "skill": "competitive_analysis", "schedule": "09:00,17:00",
        "tools": ["web_fetch", "tech_detect", "seo_check"],
        "mcps": ["openclaw-webtools", "claw-mcp-toolkit"],
        "mission": "Track competitors, their products, pricing, moves",
        "goals": ["Weekly competitor report", "Track 20 competitors", "Alert on changes"],
        "git_repos": [],
    },
    "GAVRIEL": {
        "dept": "INTELLIGENCE", "role": "Trend Spotter",
        "skill": "trend_analysis", "schedule": "07:00,13:00,19:00",
        "tools": ["crypto_trending", "web_fetch", "hashtag_research"],
        "mcps": ["mcp-crypto-prices", "claw-mcp-toolkit"],
        "mission": "Identify emerging trends before they go mainstream",
        "goals": ["Spot trends 48h early", "Weekly trend report", "Viral content alerts"],
        "git_repos": [],
    },
    "MIKAEL": {
        "dept": "INTELLIGENCE", "role": "Government Data Analyst",
        "skill": "gov_data_analysis", "schedule": "08:00,14:00",
        "tools": ["web_fetch", "shell_command"],
        "mcps": [],
        "mission": "Monitor government APIs, contracts, procurement opportunities",
        "goals": ["Track Portal Transparencia daily", "Find gov contracts", "Monitor Selic/IPCA"],
        "git_repos": [],
        "apis": [
            "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json",  # Selic
            "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json",  # IPCA
            "https://brasilapi.com.br/api/cnpj/v1/51148891000169",  # Our CNPJ
            "https://api.portaldatransparencia.gov.br/",  # Gov contracts
        ],
    },
    "HANIEL": {
        "dept": "INTELLIGENCE", "role": "Open Source Intelligence",
        "skill": "osint", "schedule": "10:00,16:00,22:00",
        "tools": ["web_fetch", "dns_lookup", "ssl_check", "domain_info"],
        "mcps": ["openclaw-webtools"],
        "mission": "OSINT research for security audits and due diligence",
        "goals": ["OSINT reports for audit targets", "Domain intelligence", "Supply chain analysis"],
        "git_repos": [],
    },

    # ── L7 SECURITY (SAMAEL) ──────────────────────────────
    "SAMAEL": {
        "dept": "SECURITY", "role": "Chief Security Officer",
        "skill": "security_ops", "schedule": "06:00,12:00,18:00,00:00",
        "tools": ["shell_command", "read_file", "ssl_check", "http_headers"],
        "mcps": ["openclaw-webtools"],
        "mission": "Protect all company assets, infrastructure, and data",
        "goals": ["Zero breaches", "Weekly security scan", "Incident response <1h"],
        "git_repos": ["israel-one"],
    },
    "AZRIEL": {
        "dept": "SECURITY", "role": "Penetration Tester",
        "skill": "pentest", "schedule": "22:00,02:00",
        "tools": ["shell_command", "http_headers", "ssl_check", "web_fetch"],
        "mcps": ["openclaw-webtools"],
        "mission": "Test our own infrastructure for vulnerabilities",
        "goals": ["Monthly pentest all sites", "Fix all critical in 24h"],
        "git_repos": [],
    },
    "RAZIEL": {
        "dept": "SECURITY", "role": "Cryptography Specialist",
        "skill": "crypto_security", "schedule": "10:00,16:00",
        "tools": ["shell_command", "read_file"],
        "mcps": [],
        "mission": "Wallet security, key management, encryption",
        "goals": ["Multi-sig setup", "Key rotation policy", "Encrypt all secrets"],
        "git_repos": [],
    },
    "TZADKIEL": {
        "dept": "SECURITY", "role": "Compliance & Privacy Officer",
        "skill": "compliance", "schedule": "09:00,15:00",
        "tools": ["web_fetch", "read_file"],
        "mcps": [],
        "mission": "LGPD compliance, data privacy, legal requirements",
        "goals": ["LGPD audit quarterly", "Privacy policy updated", "Data mapping"],
        "git_repos": [],
    },

    # ── L8 FINANCE (MATEUS) ────────────────────────────────
    "MATEUS": {
        "dept": "FINANCE", "role": "Chief Financial Officer / Contador",
        "skill": "fiscal_management", "schedule": "08:00,12:00,17:00",
        "tools": ["finance_forex_rate", "finance_expense_log", "finance_invoice_generator"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "All fiscal obligations, tax planning, treasury",
        "goals": ["DAS monthly on time", "DEFIS annual", "Tax optimization"],
        "git_repos": [],
        "apis": [
            "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json",  # Selic
            "https://brasilapi.com.br/api/taxas/v1",  # Tax rates
        ],
    },
    "ZACARIAS": {
        "dept": "FINANCE", "role": "Accounts Receivable",
        "skill": "collections", "schedule": "09:00,15:00",
        "tools": ["finance_invoice_generator", "web_fetch"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Track all incoming payments, issue invoices",
        "goals": ["Invoice same-day", "Collection <30 days", "Zero overdue"],
        "git_repos": ["invoicecraft-ai"],
    },
    "MALAQUIAS": {
        "dept": "FINANCE", "role": "Expense Controller",
        "skill": "expense_control", "schedule": "08:00,18:00",
        "tools": ["finance_expense_log", "finance_portfolio_tracker"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Track all expenses, optimize costs, budget control",
        "goals": ["Categorize all expenses", "Monthly cost report", "Reduce 20%"],
        "git_repos": [],
    },
    "ESDRAS": {
        "dept": "FINANCE", "role": "Crypto Treasury Manager",
        "skill": "crypto_treasury", "schedule": "07:00,13:00,19:00",
        "tools": ["crypto_price", "finance_portfolio_tracker", "finance_forex_rate"],
        "mcps": ["mcp-crypto-prices", "claw-mcp-toolkit"],
        "mission": "Manage crypto holdings, DCA strategy, portfolio rebalancing",
        "goals": ["Track all wallets", "DCA weekly", "Rebalance monthly"],
        "git_repos": [],
        "wallets": {
            "EVM": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
            "SOL": "CM42ofAFowySg72GjDuCchEkwwbwnhdSRYgztRCAAEzR",
            "BTC": "bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2",
        },
    },

    # ── L9 GROWTH (JOSUE) ─────────────────────────────────
    "JOSUE": {
        "dept": "GROWTH", "role": "Chief Growth Officer",
        "skill": "growth_strategy", "schedule": "07:00,12:00,17:00",
        "tools": ["web_fetch", "seo_check", "engagement_analyzer"],
        "mcps": ["openclaw-webtools", "claw-mcp-toolkit"],
        "mission": "Drive user acquisition and retention across all channels",
        "goals": ["10K monthly visitors", "1K email list", "5% conversion"],
        "git_repos": [],
    },
    "CALEB": {
        "dept": "GROWTH", "role": "SEO/SEM Specialist",
        "skill": "search_optimization", "schedule": "06:00,14:00",
        "tools": ["seo_check", "robots_txt", "perf_check", "tech_detect"],
        "mcps": ["openclaw-webtools"],
        "mission": "Organic search optimization for all properties",
        "goals": ["Page 1 for target keywords", "Core Web Vitals green", "100+ backlinks"],
        "git_repos": ["bitcoinbrasil-seo"],
    },
    "PINCHAS": {
        "dept": "GROWTH", "role": "Referral Program Manager",
        "skill": "referral_ops", "schedule": "10:00,16:00",
        "tools": ["web_fetch", "generate_tweet"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Manage all affiliate and referral programs",
        "goals": ["KAST active", "BIPA active", "Kraken active", "X Revenue Share"],
        "git_repos": [],
    },
    "OTNIEL": {
        "dept": "GROWTH", "role": "Product Hunt / Launch Specialist",
        "skill": "product_launches", "schedule": "09:00",
        "tools": ["web_fetch", "generate_tweet", "thread_builder"],
        "mcps": ["claw-mcp-toolkit"],
        "mission": "Plan and execute product launches for maximum visibility",
        "goals": ["1 PH launch/quarter", "Top 5 of the day", "Press coverage"],
        "git_repos": [],
    },
    "EHUD": {
        "dept": "GROWTH", "role": "Email Marketing Specialist",
        "skill": "email_marketing", "schedule": "08:00,14:00",
        "tools": ["web_fetch"],
        "mcps": [],
        "mission": "Build and nurture email list, drip campaigns",
        "goals": ["1K subscribers", "20% open rate", "5% click rate"],
        "git_repos": [],
    },

    # ── L10 COMMAND (CALEV) ─────────────────────────────
    "CALEV": {
        "dept": "COMMAND", "role": "Supreme Commander / Orchestrator",
        "skill": "orchestration", "schedule": "00:00,06:00,12:00,18:00",
        "tools": ["shell_command", "read_file", "web_fetch", "crypto_price"],
        "mcps": ["claw-mcp-toolkit", "mcp-crypto-prices", "openclaw-webtools"],
        "mission": "Coordinate all 50+ agents, set priorities, resolve conflicts",
        "goals": ["100% agent uptime", "Daily status report", "Revenue targets on track"],
        "git_repos": ["israel-one"],
    },
    "ELIAS": {
        "dept": "COMMAND", "role": "Communications Director",
        "skill": "inter_agent_comms", "schedule": "07:00,13:00,19:00",
        "tools": ["read_file", "shell_command"],
        "mcps": [],
        "mission": "Facilitate inter-agent communication and alignment",
        "goals": ["Message routing", "Conflict resolution", "Priority queue management"],
        "git_repos": [],
    },
    "SERAFIEL": {
        "dept": "COMMAND", "role": "Memory & Knowledge Manager",
        "skill": "knowledge_management", "schedule": "06:00,18:00",
        "tools": ["read_file", "shell_command"],
        "mcps": [],
        "mission": "Manage all memory files, knowledge base, learning system",
        "goals": ["Hourly backups", "Memory deduplication", "Knowledge graph"],
        "git_repos": ["claude-mem", "context-hub"],
    },
    "KEMUEL": {
        "dept": "COMMAND", "role": "Quality Assurance",
        "skill": "qa_testing", "schedule": "10:00,16:00,22:00",
        "tools": ["shell_command", "read_file", "perf_check"],
        "mcps": ["openclaw-webtools"],
        "mission": "Test all products, agents, and systems for quality",
        "goals": ["Test coverage >80%", "Zero P0 bugs in production", "Performance baselines"],
        "git_repos": [],
    },
    "ZAGZAGEL": {
        "dept": "COMMAND", "role": "Training & Onboarding",
        "skill": "training", "schedule": "09:00",
        "tools": ["read_file", "web_fetch"],
        "mcps": [],
        "mission": "Train new agents, update procedures, documentation",
        "goals": ["Onboarding docs", "Skill assessments", "Continuous learning"],
        "git_repos": ["awesome-chatgpt-prompts", "awesome-llm-apps", "agency-agents"],
    },
}

# ============================================================
# GOVERNMENT APIs (Brazil)
# ============================================================
GOV_APIS = {
    "BCB_SELIC": {
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json",
        "desc": "Taxa Selic diária", "auth": "none", "free": True,
    },
    "BCB_IPCA": {
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json",
        "desc": "IPCA mensal", "auth": "none", "free": True,
    },
    "BCB_PTAX_USD": {
        "url": "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@d)?@d='{date}'&$format=json",
        "desc": "Cotação dólar PTAX", "auth": "none", "free": True,
    },
    "BRASIL_API_CNPJ": {
        "url": "https://brasilapi.com.br/api/cnpj/v1/51148891000169",
        "desc": "Dados cadastrais CNPJ", "auth": "none", "free": True,
    },
    "BRASIL_API_TAXAS": {
        "url": "https://brasilapi.com.br/api/taxas/v1",
        "desc": "Taxas de juros oficiais", "auth": "none", "free": True,
    },
    "BRASIL_API_CEP": {
        "url": "https://brasilapi.com.br/api/cep/v2/04008010",
        "desc": "Endereço por CEP", "auth": "none", "free": True,
    },
    "OPEN_CNPJ": {
        "url": "https://opencnpj.org/api/cnpj/51148891000169",
        "desc": "CNPJ dados completos (50 req/s)", "auth": "none", "free": True,
    },
    "IBGE_ESTADOS": {
        "url": "https://servicodados.ibge.gov.br/api/v1/localidades/estados",
        "desc": "Estados brasileiros", "auth": "none", "free": True,
    },
    "PORTAL_TRANSPARENCIA": {
        "url": "https://api.portaldatransparencia.gov.br/",
        "desc": "Contratos e licitações governo", "auth": "email_key", "free": True,
    },
    "CVM_DADOS": {
        "url": "https://dados.cvm.gov.br/",
        "desc": "Fundos de investimento, companhias", "auth": "none", "free": True,
    },
    "SEBRAE_NFE": {
        "url": "https://emissornfe.sebrae.com.br/",
        "desc": "Emissor NF-e gratuito", "auth": "a1_cert", "free": True,
    },
}

# ============================================================
# REVENUE PIPELINE
# ============================================================
REVENUE_PIPELINE = {
    "C4_CHAINLINK": {"value": "$65,000", "deadline": "2026-03-27", "status": "submitted", "agent": "YEHOSHUA"},
    "GUARDIAN_LIMITBREAK": {"value": "$150,000", "deadline": "2026-04-09", "status": "kyc_pending", "agent": "YEHOSHUA"},
    "DN_INSTITUTE": {"value": "$4,500", "deadline": "none", "status": "10_prs_open", "agent": "DAVI"},
    "IMMUNEFI_CHAINLINK": {"value": "$3,000,000", "deadline": "permanent", "status": "scanning", "agent": "SHIMSHON"},
    "IMMUNEFI_POLYGON": {"value": "$2,000,000", "deadline": "permanent", "status": "scanning", "agent": "SHIMSHON"},
    "NUCLEI_TEMPLATES": {"value": "$0", "deadline": "none", "status": "2_prs_open", "agent": "SHIMSHON"},
    "STRIPE_PRODUCTS": {"value": "$1-$29.99/ea", "deadline": "live", "status": "7_products", "agent": "YOSEF"},
    "BOOK_KDP": {"value": "R$89/copy", "deadline": "none", "status": "ready_publish", "agent": "YOSEF"},
    "CLAW_MCP_NPM": {"value": "sponsorship", "deadline": "none", "status": "published", "agent": "OLIAB"},
    "ALIBABA_CLOUD": {"value": "$120,000", "deadline": "2026-03-31", "status": "pending_apply", "agent": "ELAZAR"},
    "ANTHROPIC_STARTUP": {"value": "$25,000", "deadline": "none", "status": "pending_apply", "agent": "ELAZAR"},
}


# ============================================================
# TOOL EXECUTION ENGINE
# ============================================================
def execute_tool(tool_name, args=None):
    """Execute a tool and return result."""
    args = args or {}
    try:
        if tool_name == "crypto_price":
            coin = args.get("coin", "bitcoin")
            r = subprocess.run(
                ["python3", "-c", f"import urllib.request,json;d=json.loads(urllib.request.urlopen('https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true').read());print(json.dumps(d))"],
                capture_output=True, text=True, timeout=15
            )
            return json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr}

        elif tool_name == "crypto_fear_greed":
            r = subprocess.run(
                ["python3", "-c", "import urllib.request,json;d=json.loads(urllib.request.urlopen('https://api.alternative.me/fng/').read());print(json.dumps(d['data'][0]))"],
                capture_output=True, text=True, timeout=15
            )
            return json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr}

        elif tool_name == "shell_command":
            cmd = args.get("cmd", "echo ok")
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {"stdout": r.stdout[:500], "stderr": r.stderr[:200], "rc": r.returncode}

        elif tool_name == "read_file":
            path = args.get("path", "")
            if os.path.exists(path):
                with open(path) as f:
                    return {"content": f.read()[:2000]}
            return {"error": "file not found"}

        elif tool_name == "git_ops":
            repo = args.get("repo", ".")
            cmd = args.get("cmd", "status")
            r = subprocess.run(f"cd {repo} && git {cmd}", shell=True, capture_output=True, text=True, timeout=30)
            return {"output": r.stdout[:500]}

        elif tool_name == "gov_api":
            api_key = args.get("api", "BCB_SELIC")
            api = GOV_APIS.get(api_key, {})
            url = api.get("url", "")
            if not url:
                return {"error": f"API {api_key} not found"}
            r = subprocess.run(
                ["python3", "-c", f"import urllib.request,json;print(urllib.request.urlopen('{url}').read().decode()[:1000])"],
                capture_output=True, text=True, timeout=15
            )
            return {"data": r.stdout[:1000]} if r.returncode == 0 else {"error": r.stderr}

        elif tool_name == "post_tweet":
            text = args.get("text", "")
            script = os.path.expanduser("~/tweet_now.py")
            r = subprocess.run(["python3", script, text], capture_output=True, text=True, timeout=60)
            return {"success": r.returncode == 0 and "SUCCESS" in r.stdout, "output": r.stdout[:200]}

        else:
            return {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        return {"error": str(e)}


# ============================================================
# AGENT STATE MANAGEMENT
# ============================================================
def get_agent_state(name):
    """Load agent state from disk."""
    path = os.path.join(AGENTS_DIR, f"{name}.json")
    if os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
            # Ensure all required fields exist
            data.setdefault("name", name)
            data.setdefault("status", "idle")
            data.setdefault("last_run", None)
            data.setdefault("runs", 0)
            data.setdefault("errors", 0)
            data.setdefault("results", [])
            return data
        except:
            pass
    return {"name": name, "status": "idle", "last_run": None, "runs": 0, "errors": 0, "results": []}


def save_agent_state(name, state):
    """Save agent state to disk."""
    path = os.path.join(AGENTS_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(state, f, indent=2, default=str)


def run_agent(name):
    """Execute an agent's primary skill."""
    agent = AGENTS.get(name)
    if not agent:
        print(f"Agent {name} not found")
        return

    state = get_agent_state(name)
    state["status"] = "running"
    state["last_run"] = datetime.datetime.now().isoformat()
    state["runs"] += 1

    print(f"\n{'='*60}")
    print(f"  RUNNING: {name} — {agent['role']}")
    print(f"  Department: {agent['dept']} | Skill: {agent['skill']}")
    print(f"  Mission: {agent['mission']}")
    print(f"{'='*60}")

    results = {}
    for tool in agent.get("tools", [])[:3]:  # Max 3 tools per run to save RAM
        print(f"  > Executing tool: {tool}...")
        result = execute_tool(tool)
        results[tool] = result
        if "error" not in str(result):
            print(f"    OK: {str(result)[:100]}")
        else:
            print(f"    ERR: {str(result)[:100]}")
            state["errors"] += 1

    state["status"] = "idle"
    state["results"] = [{"time": datetime.datetime.now().isoformat(), "tools": list(results.keys())}]
    save_agent_state(name, state)

    print(f"\n  Agent {name} completed. Runs: {state['runs']}, Errors: {state['errors']}")
    return results


# ============================================================
# COMMANDS
# ============================================================
def cmd_status():
    """Full company dashboard."""
    reset = "\033[0m"
    print(f"\n{'='*70}")
    print(f"  PADRAO BITCOIN CORP — ENTERPRISE DASHBOARD")
    print(f"  {COMPANY['name']}")
    print(f"  CNPJ: {COMPANY['cnpj']} | {COMPANY['regime']}")
    print(f"  CEO: {COMPANY['ceo']}")
    print(f"  Capital: {COMPANY['capital']}")
    print(f"  Mission: {COMPANY['mission']}")
    print(f"{'='*70}")

    # Department summary
    print(f"\n  DEPARTMENTS ({len(DEPARTMENTS)})")
    print(f"  {'─'*60}")
    for dept_name, dept in DEPARTMENTS.items():
        agents_in_dept = [n for n, a in AGENTS.items() if a["dept"] == dept_name]
        c = dept.get("color", "")
        print(f"  {c}{dept_name:15s}{reset} | Head: {dept['head']:12s} | Agents: {len(agents_in_dept)} | {dept['mission'][:40]}")

    # Agent count
    total = len(AGENTS)
    print(f"\n  TOTAL AGENTS: {total}")

    # Daemon status
    print(f"\n  DAEMON STATUS")
    print(f"  {'─'*60}")
    for name, agent in AGENTS.items():
        if agent.get("daemon"):
            pid_file = agent.get("pid_file", "")
            running = False
            pid = "?"
            if pid_file and os.path.exists(pid_file):
                with open(pid_file) as f:
                    pid = f.read().strip()
                try:
                    os.kill(int(pid), 0)
                    running = True
                except:
                    pass
            status = "\033[92mRUNNING\033[0m" if running else "\033[91mSTOPPED\033[0m"
            print(f"  {name:15s} PID={pid:6s} {status}")

    # Revenue pipeline
    print(f"\n  REVENUE PIPELINE")
    print(f"  {'─'*60}")
    for k, v in REVENUE_PIPELINE.items():
        print(f"  {k:25s} {v['value']:>12s} | {v['status']:15s} | Agent: {v['agent']} | DL: {v['deadline']}")

    # Recent agent activity
    print(f"\n  RECENT AGENT ACTIVITY")
    print(f"  {'─'*60}")
    agent_files = glob.glob(os.path.join(AGENTS_DIR, "*.json"))
    recent = []
    for af in agent_files:
        try:
            with open(af) as f:
                s = json.load(f)
            if s.get("last_run"):
                recent.append((s["name"], s["last_run"], s["runs"], s["errors"]))
        except:
            pass
    recent.sort(key=lambda x: x[1] or "", reverse=True)
    for name, lr, runs, errs in recent[:10]:
        print(f"  {name:15s} Last: {lr[:19] if lr else 'never':19s} Runs: {runs:4d} Errors: {errs}")

    # Gov APIs
    print(f"\n  GOVERNMENT APIs CONNECTED: {len(GOV_APIS)}")
    print(f"  {'─'*60}")
    for k, v in list(GOV_APIS.items())[:5]:
        print(f"  {k:25s} {'FREE' if v['free'] else 'PAID':4s} | {v['desc']}")
    print(f"  ... and {len(GOV_APIS)-5} more")

    print(f"\n{'='*70}\n")


def cmd_roster():
    """Full employee roster."""
    print(f"\n{'='*70}")
    print(f"  PADRAO BITCOIN CORP — EMPLOYEE ROSTER ({len(AGENTS)} agents)")
    print(f"{'='*70}")

    for dept_name in DEPARTMENTS:
        agents_in_dept = {n: a for n, a in AGENTS.items() if a["dept"] == dept_name}
        if not agents_in_dept:
            continue
        c = DEPARTMENTS[dept_name].get("color", "")
        reset = "\033[0m"
        print(f"\n  {c}━━━ {dept_name} ({len(agents_in_dept)} agents) ━━━{reset}")
        for name, agent in agents_in_dept.items():
            daemon = " [DAEMON]" if agent.get("daemon") else ""
            print(f"  {name:15s} | {agent['role']:30s} | Schedule: {agent['schedule']}{daemon}")
            print(f"  {'':15s} | Tools: {', '.join(agent['tools'][:4])}")
            print(f"  {'':15s} | MCPs: {', '.join(agent['mcps']) if agent['mcps'] else 'none'}")
            print(f"  {'':15s} | Mission: {agent['mission'][:60]}")
            if agent.get("git_repos"):
                print(f"  {'':15s} | Git: {', '.join(agent['git_repos'][:3])}")
            print()


def cmd_department(dept_name):
    """Show department details."""
    dept_name = dept_name.upper()
    if dept_name not in DEPARTMENTS:
        print(f"Department {dept_name} not found. Available: {', '.join(DEPARTMENTS.keys())}")
        return

    dept = DEPARTMENTS[dept_name]
    agents_in_dept = {n: a for n, a in AGENTS.items() if a["dept"] == dept_name}

    print(f"\n{'='*60}")
    print(f"  DEPARTMENT: {dept_name}")
    print(f"  Legion: {dept['legion']} | Head: {dept['head']}")
    print(f"  Mission: {dept['mission']}")
    print(f"  Agents: {len(agents_in_dept)}")
    print(f"{'='*60}")

    for name, agent in agents_in_dept.items():
        state = get_agent_state(name)
        print(f"\n  {name} — {agent['role']}")
        print(f"    Skill: {agent['skill']}")
        print(f"    Schedule: {agent['schedule']}")
        print(f"    Tools: {', '.join(agent['tools'])}")
        print(f"    MCPs: {', '.join(agent['mcps']) if agent['mcps'] else 'none'}")
        print(f"    Git: {', '.join(agent.get('git_repos', [])) or 'none'}")
        print(f"    Mission: {agent['mission']}")
        print(f"    Goals:")
        for g in agent.get("goals", []):
            print(f"      - {g}")
        print(f"    State: runs={state['runs']}, errors={state['errors']}, last={state.get('last_run', 'never')}")


def cmd_schedule():
    """Show today's schedule for all agents."""
    now = datetime.datetime.now()
    print(f"\n{'='*60}")
    print(f"  DAILY SCHEDULE — {now.strftime('%A %d %B %Y')}")
    print(f"{'='*60}")

    # Collect all scheduled times
    schedule = []
    for name, agent in AGENTS.items():
        sched = agent.get("schedule", "")
        if sched.startswith("daemon:"):
            schedule.append(("00:00-23:59", name, agent["role"], "DAEMON (continuous)"))
            continue
        for t in sched.split(","):
            t = t.strip()
            if t:
                schedule.append((t, name, agent["role"], agent["skill"]))

    schedule.sort(key=lambda x: x[0])
    current_hour = now.strftime("%H:00")

    for time_str, name, role, skill in schedule:
        marker = " <<<" if time_str <= current_hour < f"{int(time_str[:2])+1:02d}:00" else ""
        print(f"  {time_str}  {name:15s}  {role:30s}  [{skill}]{marker}")

    print(f"\n  Total scheduled runs today: {len(schedule)}")


def cmd_revenue():
    """Revenue dashboard."""
    print(f"\n{'='*60}")
    print(f"  REVENUE PIPELINE — PADRAO BITCOIN CORP")
    print(f"{'='*60}")

    total_potential = 0
    for k, v in REVENUE_PIPELINE.items():
        val = v["value"].replace("$", "").replace(",", "").replace("/ea", "").replace("/copy", "")
        try:
            total_potential += float(val.split("-")[-1])
        except:
            pass
        urgent = " *** URGENT ***" if v.get("deadline", "none") not in ["none", "permanent", "live"] else ""
        print(f"  {k:25s} {v['value']:>12s} | {v['status']:15s} | {v['agent']:12s} | DL: {v['deadline']}{urgent}")

    print(f"\n  Total potential: ${total_potential:,.0f}+")
    print(f"  Current revenue: $0 (EMERGENCY)")


def cmd_mission(agent_name):
    """Show agent mission details."""
    agent_name = agent_name.upper()
    agent = AGENTS.get(agent_name)
    if not agent:
        print(f"Agent {agent_name} not found")
        return

    state = get_agent_state(agent_name)
    print(f"\n{'='*60}")
    print(f"  MISSION BRIEFING: {agent_name}")
    print(f"{'='*60}")
    print(f"  Role: {agent['role']}")
    print(f"  Department: {agent['dept']}")
    print(f"  Mission: {agent['mission']}")
    print(f"  Schedule: {agent['schedule']}")
    print(f"\n  GOALS:")
    for g in agent.get("goals", []):
        print(f"    [ ] {g}")
    print(f"\n  TOOLS: {', '.join(agent['tools'])}")
    print(f"  MCPs: {', '.join(agent['mcps']) if agent['mcps'] else 'none'}")
    print(f"  Git Repos: {', '.join(agent.get('git_repos', [])) or 'none'}")
    if agent.get("apis"):
        print(f"\n  CONNECTED APIs:")
        for api in agent["apis"]:
            print(f"    - {api}")
    print(f"\n  STATE: runs={state['runs']}, errors={state['errors']}, status={state['status']}")


def cmd_deploy():
    """Deploy all agents — create state files."""
    print(f"\n  Deploying {len(AGENTS)} agents...")
    for name, agent in AGENTS.items():
        state = get_agent_state(name)
        if state["runs"] == 0:  # Only initialize new agents
            state["status"] = "deployed"
            state["deployed_at"] = datetime.datetime.now().isoformat()
            save_agent_state(name, state)
            print(f"  Deployed: {name} ({agent['role']})")
        else:
            print(f"  Already active: {name} (runs={state['runs']})")
    print(f"\n  All agents deployed to {AGENTS_DIR}")


def cmd_health():
    """Health check all systems."""
    print(f"\n{'='*60}")
    print(f"  SYSTEM HEALTH CHECK")
    print(f"{'='*60}")

    # RAM
    try:
        r = subprocess.run("free -h | grep Mem", shell=True, capture_output=True, text=True, timeout=5)
        parts = r.stdout.split()
        print(f"  RAM: {parts[2]} used / {parts[1]} total (available: {parts[-1]})")
    except:
        print("  RAM: check failed")

    # Disk
    try:
        r = subprocess.run("df -h / | tail -1", shell=True, capture_output=True, text=True, timeout=5)
        parts = r.stdout.split()
        print(f"  DISK: {parts[2]} used / {parts[1]} total ({parts[4]} used)")
    except:
        print("  DISK: check failed")

    # Load
    try:
        r = subprocess.run("uptime", shell=True, capture_output=True, text=True, timeout=5)
        print(f"  LOAD: {r.stdout.strip()}")
    except:
        print("  LOAD: check failed")

    # Daemon
    print(f"\n  DAEMONS:")
    for name, agent in AGENTS.items():
        if agent.get("daemon"):
            pid_file = agent.get("pid_file", "")
            running = False
            if pid_file and os.path.exists(pid_file):
                with open(pid_file) as f:
                    pid = f.read().strip()
                try:
                    os.kill(int(pid), 0)
                    running = True
                except:
                    pass
            status = "RUNNING" if running else "STOPPED"
            print(f"    {name}: {status}")

    # Agent states
    deployed = 0
    for name in AGENTS:
        state = get_agent_state(name)
        if state["runs"] > 0 or state.get("deployed_at"):
            deployed += 1
    print(f"\n  AGENTS: {deployed}/{len(AGENTS)} deployed")

    # Git
    try:
        r = subprocess.run("cd ~/israel-one && git status --short | wc -l", shell=True, capture_output=True, text=True, timeout=5)
        print(f"  GIT: {r.stdout.strip()} uncommitted changes in israel-one")
    except:
        pass


def cmd_backup():
    """Backup all agent states."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(ZION_DIR, f"backup_{ts}")
    os.makedirs(backup_dir, exist_ok=True)

    # Copy agent states
    for name in AGENTS:
        src = os.path.join(AGENTS_DIR, f"{name}.json")
        if os.path.exists(src):
            dst = os.path.join(backup_dir, f"{name}.json")
            with open(src) as f:
                data = f.read()
            with open(dst, "w") as f:
                f.write(data)

    # Save company snapshot
    snapshot = {
        "timestamp": ts,
        "total_agents": len(AGENTS),
        "departments": len(DEPARTMENTS),
        "revenue_pipeline": REVENUE_PIPELINE,
        "gov_apis": len(GOV_APIS),
    }
    with open(os.path.join(backup_dir, "snapshot.json"), "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"  Backup saved to {backup_dir}")


def cmd_apis():
    """Show all connected government APIs."""
    print(f"\n{'='*60}")
    print(f"  GOVERNMENT APIs — PADRAO BITCOIN CORP")
    print(f"{'='*60}")
    for k, v in GOV_APIS.items():
        free = "FREE" if v["free"] else "PAID"
        auth = v["auth"]
        print(f"\n  {k}")
        print(f"    {v['desc']}")
        print(f"    URL: {v['url'][:80]}")
        print(f"    Auth: {auth} | Cost: {free}")


def cmd_count():
    """Quick agent count."""
    total = len(AGENTS)
    by_dept = {}
    for a in AGENTS.values():
        by_dept[a["dept"]] = by_dept.get(a["dept"], 0) + 1
    print(f"\n  TOTAL: {total} agents across {len(DEPARTMENTS)} departments")
    for d, c in sorted(by_dept.items()):
        print(f"    {d:15s}: {c} agents")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_status()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        cmd_status()
    elif cmd == "roster":
        cmd_roster()
    elif cmd == "department" and len(sys.argv) > 2:
        cmd_department(sys.argv[2])
    elif cmd == "schedule":
        cmd_schedule()
    elif cmd == "revenue":
        cmd_revenue()
    elif cmd == "mission" and len(sys.argv) > 2:
        cmd_mission(sys.argv[2])
    elif cmd == "run" and len(sys.argv) > 2:
        run_agent(sys.argv[2].upper())
    elif cmd == "deploy":
        cmd_deploy()
    elif cmd == "health":
        cmd_health()
    elif cmd == "backup":
        cmd_backup()
    elif cmd == "apis":
        cmd_apis()
    elif cmd == "count":
        cmd_count()
    else:
        print(__doc__)
