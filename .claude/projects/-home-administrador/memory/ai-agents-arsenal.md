# AI Agents Arsenal — Cloned & Ready (31 Mar 2026)

## CAPYBARA AI v1.0 — Supreme Orchestrator (Session 78 — NEW!)
- **Path**: ~/capybara-ai/capybara_core.py (1014 lines, Pure Python, stdlib only)
- **GitHub**: https://github.com/ElromEvedElElyon/capybara-ai (PRIVATE)
- **Multi-model**: Gemini free (unlimited) → Groq free (14,400/day) → fallback
- **5 engines**: CapybaraEngine, ReasoningChain, CodeGenerator, BountyHunter, EvolutionEngine
- **CLI**: `python3 capybara_core.py [status|ask|think|code|hunt|evolve]`
- **Needs**: `export GEMINI_API_KEY=...` and/or `export GROQ_API_KEY=...`
- **3.3GB RAM safe**: Pure Python stdlib, zero pip dependencies

## SINGULARITY LOOP — Autonomous Bounty Sentinela (Session 78 — NEW!)
- **Path**: ~/israel-ten/singularity_loop.py (1713 lines, Pure Python)
- **8 classes**: SingularityLogger, BountyIssue, BountyAttempt, BountyLedger, GeminiClient, GitHubOps, StrategyEngine, SingularityLoop
- **CLI**: `python3 singularity_loop.py [--live] [--once] [--status] [--interval N]`
- **Flow**: Scan GitHub issues → Analyze with Gemini → Generate fix → Submit PR → Track → Evolve
- **DRY RUN default**: Use `--live` for real PRs
- **Integrates**: Israel Framework v3.0 (IsraelAgent class)

## ISRAEL AGENT FRAMEWORK v3.0 (Session 74 — MAJOR UPGRADE)
- **Source analysis**: Claude Code full source (512K+ lines TS) cloned to ~/nirholas-claude-code/
- **Framework**: ~/israel-ten/israel_framework_v3.py — 42 tools, 10 categories, Pure Python
- **1293 agents**: 30 depts + 30 squads + 12 core + 10 named — ALL have 42 tools
- **Key patterns from Claude Code**: buildTool(), AgentTool, PermissionMode(4), EventBus, ConcurrentExecutor, SkillRegistry, HMAC Memory
- **Commands**: `python3 ~/israel-ten/army_v3_connector.py status|deploy|swarm|count`
- **Per-agent**: `python3 ~/israel-ten/agents_v3_launchers.py dez|four|nine|zion status`


## CLONED REPOS (Session 45)

### Twitter/X Agents
| Repo | Path | Type | Key Feature |
|------|------|------|-------------|
| ElizaOS v2 | ~/eliza-agent/ | TypeScript/Bun | #1 crypto Twitter agent, 17.6K stars, 200+ plugins |
| twitter-automation-ai | ~/twitter-automation-ai/ | Python/Selenium | Multi-account, stealth, no API needed |
| DOT Automation | ~/dot-automation/ | Python | Personality-driven autonomous posting |
| LangChain Social Agent | ~/social-media-agent/ | TypeScript | Official LangChain, cron scheduler |

### MCP Servers (Twitter/X)
| Repo | Path | Type | Key Feature |
|------|------|------|-------------|
| twitter-mcp-server | ~/twitter-mcp-server/ | TypeScript | Best Twitter MCP, full lifecycle |
| xai-mcp-server | ~/xai-mcp-server/ | TypeScript | Grok image/video/search/chat |
| grok-search-mcp | ~/grok-search-mcp/ | TypeScript | Twitter search via Grok API |
| x-mcp-server | ~/x-mcp-server/ | TypeScript | 16 tools for X integration |

### Frameworks
| Repo | Path | Type | Key Feature |
|------|------|------|-------------|
| CrewAI | ~/crewAI/ | Python | Multi-agent roles, 44K stars |

### Already Present
| Repo | Path | Type |
|------|------|------|
| twitter-scraper-mcp | ~/twitter-scraper-mcp/ | MCP scraper |
| claw-mcp-toolkit | ~/claw-mcp-toolkit/ | Our MCP toolkit |
| israel-one | ~/israel-one/ | Our sentinel agent |
| twitter-mcp-server | ~/twitter-mcp-server/ | Twitter MCP |

## INTEGRATION PLAN FOR ISRAEL/ONE + @opencllaw

### Priority 1: xAI MCP Server (Grok)
- Install: `cd ~/xai-mcp-server && npm install`
- Needs: xAI API key from console.x.ai ($175 free first month)
- Tools: generate_image, chat, analyze_image, live_search, generate_video
- Use: Real-time X trend detection + content generation

### Priority 2: twitter-automation-ai (Selenium stealth)
- Install: `cd ~/twitter-automation-ai && pip install -r requirements.txt`
- Config: config/accounts.json + config/settings.json
- Features: Multi-account, proxy rotation, undetected Chrome
- Use: Post without API, stealth mode, complements tweet_now.py

### Priority 3: DOT Automation (personality)
- Install: `cd ~/dot-automation && pip install -r requirements.txt`
- Config: 4-layer personality (Identity, Cognition, Expression, Behavior)
- Use: Generate ultra-human personality for @opencllaw brand

### Priority 4: ElizaOS (full stack)
- Install: `cd ~/eliza-agent && bun install` (needs Node 23.3+)
- WARNING: Heavy (~53MB repo, large deps). May OOM on 3.3GB machine
- Use: Full crypto-native agent with Twitter + Discord + Telegram

### Priority 5: CrewAI (multi-agent crew)
- Install: `cd ~/crewAI && pip install crewai`
- Use: Orchestrate Research -> Draft -> Edit -> Post pipeline

## FREE AI ALTERNATIVES (no xAI API needed)

### Grok Free Wrapper (NO API KEY)
- Path: ~/grok-api-free/ (realasfngl/Grok-Api)
- Status: Bug com parsing scripts (grok.com mudou layout)
- Models: grok-3-auto, grok-3-fast, grok-4, grok-4-mini-thinking
- Engine: ~/israel-one/grok_free_engine.py

### Google Gemini (100% FREE UNLIMITED)
- URL: https://aistudio.google.com/apikey
- Engine: ~/israel-one/gemini_free_engine.py
- `export GEMINI_API_KEY=your_key`
- PRIORITY 1: Get key from aistudio.google.com

### Groq (FREE 14,400 req/dia)
- URL: https://console.groq.com
- Models: Llama 4, Gemma 3, Mixtral
- `export GROQ_API_KEY=gsk_your_key`

### HARPA AI (Chrome Extension FREE)
- URL: https://harpa.ai
- Combines: GPT, Claude, Gemini, Grok in one extension
- 100+ automation commands including Twitter content
- Free tier available

### xAI API (NEEDS $5 spend first for data sharing)
- Console: https://console.x.ai — @opencllaw linked
- $25 signup credits BUT need to spend $5 to unlock $150/mo
- UNIQUE: Only model with REAL-TIME X/Twitter data

## TOP COMMERCIAL TOOLS (no clone needed)
- OpenTweet: $5.99/mo posting API (17x cheaper than Twitter API)
- Tweet Hunter: $49-99/mo, AI ghostwriter + CRM
- Typefully: Free-$49/mo, threads + scheduling
- NoimosAI: Full autonomous X management fleet
