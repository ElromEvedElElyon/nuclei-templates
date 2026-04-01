# Atomus AI — Project Reference

## Overview
- **Name**: atomus-ai
- **Concept**: Like an atom — the fundamental building block for everything AI agents need
- **GitHub**: https://github.com/ElromEvedElElyon/atomus-ai
- **npm**: atomus-ai (PENDING PUBLISH — needs npm login)
- **License**: MIT
- **Status**: v1.0.0 built, 46 tests passing, NOT YET on npm

## Technical Architecture
- **Language**: TypeScript (strict mode)
- **Output**: CJS + ESM dual format via tsup
- **Dependencies**: ZERO external (only Node.js built-in crypto for shield)
- **Node.js**: >=18.0.0
- **Bundle**: ~10KB total, each module ~1KB, fully tree-shakeable

## 10 Modules
1. **parse** — Extract JSON/XML/fields from LLM outputs (handles code blocks, repairs malformed JSON)
2. **retry** — Exponential backoff, RateLimiter, CircuitBreaker (handles 429, timeouts, Retry-After)
3. **tokens** — Fast token estimation ~5% accuracy (no tiktoken dependency)
4. **cost** — Pricing for 20+ models (Claude 4, GPT-4o, Gemini, DeepSeek, Llama, Mistral), BudgetTracker
5. **schema** — Fluent tool schema builder → Claude, OpenAI, MCP formats
6. **memory** — ConversationMemory (sliding window + summarization), AgentMemory (KV store with TTL)
7. **stream** — SSE parser, StreamAccumulator, processClaudeStream, processOpenAIStream
8. **shield** — AgentIdentity (Ed25519), Cipher (AES-256-GCM), HMAC, sanitizeInput (anti prompt injection)
9. **agent** — Agent base class, tool registration, reasoning loop, AgentSwarm (multi-agent)
10. **index** — Re-exports everything

## Key Files
- `/home/administrador/atomus-ai/` — project root
- `src/` — TypeScript source
- `dist/` — Built output (CJS + ESM + .d.ts)
- `test/test.mjs` — 46 tests using node:test
- `tsup.config.ts` — Build config

## Israel Two Agent
- **File**: `~/israel-one/israel_two.py`
- **Purpose**: npm ecosystem dominance — publishing, marketing, adoption
- **State**: `~/.zion/israel_two_state.json`
- **Sub-agents**: npm-publisher, readme-optimizer, issue-hunter, dependency-tracker, sponsor-outreach, mcp-integrator, template-generator, benchmark-runner
- **Commands**: status, check, publish, plan, opportunities, spawn, report

## Monetization Strategy
### Immediate ($0-$500/mo)
- GitHub Sponsors page (needs setup)
- npm bounties via Opire/Algora for atomus-ai issues

### Growth ($500-$5000/mo)
- Open Collective
- Tidelift (when 1000+ dependents)
- Corporate sponsorship

### Scale ($5000+/mo)
- atomus-ai/pro (enterprise features)
- Consulting built on atomus-ai expertise
- Conference speaking
- Training/courses

## Adoption Plan (4 phases)
### Phase 1 — Launch (Week 1): 100 downloads
- [ ] npm login + publish
- [ ] GitHub Sponsors page
- [ ] X announcement (@opencllaw)
- [ ] Submit to awesome-ai-agents lists
- [ ] 3 example projects

### Phase 2 — Growth (Week 2-4): 1,000 downloads/week
- [ ] MCP server template using atomus-ai
- [ ] Submit to Glama MCP directory
- [ ] Stack Overflow answers with atomus-ai
- [ ] npm comparison article

### Phase 3 — Authority (Week 5-12): 10,000 downloads/week
- [ ] v2.0 release with new modules
- [ ] YouTube tutorials
- [ ] Official integrations (LangChain, Vercel AI)
- [ ] Tidelift application

### Phase 4 — Dominance (Week 13+): 100,000+ downloads/week
- [ ] Corporate sponsors
- [ ] Enterprise license
- [ ] Foundation setup

## NPM ACCOUNT
- **Username**: elromevedelelyon (CONFIRMED WORKING)
- **Auth**: Legacy login + OTP via email (standardbitcoin.io@gmail.com)
- **2FA**: Email OTP required for login and publish
- **Script**: `~/npm-publish-claw-mcp.sh` (has credentials)

## BLOCKERS
- **npm OTP**: Login works but OTP goes to standardbitcoin.io@gmail.com (Gmail cookies EXPIRED, need Firefox open to Gmail to read OTP)
- **GitHub Sponsors**: Need to enable on GitHub profile (browser)
- **Gmail Atom feed**: Cookies expired — need to re-login to Gmail in Firefox and run `python3 ~/gmail_reader.py --refresh`

## Competitive Landscape
| Package | Weekly DL | Deps | Size | Our advantage |
|---------|-----------|------|------|---------------|
| langchain | 2M+ | 50+ | 2MB+ | 200x smaller, zero deps |
| ai (Vercel) | 500K+ | 10+ | 200KB+ | More utilities, universal |
| tiktoken | 1M+ | 1 | 3MB+ | 300x smaller, good enough accuracy |
| openai | 3M+ | 5 | 500KB+ | Complementary (retry/stream) |

## Future Modules (v2.0+)
- `atomus-ai/rag` — RAG pipeline utilities
- `atomus-ai/eval` — LLM evaluation framework
- `atomus-ai/prompt` — Prompt engineering templates
- `atomus-ai/cache` — Semantic caching for LLM calls
- `atomus-ai/guard` — Content safety/moderation
- `atomus-ai/quantum` — Post-quantum crypto wrappers (when standards finalize)
