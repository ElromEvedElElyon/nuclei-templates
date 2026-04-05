# Claude Code — Estado Real (5 Apr 2026)

## VERSAO
- **Instalada**: v2.1.92 (4 Apr 2026) — ATUALIZADO de v2.1.63
- **Sessao atual**: v2.1.63 (REINICIAR para ativar v2.1.92)
- Auto-updates: ON
- Source code: ~/nirholas-claude-code/ (512K+ lines TS, referencia)

## MODELOS REAIS DISPONIVEIS

| Modelo | ID | $/MTok In | $/MTok Out | Context | Max Out |
|--------|-----|----------|-----------|---------|---------|
| **Opus 4.6** | claude-opus-4-6 | $5 | $25 | 1M | 128K |
| **Sonnet 4.6** | claude-sonnet-4-6 | $3 | $15 | 1M | 64K |
| **Haiku 4.5** | claude-haiku-4-5-20251001 | $1 | $5 | 200K | 64K |

### Legacy (ainda na API)
- Sonnet 4.5, Opus 4.5, Opus 4.1, Sonnet 4.0, Opus 4.0
- Haiku 3 — DEPRECATED, retira 19 Apr 2026

### Mythos/Capybara — NAO DISPONIVEL
- Teste interno early-access. Leak Fortune 27 Mar. Sem release date.
- Ver: claude-mythos-intel.md

## FEATURES v2.1.64→v2.1.92 (DISPONIVEIS POS-RESTART)

### Novos Comandos
- `/powerup` — Lessons interativas
- `/effort low|medium|high` — Ajustar profundidade
- `/loop 5m <prompt>` — Rodar prompts em intervalo
- `/simplify` — Review code quality
- `/color` — Mudar cor prompt bar
- `/plan <desc>` — Plan mode com descricao direta
- `/release-notes` — Interactive version picker
- `/cost` — Per-model cost breakdown

### Novas Capacidades
- **ExitWorktree tool** — Sair de worktree
- **Named Subagents** — @mention typeahead
- **MCP Elicitation** — Servers pedem input via dialogs
- **Remote sessions** — Bridge para claude.ai/code (browser/phone)
- **Computer Use** — Point, click, navigate (Pro/Max)
- **Cloud scheduled tasks** — Cron em infra Anthropic
- **Auto-fix CI** — Cloud corrige PRs automaticamente
- **300K output** — Batches API com beta header

### Performance
- Write tool diff 60% mais rapido
- 74% menos re-renders
- Startup ~500ms mais rapido
- SSE transport linear time

### Seguranca
- `sandbox.failIfUnavailable`
- `allowRead` em regioes denyRead
- `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`

### Hooks Novos
- `CwdChanged`, `FileChanged`, `TaskCreated`
- `PermissionDenied` — retry on denial
- `PostCompact` — after compaction
- Conditional `if` field em hooks

### Config/Env Vars Novos
- `CLAUDE_CODE_NO_FLICKER=1`
- `CLAUDE_CODE_DISABLE_CRON`
- `ANTHROPIC_CUSTOM_MODEL_OPTION`
- `MCP_CONNECTION_NONBLOCKING=true`

### Removidos
- `/tag`, `/vim` removidos (usar /config)
- `/output-style` deprecated
- Agent `resume` parameter removido

## TOOLS COMPLETOS (33 tools built-in)
AgentTool, AskUserQuestion, Bash, Brief, Config, EnterPlanMode, EnterWorktree, ExitPlanMode, ExitWorktree, FileEdit, FileRead, FileWrite, Glob, Grep, LSP, ListMcpResources, MCPTool, McpAuth, NotebookEdit, PowerShell, ReadMcpResource, RemoteTrigger, ScheduleCron, SendMessage, Skill, Sleep, SyntheticOutput, TaskTools (Create/Get/List/Output/Stop/Update), TeamTools, TodoWrite, ToolSearch, WebFetch, WebSearch

## AGENT TYPES (built-in)
1. general-purpose — Research, code, multi-step (ALL tools)
2. Explore — Fast codebase search (read-only)
3. Plan — Architecture planning (read-only)
4. claude-code-guide — Claude Code help
5. statusline-setup — Status line config
6. code-reviewer — PR review
7. revenue-accelerator — Revenue/bounties
8. deployer — Build/deploy
9. bounty-hunter — Security audit

## MCP SERVERS ATIVOS (desta maquina — ~/.mcp.json)
1. **xai-grok** — Grok chat/image/vision/search (KEY PENDENTE)
2. **grok-search** — Web/news/X search (KEY PENDENTE)
3. **x-mcp** — Twitter/X CRUD (OAuth ATIVO)
4. **mythos-edge** — Scanner Anthropic + audit via modelo ATUAL (NAO é Mythos)
5. **mcp-crypto-prices** — CoinGecko data
6. **openclaw-webtools** — SEO/DNS/SSL/headers
7. **claw-mcp-toolkit** — Crypto/social/finance/productivity
8. **sequential-thinking** — Chain-of-thought
9. **paypal** — PayPal HTTP MCP

## POWER-USER TECHNIQUES
- `/compact` — Liberar context window
- `/effort` — Ajustar reasoning por task
- `/fast` — Mesmo modelo, output mais rapido
- `/plan` — Planejar antes de implementar
- Parallel Agent spawning para pesquisa
- `/plugin` marketplace para estender
- `/hooks` para automacao em tool events
- Git worktrees para experimentos isolados
- CLAUDE.md para instrucoes persistentes
