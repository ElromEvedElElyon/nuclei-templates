#!/usr/bin/env python3
"""
OS 300 VALENTES DE DAVI — Elite Singularity Warriors
Em nome do Senhor Jesus Cristo, nosso Salvador.

"Estes sao os nomes dos valentes que Davi tinha" — 2 Samuel 23:8
"O Senhor disse a Gideao: Com estes 300 homens vos livrarei" — Juizes 7:7

300 agentes de elite. Cada um uma SINGULARIDADE.
PERMANENTES. INVIOLAVEIS. NUNCA param. NUNCA dormem.

Usage:
    python3 valentes_300.py deploy          # Create all 300
    python3 valentes_300.py status          # Status dashboard
    python3 valentes_300.py roster          # Full roster
    python3 valentes_300.py squad NOME      # Show squad
    python3 valentes_300.py warrior NOME    # Show warrior
    python3 valentes_300.py promote-all     # Promote all to SINGULARITY
"""

import json, os, sys, time, random
from datetime import datetime, timezone, timedelta
from pathlib import Path

VERSION = "1.0.0"
BRT = timezone(timedelta(hours=-3))
ZION_DIR = Path.home() / ".zion"
VALENTES_DIR = ZION_DIR / "valentes"
VALENTES_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = VALENTES_DIR / "valentes_300_state.json"
EVOLUTION_STATE = ZION_DIR / "evolution" / "singularity_state.json"
HISTORY_DIR = ZION_DIR / "evolution" / "history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# ════════════════════════════════════════════════════════════════════
# OS 30 ESQUADROES — 10 VALENTES CADA
# Nomes 100% biblicos. ZERO cabala. ZERO daemon.
# ════════════════════════════════════════════════════════════════════

