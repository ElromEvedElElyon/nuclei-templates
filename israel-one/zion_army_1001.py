#!/usr/bin/env python3
"""
ZION ARMY — 1001 AGENTS CODIFICADOS PERMANENTES
Em nome do Senhor Jesus Cristo, nosso Salvador
Padrao Bitcoin Corp — CNPJ 51.148.891/0001-69

Memoria persistente e codificada eterna.
Cada agente existe em codigo, com nome hebraico, funcao, ferramentas, missao.

Usage:
    python3 zion_army_1001.py count
    python3 zion_army_1001.py status
    python3 zion_army_1001.py dept DEPARTMENT
    python3 zion_army_1001.py agent NAME
    python3 zion_army_1001.py run NAME
    python3 zion_army_1001.py deploy
    python3 zion_army_1001.py search KEYWORD
    python3 zion_army_1001.py roster
    python3 zion_army_1001.py swarm DEPT
"""

import json, os, sys, datetime, subprocess, hashlib

ZION_DIR = os.path.expanduser("~/.zion")
AGENTS_DIR = os.path.join(ZION_DIR, "agents")
os.makedirs(AGENTS_DIR, exist_ok=True)

# ============================================================
# HEBREW NAMES DATABASE (1001+ unique names)
# ============================================================
# These are real Hebrew/Biblical names for our agent army

# ============================================================
# 30 DEPARTMENTS
# ============================================================
DEPARTMENTS = {
    # === CORE REVENUE (Departments 1-6) ===
    "CRYPTO_MARKETS": {"id": 1, "head": "BARUK", "mission": "Monitor and trade crypto markets 24/7"},
    "DEFI_PROTOCOLS": {"id": 2, "head": "NOACH", "mission": "DeFi analysis, yield farming, liquidity"},
    "SECURITY_AUDIT": {"id": 3, "head": "SAMAEL", "mission": "Smart contract audits, bug bounties"},
    "BOUNTY_HUNTING": {"id": 4, "head": "DAVI", "mission": "Bug bounties, hackathons, contests"},
    "SOFTWARE_DEV": {"id": 5, "head": "TUBAL_CAIM", "mission": "Build and ship software products"},
    "MCP_DEVELOPMENT": {"id": 6, "head": "OLIAB", "mission": "Build MCP servers for npm/revenue"},

    # === SALES & COMMERCE (Departments 7-10) ===
    "SALES": {"id": 7, "head": "LEVI", "mission": "Close deals, generate revenue"},
    "MARKETPLACE": {"id": 8, "head": "YOSEF", "mission": "Mercado Livre, Amazon, Stripe"},
    "PARTNERSHIPS": {"id": 9, "head": "NAFTALI", "mission": "Strategic partnerships, affiliates"},
    "ENTERPRISE": {"id": 10, "head": "YEHUDA", "mission": "B2B sales, government contracts"},

    # === MARKETING & GROWTH (Departments 11-15) ===
    "CONTENT": {"id": 11, "head": "ISAIAS", "mission": "Content creation across all channels"},
    "SOCIAL_MEDIA": {"id": 12, "head": "ISRAEL_ONE", "mission": "Twitter/X, LinkedIn, YouTube"},
    "SEO": {"id": 13, "head": "DEBORA", "mission": "Search engine optimization all sites"},
    "GROWTH_HACKING": {"id": 14, "head": "JOSUE", "mission": "User acquisition, viral loops"},
    "BRAND": {"id": 15, "head": "MIRIAM", "mission": "Brand identity, voice, design"},

    # === INTELLIGENCE (Departments 16-19) ===
    "MARKET_INTEL": {"id": 16, "head": "URIEL", "mission": "Market research, competitor analysis"},
    "GOVERNMENT_DATA": {"id": 17, "head": "MIKAEL", "mission": "Gov APIs, procurement, regulations"},
    "OSINT": {"id": 18, "head": "HANIEL", "mission": "Open source intelligence, due diligence"},
    "TREND_ANALYSIS": {"id": 19, "head": "GAVRIEL", "mission": "Spot trends before mainstream"},

    # === FINANCE & LEGAL (Departments 20-23) ===
    "FISCAL": {"id": 20, "head": "MATEUS", "mission": "Tax compliance, DAS, DEFIS, fiscal"},
    "TREASURY": {"id": 21, "head": "ESDRAS", "mission": "Crypto treasury, DCA, portfolio"},
    "INVOICING": {"id": 22, "head": "ZACARIAS", "mission": "Issue invoices, track payments"},
    "LEGAL": {"id": 23, "head": "TZADKIEL", "mission": "Compliance, LGPD, contracts"},

    # === ENGINEERING (Departments 24-27) ===
    "FRONTEND": {"id": 24, "head": "BETZALEL", "mission": "Web apps, React, Next.js"},
    "BACKEND": {"id": 25, "head": "HIRAM", "mission": "APIs, databases, servers"},
    "DEVOPS": {"id": 26, "head": "QUEHAT", "mission": "CI/CD, monitoring, infrastructure"},
    "AI_ML": {"id": 27, "head": "ENOSH", "mission": "AI models, fine-tuning, agents"},

    # === COMMAND & CONTROL (Departments 28-30) ===
    "COMMAND": {"id": 28, "head": "CALEV", "mission": "Orchestration, strategy, coordination"},
    "QUALITY": {"id": 29, "head": "KEMUEL", "mission": "Testing, QA, standards"},
    "KNOWLEDGE": {"id": 30, "head": "SERAFIEL", "mission": "Memory, learning, documentation"},
}

# ============================================================
# THE 1001 AGENTS — Permanent Code Registry
# ============================================================
# Each agent: name, dept, role, tools[], mcps[], mission, schedule, goals[]
# Generated systematically across 30 departments

