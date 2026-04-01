# Claude Code Mastery — Complete Internal Architecture
# Session 72: instructkr reverse-eng | Session 74: FULL SOURCE (nirholas/claude-code)
# Updated: 31 Mar 2026 — Session 74

## FULL SOURCE CODE (Session 74)
- **Cloned**: ~/nirholas-claude-code/ — COMPLETE Claude Code source (512K+ lines TS)
- **40 tools** (not 30), **85+ commands**, React/Ink UI, Bun runtime
- **Key files**: QueryEngine.ts (46K), Tool.ts (794), commands.ts (758), main.tsx (4684)
- **Patterns extracted → Israel Framework v3.0**: buildTool(), PermissionMode(4), AgentTool, EventBus, ConcurrentExecutor, SkillRegistry, HMAC Memory
- **MCP Server**: mcp-server/ — 8 tools, 3 resources, 5 prompts, STDIO+HTTP transport
- **Feature flags**: PROACTIVE, KAIROS, BRIDGE_MODE, VOICE_MODE, COORDINATOR_MODE
- **Hidden**: /bughunter, /ant-trace, /good-claude, /ultraplan, /teleport, /thinkback

## COMPLETE TOOL INVENTORY (30 Tools)
1. **AgentTool** — Sub-agents: general-purpose, explore, plan, claude-code-guide, statusline-setup, verification
2. **AskUserQuestionTool** — Interactive questions with options
3. **BashTool** — Shell command execution with sandbox
4. **BriefTool** — Upload/attach files to context
5. **ConfigTool** — Settings management
6. **EnterPlanModeTool** — Switch to plan mode
7. **EnterWorktreeTool** — Git worktree isolation
8. **ExitPlanModeV2Tool** — Exit plan with permissions
9. **ExitWorktreeTool** — Close worktree
10. **FileEditTool** — Exact string replacement
11. **FileReadTool** — Read files (text + images + PDFs)
12. **FileWriteTool** — Create/overwrite files
13. **GlobTool** — Pattern-based file search
14. **GrepTool** — Ripgrep content search
15. **LSPTool** — Language Server Protocol integration
16. **ListMcpResourcesTool** — List MCP resources
17. **MCPTool** — Call MCP server tools
18. **McpAuthTool** — MCP OAuth authentication
19. **NotebookEditTool** — Jupyter notebook editing
20. **PowerShellTool** — Windows PowerShell
21. **ReadMcpResourceTool** — Read MCP resources
22. **RemoteTriggerTool** — Trigger remote sessions
23. **ScheduleCronTool** — Cron job management (Create/Delete/List)
24. **SendMessageTool** — Send messages (Slack?)
25. **SkillTool** — Execute skills/slash commands
26. **SleepTool** — Wait/delay
27. **SyntheticOutputTool** — Synthetic output generation
28. **TaskTools** — Create/Get/List/Output/Stop/Update tasks
29. **TeamTools** — Create/Delete teams
30. **TodoWriteTool** — Todo list management
31. **ToolSearchTool** — Search available tools
32. **WebFetchTool** — Fetch web content
33. **WebSearchTool** — Web search

## COMPLETE COMMAND INVENTORY (60+ Slash Commands)
### Core Commands
- `/add-dir` — Add directory to context
- `/agents` — View/manage sub-agents
- `/branch` — Git branch operations
- `/brief` — Quick briefing/attach files
- `/chrome` — Browser control
- `/clear` — Clear conversation/caches
- `/commit` — Git commit
- `/commit-push-pr` — Commit, push, and create PR
- `/compact` — Compress context
- `/config` — View/edit settings
- `/context` — Manage context window
- `/copy` — Copy content
- `/cost` — View cost/usage
- `/desktop` — Desktop app controls
- `/diff` — View git diff
- `/doctor` — Diagnose issues
- `/effort` — Set reasoning effort level
- `/exit` — End session
- `/export` — Export conversation
- `/fast` — Toggle fast mode (same model, faster)
- `/feedback` — Submit feedback
- `/files` — List files in context
- `/help` — Show help
- `/hooks` — Manage hooks
- `/ide` — IDE integration
- `/init` — Initialize CLAUDE.md
- `/insights` — Usage analytics
- `/keybindings` — Customize shortcuts
- `/login` / `/logout` — Auth management
- `/mcp` — MCP server management
- `/memory` — View/edit memory files
- `/mobile` — Mobile app controls
- `/model` — Switch model
- `/permissions` — Permission settings
- `/plan` — Enter plan mode
- `/plugin` — Plugin management (marketplace, install, discover)
- `/release-notes` — Show latest changes
- `/remote-env` / `/remote-setup` — Remote environment
- `/rename` — Rename session
- `/resume` — Resume previous session
- `/review` — Code review
- `/rewind` — Undo changes
- `/sandbox-toggle` — Toggle sandbox mode
- `/security-review` — Security audit
- `/session` — Session management
- `/share` — Share conversation
- `/skills` — View/manage skills
- `/stats` — Session statistics
- `/status` — Current status
- `/stickers` — Visual stickers
- `/tag` — Tag sessions
- `/tasks` — Task management
- `/theme` / `/color` — Visual theme
- `/thinkback` — Review thinking process
- `/ultraplan` — Advanced planning mode
- `/upgrade` — Update Claude Code
- `/usage` / `/extra-usage` — Usage tracking
- `/version` — Show version
- `/vim` — Vim mode toggle
- `/voice` — Voice input