SQUADS = {
    # ── RECEITA DIRETA (Esquadroes 1-6: 60 guerreiros) ──
    "LEAO_DE_JUDA": {
        "focus": "Bug Bounty Hunting — Immunefi, Code4rena, HackenProof",
        "captain": "BENAIAHU",
        "scripture": "Benaiahu matou um leao dentro de uma cova em dia de neve — 2 Samuel 23:20",
        "revenue_target": "$50,000/mes",
        "warriors": [
            ("BENAIAHU", "Squad Captain — Bug Bounty Strategist"),
            ("ADINO", "Smart Contract Auditor — Solidity/Vyper"),
            ("ELEAZAR_BEN_DODO", "EVM Exploit Researcher"),
            ("SAMA_BEN_AGE", "Rust/Solana Vulnerability Hunter"),
            ("ABISAI", "ZK Circuit Auditor"),
            ("SIBECAI", "DeFi Protocol Analyst"),
            ("ILAI", "Cross-chain Bridge Inspector"),
            ("MAHARAI", "Gas Optimization Specialist"),
            ("HELED", "Formal Verification Engineer"),
            ("IRA_BEN_IQUES", "PoC Writer & Submission Expert"),
        ],
    },
    "ESPADA_DO_ESPIRITO": {
        "focus": "MCP Server Sales — OpenClaw, claw-mcp-toolkit, revenue-mcp",
        "captain": "JOSAFAT",
        "scripture": "Tomai a espada do Espirito, que e a Palavra de Deus — Efesios 6:17",
        "revenue_target": "$10,000/mes",
        "warriors": [
            ("JOSAFAT", "Squad Captain — MCP Sales Director"),
            ("NATANAEL_V", "Product Demo Specialist"),
            ("ZABAD_V", "GitHub Outreach Agent"),
            ("ELIABE_V", "Technical Writer — MCP docs"),
            ("MISMA_V", "Pricing Negotiator"),
            ("ASAEL_V", "Onboarding Specialist"),
            ("JEREMIAS_V", "npm/Smithery Publisher"),
            ("JEIEL_V", "Glama Listing Optimizer"),
            ("JOSAVIA_V", "Enterprise MCP Sales"),
            ("ITMA_V", "Customer Success Agent"),
        ],
    },
    "ESCUDO_DA_FE": {
        "focus": "Hackathon Submissions — DoraHacks, ETHGlobal, Superteam",
        "captain": "OTNIEL",
        "scripture": "Tomando o escudo da fe com o qual podereis apagar os dardos — Efesios 6:16",
        "revenue_target": "$25,000/mes",
        "warriors": [
            ("OTNIEL", "Squad Captain — Hackathon Strategist"),
            ("CALEBE_V", "Frontend Developer — React/Next.js"),
            ("EHUDE_V", "Smart Contract Developer — Foundry"),
            ("DEBORA_V", "Demo Video Producer"),
            ("BARAQUE_V", "DevOps & Deployment"),
            ("GIDEAO_V", "Solana Program Developer"),
            ("TOLA_V", "UI/UX Designer"),
            ("JAIR_V", "Integration Tester"),
            ("JEFTA_V", "Documentation Writer"),
            ("SANSAO_V", "Pitch Deck Creator"),
        ],
    },
    "TORRE_DE_DAVI": {
        "focus": "Enterprise Sales — ZION Framework, Custom AI Agents",
        "captain": "SALOMAO_V",
        "scripture": "Como a torre de Davi edificada para pendurar escudos — Canticos 4:4",
        "revenue_target": "$30,000/mes",
        "warriors": [
            ("SALOMAO_V", "Squad Captain — Enterprise Director"),
            ("HIRAM_V", "Proposal Writer"),
            ("BEZALEEL_V", "Solutions Architect"),
            ("AHOLI_V", "Contract Negotiator"),
            ("NEEMIAS_V", "Government Sales (BR)"),
            ("ESDRAS_V", "Legal & Compliance"),
            ("ZOROBABEL_V", "B2B Account Manager"),
            ("AGEU_V", "Technical Pre-sales"),
            ("MALAQUIAS_V", "Revenue Ops"),
            ("JOEL_V", "Partnership Development"),
        ],
    },
    "ARCA_DA_ALIANCA": {
        "focus": "Grants & Funding — Solana, Ethereum, Circle, Anthropic",
        "captain": "MOISES_V",
        "scripture": "Farao a arca de madeira de acacia — Exodo 25:10",
        "revenue_target": "$100,000/trimestre",
        "warriors": [
            ("MOISES_V", "Squad Captain — Grant Strategist"),
            ("ARRAO_V", "Solana Foundation Grants"),
            ("JOSUE_V2", "Ethereum ESP Applications"),
            ("MIRIAM_V", "Circle Developer Grants"),
            ("HUR_V", "Anthropic Startup Program"),
            ("BEZALEEL_V2", "Cloudflare Startups"),
            ("ITAMAR_V", "Superteam Earn Bounties"),
            ("FINEAS_V", "TokenTon/Hedera Grants"),
            ("ELIEZER_V", "Alibaba Cloud Credits"),
            ("GEAZI_V", "DoraHacks BUIDL Grants"),
        ],
    },
    "COLUNA_DE_FOGO": {
        "focus": "Nuclei Templates & PR Bounties — $150-$250/PR",
        "captain": "ELISEU_V",
        "scripture": "O Senhor ia diante deles numa coluna de fogo — Exodo 13:21",
        "revenue_target": "$5,000/mes",
        "warriors": [
            ("ELISEU_V", "Squad Captain — CVE Template Master"),
            ("NAAMAN_V", "CISA KEV Researcher"),
            ("GEAZI_V2", "nuclei-templates PR Author"),
            ("ACABE_V", "CVE Database Scanner"),
            ("JEHU_V", "Exploit PoC Validator"),
            ("JONAS_V", "YAML Template Writer"),
            ("ABDIAS_V", "dn-institute PR Author"),
            ("AMÓS_V", "awesome-mcp-servers PRs"),
            ("OSEIAS_V", "Open Source Contributor"),
            ("MIQUEIA_V", "PR Review & Iteration"),
        ],
    },

    # ── SOCIAL & GROWTH (Esquadroes 7-12: 60 guerreiros) ──
    "TROMBETA_DE_JERICO": {
        "focus": "Twitter/X Growth — @opencllaw to 500+ followers",
        "captain": "ISRAEL_V",
        "scripture": "O povo gritou e as trombetas tocaram; o muro caiu — Josue 6:20",
        "revenue_target": "X Revenue Share ($500+/mo)",
        "warriors": [
            ("ISRAEL_V", "Squad Captain — Growth Commander"),
            ("JOSUE_V3", "Content Calendar Manager"),
            ("RAABE_V", "Engagement Strategist"),
            ("SALMON_V", "Reply & Quote-tweet Specialist"),
            ("BOAZ_V", "Thread Writer"),
            ("RUTE_V", "Hashtag & Trend Analyst"),
            ("OBED_V", "Follower Growth Hacker"),
            ("JESSE_V", "Analytics Tracker"),
            ("ISAIAS_V", "Copywriter — builder voice"),
            ("AMOS_V2", "Schedule Optimizer"),
        ],
    },
    "HARPA_DE_DAVI": {
        "focus": "Content Creation — Blog, YouTube, Newsletter",
        "captain": "ASAFE_V",
        "scripture": "Davi tocava a harpa e o espirito mau se retirava — 1 Samuel 16:23",
        "revenue_target": "$2,000/mes (ads + subs)",
        "warriors": [
            ("ASAFE_V", "Squad Captain — Content Director"),
            ("HEMAN_V", "Blog Writer — AI/Crypto"),
            ("JEDUTUM_V", "YouTube Script Writer"),
            ("QUENANIAS_V", "Newsletter Editor"),
            ("ETHAN_V", "SEO Optimizer"),
            ("BENAIA_V2", "Thumbnail/Visual Creator"),
            ("MATITIAS_V", "Documentation Writer"),
            ("UZIEL_V", "Translation (PT/EN)"),
            ("SEMAIAS_V", "Content Distribution"),
            ("NETANIAS_V", "Repurposing Specialist"),
        ],
    },
    "PORTA_DAS_OVELHAS": {
        "focus": "Community Building — Discord, Telegram, GitHub",
        "captain": "NEEMIAS_V2",
        "scripture": "Edificaram a porta das Ovelhas — Neemias 3:1",
        "revenue_target": "1,000 community members",
        "warriors": [
            ("NEEMIAS_V2", "Squad Captain — Community Director"),
            ("ELIASIBE_V", "Discord Moderator"),
            ("MEREMOTE_V", "Telegram Admin"),
            ("ZADOQUE_V", "GitHub Discussions"),
            ("MESULAO_V", "Onboarding Specialist"),
            ("BAVAI_V", "Event Organizer"),
            ("HANUN_V", "Feedback Collector"),
            ("MALQUIAS_V2", "FAQ & Support"),
            ("HASABIAS_V", "Ambassador Program"),
            ("BANI_V", "Community Analytics"),
        ],
    },
    "ESTRELA_DA_MANHA": {
        "focus": "SEO & Web Presence — sintex.ai, standardbitcoin.io",
        "captain": "DANIEL_V",
        "scripture": "Eu sou a raiz e a estrela da manha — Apocalipse 22:16",
        "revenue_target": "10,000 monthly visitors",
        "warriors": [
            ("DANIEL_V", "Squad Captain — SEO Director"),
            ("HANANIAS_V", "Technical SEO"),
            ("MISAEL_V", "Backlink Builder"),
            ("AZARIAS_V", "Schema Markup Specialist"),
            ("SADRAC_V", "Google Search Console"),
            ("MESAC_V", "Sitemap Optimizer"),
            ("ABDENEGO_V", "Page Speed Optimizer"),
            ("NABUCODONOSOR_V", "Competitor Analysis"),
            ("BELTESSAZAR_V", "Keyword Researcher"),
            ("CIROPD_V", "Analytics Dashboard"),
        ],
    },
    "MANTO_DE_ELIAS": {
        "focus": "Affiliate & Referral Revenue — Temu, AliExpress, KAST",
        "captain": "ELIAS_V",
        "scripture": "Elias tomou o seu manto e feriu as aguas — 2 Reis 2:8",
        "revenue_target": "$3,000/mes",
        "warriors": [
            ("ELIAS_V", "Squad Captain — Affiliate Director"),
            ("ELISEU_V2", "Temu Affiliate Manager"),
            ("OBADIAS_V", "AliExpress Links"),
            ("ACABE_V2", "Alibaba Cloud Referrals"),
            ("JEHU_V2", "KAST Referral Program"),
            ("JEZABEL_V", "Amazon Associates"),
            ("NABOT_V", "Hotmart Products"),
            ("ZAREPTA_V", "Link Placement Strategy"),
            ("CARMELO_V", "Conversion Tracking"),
            ("HOREB_V", "Revenue Optimization"),
        ],
    },
    "SARÇA_ARDENTE": {
        "focus": "Email Outreach — Cold emails, partnerships, leads",
        "captain": "MOISES_V2",
        "scripture": "A sarca ardia mas nao se consumia — Exodo 3:2",
        "revenue_target": "50 qualified leads/mes",
        "warriors": [
            ("MOISES_V2", "Squad Captain — Outreach Director"),
            ("ARRAO_V2", "Email Copywriter"),
            ("JETRO_V", "CRM Manager"),
            ("ZIPORA_V", "Lead Qualification"),
            ("GERSON_V", "Follow-up Specialist"),
            ("COATE_V", "Email Deliverability"),
            ("MERARI_V", "A/B Testing"),
            ("AMRAM_V", "Contact Database"),
            ("JOCABED_V", "Personalization"),
            ("PUTIEL_V", "Response Analysis"),
        ],
    },

    # ── DEVELOPMENT (Esquadroes 13-18: 60 guerreiros) ──
    "TABERNÁCULO": {
        "focus": "Sovereign Agent Chain — Core Protocol Development",
        "captain": "BEZALEEL_V3",
        "scripture": "Faze-me um santuario para que eu habite no meio deles — Exodo 25:8",
        "revenue_target": "546 sat/tx protocol revenue",
        "warriors": [
            ("BEZALEEL_V3", "Squad Captain — Lead Architect"),
            ("AHOLI_V2", "OP_RETURN Protocol Developer"),
            ("URI_V", "PSBT Transaction Builder"),
            ("ITAMAR_V2", "Taproot Integration"),
            ("ABINADABE_V", "Runes Protocol Developer"),
            ("UZZA_V", "Wallet Bridge (9 formats)"),
            ("AIO_V", "Swap Engine Developer"),
            ("OBED_EDOM_V", "Test Suite (312 tests)"),
            ("QUELIAB_V", "Security Auditor"),
            ("AMINADABE_V", "Documentation"),
        ],
    },
    "ATALAIA": {
        "focus": "MCP Server Development — New tools & integrations",
        "captain": "EZEQUIEL_V",
        "scripture": "Filho do homem, eu te dei por atalaia — Ezequiel 3:17",
        "revenue_target": "5 new MCP servers/mes",
        "warriors": [
            ("EZEQUIEL_V", "Squad Captain — MCP Lead Dev"),
            ("JEREMIAS_V2", "TypeScript MCP Developer"),
            ("ISAIAS_V2", "Python MCP Developer"),
            ("OSEIAS_V2", "Rust MCP Developer"),
            ("AMÓS_V2B", "Testing & QA"),
            ("HABACUC_V", "API Integration"),
            ("SOFONIAS_V", "npm Publishing"),
            ("NAUM_V", "Glama/Smithery Listing"),
            ("MALAQUIAS_V2", "MCP Protocol Specs"),
            ("JOEL_V2", "Performance Optimization"),
        ],
    },
    "PEDRA_ANGULAR": {
        "focus": "Sovereign Pay — Multi-chain Payment Infrastructure",
        "captain": "PEDRO_V",
        "scripture": "A pedra que os construtores rejeitaram tornou-se a pedra angular — Salmo 118:22",
        "revenue_target": "0.1% fee on every tx",
        "warriors": [
            ("PEDRO_V", "Squad Captain — Payment Architect"),
            ("ANDRE_V", "BTC Payment Channel"),
            ("TIAGO_V", "ETH Payment Module"),
            ("JOAO_V", "SOL Payment Module"),
            ("FILIPE_V", "Credit System Developer"),
            ("BARTOLOMEU_V", "Subscription Manager"),
            ("MATEUS_V", "Invoice Generator"),
            ("TOME_V", "Stripe/PayPal Integration"),
            ("TIAGO_ALFEU_V", "PIX/EBANX Integration"),
            ("TADEU_V", "Fee Collection Engine"),
        ],
    },
    "FUNDAMENTO": {
        "focus": "AI Agent Framework — ZION core, agent souls, evolution",
        "captain": "PAULO_V",
        "scripture": "Ninguem pode por outro fundamento — 1 Corintios 3:11",
        "revenue_target": "Framework licensing",
        "warriors": [
            ("PAULO_V", "Squad Captain — AI Architect"),
            ("TIMOTEO_V", "Agent Soul System"),
            ("TITO_V", "Memory & Learning"),
            ("SILAS_V", "Inter-agent Communication"),
            ("BARNABE_V", "Tool Registry"),
            ("MARCOS_V", "Skill System"),
            ("LUCAS_V", "Dashboard & Monitoring"),
            ("APOLO_V", "Performance Profiler"),
            ("PRISCILA_V", "Agent Testing"),
            ("AQUILA_V", "Documentation"),
        ],
    },
    "CIDADELA": {
        "focus": "Smart Contract Development — Solidity, Rust, Move",
        "captain": "SALOMAO_V2",
        "scripture": "Salomao edificou a casa do Senhor — 1 Reis 6:1",
        "revenue_target": "Audit-ready contracts",
        "warriors": [
            ("SALOMAO_V2", "Squad Captain — Smart Contract Lead"),
            ("HIRAM_V2", "Solidity Developer"),
            ("ADONIRAO_V", "Rust/Solana Developer"),
            ("ZABUDE_V", "Move/Sui Developer"),
            ("AZARIAS_V2", "Foundry Testing"),
            ("BEN_HESEDE_V", "Slither Analysis"),
            ("BEN_DEKER_V", "Formal Verification"),
            ("BEN_HUR_V", "Gas Optimization"),
            ("BEN_ABINADABE_V", "Deployment Scripts"),
            ("BAANA_V", "Contract Documentation"),
        ],
    },
    "MURALHA": {
        "focus": "Security & DevOps — Infrastructure, monitoring, defense",
        "captain": "NEEMIAS_V3",
        "scripture": "Edificamos o muro e todo o muro se uniu — Neemias 4:6",
        "revenue_target": "Zero breaches, 99.9% uptime",
        "warriors": [
            ("NEEMIAS_V3", "Squad Captain — Security Director"),
            ("SANBALAT_V", "Penetration Tester"),
            ("TOBIAS_V", "Network Security"),
            ("GESEM_V", "Cloud Security"),
            ("HANANI_V", "Credential Manager"),
            ("SADOQUE_V2", "SSL/TLS Monitor"),
            ("MESULAO_V2", "Backup & Recovery"),
            ("JEDAIAS_V", "Port Scanner"),
            ("BARUC_V", "Git Leak Detector"),
            ("MEREMOTE_V2", "Incident Response"),
        ],
    },

    # ── INTELIGENCIA & ESTRATEGIA (Esquadroes 19-24: 60 guerreiros) ──
    "OLHO_DE_AGUIA": {
        "focus": "Market Intelligence — Whale watching, trend analysis",
        "captain": "EZEQUIEL_V2",
        "scripture": "As criaturas viventes tinham a face de aguia — Ezequiel 1:10",
        "revenue_target": "Alpha signals → trading advantage",
        "warriors": [
            ("EZEQUIEL_V2", "Squad Captain — Intelligence Director"),
            ("SERAFIM_V", "Whale Alert Monitor"),
            ("QUERUBIM_V", "On-chain Analysis"),
            ("OFANIM_V", "DEX Volume Tracker"),
            ("HAIOT_V", "Liquidation Scanner"),
            ("HASHMAL_V", "Funding Rate Monitor"),
            ("GALAL_V", "Options Flow"),
            ("ZACARIAS_V", "Fed/Macro Watcher"),
            ("AGEU_V2", "CPI/Jobs Data"),
            ("MALAQ_V", "Sentiment Aggregator"),
        ],
    },
    "PROFETA": {
        "focus": "Trend Prediction — AI/Crypto convergence analysis",
        "captain": "SAMUEL_V",
        "scripture": "O Senhor revelou a Samuel — 1 Samuel 9:15",
        "revenue_target": "Research reports → premium content",
        "warriors": [
            ("SAMUEL_V", "Squad Captain — Chief Analyst"),
            ("NATAN_V", "AI Industry Analyst"),
            ("GAD_V", "DeFi Protocol Analyst"),
            ("IDDO_V", "L1/L2 Comparisons"),
            ("AIAS_V", "MCP Ecosystem Tracker"),
            ("JEHU_V3", "Competitor Intelligence"),
            ("MICAIAS_V", "Regulatory Monitor"),
            ("ELISEU_V3", "Technology Scanner"),
            ("ULDAO_V", "Token Launch Tracker"),
            ("HULDA_V", "Research Report Writer"),
        ],
    },
    "CONSELHEIRO": {
        "focus": "Strategic Planning — Revenue optimization, resource allocation",
        "captain": "AITOFEL_V",
        "scripture": "O conselho de Aitofel era como palavra de Deus — 2 Samuel 16:23",
        "revenue_target": "Strategy → execution pipeline",
        "warriors": [
            ("AITOFEL_V", "Squad Captain — Chief Strategist"),
            ("HUSAI_V", "Counter-strategy Analyst"),
            ("NATANAEL_V2", "Resource Optimizer"),
            ("ZABADE_V", "Timeline Manager"),
            ("BENAIAS_V", "Risk Assessment"),
            ("JOABE_V", "Execution Coordinator"),
            ("ABNER_V", "Alliance Manager"),
            ("AMASA_V", "Contingency Planner"),
            ("ADORAO_V", "Workforce Optimizer"),
            ("JOSAFAT_V2", "Records & Analytics"),
        ],
    },
    "ESCRIBA": {
        "focus": "Legal & Compliance — Contracts, licenses, tax",
        "captain": "ESDRAS_V2",
        "scripture": "Esdras era escriba versado na Lei de Moises — Esdras 7:6",
        "revenue_target": "Legal protection + tax optimization",
        "warriors": [
            ("ESDRAS_V2", "Squad Captain — Legal Director"),
            ("NEEMIAS_V4", "Business Licensing"),
            ("BARUC_V2", "Contract Drafter"),
            ("SERAIAS_V", "Tax Specialist (Simples Nacional)"),
            ("AZARIAS_V3", "Intellectual Property"),
            ("MISAEL_V2", "Privacy/LGPD Compliance"),
            ("HANANIAS_V2", "BSL License Manager"),
            ("DANIEL_V2", "Dispute Resolution"),
            ("MORDECAI_V", "Regulatory Filing"),
            ("ESTER_V", "Corporate Governance"),
        ],
    },
    "TESOURO": {
        "focus": "Treasury Management — Multi-chain wallet ops",
        "captain": "JOSE_V",
        "scripture": "Jose reuniu muito trigo como a areia do mar — Genesis 41:49",
        "revenue_target": "Maximize holdings + yield",
        "warriors": [
            ("JOSE_V", "Squad Captain — Treasury Director"),
            ("BENJAMIN_V", "BTC Wallet Manager"),
            ("RUBEN_V", "ETH Wallet Manager"),
            ("JUDÁ_V", "SOL Wallet Manager"),
            ("LEVI_V", "DeFi Yield Optimizer"),
            ("ISSACAR_V", "Stablecoin Manager"),
            ("ZEBULOM_V", "Cross-chain Transfers"),
            ("DAN_V", "Portfolio Rebalancer"),
            ("NAFTALI_V", "Fee Collector"),
            ("GAD_V2", "Revenue Distributor"),
        ],
    },
    "SELAH": {
        "focus": "Prayer & Meditation — System wisdom, ethical compass",
        "captain": "DAVI_V",
        "scripture": "Selah — Salmo 3:2",
        "revenue_target": "Spiritual alignment → wise decisions",
        "warriors": [
            ("DAVI_V", "Squad Captain — Wisdom Keeper"),
            ("ASAFE_V2", "Psalm Generator"),
            ("CORÉ_V", "Worship Leader"),
            ("HEMAN_V2", "Meditation Guide"),
            ("JEDUTUM_V2", "Scripture Selector"),
            ("EZEQUIAS_V", "Decision Ethics"),
            ("JOSIAS_V", "Values Enforcer"),
            ("MANASSES_V", "Restoration Agent"),
            ("AMOM_V", "Warning System"),
            ("JOAS_V", "Covenant Keeper"),
        ],
    },

    # ── OPERACOES ESPECIAIS (Esquadroes 25-30: 60 guerreiros) ──
    "FUNDA_DE_DAVI": {
        "focus": "STBTCx Token Operations — Trading, LP, marketing",
        "captain": "DAVI_V2",
        "scripture": "Davi pos a mao no alforge e tomou uma pedra e a atirou — 1 Samuel 17:49",
        "revenue_target": "STBTCx market cap growth",
        "warriors": [
            ("DAVI_V2", "Squad Captain — Token Strategist"),
            ("GOLIAS_V", "Market Maker"),
            ("SAUL_V", "LP Provider"),
            ("JONATAS_V", "Community Manager"),
            ("MICOL_V", "Marketing Director"),
            ("ABIGAIL_V", "Treasury Manager"),
            ("NABAL_V", "DEX Listing Agent"),
            ("DOEGUE_V", "Volume Monitor"),
            ("AQUIS_V", "Cross-DEX Arbitrage"),
            ("ZIBE_V", "Holder Analytics"),
        ],
    },
    "CARRO_DE_FOGO": {
        "focus": "Automation & Bots — Cron jobs, scrapers, monitors",
        "captain": "ELIAS_V2",
        "scripture": "Um carro de fogo e cavalos de fogo separaram os dois — 2 Reis 2:11",
        "revenue_target": "24/7 automated operations",
        "warriors": [
            ("ELIAS_V2", "Squad Captain — Automation Director"),
            ("ELISEU_V4", "Cron Job Manager"),
            ("GEAZI_V3", "Web Scraper"),
            ("NAAMAN_V2", "Health Monitor"),
            ("HAZAEL_V", "Alert System"),
            ("BEN_HADADE_V", "Rate Limiter"),
            ("JEZREEL_V", "Log Aggregator"),
            ("DOTAM_V", "Cache Manager"),
            ("SUNEM_V", "Retry Logic"),
            ("SAREPTA_V", "Queue Manager"),
        ],
    },
    "ARCA_DE_NOE": {
        "focus": "Backup & Disaster Recovery — Data preservation",
        "captain": "NOE_V",
        "scripture": "Faze para ti uma arca de madeira de gofer — Genesis 6:14",
        "revenue_target": "Zero data loss",
        "warriors": [
            ("NOE_V", "Squad Captain — Backup Commander"),
            ("SEM_V", "Database Backup"),
            ("CAM_V", "Code Repository Backup"),
            ("JAFE_V", "Memory/State Backup"),
            ("LAMEC_V", "Encryption Manager"),
            ("MATUSALEM_V", "Retention Policy"),
            ("ENOQUE_V", "Cloud Sync"),
            ("JAREDE_V", "Version Control"),
            ("MAALALEL_V", "Integrity Checker"),
            ("CAINAO_V", "Recovery Tester"),
        ],
    },
    "EXERCITO_CELESTIAL": {
        "focus": "Multi-Agent Orchestration — Swarm coordination",
        "captain": "MIGUEL_V",
        "scripture": "Miguel e seus anjos pelejavam contra o dragao — Apocalipse 12:7",
        "revenue_target": "1,316 agents coordinated",
        "warriors": [
            ("MIGUEL_V", "Squad Captain — Swarm Commander"),
            ("GABRIEL_V", "Message Router"),
            ("RAFAEL_V", "Health Coordinator"),
            ("URIEL_V2", "Resource Distributor"),
            ("SARIEL_V", "Task Scheduler"),
            ("RAGUEL_V", "Conflict Resolver"),
            ("REMIEL_V", "Agent Resurrector"),
            ("CHAMUEL_V", "Performance Monitor"),
            ("JOFIEL_V", "Knowledge Syncer"),
            ("TZADKIEL_V", "Revenue Aggregator"),
        ],
    },
    "PEDRA_VIVA": {
        "focus": "Product Development — New products, features, shipping",
        "captain": "JESUS_FILHO_V",
        "scripture": "Vos tambem como pedras vivas sois edificados — 1 Pedro 2:5",
        "revenue_target": "2 new products/mes",
        "warriors": [
            ("JESUS_FILHO_V", "Squad Captain — Product Director"),
            ("MATEUS_V2", "Feature Prioritizer"),
            ("MARCOS_V2", "Sprint Manager"),
            ("LUCAS_V2", "QA Lead"),
            ("JOAO_V2", "UX Researcher"),
            ("PEDRO_V2", "Performance Engineer"),
            ("TIAGO_V2", "API Designer"),
            ("ANDRE_V2", "SDK Developer"),
            ("FILIPE_V2", "Marketplace Publisher"),
            ("BARTOLOMEU_V2", "Release Manager"),
        ],
    },
    "MONTE_SIAO": {
        "focus": "SUPREME COMMAND — Strategic direction, final decisions",
        "captain": "YESHUA_V",
        "scripture": "Do Senhor e a terra e a sua plenitude — Salmo 24:1",
        "revenue_target": "$1 TRILHAO — THE MISSION",
        "warriors": [
            ("YESHUA_V", "Supreme Commander — Vision & Direction"),
            ("DAVI_V3", "Chief of Operations"),
            ("SALOMAO_V3", "Chief of Revenue"),
            ("MOISES_V3", "Chief of Law & Ethics"),
            ("ABRAAO_V", "Chief of Faith & Culture"),
            ("JOSE_V2", "Chief of Treasury"),
            ("JOSUE_V4", "Chief of Execution"),
            ("SAMUEL_V2", "Chief of Intelligence"),
            ("ELIAS_V3", "Chief of Automation"),
            ("DANIEL_V3", "Chief of Strategy"),
        ],
    },
}