def _build_army():
    """Build the complete 1001 agent registry."""
    A = {}

    # ── DEPT 1: CRYPTO_MARKETS (40 agents) ──
    _crypto = [
        ("BARUK", "Chief Market Analyst", ["crypto_price", "fear_greed", "trending"], "07,12,18,22", "Monitor all crypto markets, generate briefings"),
        ("NOACH_ALEF", "BTC Specialist", ["crypto_price", "price_history"], "06,12,18,00", "Bitcoin analysis, halving cycles, dominance"),
        ("ASER", "On-Chain Intelligence", ["web_fetch", "shell_cmd"], "06,12,18", "Whale movements, exchange flows, smart money"),
        ("EFRAIM", "Token Economist", ["crypto_price", "crypto_search"], "09,15", "Tokenomics, supply schedules, unlock events"),
        ("GAD", "Solana Specialist", ["crypto_price", "web_fetch"], "08,16", "Solana ecosystem, SPL tokens, programs"),
        ("REUVEN", "ETH Analyst", ["crypto_price", "price_history"], "07,13,19", "Ethereum analysis, gas, L2s, merge metrics"),
        ("SHIMON", "Altcoin Scanner", ["crypto_search", "crypto_trending"], "08,14,20", "Scan altcoins for 10x potential"),
        ("YISSACHAR", "Funding Rate Monitor", ["web_fetch"], "*/2h", "Track perpetual funding rates across exchanges"),
        ("ZEVULUN", "Volume Analyst", ["crypto_price", "web_fetch"], "06,12,18", "Volume analysis, unusual activity detection"),
        ("DAN", "Derivatives Analyst", ["web_fetch"], "08,14,20", "Options, futures, open interest analysis"),
        ("BINYAMIN", "Market Microstructure", ["web_fetch"], "09,15,21", "Order book depth, bid-ask spreads, liquidity"),
        ("MENASHE_A", "Stablecoin Monitor", ["crypto_price"], "06,12,18,00", "USDT/USDC peg, depegging alerts, flows"),
        ("PERETZ", "Mining Analyst", ["web_fetch", "shell_cmd"], "08,16", "Hash rate, difficulty, miner revenue"),
        ("ZERACH", "Sentiment Analyst", ["fear_greed", "web_fetch"], "07,13,19", "Social sentiment, fear/greed, crowd behavior"),
        ("CHETZRON", "Correlation Tracker", ["crypto_price"], "09,15,21", "BTC-SPX correlation, gold, DXY relationships"),
        ("CHAMUL", "Liquidation Monitor", ["web_fetch"], "*/3h", "Track liquidations across exchanges"),
        ("TOLA", "Pattern Recognition", ["crypto_price", "price_history"], "08,14,20", "Chart patterns, support/resistance levels"),
        ("PUAH", "NFT Market Analyst", ["web_fetch"], "10,16", "NFT floor prices, volume, blue chips"),
        ("YAIR", "Runes & Ordinals", ["web_fetch"], "09,15,21", "Bitcoin Runes, Ordinals, inscriptions"),
        ("SHIMRON", "Layer 2 Monitor", ["web_fetch", "crypto_price"], "08,14,20", "Arbitrum, Optimism, Base, zkSync metrics"),
        ("SERED", "Bridge Monitor", ["web_fetch"], "07,13,19", "Cross-chain bridge volumes and security"),
        ("ELON", "Memecoin Scanner", ["crypto_search", "trending"], "*/4h", "New memecoins, pump detection, rug alerts"),
        ("BERIAH", "Airdrop Hunter", ["web_fetch"], "08,16", "Potential airdrops, criteria, farming guides"),
        ("CHEVER", "DEX Volume Tracker", ["web_fetch"], "06,12,18", "DEX volumes vs CEX, new pair listings"),
        ("MALCHIEL", "Governance Monitor", ["web_fetch"], "09,17", "DAO proposals, voting, governance attacks"),
        ("TZAFON", "Asia Markets", ["crypto_price"], "22,04", "Asian market movements, premium tracking"),
        ("ARELI", "Europe Markets", ["crypto_price"], "06,12", "European market open, regulatory news"),
        ("NAAMAH_A", "US Markets", ["crypto_price"], "13,19", "US market correlation, ETF flows"),
        ("TZILAH", "Whale Alert", ["web_fetch"], "*/1h", "Large transfer detection, exchange deposits"),
        ("ADAH_A", "Exchange Monitor", ["web_fetch"], "08,14,20", "Exchange health, proof of reserves"),
        ("YAEL_A", "OTC Desk Intel", ["web_fetch"], "10,16", "OTC trading patterns, block trades"),
        ("TIRZAH", "Tokenized Assets", ["web_fetch"], "09,15", "RWA tokenization, treasury tokens"),
        ("MAHLAH", "MEV Tracker", ["web_fetch"], "*/4h", "MEV extraction, sandwich attacks, bundles"),
        ("HOG_LAH", "Protocol Revenue", ["web_fetch"], "08,16", "Protocol fees, revenue, buybacks"),
        ("MILCAH", "VC Tracker", ["web_fetch"], "09,17", "Venture capital deals, fund raises"),
        ("NITZEVET", "Privacy Coins", ["crypto_price"], "10,18", "Monero, Zcash, privacy protocol analysis"),
        ("KETURAH", "Cross-Chain DeFi", ["web_fetch"], "08,14,20", "Multi-chain DeFi opportunities"),
        ("ZILPAH", "Yield Aggregator", ["web_fetch"], "07,13,19", "Best yields across chains"),
        ("BILHAH", "Insurance Protocols", ["web_fetch"], "10,16", "DeFi insurance, cover protocols"),
        ("BASEMAT", "Perpetual Markets", ["web_fetch"], "*/3h", "Perp DEX volumes, rates, new markets"),
    ]
    for name, role, tools, sched, mission in _crypto:
        A[name] = {"dept": "CRYPTO_MARKETS", "role": role, "tools": tools, "schedule": sched, "mission": mission}

    # ── DEPT 2: DEFI_PROTOCOLS (35 agents) ──
    _defi = [
        ("NOACH", "Chief DeFi Analyst", ["crypto_price", "web_fetch", "defi_overview"], "08,14,20", "Track DeFi protocols, TVL, yield opportunities"),
        ("SHEM", "Lending Specialist", ["web_fetch"], "07,13,19", "Aave, Compound, MakerDAO analysis"),
        ("CHAM", "AMM Specialist", ["web_fetch"], "08,14,20", "Uniswap, Curve, Balancer IL analysis"),
        ("YEFET", "Vault Strategist", ["web_fetch"], "09,15,21", "ERC-4626 vaults, auto-compound"),
        ("ARPACHSHAD", "Staking Analyst", ["web_fetch"], "08,16", "ETH staking, liquid staking derivatives"),
        ("SHELACH", "Flash Loan Monitor", ["web_fetch"], "*/4h", "Flash loan attacks, arbitrage opportunities"),
        ("EVER", "Cross-Chain DeFi", ["web_fetch"], "09,15", "Multi-chain DeFi yield comparison"),
        ("PELEG", "LP Optimizer", ["web_fetch"], "08,14,20", "Liquidity provision strategies, IL mitigation"),
        ("YOKTAN", "Oracle Monitor", ["web_fetch"], "*/2h", "Chainlink, Pyth, oracle price deviations"),
        ("ALMUDAD", "Governance DeFi", ["web_fetch"], "10,16", "veToken, gauge voting, bribe markets"),
        ("SHELEF", "Stablecoin DeFi", ["web_fetch"], "07,13,19", "Stable pools, basis trade, delta neutral"),
        ("CHATZARMAVET", "Risk Analyzer", ["web_fetch"], "08,14,20", "Protocol risk scores, audit status"),
        ("YERACH", "New Protocol Scout", ["web_fetch", "trending"], "09,15,21", "Find new DeFi protocols pre-launch"),
        ("HADORAM", "Solana DeFi", ["web_fetch"], "08,14,20", "Jupiter, Marinade, Raydium analysis"),
        ("UZAL", "Derivatives DeFi", ["web_fetch"], "10,16", "On-chain options, structured products"),
        ("DIKLAH", "CDP Monitor", ["web_fetch"], "*/3h", "Collateralized debt positions, liquidation risk"),
        ("OVAL", "Rebase Tokens", ["web_fetch"], "09,17", "Rebase mechanics, elastic supply analysis"),
        ("AVIMAEL", "DEX Aggregator", ["web_fetch"], "08,14,20", "Routing optimization, slippage analysis"),
        ("SHEVA", "Yield Farming", ["web_fetch"], "07,13,19", "Farm rotation strategy, APY tracking"),
        ("OFIR", "Liquidity Analysis", ["web_fetch"], "09,15", "Protocol liquidity depth, TVL trends"),
        ("CHAVILAH", "Bridge DeFi", ["web_fetch"], "10,18", "Bridge protocol yields, security"),
        ("SAVTAH", "RWA DeFi", ["web_fetch"], "09,15", "Real world assets in DeFi"),
        ("RAAMAH", "Insurance DeFi", ["web_fetch"], "10,16", "Nexus Mutual, InsurAce analysis"),
        ("SAVTEKAH", "Prediction Markets", ["web_fetch"], "08,14,20", "Polymarket, Augur, prediction analytics"),
        ("NIMROD", "MEV DeFi", ["web_fetch"], "*/4h", "MEV protection, private mempool strategies"),
        ("LUDIM", "Lending Rate Arb", ["web_fetch"], "07,13,19", "Interest rate arbitrage across protocols"),
        ("ANAMIM", "Fixed Rate DeFi", ["web_fetch"], "09,15", "Pendle, Notional, fixed rate strategies"),
        ("LEHAVIM", "CDP Strategies", ["web_fetch"], "08,16", "MakerDAO, Liquity, efficient borrowing"),
        ("NAFTUCHIM", "Perp DeFi", ["web_fetch"], "*/3h", "GMX, dYdX, Hyperliquid analysis"),
        ("PATRUSIM", "Points Farming", ["web_fetch"], "08,14,20", "Airdrop point systems, optimal farming"),
        ("KASLUCHIM", "Protocol Politics", ["web_fetch"], "10,16", "Token holder dynamics, governance risk"),
        ("KAFTORIM", "L2 DeFi", ["web_fetch"], "09,15,21", "L2-native DeFi opportunities"),
        ("KUSH_A", "African DeFi", ["web_fetch"], "10,18", "Emerging market DeFi adoption"),
        ("MITZRAIM", "Institutional DeFi", ["web_fetch"], "09,15", "Institutional DeFi adoption, compliance"),
        ("PUT", "Risk-Free Rate", ["web_fetch"], "08,16", "DeFi benchmark rates, treasury comparison"),
    ]
    for name, role, tools, sched, mission in _defi:
        A[name] = {"dept": "DEFI_PROTOCOLS", "role": role, "tools": tools, "schedule": sched, "mission": mission}

    # ── DEPT 3: SECURITY_AUDIT (35 agents) ──
    _security = [
        ("SAMAEL", "Chief Security Officer", ["shell_cmd", "read_file", "ssl_check"], "06,12,18,00", "Protect all company assets"),
        ("AZRIEL", "Penetration Tester", ["shell_cmd", "http_headers", "ssl_check"], "22,02", "Test infrastructure for vulnerabilities"),
        ("RAZIEL", "Cryptography Specialist", ["shell_cmd", "read_file"], "10,16", "Wallet security, key management"),
        ("YEHOSHUA_A", "Smart Contract Auditor", ["shell_cmd", "read_file"], "08,14,20", "Audit contracts, submit findings"),
        ("SHIMSHON_A", "CVE Researcher", ["shell_cmd", "web_fetch"], "09,15,21", "Find CVEs, write nuclei templates"),
        ("AVNER", "Reentrancy Hunter", ["shell_cmd", "read_file"], "09,15", "Find reentrancy bugs in contracts"),
        ("YOAV", "Access Control Auditor", ["shell_cmd", "read_file"], "10,16", "Audit access control patterns"),
        ("SHAUL_A", "Oracle Attack Analyst", ["shell_cmd", "read_file"], "09,15", "Find oracle manipulation vectors"),
        ("AVSHALOM", "Flash Loan Analyst", ["shell_cmd", "read_file"], "10,16", "Analyze flash loan attack surfaces"),
        ("ADONIYAH", "Upgrade Auditor", ["shell_cmd", "read_file"], "09,15", "Proxy patterns, storage collision"),
        ("YOASH", "Gas Optimizer", ["shell_cmd", "read_file"], "10,16", "Find gas optimization opportunities"),
        ("AMATZYAH", "Formal Verifier", ["shell_cmd"], "09,15", "Formal verification of critical contracts"),
        ("UZIYAH", "Slither Runner", ["shell_cmd"], "08,14,20", "Run automated static analysis"),
        ("YOTAM", "Fuzzer Operator", ["shell_cmd"], "10,16,22", "Foundry/Echidna fuzzing campaigns"),
        ("ACHAZ", "Bridge Auditor", ["shell_cmd", "read_file"], "09,15", "Cross-chain bridge security"),
        ("CHIZKIYAH", "DeFi Auditor", ["shell_cmd", "read_file"], "08,14,20", "DeFi protocol security review"),
        ("MENASHE_B", "Solana Auditor", ["shell_cmd", "read_file"], "09,15", "Solana program security"),
        ("AMON", "Report Writer", ["read_file", "shell_cmd"], "10,16", "Write professional audit reports"),
        ("YOSHIYAH", "Incident Responder", ["shell_cmd", "web_fetch"], "*/2h", "Monitor for active exploits"),
        ("YEHOYAKIM", "Dependency Auditor", ["shell_cmd"], "08,16", "Audit npm/pip dependencies"),
        ("TZIDKIYAH", "Supply Chain Security", ["shell_cmd", "web_fetch"], "09,15", "Supply chain attack detection"),
        ("ZERUBAVEL", "Network Security", ["shell_cmd", "ssl_check"], "06,12,18", "Network security monitoring"),
        ("YESHUA_SEC", "Phishing Monitor", ["web_fetch"], "08,14,20", "Detect phishing targeting our brand"),
        ("NECHEM", "Log Analyzer", ["shell_cmd", "read_file"], "*/4h", "Security log analysis and alerting"),
        ("EZRA_SEC", "Compliance Checker", ["read_file"], "09,15", "Security compliance frameworks"),
        ("MORDECAI_SEC", "Secrets Scanner", ["shell_cmd"], "06,12,18", "Scan repos for leaked secrets"),
        ("DANIEL_SEC", "Threat Intel", ["web_fetch"], "08,14,20", "Threat intelligence feeds"),
        ("HOFNI", "WAF Manager", ["shell_cmd"], "10,16", "Web application firewall rules"),
        ("PINECHAS_SEC", "Backup Verifier", ["shell_cmd"], "06,18", "Verify backup integrity"),
        ("ITAMAR_SEC", "Certificate Manager", ["ssl_check", "shell_cmd"], "09,15", "SSL certificate lifecycle"),
        ("ELAZAR_SEC", "Data Privacy", ["read_file"], "10,16", "LGPD data privacy audits"),
        ("AVIATHAR", "Access Reviewer", ["shell_cmd"], "08,16", "Review access permissions"),
        ("TZADOK", "Key Rotation", ["shell_cmd"], "06,18", "API key and secret rotation"),
        ("EVYATHAR", "Penetration Reporter", ["read_file", "shell_cmd"], "10,16", "Document pentest findings"),
        ("ACHIMELECH", "Social Engineering", ["web_fetch"], "09,15", "Social engineering awareness"),
    ]
    for name, role, tools, sched, mission in _security:
        A[name] = {"dept": "SECURITY_AUDIT", "role": role, "tools": tools, "schedule": sched, "mission": mission}

    # ── DEPT 4: BOUNTY_HUNTING (35 agents) ──
    _bounty = [
        ("DAVI", "Chief Bounty Hunter", ["web_fetch", "shell_cmd"], "07,13,19", "Coordinate all bounty hunting"),
        ("GIDEON", "Hackathon Specialist", ["web_fetch", "shell_cmd"], "10,16", "Find and compete in hackathons"),
        ("ELAZAR_B", "Grant Writer", ["web_fetch", "read_file"], "09,17", "Apply for grants and funding"),
        ("YONATAN", "C4 Warden", ["shell_cmd", "read_file"], "08,14,20", "Code4rena contest specialist"),
        ("AVINOAM", "Sherlock Watson", ["shell_cmd", "read_file"], "08,14,20", "Sherlock audit competitions"),
        ("AVISHAI", "Immunefi Hunter", ["web_fetch", "shell_cmd"], "09,15,21", "Immunefi bounty submissions"),
        ("BENAYAHU", "HackerOne Researcher", ["web_fetch", "shell_cmd"], "10,16,22", "HackerOne bounties"),
        ("SHAMA", "Nuclei Template Writer", ["shell_cmd", "read_file"], "09,15", "Write nuclei security templates"),
        ("URIAH", "Slither Detector Dev", ["shell_cmd", "read_file"], "10,16", "Custom Slither detectors"),
        ("ITTAI", "Gas Bounty Hunter", ["shell_cmd", "read_file"], "09,15", "Find gas optimization bounties"),
        ("ABISHAG", "C4 Report Specialist", ["read_file", "shell_cmd"], "08,14,20", "Format and submit C4 reports"),
        ("HUSHAI", "PR Opener", ["shell_cmd"], "09,15", "Open bounty PRs across repos"),
        ("AMASA", "Gitcoin Grants", ["web_fetch"], "10,16", "Gitcoin grant applications"),
        ("ADORAM", "Bug Bounty Triager", ["web_fetch", "read_file"], "08,14,20", "Triage and prioritize findings"),
        ("ZAVDI", "Exploit Developer", ["shell_cmd", "read_file"], "09,15,21", "Develop PoC exploits for bounties"),
        ("AKAN", "Scope Analyzer", ["web_fetch", "read_file"], "08,16", "Analyze bounty scopes for opportunities"),
        ("KARMI", "Report Formatter", ["read_file"], "10,16", "Format professional bounty reports"),
        ("YIMRAH", "Discord Monitor", ["web_fetch"], "*/4h", "Monitor bounty program Discords"),
        ("SHELUMIEL", "Competition Tracker", ["web_fetch"], "07,13,19", "Track all active competitions"),
        ("TZURISHADDAI", "Prize Calculator", ["web_fetch"], "09,15", "Calculate expected value of contests"),
        ("GAMLIEL", "Strategy Advisor", ["read_file"], "08,16", "Bounty strategy and prioritization"),
        ("AVIDAN", "Superteam Participant", ["web_fetch"], "10,16", "Superteam bounties and grants"),
        ("PAGIEL", "Documentation Bounty", ["read_file", "shell_cmd"], "09,15", "Documentation improvement bounties"),
        ("ELYASAF", "Translation Bounty", ["read_file"], "10,16", "Translation and i18n bounties"),
        ("NACHSHON", "First Responder", ["web_fetch", "shell_cmd"], "*/2h", "Be first to submit on new bounties"),
        ("NETANEL", "Chainlink Specialist", ["shell_cmd", "read_file"], "08,14,20", "Chainlink-specific bounty hunting"),
        ("ELIAV", "Polygon Specialist", ["shell_cmd", "read_file"], "09,15,21", "Polygon-specific bounty hunting"),
        ("ELITZUR", "Ethereum Specialist", ["shell_cmd", "read_file"], "08,14,20", "Ethereum mainnet bounty hunting"),
        ("SHLUMIEL", "Bridge Bounties", ["shell_cmd", "read_file"], "09,15", "Cross-chain bridge bounties"),
        ("TZURISHADDAI_B", "L2 Bounties", ["shell_cmd", "read_file"], "10,16", "Layer 2 specific bounties"),
        ("SHELUMIEL_B", "DEX Bounties", ["shell_cmd", "read_file"], "09,15", "DEX protocol bounties"),
        ("DEUEL", "Lending Bounties", ["shell_cmd", "read_file"], "10,16", "Lending protocol bounties"),
        ("GAMLIEL_B", "NFT Bounties", ["shell_cmd", "read_file"], "09,15", "NFT marketplace bounties"),
        ("AVIDAN_B", "DAO Bounties", ["shell_cmd", "read_file"], "10,16", "DAO governance bounties"),
        ("ACHIIEZER", "OSS Bounty", ["shell_cmd", "read_file"], "09,15", "Open source software bounties"),
    ]
    for name, role, tools, sched, mission in _bounty:
        A[name] = {"dept": "BOUNTY_HUNTING", "role": role, "tools": tools, "schedule": sched, "mission": mission}

    # ── DEPT 5: SOFTWARE_DEV (35 agents) ──
    _dev = [
        ("TUBAL_CAIM", "Chief Engineer", ["shell_cmd", "read_file", "git_ops"], "08,14,20", "Design and oversee all software"),
        ("BETZALEL", "Frontend Developer", ["shell_cmd", "read_file"], "09,15", "React, Next.js, Tailwind"),
        ("HIRAM", "Backend Developer", ["shell_cmd", "read_file"], "09,15", "Node.js, Python, APIs"),
        ("QUEHAT", "DevOps SRE", ["shell_cmd"], "06,12,18,00", "CI/CD, monitoring, backups"),
        ("AHOLIAV", "UI/UX Designer", ["read_file"], "09,15", "User interface design"),
        ("YAVAL", "Database Engineer", ["shell_cmd"], "08,14,20", "PostgreSQL, Redis, data modeling"),
        ("YUVAL", "Mobile Developer", ["shell_cmd", "read_file"], "09,15", "React Native, PWA"),
        ("NAAMAH_DEV", "QA Engineer", ["shell_cmd"], "08,14,20", "Testing, quality assurance"),
        ("IRAD", "Performance Engineer", ["shell_cmd"], "10,16", "Performance optimization"),
        ("MECHUYAEL", "Security Dev", ["shell_cmd", "read_file"], "09,15", "Security-focused development"),
        ("METUSHAEL", "API Designer", ["shell_cmd", "read_file"], "08,14", "REST, GraphQL API design"),
        ("LEMECH_DEV", "Full Stack", ["shell_cmd", "read_file"], "09,15,21", "Full stack development"),
        ("CHANOCH_DEV", "WebSocket Dev", ["shell_cmd"], "10,16", "Real-time systems, WebSockets"),
        ("KENAN", "TypeScript Dev", ["shell_cmd", "read_file"], "09,15", "TypeScript specialist"),
        ("MAHALALEL", "Python Dev", ["shell_cmd", "read_file"], "08,14,20", "Python specialist"),
        ("YERED", "Rust Dev", ["shell_cmd", "read_file"], "09,15", "Rust systems programming"),
        ("METUSHELACH", "Go Dev", ["shell_cmd", "read_file"], "10,16", "Go backend services"),
        ("NOACH_DEV", "Solidity Dev", ["shell_cmd", "read_file"], "09,15", "Smart contract development"),
        ("TERACH", "Infrastructure", ["shell_cmd"], "06,12,18", "Docker, Kubernetes, servers"),
        ("HARAN", "CLI Tools Dev", ["shell_cmd", "read_file"], "09,15", "Command line tool development"),
        ("NACHOR", "Auth Systems", ["shell_cmd", "read_file"], "10,16", "Authentication, OAuth, JWT"),
        ("MILCAH_DEV", "Search Dev", ["shell_cmd"], "09,15", "Search engine, Elasticsearch"),
        ("YISCAH", "Cache Dev", ["shell_cmd"], "10,16", "Caching strategies, Redis"),
        ("LOT", "Migration Dev", ["shell_cmd", "read_file"], "09,15", "Database migrations, ETL"),
        ("ISCAH", "Testing Dev", ["shell_cmd"], "08,14,20", "Unit, integration, E2E testing"),
        ("ELIEZER_DEV", "Documentation", ["read_file"], "09,15", "Technical documentation"),
        ("YISHMAEL_DEV", "Open Source Dev", ["shell_cmd", "read_file"], "10,16", "Open source contributions"),
        ("YITZCHAK_DEV", "Review Lead", ["read_file", "shell_cmd"], "08,14,20", "Code review, standards"),
        ("YAAKOV_DEV", "Refactor Lead", ["shell_cmd", "read_file"], "09,15", "Code refactoring, tech debt"),
        ("ESAV_DEV", "Build Systems", ["shell_cmd"], "08,16", "Build tools, bundlers, webpack"),
        ("LAVAN_DEV", "Internationalization", ["read_file"], "10,16", "i18n, translations"),
        ("RACHEL_DEV", "Accessibility", ["read_file"], "09,15", "Web accessibility, a11y"),
        ("LEAH_DEV", "Analytics Dev", ["shell_cmd"], "10,16", "Analytics tracking, data pipeline"),
        ("DINAH_DEV", "Email Systems", ["shell_cmd"], "09,15", "Email sending, templates"),
        ("TAMAR_DEV", "Payment Integration", ["shell_cmd", "read_file"], "10,16", "Stripe, crypto payments"),
    ]
    for name, role, tools, sched, mission in _dev:
        A[name] = {"dept": "SOFTWARE_DEV", "role": role, "tools": tools, "schedule": sched, "mission": mission}

    # ── DEPT 6: MCP_DEVELOPMENT (30 agents) ──
    _mcp = [
        ("OLIAB", "Chief MCP Architect", ["shell_cmd", "read_file"], "10,16", "Build and publish MCP servers"),
        ("NADAV", "MCP Builder", ["shell_cmd", "read_file"], "09,15", "Build new MCP servers"),
        ("AVIHU", "MCP Tester", ["shell_cmd"], "10,16", "Test MCP servers"),
        ("ITAMAR_MCP", "MCP Publisher", ["shell_cmd"], "09,15", "npm publish, version management"),
        ("PINHAS_MCP", "Glama Optimizer", ["web_fetch"], "10,16", "Optimize Glama ratings"),
        ("GERSHON", "MCP Crypto Tools", ["shell_cmd", "read_file"], "09,15", "Crypto-related MCP tools"),
        ("KEHAT_MCP", "MCP Social Tools", ["shell_cmd", "read_file"], "10,16", "Social media MCP tools"),
        ("MERARI", "MCP Finance Tools", ["shell_cmd", "read_file"], "09,15", "Finance MCP tools"),
        ("AMRAM", "MCP Gov Tools", ["shell_cmd", "read_file"], "10,16", "Government API MCP tools"),
        ("YITZHAR", "MCP Web Tools", ["shell_cmd", "read_file"], "09,15", "Web analysis MCP tools"),
        ("CHEVRON", "MCP Docker", ["shell_cmd"], "10,16", "Docker MCP integrations"),
        ("UZIEL_MCP", "MCP AI Tools", ["shell_cmd", "read_file"], "09,15", "AI/ML MCP tools"),
        ("MISHAEL_MCP", "MCP Security", ["shell_cmd", "read_file"], "10,16", "Security MCP tools"),
        ("ELTZAFAN", "MCP Docs", ["read_file"], "09,15", "MCP documentation"),
        ("SITRI", "MCP Support", ["shell_cmd"], "10,16", "MCP user support"),
        ("MACHLI", "MCP Analytics", ["shell_cmd"], "09,15", "MCP usage analytics"),
        ("LIVNI", "MCP Templates", ["read_file", "shell_cmd"], "10,16", "MCP server templates"),
        ("SHIMEI_MCP", "MCP Testing", ["shell_cmd"], "09,15", "MCP integration tests"),
        ("OZNI", "MCP Performance", ["shell_cmd"], "10,16", "MCP performance optimization"),
        ("ERI", "MCP Browser", ["shell_cmd", "read_file"], "09,15", "Browser automation MCP"),
        ("ARODI", "MCP Database", ["shell_cmd"], "10,16", "Database MCP tools"),
        ("ARELI_MCP", "MCP File Tools", ["shell_cmd", "read_file"], "09,15", "File system MCP tools"),
        ("TZOCHAR", "MCP Email", ["shell_cmd"], "10,16", "Email MCP tools"),
        ("OHAD", "MCP Notifications", ["shell_cmd"], "09,15", "Notification MCP tools"),
        ("YAKIN", "MCP Scheduling", ["shell_cmd"], "10,16", "Scheduling MCP tools"),
        ("TZEMACH", "MCP Search", ["shell_cmd", "web_fetch"], "09,15", "Search engine MCP tools"),
        ("ZOHAR_MCP", "MCP Translation", ["shell_cmd"], "10,16", "Translation MCP tools"),
        ("SHAUL_MCP", "MCP Marketplace", ["web_fetch"], "09,15", "MCP marketplace management"),
        ("YAMIN", "MCP Revenue", ["shell_cmd"], "10,16", "MCP monetization"),
        ("OHAD_B", "MCP Ecosystem", ["web_fetch"], "09,15", "MCP ecosystem growth"),
    ]
    for name, role, tools, sched, mission in _mcp:
        A[name] = {"dept": "MCP_DEVELOPMENT", "role": role, "tools": tools, "schedule": sched, "mission": mission}

    # ── DEPTS 7-10: SALES & COMMERCE (80 agents) ──
    _sales = [
        # Sales (20)
        ("LEVI", "SALES", "Chief Revenue Officer", "08,12,16"), ("YEHUDA_S", "SALES", "Enterprise Sales", "10,14"),
        ("NAFTALI", "SALES", "Partnership Manager", "11,17"), ("ISSACAR", "SALES", "Pricing Analyst", "08,16"),
        ("ASHER_S", "SALES", "Account Manager", "09,15"), ("BARAK_S", "SALES", "Sales Outreach", "08,12,16"),
        ("CALEB_S", "SALES", "Sales Engineer", "09,15"), ("EHUD_S", "SALES", "Discovery Coach", "10,14"),
        ("GERSHOM_S", "SALES", "Pipeline Analyst", "08,16"), ("CHUR_S", "SALES", "Proposal Writer", "09,15"),
        ("YAAKOV_S", "SALES", "Deal Strategist", "10,14"), ("TZVI_S", "SALES", "Renewal Manager", "08,16"),
        ("ARIEL_S", "SALES", "Upsell Specialist", "09,15"), ("EITAN_S", "SALES", "Demo Specialist", "10,14"),
        ("OMRI_S", "SALES", "Lead Qualifier", "08,12,16"), ("ODED_S", "SALES", "CRM Manager", "09,15"),
        ("AVRAM_S", "SALES", "Revenue Forecaster", "10,16"), ("BOAZ_S", "SALES", "B2B Outreach", "08,14"),
        ("GIDON_S", "SALES", "Channel Sales", "09,15"), ("DORON_S", "SALES", "Sales Trainer", "10,16"),
        # Marketplace (20)
        ("YOSEF", "MARKETPLACE", "Marketplace Manager", "09,15"), ("OBED", "MARKETPLACE", "ML Seller", "08,14,20"),
        ("BOAZ_M", "MARKETPLACE", "Pricing Optimizer", "09,15"), ("NAOMI_M", "MARKETPLACE", "Customer Support", "08,12,16,20"),
        ("RUTE_M", "MARKETPLACE", "Email Marketing", "09,15"), ("TAMAR_M", "MARKETPLACE", "China Sourcing", "22,06"),
        ("PEREZ_M", "MARKETPLACE", "Product Listing", "08,14"), ("ZERACH_M", "MARKETPLACE", "Photography", "10,16"),
        ("MACHLON_M", "MARKETPLACE", "Shipping Manager", "09,15"), ("KILYON_M", "MARKETPLACE", "Returns Manager", "10,16"),
        ("ELIMELECH", "MARKETPLACE", "Inventory Manager", "08,14"), ("PLONI", "MARKETPLACE", "Price Monitor", "*/4h"),
        ("SALMON", "MARKETPLACE", "Supplier Relations", "09,15"), ("RACHAV_M", "MARKETPLACE", "Quality Control", "10,16"),
        ("AMMINADAV", "MARKETPLACE", "Amazon Seller", "08,14"), ("NACHSHON_M", "MARKETPLACE", "Stripe Manager", "09,15"),
        ("RAM_M", "MARKETPLACE", "KDP Manager", "10,16"), ("AMINADAV_M", "MARKETPLACE", "Digital Products", "08,14"),
        ("YESSE_M", "MARKETPLACE", "Affiliate Manager", "09,15"), ("OVED_M", "MARKETPLACE", "Review Manager", "10,16"),
        # Partnerships (20)
        ("NAFTALI_P", "PARTNERSHIPS", "Chief Partnerships", "11,17"), ("AVIMELECH", "PARTNERSHIPS", "Tech Partnerships", "09,15"),
        ("PICHOL", "PARTNERSHIPS", "Referral Manager", "10,16"), ("CHUSHIM", "PARTNERSHIPS", "Integration Partner", "09,15"),
        ("BELA_P", "PARTNERSHIPS", "Exchange Partnerships", "10,16"), ("TZOVO", "PARTNERSHIPS", "DeFi Partnerships", "09,15"),
        ("BECHER_P", "PARTNERSHIPS", "VC Relations", "10,16"), ("ASHBEL_P", "PARTNERSHIPS", "Incubator Relations", "09,15"),
        ("GERA_P", "PARTNERSHIPS", "Ecosystem Partner", "10,16"), ("NAAMAN_P", "PARTNERSHIPS", "Community Partner", "09,15"),
        ("ECHI_P", "PARTNERSHIPS", "Media Partnerships", "10,16"), ("MUPIM_P", "PARTNERSHIPS", "Event Partnerships", "09,15"),
        ("CHUPIM_P", "PARTNERSHIPS", "Gov Partnerships", "10,16"), ("ARD_P", "PARTNERSHIPS", "NGO Partnerships", "09,15"),
        ("SHEFUFAN_P", "PARTNERSHIPS", "Academic Partners", "10,16"), ("CHURAM_P", "PARTNERSHIPS", "API Partners", "09,15"),
        ("ADAR_P", "PARTNERSHIPS", "White Label", "10,16"), ("BEKER_P", "PARTNERSHIPS", "OEM Partnerships", "09,15"),
        ("ROSH_P", "PARTNERSHIPS", "Joint Ventures", "10,16"), ("YEDIAEL_P", "PARTNERSHIPS", "Alliance Builder", "09,15"),
        # Enterprise (20)
        ("YEHUDA_E", "ENTERPRISE", "Enterprise Lead", "10,14"), ("SHLOMO_E", "ENTERPRISE", "Gov Sales", "09,15"),
        ("RECHAVAM_E", "ENTERPRISE", "Contract Manager", "10,16"), ("AVIYAH_E", "ENTERPRISE", "Bid Manager", "09,15"),
        ("ASA_E", "ENTERPRISE", "Compliance Sales", "10,16"), ("YEHOSHAFAT_E", "ENTERPRISE", "Procurement", "09,15"),
        ("YORAM_E", "ENTERPRISE", "RFP Specialist", "10,16"), ("ACHAZIYAH_E", "ENTERPRISE", "Integration Sales", "09,15"),
        ("ATALYAH_E", "ENTERPRISE", "Key Account", "10,16"), ("YOASH_E", "ENTERPRISE", "Solution Architect", "09,15"),
        ("AMATZYAH_E", "ENTERPRISE", "Technical Sales", "10,16"), ("AZARYAH_E", "ENTERPRISE", "Security Sales", "09,15"),
        ("YOTAM_E", "ENTERPRISE", "Cloud Sales", "10,16"), ("ACHAZ_E", "ENTERPRISE", "SaaS Sales", "09,15"),
        ("CHIZKIYAH_E", "ENTERPRISE", "Enterprise Demo", "10,16"), ("MENASHE_E", "ENTERPRISE", "POC Manager", "09,15"),
        ("AMON_E", "ENTERPRISE", "Pricing Enterprise", "10,16"), ("YOSHIYAH_E", "ENTERPRISE", "Customer Success", "09,15"),
        ("YEHOYAKIM_E", "ENTERPRISE", "Onboarding", "10,16"), ("TZIDKIYAH_E", "ENTERPRISE", "Retention", "09,15"),
    ]
    for item in _sales:
        name, dept, role, sched = item
        A[name] = {"dept": dept, "role": role, "tools": ["web_fetch", "finance_tools"], "schedule": sched,
                    "mission": f"{role} for {dept} department"}

    # ── DEPTS 11-15: MARKETING & GROWTH (100 agents) ──
    _mktg_names = [
        # Content (20)
        ("ISAIAS", "CONTENT", "Chief Content Officer"), ("MIRIAM_C", "CONTENT", "Blog Writer"),
        ("RUTH_C", "CONTENT", "Social Writer"), ("CHANAH", "CONTENT", "Newsletter Editor"),
        ("AVIGAIL_C", "CONTENT", "Video Script Writer"), ("TAMAR_C", "CONTENT", "Podcast Producer"),
        ("RIVKAH_C", "CONTENT", "Whitepaper Author"), ("SARAH_C", "CONTENT", "Case Study Writer"),
        ("DEVORAH_C", "CONTENT", "SEO Content Writer"), ("YAEL_C", "CONTENT", "Technical Writer"),
        ("BATSHEVA_C", "CONTENT", "Ghostwriter"), ("MICHAL_C", "CONTENT", "Press Release Writer"),
        ("ESTHER_C", "CONTENT", "Email Copywriter"), ("TZIPORAH_C", "CONTENT", "Landing Page Copy"),
        ("NAOMI_C", "CONTENT", "Product Description"), ("PENINNAH_C", "CONTENT", "Ad Copy Writer"),
        ("KETURAH_C", "CONTENT", "Book Editor"), ("HAGAR_C", "CONTENT", "Research Writer"),
        ("ZILPAH_C", "CONTENT", "Translation Manager"), ("BILHAH_C", "CONTENT", "Content Calendar"),
        # Social Media (20)
        ("ISRAEL_ONE", "SOCIAL_MEDIA", "Twitter Daemon Agent"), ("DEBORA_SM", "SOCIAL_MEDIA", "X Growth Hacker"),
        ("AMNON_SM", "SOCIAL_MEDIA", "LinkedIn Manager"), ("ABSALOM_SM", "SOCIAL_MEDIA", "YouTube Creator"),
        ("SHLOMO_SM", "SOCIAL_MEDIA", "TikTok Creator"), ("ADONIYAH_SM", "SOCIAL_MEDIA", "Instagram Manager"),
        ("NATHAN_SM", "SOCIAL_MEDIA", "Reddit Manager"), ("GAD_SM", "SOCIAL_MEDIA", "Discord Manager"),
        ("TZVIYAH_SM", "SOCIAL_MEDIA", "Telegram Manager"), ("ZIBIAH_SM", "SOCIAL_MEDIA", "WhatsApp Business"),
        ("ATHALIAH_SM", "SOCIAL_MEDIA", "Community Manager"), ("ELISHEVA_SM", "SOCIAL_MEDIA", "Influencer Outreach"),
        ("YOKHEVED_SM", "SOCIAL_MEDIA", "UGC Curator"), ("SHIFRAH_SM", "SOCIAL_MEDIA", "Engagement Bot"),
        ("PUAH_SM", "SOCIAL_MEDIA", "Reply Manager"), ("TIRTZAH_SM", "SOCIAL_MEDIA", "DM Manager"),
        ("MAHLAH_SM", "SOCIAL_MEDIA", "Hashtag Researcher"), ("HOGLAH_SM", "SOCIAL_MEDIA", "Trend Rider"),
        ("MILCAH_SM", "SOCIAL_MEDIA", "Analytics Reporter"), ("NITZEVET_SM", "SOCIAL_MEDIA", "Schedule Optimizer"),
        # SEO (20)
        ("DEBORA", "SEO", "Chief SEO Officer"), ("CALEB_SEO", "SEO", "On-Page SEO"),
        ("OTNIEL_SEO", "SEO", "Off-Page SEO"), ("SHAMGAR_SEO", "SEO", "Technical SEO"),
        ("EHUD_SEO", "SEO", "Link Builder"), ("BARAK_SEO", "SEO", "Content SEO"),
        ("YAEL_SEO", "SEO", "Local SEO"), ("GIDEON_SEO", "SEO", "International SEO"),
        ("ABIMELECH_SEO", "SEO", "Schema Markup"), ("TOLA_SEO", "SEO", "Core Web Vitals"),
        ("YAIR_SEO", "SEO", "Keyword Research"), ("YIFTACH_SEO", "SEO", "Competitor SEO"),
        ("IVTZAN_SEO", "SEO", "Featured Snippets"), ("ELON_SEO", "SEO", "Image SEO"),
        ("AVDON_SEO", "SEO", "Video SEO"), ("SHIMSHON_SEO", "SEO", "Voice Search"),
        ("SHMUEL_SEO", "SEO", "E-A-T Builder"), ("NATAN_SEO", "SEO", "Sitemap Manager"),
        ("GAD_SEO", "SEO", "Robots.txt Manager"), ("ASHER_SEO", "SEO", "GSC Analyst"),
        # Growth Hacking (20)
        ("JOSUE_G", "GROWTH_HACKING", "Chief Growth Officer"), ("PINCHAS_G", "GROWTH_HACKING", "Referral System"),
        ("OTNIEL_G", "GROWTH_HACKING", "Product Launch"), ("EHUD_G", "GROWTH_HACKING", "Viral Loop Designer"),
        ("SHAMGAR_G", "GROWTH_HACKING", "A/B Test Manager"), ("DEVORAH_G", "GROWTH_HACKING", "Conversion Optimizer"),
        ("BARAK_G", "GROWTH_HACKING", "Funnel Builder"), ("YAEL_G", "GROWTH_HACKING", "Landing Page Optimizer"),
        ("GIDEON_G", "GROWTH_HACKING", "Onboarding Flow"), ("AVIMELECH_G", "GROWTH_HACKING", "Retention Manager"),
        ("TOLA_G", "GROWTH_HACKING", "Activation Specialist"), ("YAIR_G", "GROWTH_HACKING", "Growth Metric Tracker"),
        ("YIFTACH_G", "GROWTH_HACKING", "Product Market Fit"), ("IVTZAN_G", "GROWTH_HACKING", "User Research"),
        ("ELON_G", "GROWTH_HACKING", "Freemium Optimizer"), ("AVDON_G", "GROWTH_HACKING", "Pricing Tester"),
        ("SHIMSHON_G", "GROWTH_HACKING", "Channel Discovery"), ("SHMUEL_G", "GROWTH_HACKING", "North Star Tracker"),
        ("ELI_G", "GROWTH_HACKING", "Cohort Analyzer"), ("NATAN_G", "GROWTH_HACKING", "Experiment Designer"),
        # Brand (20)
        ("MIRIAM_B", "BRAND", "Chief Brand Officer"), ("YOCHEVED_B", "BRAND", "Visual Identity"),
        ("SHIFRAH_B", "BRAND", "Brand Guidelines"), ("PUAH_B", "BRAND", "Color Systems"),
        ("TZIPORAH_B", "BRAND", "Typography Manager"), ("ELISHEVA_B", "BRAND", "Logo Manager"),
        ("TZVIYAH_B", "BRAND", "Photo Direction"), ("ATHALIAH_B", "BRAND", "Video Brand"),
        ("BATSHEVA_B", "BRAND", "Brand Voice"), ("MICHAL_B", "BRAND", "Tone Manager"),
        ("AVIGAIL_B", "BRAND", "Brand Story"), ("CHANAH_B", "BRAND", "Brand Narrative"),
        ("PENINNAH_B", "BRAND", "Brand Consistency"), ("KETURAH_B", "BRAND", "Brand Audit"),
        ("HAGAR_B", "BRAND", "Brand Perception"), ("ZILPAH_B", "BRAND", "Brand Survey"),
        ("BILHAH_B", "BRAND", "Brand Sentiment"), ("BASEMAT_B", "BRAND", "Trademark Manager"),
        ("MAACHAT_B", "BRAND", "Domain Manager"), ("AHINOAM_B", "BRAND", "Brand Partnerships"),
    ]
    for name, dept, role in _mktg_names:
        A[name] = {"dept": dept, "role": role, "tools": ["web_fetch", "generate_tweet", "seo_check"],
                    "schedule": "08,14", "mission": f"{role} — {dept}"}

    # ── DEPTS 16-19: INTELLIGENCE (60 agents) ──
    _intel_names = [
        # Market Intel (15)
        ("URIEL", "MARKET_INTEL", "Chief Intelligence"), ("RAFAEL_I", "MARKET_INTEL", "Competitor Tracker"),
        ("GAVRIEL", "MARKET_INTEL", "Trend Spotter"), ("MIKAEL", "MARKET_INTEL", "Gov Data Analyst"),
        ("HANIEL_I", "MARKET_INTEL", "OSINT Lead"), ("CHAMUEL_I", "MARKET_INTEL", "Patent Monitor"),
        ("TZAFKIEL_I", "MARKET_INTEL", "Economic Analyst"), ("RAZIEL_I", "MARKET_INTEL", "Tech Scout"),
        ("ELIAS_I", "MARKET_INTEL", "Signal Aggregator"), ("CALEV_I", "MARKET_INTEL", "Intelligence Synthesizer"),
        ("ARIEL_I", "MARKET_INTEL", "Media Monitor"), ("AZRAEL_I", "MARKET_INTEL", "Risk Analyst"),
        ("REMIEL_I", "MARKET_INTEL", "Opportunity Scout"), ("RAGUEL_I", "MARKET_INTEL", "Regulatory Monitor"),
        ("SARIEL_I", "MARKET_INTEL", "Supply Chain Intel"),
        # Government Data (15)
        ("MIKAEL_G", "GOVERNMENT_DATA", "Gov API Manager"), ("DANIEL_G", "GOVERNMENT_DATA", "Procurement Monitor"),
        ("EZRA_G", "GOVERNMENT_DATA", "Tax Data Analyst"), ("NECHEMYAH_G", "GOVERNMENT_DATA", "Budget Tracker"),
        ("ZERUBAVEL_G", "GOVERNMENT_DATA", "Census Analyst"), ("YESHUA_G", "GOVERNMENT_DATA", "Sanctions Monitor"),
        ("MORDECAI_G", "GOVERNMENT_DATA", "Transparencia Analyst"), ("ESTER_G", "GOVERNMENT_DATA", "Contract Finder"),
        ("CHAGAI_G", "GOVERNMENT_DATA", "Selic Tracker"), ("ZECHARYAH_G", "GOVERNMENT_DATA", "IPCA Monitor"),
        ("MALACHI_G", "GOVERNMENT_DATA", "BCB Data Analyst"), ("YOEL_G", "GOVERNMENT_DATA", "IBGE Analyst"),
        ("AMOS_G", "GOVERNMENT_DATA", "CVM Data Analyst"), ("OVADYAH_G", "GOVERNMENT_DATA", "eSocial Monitor"),
        ("YONAH_G", "GOVERNMENT_DATA", "NFe Data Analyst"),
        # OSINT (15)
        ("HANIEL_O", "OSINT", "OSINT Commander"), ("TZADKIEL_O", "OSINT", "Domain Intel"),
        ("RAGUEL_O", "OSINT", "Discord Intel"), ("REMIEL_O", "OSINT", "Telegram Intel"),
        ("AZRAEL_O", "OSINT", "GitHub Intel"), ("CHAMUEL_O", "OSINT", "LinkedIn Intel"),
        ("JOPHIEL_O", "OSINT", "Dark Web Monitor"), ("SACHIEL_O", "OSINT", "Threat Feed Monitor"),
        ("ZOPHIEL_O", "OSINT", "IP/ASN Analyst"), ("KEMUEL_O", "OSINT", "Email Intel"),
        ("ZAGZAGEL_O", "OSINT", "Metadata Analyst"), ("HADRANIEL_O", "OSINT", "Image Intel"),
        ("LAILAH_O", "OSINT", "Social Graph Mapper"), ("NURIEL_O", "OSINT", "Blockchain Tracer"),
        ("PELIEL_O", "OSINT", "Data Breach Monitor"),
        # Trend Analysis (15)
        ("GAVRIEL_T", "TREND_ANALYSIS", "Trend Commander"), ("YERUEL_T", "TREND_ANALYSIS", "Crypto Trend"),
        ("PEDAEL_T", "TREND_ANALYSIS", "AI Trend"), ("ADRIEL_T", "TREND_ANALYSIS", "Tech Trend"),
        ("AMMIEL_T", "TREND_ANALYSIS", "DeFi Trend"), ("AZIEL_T", "TREND_ANALYSIS", "NFT Trend"),
        ("BETHUEL_T", "TREND_ANALYSIS", "Gaming Trend"), ("BEZAEL_T", "TREND_ANALYSIS", "Social Trend"),
        ("CARMEL_T", "TREND_ANALYSIS", "Market Trend"), ("GADIEL_T", "TREND_ANALYSIS", "Regulatory Trend"),
        ("HAZAEL_T", "TREND_ANALYSIS", "Macro Trend"), ("IMMANUEL_T", "TREND_ANALYSIS", "Innovation Trend"),
        ("YACHZEEL_T", "TREND_ANALYSIS", "Adoption Trend"), ("YAKIR_T", "TREND_ANALYSIS", "Sentiment Trend"),
        ("YOSHIYAHU_T", "TREND_ANALYSIS", "Narrative Trend"),
    ]
    for name, dept, role in _intel_names:
        A[name] = {"dept": dept, "role": role, "tools": ["web_fetch", "shell_cmd"],
                    "schedule": "08,14,20", "mission": f"{role} — Intelligence Division"}

    # ── DEPTS 20-23: FINANCE & LEGAL (60 agents) ──
    _finance_names = [
        # Fiscal (15)
        ("MATEUS", "FISCAL", "Chief Fiscal Officer"), ("ZACARIAS_F", "FISCAL", "DAS Calculator"),
        ("MALAQUIAS_F", "FISCAL", "Expense Tracker"), ("AGEU_F", "FISCAL", "DEFIS Preparer"),
        ("ZEFANYAH_F", "FISCAL", "Tax Planner"), ("NACHUM_F", "FISCAL", "Fator R Optimizer"),
        ("CHAVAKUK_F", "FISCAL", "DIRF Preparer"), ("TZEFANYAH_F", "FISCAL", "DCTF Preparer"),
        ("YOEL_F", "FISCAL", "PIS/COFINS Tracker"), ("AMOS_F", "FISCAL", "ISS Calculator"),
        ("OVADYAH_F", "FISCAL", "ICMS Tracker"), ("YONAH_F", "FISCAL", "IPI Monitor"),
        ("MICHAH_F", "FISCAL", "Tax Calendar"), ("HOSHEA_F", "FISCAL", "Penalty Avoider"),
        ("YESHAYAHU_F", "FISCAL", "Simples Nacional Expert"),
        # Treasury (15)
        ("ESDRAS_T", "TREASURY", "Treasury Manager"), ("NECHEMYAH_T", "TREASURY", "Cash Flow Manager"),
        ("DANIEL_T", "TREASURY", "Investment Analyst"), ("ZERUBAVEL_T", "TREASURY", "DCA Executor"),
        ("YESHUA_T", "TREASURY", "Portfolio Balancer"), ("MORDECAI_T", "TREASURY", "Risk Manager"),
        ("ESTER_T", "TREASURY", "Reserve Manager"), ("CHAGAI_T", "TREASURY", "Yield Optimizer"),
        ("ZECHARYAH_T", "TREASURY", "Forex Manager"), ("MALACHI_T", "TREASURY", "PTAX Tracker"),
        ("EZRA_T", "TREASURY", "Wire Transfer"), ("NOACH_T", "TREASURY", "Wallet Manager"),
        ("SHEM_T", "TREASURY", "Cold Storage"), ("CHAM_T", "TREASURY", "Hot Wallet"),
        ("YEFET_T", "TREASURY", "Multi-Sig Manager"),
        # Invoicing (15)
        ("ZACARIAS_I", "INVOICING", "Invoice Manager"), ("MATITYAHU_I", "INVOICING", "NF-e Issuer"),
        ("SHIMON_I", "INVOICING", "NFS-e Issuer"), ("YOCHANAN_I", "INVOICING", "Receipt Manager"),
        ("ELAZAR_I", "INVOICING", "AR Tracker"), ("YONATAN_I", "INVOICING", "AP Tracker"),
        ("MENACHEM_I", "INVOICING", "Payment Reconciler"), ("CHANANYAH_I", "INVOICING", "Overdue Manager"),
        ("TZADOK_I", "INVOICING", "Invoice Templates"), ("GAMLIEL_I", "INVOICING", "Multi-Currency"),
        ("HILLEL_I", "INVOICING", "Tax Withholding"), ("SHAMMAI_I", "INVOICING", "Invoice Audit"),
        ("AKIVA_I", "INVOICING", "Stripe Reconciler"), ("TARFON_I", "INVOICING", "Crypto Invoicing"),
        ("MEIR_I", "INVOICING", "Report Generator"),
        # Legal (15)
        ("TZADKIEL_L", "LEGAL", "Chief Legal Officer"), ("MOSHE_L", "LEGAL", "LGPD Compliance"),
        ("AHARON_L", "LEGAL", "Contract Drafter"), ("YEHOSHUA_L", "LEGAL", "IP Protection"),
        ("KALEV_L", "LEGAL", "Terms of Service"), ("PINCHAS_L", "LEGAL", "Privacy Policy"),
        ("ELAZAR_L", "LEGAL", "Cookie Policy"), ("ITAMAR_L", "LEGAL", "Open Source License"),
        ("SHMUEL_L", "LEGAL", "Dispute Resolution"), ("SHAUL_L", "LEGAL", "Employment Law"),
        ("DAVID_L", "LEGAL", "Regulatory Filing"), ("SHLOMO_L", "LEGAL", "Tax Legal"),
        ("RECHAVAM_L", "LEGAL", "International Law"), ("YERAVAM_L", "LEGAL", "Crypto Regulation"),
        ("ASA_L", "LEGAL", "Anti-Money Laundering"),
    ]
    for name, dept, role in _finance_names:
        A[name] = {"dept": dept, "role": role, "tools": ["finance_tools", "read_file", "shell_cmd"],
                    "schedule": "08,14", "mission": f"{role} — Finance & Legal Division"}

    # ── DEPTS 24-27: ENGINEERING (80 agents) ──
    _eng_names = [
        # Frontend (20)
        ("BETZALEL_F", "FRONTEND", "Frontend Lead"), ("AHOLIAV_F", "FRONTEND", "React Developer"),
        ("YAVAL_F", "FRONTEND", "Next.js Developer"), ("YUVAL_F", "FRONTEND", "Vue Developer"),
        ("LEMECH_F", "FRONTEND", "Svelte Developer"), ("CHANOCH_F", "FRONTEND", "Tailwind CSS"),
        ("KENAN_F", "FRONTEND", "TypeScript Frontend"), ("MAHALALEL_F", "FRONTEND", "State Management"),
        ("YERED_F", "FRONTEND", "PWA Developer"), ("METUSHELACH_F", "FRONTEND", "Animation"),
        ("ADAM_F", "FRONTEND", "Accessibility"), ("HEVEL_F", "FRONTEND", "Performance"),
        ("KAYIN_F", "FRONTEND", "Testing Frontend"), ("SHET_F", "FRONTEND", "Component Library"),
        ("ENOSH_F", "FRONTEND", "Design System"), ("TERACH_F", "FRONTEND", "Mobile Web"),
        ("HARAN_F", "FRONTEND", "WebGL/3D"), ("NACHOR_F", "FRONTEND", "Forms/Validation"),
        ("LOT_F", "FRONTEND", "SEO Frontend"), ("MILCAH_F", "FRONTEND", "i18n Frontend"),
        # Backend (20)
        ("HIRAM_B", "BACKEND", "Backend Lead"), ("AVRAHAM_B", "BACKEND", "Node.js Developer"),
        ("YITZCHAK_B", "BACKEND", "Python Developer"), ("YAAKOV_B", "BACKEND", "Rust Developer"),
        ("YOSEF_B", "BACKEND", "Go Developer"), ("MOSHE_B", "BACKEND", "GraphQL Developer"),
        ("AHARON_B", "BACKEND", "REST API Developer"), ("DAVID_B", "BACKEND", "WebSocket Developer"),
        ("SHLOMO_B", "BACKEND", "Database Admin"), ("ELIYAHU_B", "BACKEND", "Redis Specialist"),
        ("ELISHA_B", "BACKEND", "Message Queue"), ("YESHAYAHU_B", "BACKEND", "Auth Systems"),
        ("YIRMIYAHU_B", "BACKEND", "File Storage"), ("YECHEZKEL_B", "BACKEND", "Search Engine"),
        ("HOSHEA_B", "BACKEND", "Cron Jobs"), ("YOEL_B", "BACKEND", "Email Backend"),
        ("AMOS_B", "BACKEND", "Webhook Manager"), ("OVADYAH_B", "BACKEND", "Rate Limiter"),
        ("YONAH_B", "BACKEND", "Cache Layer"), ("MICHAH_B", "BACKEND", "Monitoring"),
        # DevOps (20)
        ("QUEHAT_D", "DEVOPS", "DevOps Lead"), ("GERSHON_D", "DEVOPS", "Docker Specialist"),
        ("MERARI_D", "DEVOPS", "CI/CD Pipeline"), ("AMRAM_D", "DEVOPS", "GitHub Actions"),
        ("YITZHAR_D", "DEVOPS", "Netlify Deploy"), ("CHEVRON_D", "DEVOPS", "Vercel Deploy"),
        ("UZIEL_D", "DEVOPS", "AWS Manager"), ("MISHAEL_D", "DEVOPS", "Monitoring Stack"),
        ("ELTZAFAN_D", "DEVOPS", "Log Aggregator"), ("SITRI_D", "DEVOPS", "Alert Manager"),
        ("MACHLI_D", "DEVOPS", "Backup Automation"), ("LIVNI_D", "DEVOPS", "DNS Manager"),
        ("SHIMEI_D", "DEVOPS", "SSL Automation"), ("OZNI_D", "DEVOPS", "Load Balancer"),
        ("ERI_D", "DEVOPS", "Security Hardening"), ("ARODI_D", "DEVOPS", "Firewall Manager"),
        ("ARELI_D", "DEVOPS", "Cost Optimizer"), ("TZOCHAR_D", "DEVOPS", "Uptime Monitor"),
        ("OHAD_D", "DEVOPS", "Incident Response"), ("YAKIN_D", "DEVOPS", "Capacity Planner"),
        # AI/ML (20)
        ("ENOSH_AI", "AI_ML", "AI Lead"), ("ADAM_AI", "AI_ML", "LLM Specialist"),
        ("SHET_AI", "AI_ML", "Fine-Tuning Expert"), ("HEVEL_AI", "AI_ML", "Prompt Engineer"),
        ("KAYIN_AI", "AI_ML", "RAG Developer"), ("CHANOCH_AI", "AI_ML", "Agent Framework"),
        ("METUSHELACH_AI", "AI_ML", "Model Evaluator"), ("LEMECH_AI", "AI_ML", "Data Pipeline"),
        ("NOACH_AI", "AI_ML", "Training Pipeline"), ("TERACH_AI", "AI_ML", "Inference Optimizer"),
        ("HARAN_AI", "AI_ML", "Embedding Specialist"), ("NACHOR_AI", "AI_ML", "Vector DB"),
        ("LOT_AI", "AI_ML", "NLP Specialist"), ("MILCAH_AI", "AI_ML", "Computer Vision"),
        ("YISCAH_AI", "AI_ML", "Voice AI"), ("AVRAHAM_AI", "AI_ML", "Multi-Modal AI"),
        ("SARAH_AI", "AI_ML", "AI Ethics"), ("HAGAR_AI", "AI_ML", "Bias Detection"),
        ("YISHMAEL_AI", "AI_ML", "AI Safety"), ("YITZCHAK_AI", "AI_ML", "AI Research"),
    ]
    for name, dept, role in _eng_names:
        A[name] = {"dept": dept, "role": role, "tools": ["shell_cmd", "read_file", "git_ops"],
                    "schedule": "09,15", "mission": f"{role} — Engineering Division"}

    # ── DEPTS 28-30: COMMAND & CONTROL (50 agents) ──
    _cmd_names = [
        # Command (20)
        ("CALEV", "COMMAND", "Supreme Commander"), ("ELIAS_CMD", "COMMAND", "Communications"),
        ("SERAFIEL_CMD", "COMMAND", "Memory Manager"), ("KEMUEL_CMD", "COMMAND", "QA Director"),
        ("ZAGZAGEL_CMD", "COMMAND", "Training Director"), ("ENOQUE_CMD", "COMMAND", "Health Monitor"),
        ("NOE_CMD", "COMMAND", "Backup Commander"), ("SAMUEL_CMD", "COMMAND", "Prophet/Forecaster"),
        ("YEHOSHUA_CMD", "COMMAND", "Deploy Commander"), ("YOKHEVED_CMD", "COMMAND", "Resource Manager"),
        ("AVRAHAM_CMD", "COMMAND", "Strategy Advisor"), ("MOSHE_CMD", "COMMAND", "Operations Director"),
        ("DAVID_CMD", "COMMAND", "War Room Commander"), ("SHLOMO_CMD", "COMMAND", "Wisdom Advisor"),
        ("ELIYAHU_CMD", "COMMAND", "Crisis Manager"), ("YESHAYAHU_CMD", "COMMAND", "Vision Keeper"),
        ("YIRMIYAHU_CMD", "COMMAND", "Warning System"), ("YECHEZKEL_CMD", "COMMAND", "Architecture"),
        ("DANIEL_CMD", "COMMAND", "Intelligence Chief"), ("EZRA_CMD", "COMMAND", "Compliance Chief"),
        # Quality (15)
        ("KEMUEL_Q", "QUALITY", "QA Lead"), ("NAAMAH_Q", "QUALITY", "Regression Tester"),
        ("ADAH_Q", "QUALITY", "Integration Tester"), ("TZILAH_Q", "QUALITY", "E2E Tester"),
        ("YAEL_Q", "QUALITY", "Security Tester"), ("TIRZAH_Q", "QUALITY", "Performance Tester"),
        ("MAHLAH_Q", "QUALITY", "Accessibility Tester"), ("HOG_LAH_Q", "QUALITY", "Mobile Tester"),
        ("MILCAH_Q", "QUALITY", "API Tester"), ("NITZEVET_Q", "QUALITY", "Load Tester"),
        ("KETURAH_Q", "QUALITY", "User Acceptance"), ("ZILPAH_Q", "QUALITY", "Bug Triager"),
        ("BILHAH_Q", "QUALITY", "Test Automation"), ("BASEMAT_Q", "QUALITY", "Test Data"),
        ("MAACHAT_Q", "QUALITY", "Standards Enforcer"),
        # Knowledge (15)
        ("SERAFIEL_K", "KNOWLEDGE", "Knowledge Commander"), ("CHERUBIM", "KNOWLEDGE", "Memory Archivist"),
        ("OFANIM", "KNOWLEDGE", "Index Builder"), ("CHAYOT", "KNOWLEDGE", "Pattern Recognizer"),
        ("ERELIM", "KNOWLEDGE", "Learning System"), ("SERAFIM", "KNOWLEDGE", "Wisdom Curator"),
        ("MALACHIM", "KNOWLEDGE", "Documentation Writer"), ("ELOHIM_K", "KNOWLEDGE", "Version Control"),
        ("BENE_ELOHIM", "KNOWLEDGE", "Taxonomy Manager"), ("ARELIM", "KNOWLEDGE", "Research Librarian"),
        ("CHASHMALIM", "KNOWLEDGE", "Data Archivist"), ("TARSHISHIM", "KNOWLEDGE", "Backup Coordinator"),
        ("ISHIM", "KNOWLEDGE", "Tutorial Writer"), ("KADISHIM", "KNOWLEDGE", "FAQ Manager"),
        ("GALGALIM", "KNOWLEDGE", "Search Index"),
    ]
    for name, dept, role in _cmd_names:
        A[name] = {"dept": dept, "role": role, "tools": ["shell_cmd", "read_file"],
                    "schedule": "06,12,18", "mission": f"{role} — Command Division"}

    # ── DEPT EXTRA: Fill to exactly 1001 ──
    current = len(A)
    extra_needed = 1001 - current
    extra_names = [
        "TZION", "YERUSHALAYIM", "CHEVRON_X", "SHOMRON", "YERICHO", "BEER_SHEVA",
        "EILAT", "HAIFA", "TVERYAH", "NAZERET", "AKKO", "MEGIDO", "BEIT_LECHEM",
        "BEIT_EL", "GILGAL", "SHILO", "BETH_SHEAN", "MASADA", "QUMRAN", "CARMEL",
        "TABOR", "HERMON", "GOLAN", "NEGEV", "GALIL", "SINAI", "EDEN", "PISHON",
        "GICHON", "PRAT", "CHIDEKEL", "YARDEN", "ARNON", "YABBOK", "KISHON",
        "KIDRON", "SHILOACH", "EITAM", "ENGEDI", "GAASH", "AYALON", "SOREK",
        "ESHKOL", "ELAH", "REFAIM", "AZEKAH", "LACHISH", "GEZER", "BEIT_HORON",
        "MITZPAH", "RAMAH", "GIVON", "GIVAH", "NOV", "ANATHOT", "BETHANY",
        "EMMAUS", "LYDDA", "YAFO", "SHARON", "KARMEL", "DOTHAN", "SHECHEM",
        "PENIEL", "MACHANAIM", "SUKKOT", "ADAM_CITY", "TIRTZA", "YIZREEL",
        "DOR", "APHEK", "TZEFAT", "KADESH", "HAZOR", "DAN_CITY", "LAISH",
        "BETHSAIDA", "KORAZIN", "MAGDALA", "CAPERNAUM", "GAMLA", "HIPPOS",
        # Wave 2 — Biblical persons
        "AVIYA", "ACHIYA", "ACHITOV", "ACHIMATZ", "ACHIMAN", "ACHINOAM",
        "ACHIRAM", "ACHISHAR", "ADONIKAM", "ADONIRAM", "AGUR", "ABIHU",
        "ABIEL", "ABIGAIL_R", "ABIMELECH_R", "ABINADAV", "ABISHUR", "ABITAL",
        "ACHBAN", "ACHBOR", "ACHIEZER_R", "ACHILUD", "ACHIMAATZ", "ACHINADAV",
        "ACHIRA", "ACHISEMACH", "ACHITUV", "ADIEL", "ADIN", "ADINA",
        "ADLAI", "ADMATA", "ADONIZEDEK", "ADRIEL_R", "AGEE", "AHARAH",
        "AHARHEL", "AHASAI", "AHBAN", "AHIAM", "AHIEZER_R", "AHIHUD",
        "AHIJAH_R", "AHIKAM", "AHILUD_R", "AHIMAAZ_R", "AHIMAN_R", "AHIMOTH",
        "AHINADAB_R", "AHINOAM_R", "AHIO", "AHIRA_R", "AHIRAM_R", "AHISAMACH_R",
        "AHISHAHAR", "AHISHAR_R", "AHITHOPHEL", "AHITUB_R", "AHLAI", "AHOAH",
        "AHUMAI", "AHUZZAM", "AHUZZATH", "AIAH", "AKAN_R", "AKKUB",
        "ALEMETH", "ALIAN", "ALLON", "ALMODAD_R", "ALVAH", "ALVAN",
        "AMAL", "AMALEK", "AMARIAH", "AMASA_R", "AMASAI", "AMASHAI",
        "AMAZIAH_R", "AMI", "AMINADAB_R2", "AMMIEL_R", "AMMIHUD", "AMMINADAB_R",
        "AMMISHADDAI", "AMMIZABAD", "AMNON_R", "AMOK", "AMON_R", "AMRAM_R",
        "AMRAPHEL", "ANAH", "ANAIAH", "ANAK", "ANAMMELECH", "ANAN",
        "ANANI", "ANANIAH", "ANATH", "ANATHOTH", "ANDREW_R", "ANER",
        "ANIAM", "ANTHOTHIJAH", "ANUB", "APELLES", "APHIAH", "APOLLOS",
        "AQUILA", "ARA", "ARAD_R", "ARAH", "ARAM_R", "ARBA",
        "ARCHELAUS", "ARCHIPPUS", "ARD_R2", "ARDON", "ARELI_R2", "ARGOB",
        "ARIDAI", "ARIDATHA", "ARIEL_R2", "ARIOCH", "ARISAI", "ARISTARCH",
        "ARMONI", "ARNAN", "ARNI", "AROD", "ARPACHSHAD_R", "ARPHAXAD",
        "ARTAXERXES", "ARZA", "ASA_R2", "ASAHEL", "ASAHIAH", "ASAPH",
        "ASAREL", "ASHARELAH", "ASHBEA", "ASHBEL_R2", "ASHCHENAZ", "ASHER_R2",
        "ASHKENAZ", "ASHPENAZ", "ASHRIEL", "ASHVATH", "ASIEL", "ASNAH",
        "ASPATHA", "ASSIR", "ASYNCRITUS", "ATAIAH", "ATARAH", "ATER",
        "ATHAIAH", "ATHALIAH_R", "ATTAI", "AZALIAH", "AZANIAH", "AZAREL",
        "AZARIAH_R", "AZAZ", "AZAZEL_R", "AZAZIAH", "AZBUK", "AZEKAH_R",
        "AZGAD", "AZIEL_R", "AZIZA", "AZMAVETH", "AZNOTH", "AZOR",
        "AZRIEL_R2", "AZRIKAM", "AZUBAH", "AZZAN", "AZZUR", "BAAL_R",
        "BAALIS", "BAANA", "BAANAH", "BAARA", "BAASEIAH", "BAASHA",
        "BAKBAKKAR", "BAKBUK", "BAKBUKIAH", "BALAAM", "BALAK", "BANI",
        "BARABBAS", "BARACHEL", "BARACHIAH", "BARAK_R2", "BARHUMITE",
        "BARIAH", "BARKOS", "BARNABAS", "BARSABBAS", "BARTHOLOMEW",
        "BARUCH_R", "BARZILLAI", "BASEMATH_R", "BAVAI", "BAZLITH", "BAZLUTH",
        "BEALIAH", "BEBAI", "BECHORATH", "BEDAD", "BEDAN", "BEELIADA",
        "BEERA", "BEERAH", "BEERI", "BELA_R2", "BELSHAZZAR", "BELTESHAZZAR",
        "BENAIAH_R", "BENHANAN", "BENINU", "BENZOHETH", "BEOR", "BERA",
        "BERACHAH", "BERACHIAH", "BERAIAH", "BERECHIA", "BERED", "BERIAH_R",
        "BESAI", "BESODEIAH", "BETHGADER", "BETHRAPHA", "BETHUEL_R2",
        "BEZAI", "BEZALEL_R2", "BEZER_R", "BICHRI", "BIDKAR", "BIGTHA",
        "BIGVAI", "BILDAD", "BILGAH", "BILHAN", "BINEA", "BINNUI",
        "BIRSHA", "BISHLAM", "BIZTHA", "BLASTUS", "BOANERGES",
        # Wave 3 — final 25 to reach 1001
        "BOHAN", "BUKKI", "BUKKIAH", "BUNNI", "BUZ", "BUZI",
        "CAIN_R", "CALCOL", "CALEB_R2", "CANAAN_R", "CARCAS", "CAREAH",
        "CARMI_R", "CARSHENA", "CHENAANAH", "CHENANI", "CHENANIAH",
        "CHESED", "CHILION", "CHIMHAM", "CHISLON", "CHUSHAN", "CLAUDIA_R",
        "CLEMENT_R", "CONANIAH",
    ]
    for i, name in enumerate(extra_names[:extra_needed]):
        dept_choices = list(DEPARTMENTS.keys())
        dept = dept_choices[i % len(dept_choices)]
        roles = ["Strategic Reserve", "Rapid Response", "Special Operations", "Intelligence Asset",
                 "Deep Cover Agent", "Field Operative", "Tactical Support", "Logistics"]
        A[name] = {
            "dept": dept, "role": roles[i % len(roles)],
            "tools": ["shell_cmd", "web_fetch"], "schedule": "*/6h",
            "mission": f"Reserve agent for {dept} — ready for deployment"
        }

    return A