### Hidden/Internal Commands
- `/ant-trace` — Anthropic internal trace
- `/autofix-pr` — Auto-fix PR issues
- `/bridge` / `/bridge-kick` — Bridge mode
- `/btw` — Side notes
- `/bughunter` — Bug hunting mode
- `/ctx_viz` — Context visualization
- `/debug-tool-call` — Debug tool calls
- `/good-claude` — Positive reinforcement
- `/heapdump` — Memory dump
- `/mock-limits` — Test rate limits
- `/oauth-refresh` — Refresh OAuth tokens
- `/onboarding` — New user setup
- `/teleport` — Remote teleport
- `/output-style` — Output formatting

## BUILT-IN SKILLS (18 Skills)
1. **batch** — Batch operations
2. **claudeApi** — Claude API interaction
3. **claudeInChrome** — Chrome integration
4. **debug** — Debugging utilities
5. **keybindings** — Keyboard shortcut management
6. **loop** — Iterative operations
7. **loremIpsum** — Placeholder text
8. **remember** — Memory management
9. **scheduleRemoteAgents** — Schedule remote agents
10. **simplify** — Code simplification
11. **skillify** — Create new skills
12. **stuck** — Get unstuck from blocks
13. **updateConfig** — Configuration updates
14. **verify** — Verify implementations
15. **commit** — Git commit
16. **claude-developer-platform** — Build with Claude API
17. **keybindings-help** — Keyboard help

## SUBSYSTEMS ARCHITECTURE
- **assistant** — Core assistant logic
- **bootstrap** — Startup/initialization
- **bridge** — External connections
- **buddy** — Companion features
- **cli** — CLI interface
- **components** — UI components
- **constants** — Configuration constants
- **coordinator** — Agent coordination
- **entrypoints** — Entry points
- **hooks** — Event hooks system
- **keybindings** — Key binding engine
- **memdir** — Memory directory management
- **migrations** — Data migrations
- **moreright** — Permission escalation
- **native_ts** — TypeScript native modules
- **outputStyles** — Output formatting
- **plugins** — Plugin system
- **remote** — Remote execution
- **schemas** — Data schemas
- **screens** — UI screens
- **server** — Server mode
- **services** — Background services
- **skills** — Skill system
- **state** — State management
- **types** — Type definitions
- **upstreamproxy** — Proxy management
- **utils** — Utilities
- **vim** — Vim mode
- **voice** — Voice input

## AGENT TYPES (Built-in)
1. **general-purpose** — Research, code search, multi-step tasks (ALL tools)
2. **Explore** — Fast codebase exploration (read-only tools)
3. **Plan** — Architecture planning (read-only tools)
4. **claude-code-guide** — Help with Claude Code usage
5. **statusline-setup** — Configure status line
6. **verification** — Verify implementation correctness

## KEY POWER-USER TECHNIQUES
- Use `/compact` to free context window
- Use `/effort` to adjust reasoning depth per task
- Use `/fast` for quick tasks (same model, faster output)
- Use `/plan` before complex implementations
- Parallel Agent spawning for research
- `/plugin` marketplace for extending capabilities
- `/hooks` for automation on tool events
- `/skills` directory for custom slash commands
- CLAUDE.md for persistent project instructions
- `.claude/settings.json` for MCP servers and permissions
- Git worktrees for isolated experiments

## CLAUDE MYTHOS / CAPYBARA
- **Status**: Training COMPLETE, limited early access
- **Tier**: NEW 4th tier above Opus (Haiku < Sonnet < Opus < Capybara)
- **Model ID**: Unknown yet (possibly claude-capybara-*)
- **Capabilities**: "Dramatically" better than Opus 4.6 at coding + reasoning
- **Release**: Q2-Q3 2026 estimated (Polymarket: 45% by June 30)
- **Pricing**: More expensive than Opus
- **NOT available via API yet**
- Source: Fortune, SiliconANGLE, Euronews (27 Mar 2026)