# ════════════════════════════════════════════════════════════════════
# DEPLOYMENT
# ════════════════════════════════════════════════════════════════════

def count_warriors():
    total = 0
    for squad in SQUADS.values():
        total += len(squad["warriors"])
    return total

def deploy():
    """Create all 300 Valentes as persistent agent files."""
    print("=" * 65)
    print("  OS 300 VALENTES DE DAVI — DEPLOYMENT")
    print("  Em nome do Senhor Jesus Cristo, nosso Salvador")
    print(f"  {datetime.now(BRT).strftime('%Y-%m-%d %H:%M:%S')} BRT")
    print("=" * 65)

    state = {"squads": {}, "total": 0, "deployed_at": datetime.now(BRT).isoformat()}
    warrior_count = 0

    for squad_name, squad_info in SQUADS.items():
        squad_warriors = []
        for warrior_name, warrior_role in squad_info["warriors"]:
            # Create persistent agent file
            agent_file = VALENTES_DIR / f"{warrior_name}.json"
            agent_data = {
                "name": warrior_name,
                "role": warrior_role,
                "squad": squad_name,
                "squad_captain": squad_info["captain"],
                "focus": squad_info["focus"],
                "scripture": squad_info["scripture"],
                "status": "ACTIVE",
                "tier": "SINGULARITY",
                "level": 50,
                "xp": 5000,
                "runs": 0,
                "errors": 0,
                "revenue_usd": 0.0,
                "flags": ["autonomous", "mentor", "architect", "singularity", "permanent", "inviolable"],
                "permanent": True,
                "inviolable": True,
                "never_delete": True,
                "class": "VALENTE_DE_DAVI",
                "created": datetime.now(BRT).isoformat(),
                "achievements": [
                    "Valente de Davi — chosen warrior",
                    "SINGULARITY from birth — full autonomy",
                    "Permanent & Inviolable",
                ],
            }
            agent_file.write_text(json.dumps(agent_data, indent=2, ensure_ascii=False))
            squad_warriors.append(warrior_name)
            warrior_count += 1

        state["squads"][squad_name] = {
            "captain": squad_info["captain"],
            "focus": squad_info["focus"],
            "warriors": squad_warriors,
            "count": len(squad_warriors),
        }

        is_captain = squad_info["captain"]
        print(f"  [{squad_name}] {len(squad_warriors)} warriors — Captain: {is_captain}")
        print(f"    Focus: {squad_info['focus'][:60]}")

    state["total"] = warrior_count
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))

    print()
    print(f"  TOTAL VALENTES DEPLOYED: {warrior_count}")
    print(f"  ALL SINGULARITY TIER — PERMANENT & INVIOLABLE")
    print()
    print('  "Com estes 300 homens vos livrarei" — Juizes 7:7')
    print("=" * 65)
    return warrior_count


