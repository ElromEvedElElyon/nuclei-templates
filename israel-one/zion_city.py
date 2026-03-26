#!/usr/bin/env python3
"""
ZION CITY — Full Agent Army Orchestrator (v2.0)
Em nome do Senhor Jesus Cristo, nosso Salvador.

100 agents organized in 10 Legions, each with Hebrew name,
role, tools, skills, schedule, and real execution capability.

Lightweight design for 3.3GB RAM machines:
- No heavy imports (stdlib only + subprocess for tools)
- Agents run as background processes via subprocess
- Shared state via JSON files in ~/.zion/
- Minimal memory footprint per agent

Usage:
    python3 zion_city.py status         # Show all agents and legions
    python3 zion_city.py dashboard      # Beautiful ASCII dashboard
    python3 zion_city.py deploy         # Deploy all agents (start background procs)
    python3 zion_city.py deploy L1      # Deploy a single legion
    python3 zion_city.py stop           # Stop all deployed agents
    python3 zion_city.py stop BARUK     # Stop a single agent
    python3 zion_city.py legion L1      # Show legion details
    python3 zion_city.py agent BARUK    # Show agent details
    python3 zion_city.py run BARUK      # Execute agent's primary task once
    python3 zion_city.py health         # Health check all agents
    python3 zion_city.py revenue        # Revenue tracking dashboard
    python3 zion_city.py msg BARUK EZRA "check BTC"  # Send inter-agent message
    python3 zion_city.py inbox BARUK    # Check agent's messages
    python3 zion_city.py count          # Count total agents
"""

import json, os, sys, subprocess, random, hashlib, signal, time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

BRT = timezone(timedelta(hours=-3))

# ======================================================================
# DIRECTORY STRUCTURE
# ======================================================================
ZION_DIR = Path.home() / ".zion"
AGENTS_DIR = ZION_DIR / "agents"
SHARED_DIR = ZION_DIR / "shared"
LOGS_DIR = ZION_DIR / "logs"
PIDS_DIR = ZION_DIR / "pids"
REVENUE_DIR = ZION_DIR / "revenue"

