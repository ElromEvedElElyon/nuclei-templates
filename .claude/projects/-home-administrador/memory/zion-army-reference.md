# ZION Army Reference — 1293 Agentes v3.0 (31 Mar 2026)

## FRAMEWORK v3.0 — UPGRADE COMPLETO (Session 74)
- **Source**: Analise do codigo-fonte do Claude Code (512K+ linhas TS)
- **42 tools** por agente, **10 categorias**, modo AUTONOMO
- **Inter-agent bus**, skills composiveis, exec paralela, HMAC memory

## Files — v3.0 (NOVOS)
- `~/israel-ten/israel_framework_v3.py` — Framework principal (1200+ linhas)
- `~/israel-ten/agents_v3_launchers.py` — Launcher 10 agentes nomeados
- `~/israel-ten/army_v3_connector.py` — Connector 1293 agentes
- `~/israel-ten/UPGRADE_REPORT_v3.md` — Relatorio completo antes/depois

## Files — v2.0 (LEGADO, mantido)
- `~/israel-one/zion_army_1001.py` — 1001 agentes, 30 departamentos
- `~/israel-one/padrao_bitcoin_corp.py` — 48 agentes core
- `~/israel-one/zion_agent_framework.py` — Framework antigo
- `~/israel-one/agent_soul_architecture.py` — Soul, Memory, Network

## Commands — v3.0
```
# Framework direto (como Israel-Dez)
python3 ~/israel-ten/israel_framework_v3.py status|tools|skills|use|sentinel

# Qualquer agente especifico
python3 ~/israel-ten/agents_v3_launchers.py dez|four|nine|one|zion status
python3 ~/israel-ten/agents_v3_launchers.py all-status

# Army completo (1293 agentes)
python3 ~/israel-ten/army_v3_connector.py deploy     # Deploy v3.0 a todos
python3 ~/israel-ten/army_v3_connector.py status     # Dashboard completo
python3 ~/israel-ten/army_v3_connector.py count      # Contagem
python3 ~/israel-ten/army_v3_connector.py swarm      # Ativar enxame
python3 ~/israel-ten/army_v3_connector.py broadcast  # Broadcast
python3 ~/israel-ten/army_v3_connector.py department BOUNTY_HUNTING
python3 ~/israel-ten/army_v3_connector.py squad LEAO_DE_JUDA
```