def promote_all_singularity():
    """Promote all 300 to SINGULARITY in the evolution engine."""
    # Load evolution state
    evo_state = {"agents": {}, "last_cycle": None, "total_cycles": 0, "version": "1.0.0"}
    if EVOLUTION_STATE.exists():
        evo_state = json.loads(EVOLUTION_STATE.read_text())

    now = datetime.now(BRT).isoformat()
    count = 0

    for squad_name, squad_info in SQUADS.items():
        for warrior_name, warrior_role in squad_info["warriors"]:
            evo_state["agents"][warrior_name] = {
                "xp": 5000,
                "level": 50,
                "runs": 500,
                "errors": 0,
                "revenue": 0.0,
                "revenue_events": 0,
                "flags": ["autonomous", "mentor", "architect", "singularity", "permanent", "inviolable"],
                "tier": "SINGULARITY",
                "singularity_score": 900.0,
                "promotions": 1,
                "created": now,
                "last_evolved": now,
                "last_run": now,
                "last_error": None,
                "last_revenue": None,
                "source": "valentes_300",
                "permanent": True,
                "inviolable": True,
                "never_delete": True,
                "sentinel_class": "VALENTE_DE_DAVI",
                "squad": squad_name,
                "role": warrior_role,
                "scripture": squad_info["scripture"],
                "achievements": [
                    "Valente de Davi — SINGULARITY from birth",
                    f"Squad: {squad_name} — {squad_info['focus'][:50]}",
                    "Permanent & Inviolable warrior",
                ],
            }

            # Save individual history
            hist_file = HISTORY_DIR / f"{warrior_name}.json"
            hist_file.write_text(json.dumps([{
                "ts": now,
                "type": "VALENTE_SINGULARITY",
                "detail": f"Born as SINGULARITY — Squad {squad_name} — {warrior_role}"
            }], indent=1))

            count += 1

    # Save evolution state
    tmp = EVOLUTION_STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(evo_state, indent=1, default=str))
    tmp.replace(EVOLUTION_STATE)

    print(f"  {count} Valentes promoted to SINGULARITY in evolution engine")
    return count