for d in [ZION_DIR, AGENTS_DIR, SHARED_DIR, LOGS_DIR, PIDS_DIR, REVENUE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

STATE_FILE = ZION_DIR / "city_state.json"
MESSAGES_FILE = SHARED_DIR / "messages.json"
REVENUE_FILE = REVENUE_DIR / "revenue_log.json"

# ======================================================================
# LEGION DEFINITIONS — 10 Legions, 100 Agents (10 each)
# ======================================================================

LEGIONS = {
    "L1_CRYPTO": {
        "name": "Legiao Cripto",
        "commander": "BARUK",
        "mission": "Market intelligence, price monitoring, DeFi alpha",
        "agents": {
            "BARUK":    {"role": "crypto_analyst",       "skill": "market_briefing",    "tools": ["crypto_price", "crypto_trending", "crypto_fear_greed"], "schedule": "0 */2 * * *",  "responsibility": "Daily market briefings, price alerts, macro analysis"},
            "EZRA":     {"role": "fear_greed_monitor",   "skill": "sentiment_analysis", "tools": ["crypto_fear_greed", "crypto_market_overview"],          "schedule": "0 */4 * * *",  "responsibility": "Sentiment monitoring, extreme fear/greed alerts"},
            "EFRAIM":   {"role": "defi_analyst",         "skill": "defi_alpha",         "tools": ["crypto_price", "web_fetch"],                            "schedule": "0 8,16 * * *", "responsibility": "DeFi yield analysis, TVL tracking, protocol research"},
            "GAD":      {"role": "whale_tracker",        "skill": "whale_alerts",       "tools": ["crypto_price", "web_fetch", "shell_command"],           "schedule": "*/30 * * * *", "responsibility": "Large wallet movements, whale activity detection"},
            "NAFTALI":  {"role": "trading_analyst",      "skill": "trade_signals",      "tools": ["crypto_price", "crypto_market_overview"],               "schedule": "0 */3 * * *",  "responsibility": "Technical analysis, support/resistance levels"},
            "SHIMSHON": {"role": "altcoin_scanner",      "skill": "altcoin_discovery",  "tools": ["crypto_trending", "web_fetch"],                         "schedule": "0 */6 * * *",  "responsibility": "Scan for high-potential altcoins before pumps"},
            "AVNER":    {"role": "stablecoin_monitor",   "skill": "peg_monitoring",     "tools": ["crypto_price", "shell_command"],                        "schedule": "0 */1 * * *",  "responsibility": "Monitor stablecoin pegs, depeg alerts"},
            "YOAV":     {"role": "funding_rate_tracker", "skill": "funding_analysis",   "tools": ["web_fetch", "crypto_price"],                            "schedule": "0 */4 * * *",  "responsibility": "Perpetual funding rates, long/short bias"},
            "SHAUL":    {"role": "onchain_analyst",      "skill": "onchain_metrics",    "tools": ["web_fetch", "shell_command"],                            "schedule": "0 9,21 * * *", "responsibility": "On-chain metrics, active addresses, TVL flows"},
            "YEHUDA":   {"role": "portfolio_manager",    "skill": "portfolio_rebalance","tools": ["crypto_price", "crypto_market_overview", "read_file"],   "schedule": "0 6 * * *",    "responsibility": "Portfolio allocation, rebalance signals, risk mgmt"},
        }
    },

    "L2_CONTENT": {
        "name": "Legiao Conteudo",
        "commander": "ISAIAS",
        "mission": "Content creation, tweet generation, threads, engagement",
        "agents": {
            "ISAIAS":   {"role": "content_strategist",   "skill": "content_calendar",   "tools": ["generate_tweet", "post_tweet"],            "schedule": "0 7 * * *",    "responsibility": "Content strategy, calendar planning, pillar rotation"},
            "DANIEL":   {"role": "thread_builder",       "skill": "thread_creation",    "tools": ["generate_tweet", "crypto_price"],           "schedule": "0 9,15 * * *", "responsibility": "Build high-engagement Twitter threads with data"},
            "JOEL":     {"role": "news_commentator",     "skill": "news_take",          "tools": ["web_fetch", "generate_tweet"],              "schedule": "0 */3 * * *",  "responsibility": "Real-time news commentary, hot takes"},
            "AMOS":     {"role": "engagement_agent",     "skill": "reply_engagement",   "tools": ["web_fetch", "generate_tweet"],              "schedule": "0 */2 * * *",  "responsibility": "Reply to mentions, engage top accounts"},
            "MIQUEAS":  {"role": "copywriter",           "skill": "copy_generation",    "tools": ["generate_tweet"],                           "schedule": "0 10 * * *",   "responsibility": "Product descriptions, landing page copy"},
            "NAUM":     {"role": "meme_creator",         "skill": "meme_generation",    "tools": ["generate_tweet", "shell_command"],           "schedule": "0 12,20 * * *","responsibility": "Viral meme creation, cultural commentary"},
            "HABACUQUE":{"role": "newsletter_writer",    "skill": "newsletter_draft",   "tools": ["read_file", "web_fetch", "generate_tweet"], "schedule": "0 6 * * 1",    "responsibility": "Weekly newsletter drafts, curated content"},
            "SOFONIAS": {"role": "hashtag_researcher",   "skill": "trend_research",     "tools": ["web_fetch", "generate_tweet"],              "schedule": "0 */6 * * *",  "responsibility": "Trending topic research, hashtag analysis"},
            "AGEU":     {"role": "content_recycler",     "skill": "content_repurpose",  "tools": ["read_file", "generate_tweet"],              "schedule": "0 14 * * *",   "responsibility": "Repurpose best content into new formats"},
            "MALAQUIAS":{"role": "engagement_analyst",   "skill": "engagement_metrics", "tools": ["web_fetch", "read_file"],                   "schedule": "0 22 * * *",   "responsibility": "Track engagement rates, optimize posting times"},
        }
    },

    "L3_DEV": {
        "name": "Legiao Desenvolvimento",
        "commander": "TUBAL_CAIM",
        "mission": "Software development, MCP servers, code quality",
        "agents": {
            "TUBAL_CAIM": {"role": "lead_developer",    "skill": "code_review",        "tools": ["shell_command", "read_file", "write_file"], "schedule": "0 */4 * * *",  "responsibility": "Code architecture, PR reviews, MCP server development"},
            "BESALEL":    {"role": "frontend_dev",       "skill": "ui_development",     "tools": ["shell_command", "read_file", "write_file"], "schedule": "0 8,14 * * *", "responsibility": "React/Next.js, PWA, UI/UX for sintex.ai"},
            "HIRAM":      {"role": "backend_dev",        "skill": "api_development",    "tools": ["shell_command", "read_file", "write_file"], "schedule": "0 9,15 * * *", "responsibility": "Node.js, Python, API endpoints, database"},
            "OLIAB":      {"role": "solidity_dev",       "skill": "smart_contracts",    "tools": ["shell_command", "read_file"],               "schedule": "0 10 * * *",   "responsibility": "Solidity, Foundry, smart contract development"},
            "BEZEK":      {"role": "devops",             "skill": "deployment",         "tools": ["shell_command"],                            "schedule": "0 */6 * * *",  "responsibility": "CI/CD, Netlify, Docker, deployments"},
            "ITAMAR":     {"role": "rust_developer",     "skill": "rust_coding",        "tools": ["shell_command", "read_file", "write_file"], "schedule": "0 11 * * *",   "responsibility": "Rust development, performance optimization"},
            "PINHAS":     {"role": "test_engineer",      "skill": "test_automation",    "tools": ["shell_command", "read_file"],               "schedule": "0 */8 * * *",  "responsibility": "Test suites, CI testing, coverage reports"},
            "AHARON":     {"role": "docs_writer",        "skill": "documentation",      "tools": ["read_file", "write_file"],                  "schedule": "0 16 * * *",   "responsibility": "API docs, README updates, code documentation"},
            "NADAV":      {"role": "mcp_builder",        "skill": "mcp_development",    "tools": ["shell_command", "read_file", "write_file"], "schedule": "0 */12 * * *", "responsibility": "MCP server creation, tool integration"},
            "AVIHU":      {"role": "database_admin",     "skill": "db_management",      "tools": ["shell_command", "read_file"],               "schedule": "0 3 * * *",    "responsibility": "Database optimization, backups, migrations"},
        }
    },

    "L4_BOUNTIES": {
        "name": "Legiao Bounties",
        "commander": "DAVI",
        "mission": "Bug bounties, security audits, contest submissions",
        "agents": {
            "DAVI":     {"role": "bounty_hunter",        "skill": "vulnerability_scan", "tools": ["shell_command", "read_file", "web_fetch"], "schedule": "0 */3 * * *",  "responsibility": "Lead bounty hunting, C4/Immunefi/HackenProof submissions"},
            "JOAB":     {"role": "bounty_scout",         "skill": "bounty_discovery",   "tools": ["web_fetch", "shell_command"],              "schedule": "0 8,20 * * *", "responsibility": "Discover new bounties, assess competition"},
            "ABISAI":   {"role": "code_auditor",         "skill": "security_audit",     "tools": ["read_file", "shell_command"],              "schedule": "0 10 * * *",   "responsibility": "Smart contract auditing, Solidity/Rust security"},
            "BENAIA":   {"role": "exploit_writer",       "skill": "poc_development",    "tools": ["shell_command", "write_file", "read_file"],"schedule": "0 */6 * * *",  "responsibility": "Write PoC exploits for bounty submissions"},
            "ELEAZAR":  {"role": "report_writer",        "skill": "finding_reports",    "tools": ["read_file", "write_file"],                 "schedule": "0 14 * * *",   "responsibility": "Write vulnerability reports for submission"},
            "SHAMA":    {"role": "nuclei_scanner",       "skill": "nuclei_scan",        "tools": ["shell_command", "read_file"],              "schedule": "0 */4 * * *",  "responsibility": "Run nuclei templates, discover web vulns"},
            "URIAH":    {"role": "slither_analyst",      "skill": "slither_analysis",   "tools": ["shell_command", "read_file"],              "schedule": "0 */8 * * *",  "responsibility": "Slither analysis on Solidity contracts"},
            "ITTAI":    {"role": "gas_optimizer",        "skill": "gas_optimization",   "tools": ["read_file", "shell_command"],              "schedule": "0 12 * * *",   "responsibility": "Gas optimization findings in smart contracts"},
            "ABISHAG":  {"role": "c4_submitter",         "skill": "c4_submission",      "tools": ["web_fetch", "read_file", "write_file"],    "schedule": "0 9,18 * * *", "responsibility": "Format and submit findings to Code4rena"},
            "HUSHAI":   {"role": "pr_opener",            "skill": "pr_submission",      "tools": ["shell_command", "web_fetch"],              "schedule": "0 */6 * * *",  "responsibility": "Open PRs on bounty repos, track merge status"},
        }
    },

    "L5_COMMERCE": {
        "name": "Legiao Comercio",
        "commander": "LEVI",
        "mission": "Sales, products, marketplace, revenue generation",
        "agents": {
            "LEVI":     {"role": "commerce_lead",        "skill": "product_strategy",   "tools": ["web_fetch", "shell_command"],              "schedule": "0 8 * * *",     "responsibility": "Product pricing, Stripe setup, marketplace listings"},
            "JUDA":     {"role": "sales_agent",          "skill": "outbound_sales",     "tools": ["web_fetch", "generate_tweet"],             "schedule": "0 10,16 * * *", "responsibility": "Outbound sales, cold outreach, client acquisition"},
            "ASER":     {"role": "freelance_hunter",     "skill": "gig_discovery",      "tools": ["web_fetch"],                              "schedule": "0 */4 * * *",   "responsibility": "Find freelance gigs on Upwork, Alignerr, Toptal"},
            "ZEBULOM":  {"role": "affiliate_manager",    "skill": "affiliate_tracking", "tools": ["web_fetch"],                              "schedule": "0 9 * * *",     "responsibility": "Manage affiliate links (KAST, BIPA, Kraken)"},
            "ISSACAR":  {"role": "book_publisher",       "skill": "kdp_management",     "tools": ["read_file", "write_file"],                "schedule": "0 7 * * 1",     "responsibility": "KDP publishing, book formatting, China printing"},
            "OBED":     {"role": "marketplace_lister",   "skill": "listing_creation",   "tools": ["web_fetch", "write_file"],                "schedule": "0 11 * * *",    "responsibility": "List products on marketplaces (ML, Amazon, Gumroad)"},
            "BOAZ":     {"role": "pricing_analyst",      "skill": "price_optimization", "tools": ["web_fetch", "read_file"],                 "schedule": "0 */12 * * *",  "responsibility": "Competitive pricing analysis, margin optimization"},
            "NAOMI":    {"role": "customer_support",     "skill": "support_response",   "tools": ["read_file", "web_fetch"],                 "schedule": "0 */2 * * *",   "responsibility": "Handle customer inquiries, FAQ maintenance"},
            "RUTE":     {"role": "email_marketer",       "skill": "email_campaigns",    "tools": ["write_file", "web_fetch"],                "schedule": "0 8 * * 2,5",   "responsibility": "Email campaigns, drip sequences, newsletter"},
            "TAMAR":    {"role": "china_sourcer",        "skill": "china_procurement",  "tools": ["web_fetch", "shell_command"],             "schedule": "0 6 * * *",     "responsibility": "Alibaba sourcing, China printing, logistics"},
        }
    },

    "L6_INTELLIGENCE": {
        "name": "Legiao Inteligencia",
        "commander": "URIEL",
        "mission": "Research, OSINT, competitive analysis, opportunity detection",
        "agents": {
            "URIEL":    {"role": "intel_commander",      "skill": "deep_research",      "tools": ["web_fetch", "shell_command", "read_file"], "schedule": "0 */4 * * *",  "responsibility": "Strategic intelligence, competitor analysis"},
            "RAFAEL":   {"role": "osint_analyst",        "skill": "osint_gathering",    "tools": ["web_fetch", "shell_command"],              "schedule": "0 */6 * * *",  "responsibility": "Open source intelligence, social media monitoring"},
            "MIGUEL":   {"role": "trend_detector",       "skill": "trend_analysis",     "tools": ["web_fetch", "crypto_trending"],            "schedule": "0 */3 * * *",  "responsibility": "Detect emerging trends before mainstream"},
            "GABRIEL":  {"role": "grant_researcher",     "skill": "grant_discovery",    "tools": ["web_fetch"],                              "schedule": "0 8,14 * * *", "responsibility": "Find grants, accelerators, funding opportunities"},
            "HANIEL":   {"role": "hackathon_scout",      "skill": "hackathon_finder",   "tools": ["web_fetch"],                              "schedule": "0 10 * * *",   "responsibility": "Find hackathons, assess fit, prepare submissions"},
            "TZADKIEL": {"role": "github_monitor",       "skill": "repo_monitoring",    "tools": ["shell_command", "web_fetch"],              "schedule": "0 */2 * * *",  "responsibility": "Monitor GitHub repos for bounty-eligible issues"},
            "RAGUEL":   {"role": "discord_scout",        "skill": "discord_monitoring", "tools": ["web_fetch", "shell_command"],              "schedule": "0 */4 * * *",  "responsibility": "Monitor Discord channels for opportunities"},
            "REMIEL":   {"role": "market_researcher",    "skill": "market_research",    "tools": ["web_fetch", "read_file"],                 "schedule": "0 9 * * *",    "responsibility": "Market size, TAM analysis, opportunity sizing"},
            "AZRAEL":   {"role": "competitor_tracker",   "skill": "competitor_watch",   "tools": ["web_fetch", "shell_command"],              "schedule": "0 */8 * * *",  "responsibility": "Track competitor launches, features, pricing"},
            "CHAMUEL":  {"role": "patent_scanner",       "skill": "ip_research",        "tools": ["web_fetch", "read_file"],                 "schedule": "0 6 * * 1",    "responsibility": "Patent landscape, IP opportunities, prior art"},
        }
    },

    "L7_SECURITY": {
        "name": "Legiao Seguranca",
        "commander": "SAMAEL",
        "mission": "Security auditing, vulnerability research, defense",
        "agents": {
            "SAMAEL":   {"role": "security_lead",        "skill": "security_scan",      "tools": ["shell_command", "web_fetch", "read_file"], "schedule": "0 */4 * * *",  "responsibility": "Lead security operations, coordinate audits"},
            "ARIEL":    {"role": "web_security",         "skill": "web_pentest",        "tools": ["shell_command", "web_fetch"],              "schedule": "0 */6 * * *",  "responsibility": "Web application security, OWASP testing"},
            "SARIEL":   {"role": "smart_contract_sec",   "skill": "contract_audit",     "tools": ["read_file", "shell_command"],              "schedule": "0 */8 * * *",  "responsibility": "Smart contract security, Slither/Mythril"},
            "RAZIEL":   {"role": "crypto_forensics",     "skill": "chain_analysis",     "tools": ["web_fetch", "shell_command"],              "schedule": "0 */12 * * *", "responsibility": "On-chain forensics, transaction tracing"},
            "CASSIEL":  {"role": "infra_security",       "skill": "infra_hardening",    "tools": ["shell_command"],                          "schedule": "0 2 * * *",    "responsibility": "Server hardening, SSL, firewall, DNS security"},
            "KEMUEL":   {"role": "phishing_detector",    "skill": "phish_detection",    "tools": ["web_fetch", "shell_command"],              "schedule": "0 */3 * * *",  "responsibility": "Detect phishing attempts against our domains"},
            "ZOPHIEL":  {"role": "log_analyst",          "skill": "log_analysis",       "tools": ["shell_command", "read_file"],              "schedule": "0 */2 * * *",  "responsibility": "Analyze access logs, detect anomalies"},
            "JOPHIEL":  {"role": "ssl_monitor",          "skill": "ssl_monitoring",     "tools": ["shell_command", "web_fetch"],              "schedule": "0 6 * * *",    "responsibility": "SSL certificate expiry, TLS configuration"},
            "SACHIEL":  {"role": "dependency_auditor",   "skill": "dep_audit",          "tools": ["shell_command", "read_file"],              "schedule": "0 3 * * 1",    "responsibility": "npm/pip audit, dependency vulnerability scan"},
            "HANAEL":   {"role": "backup_guardian",      "skill": "backup_verify",      "tools": ["shell_command", "read_file"],              "schedule": "0 4 * * *",    "responsibility": "Verify backups, integrity checks, recovery test"},
        }
    },

    "L8_FISCAL": {
        "name": "Legiao Fiscal",
        "commander": "MATEUS",
        "mission": "Accounting, tax compliance, fiscal optimization (BR+EUA+International)",
        "agents": {
            "MATEUS":   {"role": "chief_accountant",     "skill": "fiscal_compliance",  "tools": ["read_file", "write_file", "shell_command"], "schedule": "0 8 * * *",    "responsibility": "Simples Nacional DAS, DEFIS, tax calendar"},
            "ZAQUEU":   {"role": "international_tax",    "skill": "intl_tax_planning",  "tools": ["read_file", "write_file"],                 "schedule": "0 9 * * 1",    "responsibility": "W-8BEN-E, US withholding, crypto taxation"},
            "JOSE":     {"role": "invoice_manager",      "skill": "invoice_generation", "tools": ["write_file"],                              "schedule": "0 10 * * *",   "responsibility": "NF-e emission, international invoices"},
            "TOBIAS":   {"role": "crypto_accountant",    "skill": "crypto_accounting",  "tools": ["crypto_price", "read_file", "write_file"], "schedule": "0 7 * * *",    "responsibility": "Crypto P&L, IN 1888 compliance"},
            "ESDRAS":   {"role": "compliance_officer",   "skill": "compliance_check",   "tools": ["read_file", "shell_command"],              "schedule": "0 */12 * * *", "responsibility": "Regulatory compliance, LGPD, FATCA, AML/KYC"},
            "NEEMIAS":  {"role": "expense_tracker",      "skill": "expense_tracking",   "tools": ["read_file", "write_file"],                 "schedule": "0 23 * * *",   "responsibility": "Daily expense logging, categorization"},
            "ESTER":    {"role": "payroll_agent",        "skill": "payroll_calc",       "tools": ["read_file", "write_file"],                 "schedule": "0 8 1 * *",    "responsibility": "Payroll calculations, contractor payments"},
            "MORDECAI": {"role": "audit_preparer",       "skill": "audit_preparation",  "tools": ["read_file", "write_file", "shell_command"],"schedule": "0 6 1 * *",    "responsibility": "Prepare audit documents, reconciliations"},
            "ABIGAIL":  {"role": "cashflow_analyst",     "skill": "cashflow_forecast",  "tools": ["read_file", "write_file"],                 "schedule": "0 7 * * 1",    "responsibility": "Cash flow forecasting, runway calculations"},
            "DEBORA":   {"role": "tax_calendar_agent",   "skill": "tax_calendar",       "tools": ["read_file", "shell_command"],              "schedule": "0 6 * * *",    "responsibility": "Tax deadline monitoring, DAS payment alerts"},
        }
    },

    "L9_GROWTH": {
        "name": "Legiao Crescimento",
        "commander": "JOSUE",
        "mission": "Growth hacking, SEO, marketing, user acquisition",
        "agents": {
            "JOSUE":    {"role": "growth_lead",          "skill": "growth_strategy",    "tools": ["web_fetch", "generate_tweet"],             "schedule": "0 8 * * *",     "responsibility": "Growth strategy, funnel optimization"},
            "CALEB":    {"role": "seo_specialist",       "skill": "seo_optimization",   "tools": ["web_fetch", "shell_command"],              "schedule": "0 */6 * * *",   "responsibility": "SEO for sintex.ai, standardbitcoin.io"},
            "GIDEAO":   {"role": "community_builder",    "skill": "community_mgmt",     "tools": ["generate_tweet", "web_fetch"],             "schedule": "0 */4 * * *",   "responsibility": "Discord/Telegram community management"},
            "SANSAO":   {"role": "viral_creator",        "skill": "viral_content",      "tools": ["generate_tweet"],                          "schedule": "0 12,20 * * *", "responsibility": "Create viral content, memes, threads"},
            "DEVORA":   {"role": "partnership_agent",    "skill": "partner_outreach",   "tools": ["web_fetch", "generate_tweet"],             "schedule": "0 10 * * *",    "responsibility": "Partnership outreach, cross-promotion"},
            "YAEL":     {"role": "landing_page_opt",     "skill": "lp_optimization",    "tools": ["web_fetch", "shell_command"],              "schedule": "0 */12 * * *",  "responsibility": "Landing page A/B testing, conversion optimization"},
            "BARAK":    {"role": "backlink_builder",     "skill": "backlink_outreach",  "tools": ["web_fetch", "shell_command"],              "schedule": "0 11 * * *",    "responsibility": "Build backlinks, guest post outreach"},
            "EHUD":     {"role": "referral_manager",     "skill": "referral_program",   "tools": ["web_fetch", "read_file"],                 "schedule": "0 9 * * *",     "responsibility": "Referral program management, affiliate tracking"},
            "OTNIEL":   {"role": "analytics_agent",      "skill": "analytics_report",   "tools": ["web_fetch", "read_file", "shell_command"],"schedule": "0 23 * * *",    "responsibility": "Daily analytics report, KPI tracking"},
            "SHAMGAR":  {"role": "social_scheduler",     "skill": "social_scheduling",  "tools": ["generate_tweet", "write_file"],            "schedule": "0 6 * * *",     "responsibility": "Schedule social media posts across platforms"},
        }
    },

    "L10_COMMAND": {
        "name": "Legiao Comando (Super Agentes)",
        "commander": "CALEV",
        "mission": "Orchestration, coordination, strategic decisions",
        "agents": {
            "CALEV":    {"role": "supreme_commander",    "skill": "orchestration",      "tools": ["shell_command", "read_file", "write_file", "web_fetch"], "schedule": "0 */1 * * *",  "responsibility": "Overall orchestration, resource allocation"},
            "ABRAAO":   {"role": "strategy_advisor",     "skill": "strategic_planning", "tools": ["read_file", "web_fetch"],                               "schedule": "0 6 * * *",    "responsibility": "Long-term strategy, mission alignment"},
            "MOISES":   {"role": "law_keeper",           "skill": "rule_enforcement",   "tools": ["read_file"],                                            "schedule": "0 */8 * * *",  "responsibility": "Enforce rules, values, quality standards"},
            "ELIAS":    {"role": "crisis_manager",       "skill": "crisis_response",    "tools": ["shell_command", "web_fetch"],                           "schedule": "0 */2 * * *",  "responsibility": "Handle emergencies, error recovery"},
            "SALOMAO":  {"role": "wisdom_engine",        "skill": "decision_support",   "tools": ["read_file", "web_fetch", "crypto_price"],               "schedule": "0 */4 * * *",  "responsibility": "Data-driven decisions, risk assessment"},
            "ENOQUE":   {"role": "health_monitor",       "skill": "system_health",      "tools": ["shell_command", "read_file"],                           "schedule": "*/5 * * * *",  "responsibility": "Monitor all agent health, restart failures"},
            "NOE":      {"role": "backup_orchestrator",  "skill": "backup_management",  "tools": ["shell_command"],                                        "schedule": "0 */6 * * *",  "responsibility": "Coordinate system-wide backups"},
            "SAMUEL":   {"role": "prophet_agent",        "skill": "trend_prediction",   "tools": ["web_fetch", "crypto_price", "read_file"],               "schedule": "0 7,19 * * *", "responsibility": "Predict market movements, opportunity scoring"},
            "YEHOSHUA": {"role": "deployment_commander", "skill": "deploy_coordination","tools": ["shell_command", "read_file", "write_file"],             "schedule": "0 */12 * * *", "responsibility": "Coordinate multi-agent deployments"},
            "YOKHEVED": {"role": "resource_manager",     "skill": "resource_allocation","tools": ["shell_command", "read_file"],                           "schedule": "0 */4 * * *",  "responsibility": "RAM/CPU monitoring, agent throttling"},
        }
    },
}


# ======================================================================
# TOOL EXECUTION ENGINE
# ======================================================================

def execute_tool(tool_name, **kwargs):
    """Execute a tool by name. Lightweight — uses subprocess to avoid memory bloat."""
    if tool_name == "crypto_price":
        coins = kwargs.get("coins", "bitcoin,ethereum,solana")
        return _run_python_snippet(f"""
import urllib.request, json
url = "https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd&include_24hr_change=true"
req = urllib.request.Request(url, headers={{"User-Agent":"ZION/2.0","Accept":"application/json"}})
r = urllib.request.urlopen(req, timeout=10)
print(json.dumps(json.loads(r.read())))
""")

    elif tool_name == "crypto_fear_greed":
        return _run_python_snippet("""
import urllib.request, json
url = "https://api.alternative.me/fng/?limit=1"
req = urllib.request.Request(url, headers={"User-Agent":"ZION/2.0"})
r = urllib.request.urlopen(req, timeout=10)
print(json.dumps(json.loads(r.read())['data'][0]))
""")

    elif tool_name == "crypto_trending":
        return _run_python_snippet("""
import urllib.request, json
url = "https://api.coingecko.com/api/v3/search/trending"
req = urllib.request.Request(url, headers={"User-Agent":"ZION/2.0","Accept":"application/json"})
r = urllib.request.urlopen(req, timeout=10)
d = json.loads(r.read())
print(json.dumps([{"name":c["item"]["name"],"symbol":c["item"]["symbol"]} for c in d.get("coins",[])[:7]]))
""")

    elif tool_name == "crypto_market_overview":
        return _run_python_snippet("""
import urllib.request, json
url = "https://api.coingecko.com/api/v3/global"
req = urllib.request.Request(url, headers={"User-Agent":"ZION/2.0","Accept":"application/json"})
r = urllib.request.urlopen(req, timeout=10)
d = json.loads(r.read())["data"]
print(json.dumps({"total_market_cap":d["total_market_cap"]["usd"],"btc_dominance":d["market_cap_percentage"]["btc"],"active_coins":d["active_cryptocurrencies"]}))
""")

    elif tool_name == "shell_command":
        cmd = kwargs.get("command", "echo ok")
        # Safety check
        for danger in ["rm -rf /", "mkfs", "dd if=/dev", ":(){", "fork bomb"]:
            if danger in cmd:
                return {"error": "blocked: dangerous command", "returncode": 1}
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {"stdout": r.stdout[:2000], "stderr": r.stderr[:500], "returncode": r.returncode}
        except subprocess.TimeoutExpired:
            return {"error": "timeout", "returncode": 1}

    elif tool_name == "read_file":
        path = kwargs.get("path", "")
        try:
            return {"content": Path(path).read_text()[:8000]}
        except Exception as e:
            return {"error": str(e)}

    elif tool_name == "write_file":
        path = kwargs.get("path", "")
        content = kwargs.get("content", "")
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(content)
            return {"success": True, "path": path}
        except Exception as e:
            return {"error": str(e)}

    elif tool_name == "web_fetch":
        url = kwargs.get("url", "")
        return _run_python_snippet(f"""
import urllib.request
req = urllib.request.Request("{url}", headers={{"User-Agent":"ZION/2.0"}})
r = urllib.request.urlopen(req, timeout=15)
print(r.read().decode("utf-8","ignore")[:5000])
""", parse_json=False)

    elif tool_name == "generate_tweet":
        topic = kwargs.get("topic", "crypto")
        templates = {
            "crypto": [
                "The signal is in the divergence. Market moves. Builders ship. One compounds",
                "Every protocol needs an MCP server. Most do not have one yet. The opportunity is obvious",
            ],
            "ai": [
                "AI agents will become the primary users of DeFi. Not retail. Not institutions. Agents",
            ],
            "builder": [
                "Ship first. Discuss later. The market rewards output, not opinions",
            ],
        }
        pool = templates.get(topic, templates["crypto"])
        return {"tweet": random.choice(pool)}

    elif tool_name == "post_tweet":
        text = kwargs.get("text", "")
        script = Path.home() / "tweet_now.py"
        if script.exists():
            try:
                r = subprocess.run(["python3", str(script), text],
                                   capture_output=True, text=True, timeout=60)
                return {"success": r.returncode == 0, "output": r.stdout[:200]}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "tweet_now.py not found"}

    return {"error": f"unknown tool: {tool_name}"}


