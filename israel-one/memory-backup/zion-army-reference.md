# ZION Army Reference — 1001 Agentes (25 Mar 2026)

## Files
- `~/israel-one/zion_army_1001.py` — 1001 agentes, 30 departamentos
- `~/israel-one/padrao_bitcoin_corp.py` — 48 agentes core, Gov APIs, revenue pipeline
- `~/israel-one/zion_city.py` — 100 agentes v2 (deploy real, messaging, revenue)
- `~/israel-one/agent.py` — Israel/One Twitter daemon (RUNNING)
- `~/israel-one/zion_agent_framework.py` — Base framework (ToolRegistry, Skills)
- `~/israel-one/agent_soul_architecture.py` — Soul, Memory, Network classes

## Commands
```
python3 zion_army_1001.py count          # 1001 agents
python3 zion_army_1001.py status         # Dashboard
python3 zion_army_1001.py deploy         # Deploy all
python3 zion_army_1001.py dept DEPT      # Department detail
python3 zion_army_1001.py agent NAME     # Agent detail
python3 zion_army_1001.py run NAME       # Execute agent
python3 zion_army_1001.py swarm DEPT     # Run 5 agents from dept
python3 zion_army_1001.py search WORD    # Search agents
python3 zion_army_1001.py roster         # Full roster

python3 padrao_bitcoin_corp.py status    # Corp dashboard
python3 padrao_bitcoin_corp.py health    # System health
python3 padrao_bitcoin_corp.py apis      # Gov APIs
python3 padrao_bitcoin_corp.py revenue   # Revenue pipeline
```

## 30 Departments
1-6 CORE: CRYPTO_MARKETS, DEFI_PROTOCOLS, SECURITY_AUDIT, BOUNTY_HUNTING, SOFTWARE_DEV, MCP_DEVELOPMENT
7-10 SALES: SALES, MARKETPLACE, PARTNERSHIPS, ENTERPRISE
11-15 MARKETING: CONTENT, SOCIAL_MEDIA, SEO, GROWTH_HACKING, BRAND
16-19 INTEL: MARKET_INTEL, GOVERNMENT_DATA, OSINT, TREND_ANALYSIS
20-23 FINANCE: FISCAL, TREASURY, INVOICING, LEGAL
24-27 ENGINEERING: FRONTEND, BACKEND, DEVOPS, AI_ML
28-30 COMMAND: COMMAND, QUALITY, KNOWLEDGE

## Key Agents
- BARUK: Chief Market Analyst (crypto_price, fear_greed)
- SAMAEL: Chief Security Officer
- DAVI: Chief Bounty Hunter
- CALEV: Supreme Commander
- ISRAEL_ONE: Twitter Sentinela (RUNNING)
- MATEUS: CFO / Contador
- MIKAEL: Government Data (BCB, IBGE, Transparencia APIs)

## Cloned Repos Knowledge (Extracted 25 Mar 2026)
- agency-agents: 90+ agent prompts (MD format), 6 departments
- everything-claude-code: 25 agents, 90+ skills, 57 commands — INSTALL THESE
- goat: 200+ onchain tools, 14 chains, MCP adapter — INTEGRATE
- solana-agent-kit: 60+ Solana actions (Jupiter, Drift, Pump.fun)
- system-prompts-and-models: Manus, Cursor, Devin prompts — competitive intel
- awesome-llm-apps: 70+ apps, finance agents, LLM cost optimizer
- 500-AI-Agents-Projects: 500+ use cases across 30 industries
- claude-code-is-programmable: CLI patterns, --allowedTools, voice
- archestra: Dual LLM security, 96% cost optimizer
- agenticSeek: Agent routing, stealth browser

## Resource Distribution System (25 Mar 2026)
- `~/israel-one/zion_resources.py` — Distribui MCPs, skills, tools, repos, memórias
- **7 MCPs**: claw-mcp-toolkit (29 tools), mcp-crypto-prices (6), openclaw-webtools (8), firefox-devtools (4), twitter (4), filesystem (4), sequential-thinking (1)
- **54 skills** em 7 categorias: ENGINEERING, AI_ML, BUSINESS, SECURITY, MARKETING, FINANCE, COMMAND
- **81 repos git** categorizados por departamento
- **18 memory files** compartilhados
- **14 Gov APIs** (BCB Selic/IPCA/PTAX, BrasilAPI, OpenCNPJ, IBGE, Transparência, CVM, Sebrae NFe)
- **X/Twitter feed**: Posts do Israel/One alimentam todos agentes via `~/.zion/feeds/x_feed.json`
- Comandos: `python3 zion_resources.py [distribute|agent NAME|dept DEPT|mcps|repos|skills|feed|update|sync]`
- **2,799 MCP assignments**, **12,155 skill assignments**, **8,011 repo assignments** distribuídos

## State Dir: ~/.zion/ (4.1MB)
- agents/: 1001 JSON state files com resources embedded
- shared/: distribution_manifest.json, knowledge_index.json, messages
- feeds/: x_feed.json (posts do Twitter para alimentar agentes)
- logs/: Agent logs
- revenue/: Revenue events