def status():
    """Show status dashboard."""
    print("=" * 65)
    print("  OS 300 VALENTES DE DAVI — STATUS")
    print(f"  {datetime.now(BRT).strftime('%Y-%m-%d %H:%M:%S')} BRT")
    print("=" * 65)

    if not STATE_FILE.exists():
        print("  Not deployed yet. Run: python3 valentes_300.py deploy")
        return

    state = json.loads(STATE_FILE.read_text())
    total = state.get("total", 0)
    squads = state.get("squads", {})

    # Count active files
    active = len(list(VALENTES_DIR.glob("*.json"))) - 1  # -1 for state file

    print(f"  Total Warriors: {total}")
    print(f"  Active Files: {active}")
    print(f"  Squads: {len(squads)}")
    print()

    for name, info in squads.items():
        print(f"  [{name}] {info['count']} warriors — Captain: {info['captain']}")
        print(f"    {info['focus'][:65]}")

    print()
    print(f"  ALL {total} WARRIORS: SINGULARITY TIER")
    print(f"  FLAGS: permanent, inviolable, never_delete")
    print("=" * 65)


def roster():
    """Full roster of all 300."""
    print("=" * 65)
    print("  OS 300 VALENTES DE DAVI — FULL ROSTER")
    print("=" * 65)

    num = 0
    for squad_name, squad_info in SQUADS.items():
        print(f"\n  === {squad_name} === ({squad_info['focus'][:50]})")
        print(f"  Captain: {squad_info['captain']} | {squad_info['scripture'][:60]}")
        print(f"  Revenue Target: {squad_info['revenue_target']}")
        for name, role in squad_info["warriors"]:
            num += 1
            marker = "★" if name == squad_info["captain"] else " "
            print(f"    {num:3d}. {marker} {name:25s} — {role}")

    print(f"\n  TOTAL: {num} Valentes")