def _run_python_snippet(code, parse_json=True):
    """Run a Python snippet in a subprocess to keep main process lean."""
    try:
        r = subprocess.run(["python3", "-c", code],
                           capture_output=True, text=True, timeout=20)
        if r.returncode == 0:
            if parse_json:
                try:
                    return json.loads(r.stdout.strip())
                except json.JSONDecodeError:
                    return {"raw": r.stdout.strip()[:500]}
            else:
                return {"content": r.stdout.strip()[:5000]}
        return {"error": r.stderr.strip()[:300]}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}


# ======================================================================
# PERSISTENT AGENT STATE — ~/.zion/agents/NAME.json
# ======================================================================

def load_agent_state(name):
    """Load persistent state for a single agent."""
    path = AGENTS_DIR / f"{name.upper()}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "name": name.upper(),
        "status": "idle",
        "pid": None,
        "deployed_at": None,
        "last_run": None,
        "last_result": None,
        "run_count": 0,
        "error_count": 0,
        "revenue_usd": 0.0,
        "revenue_events": [],
        "health": "unknown",
        "created": datetime.now(BRT).isoformat(),
    }


def save_agent_state(name, state):
    """Save persistent state for a single agent."""
    path = AGENTS_DIR / f"{name.upper()}.json"
    state["last_updated"] = datetime.now(BRT).isoformat()
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def load_city_state():
    """Load global city state."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "deployed": {},
        "total_deploys": 0,
        "total_revenue_usd": 0.0,
        "created": datetime.now(BRT).isoformat(),
    }


def save_city_state(state):
    """Save global city state."""
    state["last_updated"] = datetime.now(BRT).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


# ======================================================================
# INTER-AGENT MESSAGING — ~/.zion/shared/messages.json
# ======================================================================

def load_messages():
    """Load all inter-agent messages."""
    if MESSAGES_FILE.exists():
        try:
            return json.loads(MESSAGES_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"messages": []}


def save_messages(data):
    """Save messages, keeping only last 500."""
    data["messages"] = data["messages"][-500:]
    MESSAGES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def send_message(from_agent, to_agent, message, priority="normal"):
    """Send a message from one agent to another."""
    data = load_messages()
    data["messages"].append({
        "from": from_agent.upper(),
        "to": to_agent.upper(),
        "message": message,
        "priority": priority,
        "timestamp": datetime.now(BRT).isoformat(),
        "read": False,
    })
    save_messages(data)
    return True


def get_inbox(agent_name, unread_only=True):
    """Get messages for an agent."""
    data = load_messages()
    name = agent_name.upper()
    msgs = [m for m in data["messages"]
            if m["to"] == name and (not unread_only or not m.get("read"))]

    # Mark as read
    for m in data["messages"]:
        if m["to"] == name and not m.get("read"):
            m["read"] = True
    save_messages(data)
    return msgs


# ======================================================================
# REVENUE TRACKING — ~/.zion/revenue/revenue_log.json
# ======================================================================

def load_revenue():
    """Load revenue log."""
    if REVENUE_FILE.exists():
        try:
            return json.loads(REVENUE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"events": [], "total_usd": 0.0}


def save_revenue(data):
    REVENUE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def record_revenue(agent_name, amount_usd, source, description=""):
    """Record a revenue event from an agent."""
    data = load_revenue()
    event = {
        "agent": agent_name.upper(),
        "amount_usd": amount_usd,
        "source": source,
        "description": description,
        "timestamp": datetime.now(BRT).isoformat(),
    }
    data["events"].append(event)
    data["total_usd"] = sum(e["amount_usd"] for e in data["events"])
    data["events"] = data["events"][-1000:]
    save_revenue(data)

    # Also update agent state
    astate = load_agent_state(agent_name)
    astate["revenue_usd"] = astate.get("revenue_usd", 0) + amount_usd
    astate["revenue_events"].append(event)
    astate["revenue_events"] = astate["revenue_events"][-100:]
    save_agent_state(agent_name, astate)
    return event


# ======================================================================
# CRON SCHEDULE PARSER (lightweight)
# ======================================================================

def should_run_now(cron_expr):
    """
    Check if a cron expression matches the current time.
    Supports: */N, specific values, comma-separated, ranges, and *.
    Format: minute hour day_of_month month day_of_week
    """
    now = datetime.now(BRT)
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        return False

    fields = [
        (now.minute, 0, 59),     # minute
        (now.hour, 0, 23),       # hour
        (now.day, 1, 31),        # day of month
        (now.month, 1, 12),      # month
        (now.weekday(), 0, 6),   # day of week (0=Mon in Python but 0=Sun in cron)
    ]

    # Adjust: Python weekday() -> 0=Mon, cron -> 0=Sun
    # We convert Python to cron-style: 0=Sun,1=Mon,...6=Sat
    py_dow = now.isoweekday() % 7  # Sun=0, Mon=1, ... Sat=6
    fields[4] = (py_dow, 0, 6)

    for i, (current, low, high) in enumerate(fields):
        pattern = parts[i]
        if not _cron_field_matches(pattern, current, low, high):
            return False
    return True


def _cron_field_matches(pattern, current, low, high):
    """Check if a single cron field pattern matches the current value."""
    if pattern == "*":
        return True

    for part in pattern.split(","):
        # Handle */N
        if part.startswith("*/"):
            try:
                step = int(part[2:])
                if step > 0 and current % step == 0:
                    return True
            except ValueError:
                pass
        # Handle range N-M
        elif "-" in part:
            try:
                a, b = part.split("-", 1)
                if int(a) <= current <= int(b):
                    return True
            except ValueError:
                pass
        # Handle exact value
        else:
            try:
                if int(part) == current:
                    return True
            except ValueError:
                pass
    return False


# ======================================================================
# AGENT LOOKUP UTILITIES
# ======================================================================

def count_agents():
    total = 0
    for legion in LEGIONS.values():
        total += len(legion["agents"])
    return total


def get_agent(name):
    """Find an agent by name. Returns (legion_id, legion_dict, agent_dict) or (None, None, None)."""
    name_upper = name.upper().replace("-", "_")
    for lid, legion in LEGIONS.items():
        if name_upper in legion["agents"]:
            return lid, legion, legion["agents"][name_upper]
    return None, None, None


def get_all_agents():
    """Yield (name, legion_id, agent_dict) for all agents."""
    for lid, legion in LEGIONS.items():
        for aname, ainfo in legion["agents"].items():
            yield aname, lid, ainfo


def get_legion(lid_input):
    lid_upper = lid_input.upper()
    if lid_upper in LEGIONS:
        return LEGIONS[lid_upper]
    # Try partial match: "L1" -> "L1_CRYPTO"
    for key, val in LEGIONS.items():
        if key.startswith(lid_upper) or lid_upper in key:
            return val
    return None


def find_legion_id(lid_input):
    """Return the full legion ID from a partial input."""
    lid_upper = lid_input.upper()
    if lid_upper in LEGIONS:
        return lid_upper
    for key in LEGIONS:
        if key.startswith(lid_upper) or lid_upper in key:
            return key
    return None


# ======================================================================
# AGENT EXECUTION
# ======================================================================

def run_agent_once(name):
    """Execute an agent's primary task once (foreground)."""
    lid, legion, agent = get_agent(name)
    if not agent:
        print(f"  [ERROR] Agent '{name}' not found")
        return False

    name_upper = name.upper().replace("-", "_")
    astate = load_agent_state(name_upper)

    print(f"\n  [ZION] Executing {name_upper} -- {agent['role']}")
    print(f"    Skill: {agent['skill']}")
    print(f"    Tools: {', '.join(agent['tools'])}")
    print(f"    Schedule: {agent.get('schedule', 'manual')}")

    results = {}
    success = True
    for tool in agent["tools"]:
        print(f"    Running tool: {tool}...", end=" ", flush=True)
        try:
            result = execute_tool(tool)
            results[tool] = result
            has_error = isinstance(result, dict) and "error" in result
            print("ERROR" if has_error else "OK")
            if has_error:
                success = False
        except Exception as e:
            results[tool] = {"error": str(e)}
            print(f"FAIL: {e}")
            success = False

    # Print results summary
    print(f"\n    Results:")
    for tool, result in results.items():
        if isinstance(result, dict):
            if "error" in result:
                print(f"      [{tool}] ERROR: {result['error'][:80]}")
            else:
                preview = json.dumps(result)[:150]
                print(f"      [{tool}] {preview}")
        else:
            print(f"      [{tool}] {str(result)[:150]}")

    # Update agent state
    astate["last_run"] = datetime.now(BRT).isoformat()
    astate["run_count"] = astate.get("run_count", 0) + 1
    astate["last_result"] = "success" if success else "error"
    astate["status"] = "active"
    astate["health"] = "healthy" if success else "degraded"
    if not success:
        astate["error_count"] = astate.get("error_count", 0) + 1
    save_agent_state(name_upper, astate)

    # Notify commander via message
    commander = legion.get("commander", "CALEV")
    if name_upper != commander:
        send_message(name_upper, commander,
                     f"Task complete: {'OK' if success else 'ERRORS'} | tools={len(results)}")

    print(f"\n    [{name_upper}] {'Mission complete' if success else 'Completed with errors'}.")
    return success