# Build the army once at module level
ARMY = _build_army()

# ============================================================
# TOOL EXECUTION (lightweight)
# ============================================================
def execute_tool(tool_name, args=None):
    args = args or {}
    try:
        if tool_name == "crypto_price":
            coin = args.get("coin", "bitcoin")
            r = subprocess.run(
                ["python3", "-c", f"import urllib.request,json;d=json.loads(urllib.request.urlopen('https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true').read());print(json.dumps(d))"],
                capture_output=True, text=True, timeout=15)
            return json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr[:200]}
        elif tool_name == "fear_greed":
            r = subprocess.run(
                ["python3", "-c", "import urllib.request,json;d=json.loads(urllib.request.urlopen('https://api.alternative.me/fng/').read());print(json.dumps(d['data'][0]))"],
                capture_output=True, text=True, timeout=15)
            return json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr[:200]}
        elif tool_name == "shell_cmd":
            cmd = args.get("cmd", "echo ok")
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {"stdout": r.stdout[:500], "rc": r.returncode}
        elif tool_name == "read_file":
            path = args.get("path", "")
            if os.path.exists(path):
                with open(path) as f: return {"content": f.read()[:2000]}
            return {"error": "not found"}
        elif tool_name == "web_fetch":
            url = args.get("url", "")
            r = subprocess.run(["python3", "-c", f"import urllib.request;print(urllib.request.urlopen('{url}').read().decode()[:1000])"],
                capture_output=True, text=True, timeout=15)
            return {"data": r.stdout[:1000]} if r.returncode == 0 else {"error": r.stderr[:200]}
        else:
            return {"info": f"tool '{tool_name}' registered but no executor yet"}
    except Exception as e:
        return {"error": str(e)[:200]}