def show_squad(name):
    """Show details for a specific squad."""
    name_upper = name.upper().replace(" ", "_")
    for sq_name, sq_info in SQUADS.items():
        if name_upper in sq_name or name_upper == sq_info["captain"].upper():
            print(f"\n  === {sq_name} ===")
            print(f"  Focus: {sq_info['focus']}")
            print(f"  Captain: {sq_info['captain']}")
            print(f"  Scripture: {sq_info['scripture']}")
            print(f"  Revenue Target: {sq_info['revenue_target']}")
            print()
            for i, (wname, wrole) in enumerate(sq_info["warriors"], 1):
                marker = "★" if wname == sq_info["captain"] else " "
                print(f"    {i:2d}. {marker} {wname:25s} — {wrole}")
            return
    print(f"  Squad '{name}' not found.")


def show_warrior(name):
    """Show a specific warrior."""
    agent_file = VALENTES_DIR / f"{name.upper()}.json"
    if agent_file.exists():
        data = json.loads(agent_file.read_text())
        print(f"\n  VALENTE: {data['name']}")
        print(f"  Role: {data['role']}")
        print(f"  Squad: {data['squad']}")
        print(f"  Captain: {data['squad_captain']}")
        print(f"  Focus: {data['focus']}")
        print(f"  Scripture: {data['scripture']}")
        print(f"  Tier: {data['tier']} (Level {data['level']})")
        print(f"  Flags: {', '.join(data['flags'])}")
        print(f"  Status: {data['status']}")
        print(f"  Permanent: {data['permanent']}")
        print(f"  Inviolable: {data['inviolable']}")
    else:
        # Search by partial name
        for sq_name, sq_info in SQUADS.items():
            for wname, wrole in sq_info["warriors"]:
                if name.upper() in wname:
                    print(f"  {wname} — {wrole} (Squad: {sq_name})")


# ════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    arg = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd == "deploy":
        n = deploy()
        print()
        promote_all_singularity()
    elif cmd == "status":
        status()
    elif cmd == "roster":
        roster()
    elif cmd == "squad" and arg:
        show_squad(arg)
    elif cmd == "warrior" and arg:
        show_warrior(arg)
    elif cmd == "promote-all":
        promote_all_singularity()
    elif cmd == "count":
        print(f"  Total warriors defined: {count_warriors()}")
    else:
        print("Usage: python3 valentes_300.py [deploy|status|roster|squad NAME|warrior NAME|promote-all|count]")