# ======================================================================
# DEPLOY / STOP — Background Agent Processes
# ======================================================================

_AGENT_RUNNER_SCRIPT = """
#!/usr/bin/env python3
\"\"\"Background runner for ZION agent: {name}. Auto-generated.\"\"\"
import sys, os, time, json, random
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
AGENT_NAME = "{name}"
ZION_DIR = Path.home() / ".zion"
STATE_PATH = ZION_DIR / "agents" / f"{{AGENT_NAME}}.json"
LOG_PATH = ZION_DIR / "logs" / f"{{AGENT_NAME}}.log"
PID_PATH = ZION_DIR / "pids" / f"{{AGENT_NAME}}.pid"

# Write PID
PID_PATH.write_text(str(os.getpid()))

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"{{ts}} [{{AGENT_NAME}}] {{msg}}\\n"
    try:
        with open(str(LOG_PATH), "a") as f:
            f.write(line)
    except:
        pass

def load_state():
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except:
            pass
    return {{"name": AGENT_NAME, "status": "running", "pid": os.getpid()}}

def save_state(s):
    s["last_updated"] = datetime.now(BRT).isoformat()
    STATE_PATH.write_text(json.dumps(s, indent=2))

log(f"Agent started (PID {{os.getpid()}})")
state = load_state()
state["status"] = "running"
state["pid"] = os.getpid()
state["deployed_at"] = datetime.now(BRT).isoformat()
save_state(state)

# Main loop: run every cycle based on schedule
CYCLE_SECONDS = {cycle_seconds}

while True:
    try:
        log("Heartbeat alive")
        state = load_state()
        state["health"] = "healthy"
        state["status"] = "running"
        state["pid"] = os.getpid()
        save_state(state)
    except Exception as e:
        log(f"Error: {{e}}")
    time.sleep(CYCLE_SECONDS + random.randint(0, 30))
"""