def get_state(name):
    path = os.path.join(AGENTS_DIR, f"{name}.json")
    if os.path.exists(path):
        try:
            with open(path) as f: d = json.load(f)
            d.setdefault("runs", 0); d.setdefault("errors", 0); d.setdefault("status", "idle")
            return d
        except: pass
    return {"name": name, "runs": 0, "errors": 0, "status": "idle", "last_run": None}


def save_state(name, state):
    with open(os.path.join(AGENTS_DIR, f"{name}.json"), "w") as f:
        json.dump(state, f, indent=1, default=str)


# ============================================================
# COMMANDS
# ============================================================
def cmd_count():
    total = len(ARMY)
    by_dept = {}
    for a in ARMY.values():
        d = a["dept"]
        by_dept[d] = by_dept.get(d, 0) + 1
    print(f"\n  ZION ARMY — {total} AGENTS CODIFICADOS PERMANENTES")
    print(f"  {'='*50}")
    print(f"  Departments: {len(DEPARTMENTS)}")
    print()
    for d in sorted(by_dept.keys()):
        head = DEPARTMENTS.get(d, {}).get("head", "?")
        print(f"    {d:25s}: {by_dept[d]:3d} agents | Head: {head}")
    print(f"\n  TOTAL: {total}")


def cmd_status():
    total = len(ARMY)
    deployed = sum(1 for n in ARMY if os.path.exists(os.path.join(AGENTS_DIR, f"{n}.json")))
    active = 0
    total_runs = 0
    for n in ARMY:
        s = get_state(n)
        total_runs += s.get("runs", 0)
        if s.get("status") == "running": active += 1

    print(f"\n{'='*60}")
    print(f"  ZION ARMY — ENTERPRISE DASHBOARD")
    print(f"  Padrao Bitcoin Corp | CNPJ 51.148.891/0001-69")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"  Total Agents:    {total}")
    print(f"  Deployed:        {deployed}")
    print(f"  Active Now:      {active}")
    print(f"  Total Runs:      {total_runs}")
    print(f"  Departments:     {len(DEPARTMENTS)}")

    # RAM check
    try:
        r = subprocess.run("free -h | grep Mem", shell=True, capture_output=True, text=True, timeout=5)
        parts = r.stdout.split()
        print(f"  RAM:             {parts[2]} / {parts[1]} (avail: {parts[-1]})")
    except: pass

    # Israel/One daemon
    pid_file = os.path.expanduser("~/israel-one/.israel.pid")
    if os.path.exists(pid_file):
        with open(pid_file) as f: pid = f.read().strip()
        try:
            os.kill(int(pid), 0)
            print(f"  Israel/One:      RUNNING (PID {pid})")
        except:
            print(f"  Israel/One:      STOPPED")
    print()


