# GitFlix v6.2 — Solana AI Agent Marketplace | Session 81 (1 Apr 2026)
# Build: 382KB/112KB gzip | 44 modules | React 19 + TS + Vite
# SOLANA ONLY — Phantom wallet, Metaplex Core, MagicEden
# v6.2: 5 security fixes (Pro bypass, XSS DOMParser, CSP, mobile grid, fails-open)
# CRITICO: NUNCA usar "Melekh" — renomeado para Solomon. Ver regras em MEMORY.md
# IMPORTANT: Deploy to `gitflix-app` repo: npx gh-pages -d dist --dotfiles --repo gitflix-app.git

## WHAT CHANGED v6.1 (Session 80)
- **SOLANA ONLY**: Removed ALL Polygon/MetaMask/MATIC/EVM references
- **useWallet.ts**: Phantom-only, eager connect, accountChanged listener, signMessage
- **CreaturesMarketplace.tsx**: Complete rewrite (1315 insertions):
  - 4 tabs: AI Agents (11) | Claude Buddies (18) | Create Agent | .agent.md
  - WalletBar: Phantom logo SVG, SOL badge, Solscan link, copy address, disconnect
  - CollectionHero: SOL pricing, 6 stat boxes (floor/volume/items/listed/brains/providers)
  - AgentCard: MagicEden-quality (rarity badge, SOL badge, MCP brain, compatibility icons)
  - AgentDetail: 2-column layout, stat bars, 5 brain sections, Solscan/MagicEden links
  - CreateAgent: form to generate .agent.md, anonymous listing toggle, 85% creator rev
  - AgentMdSpec: interop docs (Claude+OpenAI+Grok+Gemini), example .agent.md
  - PaymentModal: SOL address copy, PayPal link, tx hash verification
  - Solomon banner: owner's champion, clickable for detail, NOT for sale
  - Sort: default/price-asc/price-desc/power/intel
  - Filter: all/legendary/epic/rare/common
  - Design system: Inter font, Solana purple (#9945FF), green (#14F195), dark theme
- **BuddyArena.tsx**: Updated to Solana/Metaplex Core/MagicEden/0.05 SOL
- **i18n**: Removed MetaMask/Polygon keys, added market.* keys (14 langs)
- **llms.txt**: v6.0, Solana-first, .agent.md standard

## AGENT DATA (12 agents, all Solana)
- Solomon (supreme, 0.72 SOL, OWNER), Baraq (legendary, 0.36), Nesher (legendary, 0.29)
- Aryeh (epic, 0.22), Gavriel (epic, 0.18), Tzuriel (epic, 0.22), Rafael (epic, 0.18)
- Ezer (rare, 0.11), Hashmal (rare, 0.11), Kalev (rare, 0.14)
- Raziel (legendary, 0.32), Fenix (common, 0.07)
- Each has: soul, memory[], mcpServers[], tools[], skills[], compatibility[], creator, priceSol

## .agent.md INTEROPERABILITY STANDARD
- YAML frontmatter: name, version, chain, creator, price_sol, compatibility
- Sections: Soul, Skills, MCP Tools, MCP Servers, Memory Domains, Usage
- Compatible with: Claude Code (CLAUDE.md), OpenAI Codex (AGENTS.md), Grok, Gemini
- Anonymous listings supported (creator can hide wallet)
- On-chain ownership via Solana NFT (Metaplex Core)

## ENDPOINTS (ALL 200 VERIFIED)
- Frontend: https://elromevedelelyon.github.io/gitflix-app/ — LIVE
- llms.txt, metadata/collection.json, metadata/{1-12}.json — ALL 200
- Backend: 7 Netlify Functions (search, readme, repo, checkout, webhook, verify, status)

## BUSINESS MODEL v4.0 — AI Agent Marketplace
- FREE: browse + Claude Buddies (no blockchain)
- AGENT: buy agents in SOL (Phantom wallet) or PayPal, 85% to creator, 15% platform
- PRO ($9.99 lifetime): unlimited repo views
- CREATE: generate .agent.md, list on marketplace (email submission)
- Anonymous listings: privacy-first trading

## SECURITY FIXES v6.2 (Session 81 — 31 Mar 2026)
- [x] **CRITICAL FIX**: Removed `?pro=1` bypass — now requires valid session_id from Stripe
- [x] **CRITICAL FIX**: verifySession no longer calls doActivate() on network error
- [x] **HIGH FIX**: XSS sanitizer replaced — regex → DOMParser-based (strips all on* attrs, javascript: URLs, SVG vectors)
- [x] **HIGH FIX**: CSP meta tag added to index.html (script-src self, frame-src none, object-src none)
- [x] **MEDIUM FIX**: AgentDetail mobile grid — responsive 1-col on <768px

## AUDIT RESULTS (3 agents, Session 81)
- **Codebase audit**: 3/10 — frontend prototype, no real blockchain, fake stats
- **UX audit**: Emojis as art (disqualifying), no URL routing, manual buy flow
- **Security audit**: 2 CRITICAL + 3 HIGH + 4 MEDIUM + 4 LOW + 2 INFO (5 fixed above)
- **Remaining**: tx hash accepted without on-chain verification (ProModal), Footer ToS says "$9.99/month"

## TECH DEBT / NEXT STEPS
- [ ] Deploy Anchor smart contract for on-chain listing/buying
- [ ] Metaplex Core NFT minting for each agent
- [ ] MagicEden collection submission
- [ ] Solana Agent Registry registration
- [ ] CLI tool `gfx` for agent management
- [ ] Real Phantom signAndSendTransaction for SOL payments
- [ ] Replace emojis with generated AI artwork (SVG or PNG)
- [ ] Add URL routing (react-router or hash-based)
- [ ] Real-time SOL price from CoinGecko API
- [ ] Server-side tx hash verification (Solana RPC)
- [ ] Fix Footer.tsx: "$9.99/month" → "$9.99 lifetime"