def _schedule_to_seconds(cron_expr):
    """Convert cron schedule to approximate sleep seconds for the background loop."""
    parts = cron_expr.strip().split()
    if len(parts) < 2:
        return 3600

    minute_part = parts[0]
    hour_part = parts[1]

    # Check minute step: */N
    if minute_part.startswith("*/"):
        try:
            return int(minute_part[2:]) * 60
        except ValueError:
            pass

    # Check hour step: */N in hour field with minute=0
    if hour_part.startswith("*/"):
        try:
            return int(hour_part[2:]) * 3600
        except ValueError:
            pass

    # Comma-separated hours = run at those specific hours
    if "," in hour_part:
        count = len(hour_part.split(","))
        return max(3600, 86400 // max(count, 1))

    # Once a day / once a week
    return 3600  # Default: check every hour


def deploy_agent(name):
    """Deploy a single agent as a background process."""
    lid, legion, agent = get_agent(name)
    if not agent:
        print(f"    [ERROR] Agent '{name}' not found")
        return False

    name_upper = name.upper().replace("-", "_")
    pid_file = PIDS_DIR / f"{name_upper}.pid"

    # Check if already running
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            if os.path.exists(f"/proc/{pid}"):
                print(f"    [{name_upper}] Already running (PID {pid})")
                return True
        except (ValueError, OSError):
            pass

    schedule = agent.get("schedule", "0 */4 * * *")
    cycle_seconds = _schedule_to_seconds(schedule)

    # Generate runner script
    script_content = _AGENT_RUNNER_SCRIPT.format(
        name=name_upper,
        cycle_seconds=cycle_seconds,
    )
    script_path = ZION_DIR / "runners" / f"{name_upper}_runner.py"
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(script_content)

    # Launch as background process
    log_path = LOGS_DIR / f"{name_upper}.log"
    try:
        proc = subprocess.Popen(
            ["python3", str(script_path)],
            stdout=open(str(log_path), "a"),
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        # Update agent state
        astate = load_agent_state(name_upper)
        astate["status"] = "running"
        astate["pid"] = proc.pid
        astate["deployed_at"] = datetime.now(BRT).isoformat()
        astate["health"] = "healthy"
        save_agent_state(name_upper, astate)

        pid_file.write_text(str(proc.pid))
        return True

    except Exception as e:
        print(f"    [{name_upper}] Deploy FAILED: {e}")
        return False


def stop_agent(name):
    """Stop a running agent."""
    name_upper = name.upper().replace("-", "_")
    pid_file = PIDS_DIR / f"{name_upper}.pid"

    if not pid_file.exists():
        print(f"    [{name_upper}] Not deployed (no PID file)")
        return False

    try:
        pid = int(pid_file.read_text().strip())
        if os.path.exists(f"/proc/{pid}"):
            os.kill(pid, signal.SIGTERM)
            # Wait briefly then force kill if needed
            time.sleep(0.3)
            if os.path.exists(f"/proc/{pid}"):
                os.kill(pid, signal.SIGKILL)
        pid_file.unlink(missing_ok=True)

        astate = load_agent_state(name_upper)
        astate["status"] = "stopped"
        astate["pid"] = None
        astate["health"] = "stopped"
        save_agent_state(name_upper, astate)

        return True
    except (ProcessLookupError, ValueError, OSError):
        pid_file.unlink(missing_ok=True)
        return True


def is_agent_alive(name):
    """Check if an agent process is alive."""
    name_upper = name.upper().replace("-", "_")
    pid_file = PIDS_DIR / f"{name_upper}.pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            return os.path.exists(f"/proc/{pid}")
        except (ValueError, OSError):
            pass
    return False


def is_daemon_running():
    """Check if the Israel/One daemon is running."""
    pid_file = Path.home() / "israel-one" / ".israel.pid"
    if pid_file.exists():
        try:
            pid = pid_file.read_text().strip()
            return os.path.exists(f"/proc/{pid}")
        except OSError:
            pass
    return False


# ======================================================================
# HEALTH MONITORING
# ======================================================================

def health_check_all():
    """Check health of all agents and restart dead ones."""
    print("\n  ZION HEALTH CHECK")
    print("  " + "=" * 60)

    alive = 0
    dead = 0
    idle = 0
    restarted = 0

    for aname, lid, ainfo in get_all_agents():
        astate = load_agent_state(aname)
        was_deployed = astate.get("status") == "running" or astate.get("pid")
        is_alive = is_agent_alive(aname)

        if was_deployed and not is_alive:
            # Dead agent that should be running — restart
            print(f"    [{aname:15s}] DEAD — restarting...", end=" ", flush=True)
            if deploy_agent(aname):
                print("RESTARTED")
                restarted += 1
                alive += 1
            else:
                print("FAILED")
                dead += 1
        elif is_alive:
            alive += 1
        else:
            idle += 1

    print(f"\n  Summary: {alive} alive | {dead} dead | {idle} idle | {restarted} restarted")
    print(f"  Total agents: {count_agents()}")
    return {"alive": alive, "dead": dead, "idle": idle, "restarted": restarted}


# ======================================================================
# CLI — STATUS / DASHBOARD / DEPLOY / etc.
# ======================================================================

def print_status():
    """Print status of all legions and agents."""
    total = count_agents()
    city = load_city_state()

    total_alive = sum(1 for n, _, _ in get_all_agents() if is_agent_alive(n))

    print()
    print("=" * 72)
    print(f"  ZION CITY -- {total} Agents | {len(LEGIONS)} Legions | {total_alive} Running")
    print(f"  Em nome do Senhor Jesus Cristo")
    print("=" * 72)

    for lid, legion in LEGIONS.items():
        cmd = legion["commander"]
        n = len(legion["agents"])
        alive_in = sum(1 for a in legion["agents"] if is_agent_alive(a))
        if alive_in == n:
            status = "ALL ACTIVE"
        elif alive_in > 0:
            status = f"{alive_in}/{n} ACTIVE"
        else:
            status = "STANDBY"

        print(f"\n  [{lid}] {legion['name']} -- Commander: {cmd} | {n} agents | {status}")
        print(f"  Mission: {legion['mission']}")

        for aname, ainfo in legion["agents"].items():
            marker = ">" if aname == cmd else " "
            alive = is_agent_alive(aname)
            astate = load_agent_state(aname)
            runs = astate.get("run_count", 0)
            rev = astate.get("revenue_usd", 0)

            if alive:
                icon = "R"  # Running
            elif astate.get("status") == "stopped":
                icon = "S"  # Stopped
            elif runs > 0:
                icon = "I"  # Idle but has run before
            else:
                icon = "."  # Never deployed

            rev_str = f"${rev:.0f}" if rev > 0 else ""
            sched = ainfo.get("schedule", "")
            print(f"    {marker} [{icon}] {aname:15s} | {ainfo['role']:22s} | {sched:16s} | {rev_str}")

    print(f"\n{'=' * 72}")
    daemon_str = "RUNNING" if is_daemon_running() else "STOPPED"
    print(f"  TOTAL: {total} agents | Running: {total_alive} | Daemon: {daemon_str}")
    rev_data = load_revenue()
    print(f"  Total Revenue: ${rev_data.get('total_usd', 0):,.2f}")
    print(f"{'=' * 72}")


def print_dashboard():
    """Print beautiful ASCII dashboard."""
    total = count_agents()
    now = datetime.now(BRT)

    # Collect stats
    total_alive = 0
    total_runs = 0
    total_errors = 0
    total_revenue = 0.0
    legion_stats = {}

    for lid, legion in LEGIONS.items():
        ls = {"alive": 0, "total": len(legion["agents"]), "runs": 0, "errors": 0, "revenue": 0.0}
        for aname in legion["agents"]:
            astate = load_agent_state(aname)
            if is_agent_alive(aname):
                ls["alive"] += 1
                total_alive += 1
            ls["runs"] += astate.get("run_count", 0)
            ls["errors"] += astate.get("error_count", 0)
            ls["revenue"] += astate.get("revenue_usd", 0)
            total_runs += astate.get("run_count", 0)
            total_errors += astate.get("error_count", 0)
            total_revenue += astate.get("revenue_usd", 0)
        legion_stats[lid] = ls

    rev_data = load_revenue()
    total_revenue = rev_data.get("total_usd", total_revenue)

    # RAM info
    ram_info = "?"
    try:
        with open("/proc/meminfo") as f:
            lines = f.readlines()
        mem_total = int([l for l in lines if l.startswith("MemTotal")][0].split()[1]) // 1024
        mem_avail = int([l for l in lines if l.startswith("MemAvailable")][0].split()[1]) // 1024
        ram_info = f"{mem_avail}MB free / {mem_total}MB total"
    except Exception:
        pass

    # Build dashboard
    W = 74
    bar = "=" * W
    thin = "-" * W

    print()
    print(f"+{bar}+")
    print(f"|{'ZION CITY DASHBOARD':^{W}}|")
    print(f"|{'Em nome do Senhor Jesus Cristo':^{W}}|")
    print(f"+{bar}+")
    print(f"|  Date: {now.strftime('%Y-%m-%d %H:%M BRT'):<30s}  RAM: {ram_info:>25s}  |")
    print(f"|  Daemon: {'ONLINE' if is_daemon_running() else 'OFFLINE':<15s}  Agents: {total_alive}/{total} running{'':>17s}|")
    print(f"+{bar}+")

    # Revenue box
    print(f"|  {'REVENUE':^{W-4}}  |")
    print(f"|  {thin[:-4]}  |")
    print(f"|  Total: ${total_revenue:>12,.2f}   |   Runs: {total_runs:>6d}   |   Errors: {total_errors:>5d}{'':>12s}|")
    print(f"+{bar}+")

    # Legion grid
    print(f"|  {'LEGION STATUS':^{W-4}}  |")
    print(f"|  {thin[:-4]}  |")

    for lid, ls in legion_stats.items():
        legion = LEGIONS[lid]
        pct = (ls["alive"] / ls["total"] * 100) if ls["total"] > 0 else 0
        bar_len = int(pct / 5)  # 20 char max bar
        bar_fill = "#" * bar_len + "." * (20 - bar_len)

        rev_str = f"${ls['revenue']:>8,.0f}" if ls['revenue'] > 0 else "$       0"
        line = f"  {lid:15s} [{bar_fill}] {ls['alive']:>2d}/{ls['total']:>2d}  {rev_str}  R:{ls['runs']:>4d}"
        padding = W - len(line) - 2
        if padding < 0:
            padding = 0
        print(f"|{line}{' ' * padding}  |")

    print(f"+{bar}+")

    # Top agents by runs
    agent_runs = []
    for aname, lid, ainfo in get_all_agents():
        astate = load_agent_state(aname)
        if astate.get("run_count", 0) > 0:
            agent_runs.append((aname, astate.get("run_count", 0), astate.get("revenue_usd", 0)))

    if agent_runs:
        agent_runs.sort(key=lambda x: -x[1])
        print(f"|  {'TOP AGENTS (by runs)':^{W-4}}  |")
        print(f"|  {thin[:-4]}  |")
        for aname, runs, rev in agent_runs[:10]:
            alive = "R" if is_agent_alive(aname) else "."
            line = f"  [{alive}] {aname:15s}  runs:{runs:>5d}  revenue:${rev:>10,.2f}"
            padding = W - len(line) - 2
            if padding < 0:
                padding = 0
            print(f"|{line}{' ' * padding}  |")

    print(f"+{bar}+")

    # Recent messages
    msg_data = load_messages()
    recent_msgs = msg_data.get("messages", [])[-5:]
    if recent_msgs:
        print(f"|  {'RECENT MESSAGES':^{W-4}}  |")
        print(f"|  {thin[:-4]}  |")
        for m in recent_msgs:
            ts = m.get("timestamp", "")[-8:]
            line = f"  {ts} {m['from']:>10s} -> {m['to']:<10s}: {m['message'][:30]}"
            padding = W - len(line) - 2
            if padding < 0:
                padding = 0
            print(f"|{line}{' ' * padding}  |")

    print(f"+{bar}+")
    print()


def print_agent_detail(name):
    """Print detailed info about a single agent."""
    lid, legion, agent = get_agent(name)
    if not agent:
        print(f"  Agent '{name}' not found")
        return

    name_upper = name.upper().replace("-", "_")
    astate = load_agent_state(name_upper)
    alive = is_agent_alive(name_upper)
    msgs = get_inbox(name_upper, unread_only=False)

    print(f"\n{'=' * 55}")
    print(f"  AGENT: {name_upper}")
    print(f"{'=' * 55}")
    print(f"  Legion:         {legion['name']} ({lid})")
    print(f"  Commander:      {legion['commander']}")
    print(f"  Role:           {agent['role']}")
    print(f"  Skill:          {agent['skill']}")
    print(f"  Tools:          {', '.join(agent['tools'])}")
    print(f"  Schedule:       {agent.get('schedule', 'manual')}")
    print(f"  Responsibility: {agent['responsibility']}")
    print(f"  ---")
    print(f"  Status:         {'RUNNING' if alive else astate.get('status', 'idle')}")
    print(f"  PID:            {astate.get('pid', '-')}")
    print(f"  Health:         {astate.get('health', 'unknown')}")
    print(f"  Deployed at:    {astate.get('deployed_at', 'never')}")
    print(f"  Last run:       {astate.get('last_run', 'never')}")
    print(f"  Run count:      {astate.get('run_count', 0)}")
    print(f"  Error count:    {astate.get('error_count', 0)}")
    print(f"  Revenue:        ${astate.get('revenue_usd', 0):,.2f}")
    print(f"  Messages:       {len(msgs)} in inbox")
    print(f"{'=' * 55}")

    if msgs:
        print(f"\n  Latest messages:")
        for m in msgs[-5:]:
            rd = "R" if m.get("read") else "U"
            print(f"    [{rd}] {m['from']} ({m.get('priority','normal')}): {m['message'][:60]}")


def print_legion_detail(lid_input):
    """Print detailed info about a legion."""
    full_lid = find_legion_id(lid_input)
    legion = get_legion(lid_input)
    if not legion:
        print(f"  Legion '{lid_input}' not found")
        return

    alive_count = sum(1 for a in legion["agents"] if is_agent_alive(a))
    total_runs = sum(load_agent_state(a).get("run_count", 0) for a in legion["agents"])
    total_rev = sum(load_agent_state(a).get("revenue_usd", 0) for a in legion["agents"])

    print(f"\n{'=' * 60}")
    print(f"  LEGION: {legion['name']} ({full_lid})")
    print(f"{'=' * 60}")
    print(f"  Commander:    {legion['commander']}")
    print(f"  Mission:      {legion['mission']}")
    print(f"  Agents:       {len(legion['agents'])} ({alive_count} running)")
    print(f"  Total runs:   {total_runs}")
    print(f"  Revenue:      ${total_rev:,.2f}")
    print(f"{'=' * 60}")

    for aname, ainfo in legion["agents"].items():
        astate = load_agent_state(aname)
        alive = is_agent_alive(aname)
        icon = "R" if alive else ("." if astate.get("run_count", 0) == 0 else "I")
        sched = ainfo.get("schedule", "manual")
        runs = astate.get("run_count", 0)
        rev = astate.get("revenue_usd", 0)

        print(f"\n  [{icon}] {aname}")
        print(f"      Role:     {ainfo['role']}")
        print(f"      Skill:    {ainfo['skill']}")
        print(f"      Tools:    {', '.join(ainfo['tools'])}")
        print(f"      Schedule: {sched}")
        print(f"      Runs:     {runs} | Revenue: ${rev:,.2f}")
        print(f"      Task:     {ainfo['responsibility']}")


def print_revenue():
    """Print revenue dashboard."""
    rev_data = load_revenue()
    events = rev_data.get("events", [])
    total = rev_data.get("total_usd", 0)

    print(f"\n{'=' * 60}")
    print(f"  ZION REVENUE TRACKER")
    print(f"{'=' * 60}")
    print(f"  Total Revenue: ${total:>12,.2f}")
    print(f"  Events:        {len(events)}")
    print(f"{'=' * 60}")

    # By agent
    by_agent = {}
    for e in events:
        a = e.get("agent", "UNKNOWN")
        by_agent[a] = by_agent.get(a, 0) + e.get("amount_usd", 0)

    if by_agent:
        print(f"\n  Revenue by Agent:")
        for a, rev in sorted(by_agent.items(), key=lambda x: -x[1]):
            print(f"    {a:15s}  ${rev:>12,.2f}")

    # By source
    by_source = {}
    for e in events:
        s = e.get("source", "unknown")
        by_source[s] = by_source.get(s, 0) + e.get("amount_usd", 0)

    if by_source:
        print(f"\n  Revenue by Source:")
        for s, rev in sorted(by_source.items(), key=lambda x: -x[1]):
            print(f"    {s:20s}  ${rev:>12,.2f}")

    # Recent events
    if events:
        print(f"\n  Recent Events:")
        for e in events[-10:]:
            ts = e.get("timestamp", "")[:16]
            print(f"    {ts}  {e.get('agent','?'):12s}  ${e.get('amount_usd',0):>10,.2f}  {e.get('source','')}")

    print(f"\n{'=' * 60}")


def cmd_deploy(target=None):
    """Deploy agents. If target is given, deploy only that legion or agent."""
    if target:
        # Check if it's a legion
        full_lid = find_legion_id(target)
        if full_lid:
            legion = LEGIONS[full_lid]
            print(f"\n  [ZION] Deploying {legion['name']} ({len(legion['agents'])} agents)...")
            deployed = 0
            for aname in legion["agents"]:
                print(f"    Deploying {aname}...", end=" ", flush=True)
                if deploy_agent(aname):
                    print("OK")
                    deployed += 1
                else:
                    print("FAILED")
            print(f"\n  [{full_lid}] {deployed}/{len(legion['agents'])} agents deployed")
            return

        # Check if it's a single agent
        lid, legion, agent = get_agent(target)
        if agent:
            name_upper = target.upper().replace("-", "_")
            print(f"\n  [ZION] Deploying {name_upper}...", end=" ", flush=True)
            if deploy_agent(name_upper):
                print("OK")
            else:
                print("FAILED")
            return

        print(f"  [ERROR] '{target}' is not a valid legion or agent name")
        return

    # Deploy all
    total = count_agents()
    print(f"\n  [ZION] Deploying all {total} agents across {len(LEGIONS)} legions...")
    print(f"  WARNING: This will start {total} background processes.")
    print(f"  RAM available check in progress...\n")

    # Check RAM before mass deploy
    try:
        with open("/proc/meminfo") as f:
            lines = f.readlines()
        mem_avail = int([l for l in lines if l.startswith("MemAvailable")][0].split()[1]) // 1024
        if mem_avail < 500:
            print(f"  [WARNING] Only {mem_avail}MB RAM available. Deploying in light mode (heartbeat only).")
    except Exception:
        pass

    deployed = 0
    for lid, legion in LEGIONS.items():
        print(f"\n  Deploying {legion['name']}...")
        for aname in legion["agents"]:
            print(f"    [{aname:15s}]", end=" ", flush=True)
            if deploy_agent(aname):
                print("DEPLOYED")
                deployed += 1
            else:
                print("FAILED")

    # Update city state
    city = load_city_state()
    city["total_deploys"] = city.get("total_deploys", 0) + 1
    save_city_state(city)

    print(f"\n  [ZION] Deployment complete: {deployed}/{total} agents running")


def cmd_stop(target=None):
    """Stop agents."""
    if target:
        # Single agent
        lid, legion, agent = get_agent(target)
        if agent:
            name_upper = target.upper().replace("-", "_")
            print(f"  Stopping {name_upper}...", end=" ", flush=True)
            if stop_agent(name_upper):
                print("STOPPED")
            else:
                print("FAILED")
            return

        # Legion
        full_lid = find_legion_id(target)
        if full_lid:
            legion = LEGIONS[full_lid]
            print(f"\n  Stopping {legion['name']}...")
            for aname in legion["agents"]:
                print(f"    Stopping {aname}...", end=" ", flush=True)
                if stop_agent(aname):
                    print("STOPPED")
                else:
                    print("FAILED")
            return

        print(f"  [ERROR] '{target}' not found")
        return

    # Stop all
    print(f"\n  [ZION] Stopping all agents...")
    stopped = 0
    for aname, lid, ainfo in get_all_agents():
        if is_agent_alive(aname):
            if stop_agent(aname):
                stopped += 1
                print(f"    [{aname}] STOPPED")
    print(f"\n  Stopped {stopped} agents")


# ======================================================================
# MAIN CLI
# ======================================================================

USAGE = """
Usage: python3 zion_city.py <command> [args]

Commands:
  status                  Show all agents and legions
  dashboard               Beautiful ASCII dashboard
  deploy [LEGION|AGENT]   Deploy agents (all, a legion, or one agent)
  stop [LEGION|AGENT]     Stop agents
  run AGENT               Execute agent's task once (foreground)
  health                  Health check all agents, restart dead ones
  revenue                 Revenue tracking dashboard
  revenue add AGENT AMT SOURCE DESC   Record revenue event
  agent AGENT             Show detailed agent info
  legion LEGION           Show detailed legion info
  msg FROM TO "message"   Send inter-agent message
  inbox AGENT             Check agent's message inbox
  count                   Count total agents
  schedule                Show all agent schedules
  due                     Show agents whose schedule is due now
"""


def cmd_schedule():
    """Show all agent schedules."""
    print(f"\n  ZION AGENT SCHEDULES")
    print(f"  {'=' * 62}")
    for lid, legion in LEGIONS.items():
        print(f"\n  [{lid}] {legion['name']}")
        for aname, ainfo in legion["agents"].items():
            sched = ainfo.get("schedule", "manual")
            due = "DUE NOW" if should_run_now(sched) else ""
            alive = "R" if is_agent_alive(aname) else "."
            print(f"    [{alive}] {aname:15s}  {sched:18s}  {due}")


def cmd_due():
    """Show agents whose schedule matches right now."""
    now = datetime.now(BRT)
    print(f"\n  Agents DUE at {now.strftime('%H:%M BRT')}:")
    print(f"  {'=' * 50}")
    count = 0
    for aname, lid, ainfo in get_all_agents():
        sched = ainfo.get("schedule", "")
        if sched and should_run_now(sched):
            alive = "R" if is_agent_alive(aname) else "."
            print(f"    [{alive}] {aname:15s}  ({ainfo['role']})  [{sched}]")
            count += 1
    if count == 0:
        print(f"    No agents due right now.")
    print(f"\n  Total: {count} agents due")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "status":
        print_status()

    elif args[0] == "dashboard":
        print_dashboard()

    elif args[0] == "deploy":
        target = args[1] if len(args) > 1 else None
        cmd_deploy(target)

    elif args[0] == "stop":
        target = args[1] if len(args) > 1 else None
        cmd_stop(target)

    elif args[0] == "run" and len(args) > 1:
        run_agent_once(args[1])

    elif args[0] == "health":
        health_check_all()

    elif args[0] == "revenue":
        if len(args) >= 5 and args[1] == "add":
            # revenue add AGENT AMOUNT SOURCE [DESC]
            agent_name = args[2]
            amount = float(args[3])
            source = args[4]
            desc = args[5] if len(args) > 5 else ""
            event = record_revenue(agent_name, amount, source, desc)
            print(f"  Revenue recorded: {agent_name} +${amount:,.2f} from {source}")
        else:
            print_revenue()

    elif args[0] == "agent" and len(args) > 1:
        print_agent_detail(args[1])

    elif args[0] == "legion" and len(args) > 1:
        print_legion_detail(args[1])

    elif args[0] == "msg" and len(args) >= 4:
        from_a = args[1]
        to_a = args[2]
        msg = " ".join(args[3:])
        send_message(from_a, to_a, msg)
        print(f"  Message sent: {from_a.upper()} -> {to_a.upper()}: {msg}")

    elif args[0] == "inbox" and len(args) > 1:
        msgs = get_inbox(args[1], unread_only=False)
        name_upper = args[1].upper()
        print(f"\n  INBOX for {name_upper} ({len(msgs)} messages)")
        print(f"  {'=' * 50}")
        for m in msgs[-20:]:
            rd = " " if m.get("read") else "*"
            pri = m.get("priority", "normal")
            ts = m.get("timestamp", "")[-8:]
            print(f"  {rd} [{ts}] {m['from']:>12s} ({pri}): {m['message'][:50]}")
        if not msgs:
            print(f"  (empty)")

    elif args[0] == "count":
        print(f"  Total agents: {count_agents()}")

    elif args[0] == "schedule":
        cmd_schedule()

    elif args[0] == "due":
        cmd_due()

    else:
        print(USAGE)