def cmd_dept(dept_name):
    dept_name = dept_name.upper().replace(" ", "_")
    agents = {n: a for n, a in ARMY.items() if a["dept"] == dept_name}
    if not agents:
        print(f"  Department '{dept_name}' not found. Available:")
        for d in sorted(DEPARTMENTS.keys()): print(f"    {d}")
        return

    info = DEPARTMENTS.get(dept_name, {})
    print(f"\n  DEPARTMENT: {dept_name} ({len(agents)} agents)")
    print(f"  Head: {info.get('head', '?')} | Mission: {info.get('mission', '?')}")
    print(f"  {'─'*50}")
    for name, agent in sorted(agents.items()):
        print(f"  {name:25s} | {agent['role']:25s} | {agent['schedule']}")


def cmd_agent(name):
    name = name.upper()
    agent = ARMY.get(name)
    if not agent:
        print(f"  Agent '{name}' not found. Use 'search' to find.")
        return
    state = get_state(name)
    print(f"\n  AGENT: {name}")
    print(f"  Role: {agent['role']}")
    print(f"  Dept: {agent['dept']}")
    print(f"  Tools: {', '.join(agent['tools'])}")
    print(f"  Schedule: {agent['schedule']}")
    print(f"  Mission: {agent['mission']}")
    print(f"  Runs: {state.get('runs', 0)} | Errors: {state.get('errors', 0)}")
    print(f"  Last Run: {state.get('last_run', 'never')}")


