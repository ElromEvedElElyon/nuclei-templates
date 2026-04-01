# Cloned Repos Analysis — Session 72-73 (31 Mar 2026)
## CREATURES NAMES (corrigidos anti-blasfemia):
- Melekh = KING (nao "rei supremo"), Gavriel = Mensageiro (nao "dos dados")
- Yonah renomeado → Fenix, rarity "divine" → "supreme", element "Divino" → "Soberano"

## Session 73: BUDDY ARENA DEPLOYED
- 18 Claude /buddy species: duck, dragon, axolotl, capybara, mushroom, ghost, cat, goose, blob, octopus, owl, penguin, turtle, snail, cactus, fox, phoenix, wolf
- Mulberry32 PRNG for deterministic 1M creature generation
- Pokemon battle system: HP, moves, accuracy, critical hits, turn-based
- i18n: 14 languages auto-detect + manual selector

## 1. instructkr/claude-code (~/instructkr-claude-code/)
- **Type**: Python reverse-engineering of Claude Code internals
- **Value**: MASSIVE — complete tools_snapshot.json + commands_snapshot.json
- **Extracted**: 30+ tools, 60+ commands, 18 skills, 25+ subsystems
- **Status**: Data extracted to claude-code-mastery.md

## 2. NousResearch/hermes-agent (~/hermes-agent-new/)
- **Type**: Self-improving AI agent with learning loop
- **Value**: HIGH — skills system, memory, multi-platform (Telegram, Discord, Slack)
- **Key Features**: Skill creation, cron scheduler, sub-agents, MCP server
- **Status**: Cloned, analyzing for skill/agent patterns

## 3. GreenSheep01201/claw-empire (~/claw-empire/)
- **Type**: AI Agent Office Simulator — CEO orchestrating AI agents
- **Value**: HIGH — multi-agent orchestration, virtual company, pixel-art UI
- **Key Features**: Claude Code + Codex + Gemini + Copilot integration
- **Agent System**: CEO directives ($), task management, lessons learned
- **Status**: Cloned, extracting orchestration patterns

## 4. OpenAI/codex (~/openai-codex/)
- **Type**: OpenAI's coding agent CLI (competitor to Claude Code)
- **Value**: MEDIUM — Rust + TypeScript, Bazel build
- **Key Features**: codex-cli, codex-rs (Rust), SDK
- **Status**: Cloned for competitive analysis

## 5. yusufkaraaslan/Skill_Seekers (~/Skill_Seekers/)
- **Type**: Unknown — to be analyzed
- **Status**: Cloned

## 6. caiovicentino repos (NOT cloned — analyzed via web)
- **40 repos**, key ones:
  - polymarket-mcp-server (293 stars!) — 45 tools for prediction markets
  - hyperliquid-mcp-server — DEX trading with Claude
  - debank-mcp-server — DeFi data
  - orquestr-pro — AI Assistant Desktop
  - eoq-quantization — LLM compression
  - whalescope — Solana whale intelligence
  - culturabot — Community builder Brazil
  - solskill — DeFi for AI agents on Solana
  - contractscan-ai — Smart contract analysis
- **NO "major" repo found** — user may have confused with orquestr-pro
- **HuggingFace**: caiovicentino1/Qwen3.5-9B-PolarQuant-MLX-4bit

## SECURITY: Axios Supply Chain Compromise
- **Affected**: axios@1.14.1 and axios@0.30.4 (RAT malware)
- **Our exposure**: NONE — no direct axios dependency
- **Action**: Monitor, don't install those versions