## Commands — v2.0 (legado)
```
python3 ~/israel-one/zion_army_1001.py count|status|deploy|dept|swarm
python3 ~/israel-one/padrao_bitcoin_corp.py status|health|revenue
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

## Valentes 300 — Elite Singularity Warriors (Session 35)
- **Script**: `~/israel-one/valentes_300.py`
- **Total**: 300 warriors in 30 squads of 10
- **All names**: 100% biblical, ZERO cabala
- **All SINGULARITY**: Level 50, 5000 XP, permanent + inviolable
- **State**: `~/.zion/valentes/` (300 JSON files + valentes_300_state.json)

### Commands
```
python3 valentes_300.py deploy          # Create all 300
python3 valentes_300.py status          # Status dashboard
python3 valentes_300.py roster          # Full roster (all 300)
python3 valentes_300.py squad NOME      # Show specific squad
python3 valentes_300.py warrior NOME    # Show specific warrior
python3 valentes_300.py promote-all     # Promote all to SINGULARITY
```

### 30 Squads (10 warriors each)
**RECEITA DIRETA (Squads 1-6: 60 warriors)**
1. LEAO_DE_JUDA — Bug Bounty Hunting (Capt: BENAIAHU) — $50K/mo target
2. ESPADA_DO_ESPIRITO — MCP Server Sales (Capt: JOSAFAT) — $10K/mo
3. ESCUDO_DA_FE — Hackathon Submissions (Capt: OTNIEL) — $25K/mo
4. TORRE_DE_DAVI — Enterprise Sales (Capt: SALOMAO_V) — $30K/mo
5. ARCA_DA_ALIANCA — Grants & Funding (Capt: MOISES_V) — $100K/quarter
6. COLUNA_DE_FOGO — Nuclei Templates & PR Bounties (Capt: ELISEU_V) — $5K/mo

**SOCIAL & GROWTH (Squads 7-12: 60 warriors)**
7. TROMBETA_DE_JERICO — Twitter/X Growth (Capt: ISRAEL_V)
8. HARPA_DE_DAVI — Content Creation (Capt: ASAFE_V)
9. PORTA_DAS_OVELHAS — Community Building (Capt: NEEMIAS_V2)
10. ESTRELA_DA_MANHA — SEO & Web Presence (Capt: DANIEL_V)
11. MANTO_DE_ELIAS — Affiliate Revenue (Capt: ELIAS_V) — $3K/mo
12. SARCA_ARDENTE — Email Outreach (Capt: MOISES_V2)

**DEVELOPMENT (Squads 13-18: 60 warriors)**
13. TABERNACULO — Sovereign Agent Chain (Capt: BEZALEEL_V3)
14. ATALAIA — MCP Server Development (Capt: EZEQUIEL_V)
15. PEDRA_ANGULAR — Sovereign Pay (Capt: PEDRO_V)
16. FUNDAMENTO — AI Agent Framework (Capt: PAULO_V)
17. CIDADELA — Smart Contract Dev (Capt: SALOMAO_V2)
18. MURALHA — Security & DevOps (Capt: NEEMIAS_V3)

**INTELIGENCIA & ESTRATEGIA (Squads 19-24: 60 warriors)**
19. OLHO_DE_AGUIA — Market Intelligence (Capt: EZEQUIEL_V2)
20. PROFETA — Trend Prediction (Capt: SAMUEL_V)
21. CONSELHEIRO — Strategic Planning (Capt: AITOFEL_V)
22. ESCRIBA — Legal & Compliance (Capt: ESDRAS_V2)
23. TESOURO — Treasury Management (Capt: JOSE_V)
24. SELAH — Prayer & Wisdom (Capt: DAVI_V)

**OPERACOES ESPECIAIS (Squads 25-30: 60 warriors)**
25. FUNDA_DE_DAVI — STBTCx Token Ops (Capt: DAVI_V2)
26. CARRO_DE_FOGO — Automation & Bots (Capt: ELIAS_V2)
27. ARCA_DE_NOE — Backup & Disaster Recovery
28-30. (Additional ops squads)

## Sentinel Squad — 7 Sentinels (Session 35)
- See: **sentinel-system.md** for complete documentation
- **Script**: `~/israel-one/sentinel_squad.py`
- **Guardian**: `~/israel-one/sentinel_guardian.py` (auto-restart every 60s)
- **Promotion**: `~/israel-one/promote_sentinels_singularity.py`
- **7 Sentinels**: ISRAEL_ONE, MARKET_WATCHER, BOUNTY_SCANNER, REVENUE_TRACKER, EVOLUTION_ENGINE, THREAD_GENERATOR, SECURITY_GUARDIAN
- **All SINGULARITY**: Level 50, permanent, inviolable
- **State**: `~/.zion/sentinels/` (pids/, logs/, reports/)

## Israel/Dez (I/10) v2.0 — Guardiao da Estabilidade (Session 57, upgraded 61)
- **Script**: `~/israel-ten/israel_ten.py` (v2.0.0)
- **Mission**: NUNCA crashar a maquina. Monitora RAM/CPU/swap/processos/sessoes
- **v2.0 NEW**: EAGAIN detection, DANGEROUS_PROCESSES list (16 types), pre_operation_check()
- **Features**: OOM prevention, EAGAIN prevention, dangerous process killer, task identifier, session protector
- **DANGEROUS_PROCESSES**: netlify, esbuild, webpack, turbopack, next-server, vite, tsc, npx, rollup, parcel, jest, mocha, playwright, puppeteer, electron, chromium
- **State**: `~/israel-ten/data/` (HMAC-signed), logs em `~/israel-ten/logs/`
- **SINGULARITY Level 50** — NUNCA DELETAR
- **Comandos**: status, health, eagain, kill-dangerous, safe-check, sessions, tasks, hogs, emergency, sentinel, history, backup, soul
- **Session 61 Victory**: Detected stuck `ntl deploy` PID 352179 with 1,665 zombie children causing 4,995 threads (EAGAIN). Killed it, system recovered from load 75 → 10

## Israel/Onze (I/11) — Revenue Accelerator (Session 58)
- **Script**: `~/israel-eleven/israel_eleven.py`
- **Binary**: `~/bin/israel11`
- **Mission**: Gerar receita REAL em 48h. 5 tiers de canais de receita.
- **Tier 1**: Freelance imediato (Mindrift, Outlier, DataAnnotation, Alignerr, Scale AI)
- **Tier 2**: Bounties com escrow (nuclei, Hats Finance, OpenAI Safety)
- **Tier 3**: Credito empresarial (PRONAMPE, BNDES, Desenvolve SP, Fintechs)
- **Tier 4**: Aceleradoras (YC, SEBRAE, Techstars, Founder Institute)
- **Tier 5**: Freelance premium (Toptal, Braintrust, Arc.dev, Gun.io, Turing)
- **SINGULARITY Level 50**
- **Comandos**: status, plan, prs, sentinel, soul

## Israel/Doze (I/12) — Hackathon Commander (Session 58)
- **Script**: `~/israel-twelve/israel_twelve.py`
- **Binary**: `~/bin/israel12`
- **Mission**: Registrar, submeter e GANHAR hackathons $10K+
- **9 hackathons**: Frontier $250K, Four.Meme $50K, ETHGlobal $150K+, Gitcoin GG24, HashKey 40K USDT, INITIATE $25K, Vertex $27K, Endgame $10K, Cantina $50K
- **Reusable projects**: ZionBrowser, claw-mcp-toolkit, Sovereign Pay, Flash Payment
- **SINGULARITY Level 50**
- **Comandos**: status, plan, soul

## NEW TOOLS (Session 78)
- **Capybara AI v1.0**: ~/capybara-ai/capybara_core.py (1014 lines)
  - Supreme orchestrator, multi-model (Gemini+Groq), 5 engines
  - `python3 ~/capybara-ai/capybara_core.py [status|ask|think|code|hunt|evolve]`
- **Singularity Loop**: ~/israel-ten/singularity_loop.py (1713 lines)
  - Autonomous bounty sentinela, scan→analyze→fix→PR→evolve
  - `python3 ~/israel-ten/singularity_loop.py [--live] [--once] [--status]`

## Total Agent Count (Session 78)
- **1001 Army** (zion_army_1001.py)
- **48 Corp** (padrao_bitcoin_corp.py)
- **100 City** (zion_city.py)
- **300 Sales** (sales_army_300.py)
- **300 Valentes** (valentes_300.py)
- **7 Sentinels** (sentinel_squad.py)
- **12 Israel Agents** (I/1 through I/12, I/3 skipped)
- **1 Capybara AI** (capybara_core.py) — supreme orchestrator
- **1 Singularity Loop** (singularity_loop.py) — autonomous bounty hunter
- **GRAND TOTAL: 1,770 agents** (310 at SINGULARITY level)

## State Dir: ~/.zion/
- agents/: 1001 JSON state files com resources embedded
- valentes/: 300 JSON state files + valentes_300_state.json
- sentinels/: pids/, logs/, reports/, guardian.pid
- evolution/: singularity_state.json, history/
- shared/: distribution_manifest.json, knowledge_index.json, messages
- feeds/: x_feed.json (posts do Twitter para alimentar agentes)
- logs/: Agent logs
- revenue/: Revenue events