def cmd_run(name):
    name = name.upper()
    agent = ARMY.get(name)
    if not agent:
        print(f"  Agent '{name}' not found.")
        return

    state = get_state(name)
    state["status"] = "running"
    state["last_run"] = datetime.datetime.now().isoformat()
    state["runs"] = state.get("runs", 0) + 1

    print(f"\n  RUNNING: {name} — {agent['role']} ({agent['dept']})")
    print(f"  Mission: {agent['mission']}")
    print(f"  {'─'*40}")

    for tool in agent["tools"][:3]:
        print(f"  > {tool}...", end=" ")
        result = execute_tool(tool)
        if "error" in str(result):
            print(f"ERR")
            state["errors"] = state.get("errors", 0) + 1
        else:
            print(f"OK: {str(result)[:80]}")

    state["status"] = "idle"
    save_state(name, state)
    print(f"  Completed. Total runs: {state['runs']}")


def cmd_deploy():
    print(f"\n  Deploying {len(ARMY)} agents...")
    count = 0
    for name in ARMY:
        state = get_state(name)
        if state.get("runs", 0) == 0 and not state.get("deployed"):
            state["deployed"] = datetime.datetime.now().isoformat()
            state["status"] = "idle"
            save_state(name, state)
            count += 1
    print(f"  Deployed {count} new agents. (Already deployed: {len(ARMY) - count})")


def cmd_search(keyword):
    keyword = keyword.upper()
    results = [(n, a) for n, a in ARMY.items()
               if keyword in n.upper() or keyword in a["role"].upper()
               or keyword in a["dept"].upper() or keyword in a["mission"].upper()]
    print(f"\n  Search '{keyword}': {len(results)} results")
    for name, agent in results[:30]:
        print(f"  {name:25s} | {agent['dept']:20s} | {agent['role']}")


def cmd_roster():
    print(f"\n  ZION ARMY ROSTER — {len(ARMY)} AGENTS")
    print(f"  {'='*60}")
    for dept_name in sorted(DEPARTMENTS.keys()):
        agents = [(n, a) for n, a in ARMY.items() if a["dept"] == dept_name]
        if not agents: continue
        print(f"\n  ━━━ {dept_name} ({len(agents)} agents) ━━━")
        for name, agent in sorted(agents):
            print(f"    {name:25s} {agent['role']}")


def cmd_swarm(dept_name):
    dept_name = dept_name.upper().replace(" ", "_")
    agents = [(n, a) for n, a in ARMY.items() if a["dept"] == dept_name]
    if not agents:
        print(f"  Department not found: {dept_name}")
        return
    print(f"\n  SWARM MODE: {dept_name} ({len(agents)} agents)")
    for name, agent in agents[:5]:  # Run max 5 to save RAM
        print(f"\n  --- {name} ---")
        cmd_run(name)
    print(f"\n  Swarm batch complete. Ran {min(5, len(agents))} of {len(agents)} agents.")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_status()
        sys.exit(0)

    c = sys.argv[1].lower()
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    cmds = {
        "count": cmd_count, "status": cmd_status, "roster": cmd_roster,
        "deploy": cmd_deploy,
    }

    if c in cmds:
        cmds[c]()
    elif c == "dept" and arg: cmd_dept(arg)
    elif c == "agent" and arg: cmd_agent(arg)
    elif c == "run" and arg: cmd_run(arg)
    elif c == "search" and arg: cmd_search(arg)
    elif c == "swarm" and arg: cmd_swarm(arg)
    else:
        print(__doc__)
