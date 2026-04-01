# Ariel Silva — CEO Gotas — Ecosystem Analysis (25 Mar 2026)

## Company: Gotas (gotas.com / gotas.social / the.gotas.com)
- API: api.gotas.com
- Entity: Paleta Fosforescente, LDA (Portugal)
- Market: Brazil (PIX, BRL, pt-BR)
- Uses Claude Code (CLAUDE.md in repos)

## 4 Products
1. **Gotas** (gotas.social) — Core NFT loyalty platform. Creators make "gotas" for followers
2. **GotasPAY** (commerce.gotas.com) — Crypto payment gateway, P2P or e-commerce
3. **Gotas REWARDS** (rewards.gotas.com) — Customizable loyalty/reward campaigns
4. **CRIPTO** (pix.gotas.com) — Buy crypto with PIX

## 7 Cloned Repos (24,653 LOC total)

### arielvdl-omeubancov2 (15,839 LOC) — MOST VALUABLE
- Children's digital banking app ("O Meu Banco")
- React Native 0.81.5 + Expo SDK 54 + Hono backend + Drizzle ORM + PostgreSQL
- WebAuthn/Passkeys, Google OAuth, JWT, PIN auth, Firebase push
- Google Cloud Run (southamerica-east1), Google Cloud Storage
- 37 screens, multi-currency (BRL/USD/EUR), audit logging
- Zustand state, Zod validation, repository pattern
- iOS TestFlight: 9 builds (last 17 Mar 2026)
- **PATTERNS**: Hono API template, Drizzle schema, balance-in-cents, scheduled deposits

### arielvdl-gotas (2,343 LOC) — Smart Contracts
- Solidity ^0.8.19, Chainlink VRF V2+ for provably fair raffles
- One-shot randomness, deposit tracking, time-locked withdrawals
- **PATTERNS**: Chainlink VRF integration template

### arielvdl-gotas-mktplace (1,793 LOC) — NFT Marketplace
- Solidity ^0.8.12, OpenZeppelin, Thirdweb
- Royalty + platform fee split (basis points /10000)
- Pack listings, deadline expiry, Slither CI
- **PATTERNS**: Marketplace fee split, Slither CI pipeline

### arielvdl-gotas-ecbr (3,008 LOC) — Event Gamification
- Next.js 15.4, Tailwind, Shadcn/ui, PostgreSQL
- QR scan → collect gotas → ranking → prizes
- Complex SQL with RANK() window functions
- **PATTERNS**: Event gamification flow, ranking CTEs

### arielvdl-gotas-split (75 LOC) — Revenue Splitter
- Solidity ^0.8.17, automatic 80/20 ETH split
- **PATTERNS**: Revenue splitter template

### arielvdl-gotas-web (1,595 LOC) — Marketing Site
- Next.js 15.3, Tailwind 4.x, Vercel deployment
- Strict security headers (CSP, X-Frame-Options)
- **PATTERNS**: Vercel security config, SaaS landing page

### arielvdl-buildersvoice — EMPTY (placeholder)

## Tech Stack Summary
| Tech | Usage |
|------|-------|
| Solidity | Smart contracts (raffle, marketplace, splitter) |
| TypeScript | Frontend + backend (Next.js, Hono, React Native) |
| PostgreSQL | Database (Drizzle ORM) |
| Chainlink VRF V2+ | On-chain randomness |
| OpenZeppelin | Contract security |
| Hono | Lightweight backend API |
| Google Cloud Run | Backend hosting (SP region) |
| Vercel | Frontend hosting |
| Firebase | Push notifications |
| WebAuthn | Passwordless auth |

## Revenue Model
- NFT marketplace fees (royalty + platform %)
- Crypto payment gateway fees (GotasPAY)
- PIX-to-crypto conversion fees
- Loyalty platform subscriptions
- Event gamification (B2B)

## Reusable for ZION Agents
1. Hono backend template (fast, lightweight, perfect for MCPs)
2. Drizzle ORM + PostgreSQL pattern (type-safe, audit logging)
3. NFT marketplace contract (ready to deploy)
4. Revenue splitter contract (automatic payment split)
5. Chainlink VRF template (provably fair randomness)
6. WebAuthn/Passkey implementation
7. Vercel security headers configuration
8. Event gamification system (QR → collect → rank → prize)
9. Multi-role auth (parent/child/guardian with PIN + OAuth + passkey)
10. Balance-in-cents financial pattern (integer arithmetic for money)

## GitHub: arielvdl (63 repos total — FULL SCAN COMPLETE)
- **31 original** + **32 forks**
- **Bio**: naia.today | 3 followers | Account since Jun 2018
- **Career arc**: WebDev (2020) → Columbia FinTech Bootcamp Solidity (2021) → NFT era thirdweb (2022) → Marketplace iterations (2023) → Gotas core (2024) → TypeScript pivot (2025) → AI/MCP pivot (2026)

### FLAGSHIP: Naia Platform (naia.today) — MOST IMPORTANT
- **naia-mcp-server** (JS, 20 Mar 2026): MCP Server for "Generative Engine Optimization" (GEO)
  - Measures brand visibility across ChatGPT, Gemini, Claude, Perplexity
  - Compatible with Claude Code, Cursor, VS Code, Windsurf, Replit, Lovable
  - **COMPETITOR/PARTNER POTENTIAL** — similar to our openclaw-webtools
- **naia-skills** (21 Mar 2026): Agent skills for the Naia GEO platform

### Smart Contracts (6 repos)
- gotas, gotas-mktplace, gotas-split-contract, gotas_mktplace, mktplacev3, Puppercoin

### Frontend/Web (13 repos)
- gotas-ecbr, gotas-web, omeubancov2, farmaleafv0, meusitenl, dsdsdsadasdasd, alopppp
- gotamktplace, nft-pampili-redirect, redirect-*, TESTE-nextjs, MobileLayoutCraft

### AI/MCP (4 repos)
- naia-mcp-server, naia-skills, buildersvoice (OpenAI Whisper), mintlify-docs

### NFT Projects (5 repos)
- nft-drop-vite-ts, roughdiamondsmint, unlock-roughdiamonds, 78tap, liveco

### Key Forks (32 total — learning sources)
- OpenZeppelin, PancakeSwap, thirdweb contracts, metaplex, Safemoon
- Neon (serverless Postgres), builder.io, Next.js, WordPress
- Columbia FinTech Bootcamp homework (advance-solidity)

## NAIA MCP Server — Deep Analysis (25 Mar 2026)
- **naia-mcp-server**: 256 lines, ZERO executable code — stub npm package + Smithery config
- **Architecture**: Remote-only SaaS at https://naia.today/api/v1/mcp (streamable-http transport)
- **18 MCP tools**: 5 brand mgmt + 3 GEO analysis + 4 content gen + 5 execution plans + 1 account
- **GEO Score (0-100)**: 9 dimensions — Visibility 20%, Citations 18%, Position 12%, Sentiment 10%, Consistency 10%, Risk 10%, Authority 8%, Schema 6%, Sources 6%
- **5 AI engines**: Gemini (2 credits), Perplexity (3), ChatGPT (5), Grok (5), Claude (9)
- **Pricing**: Free (1 analysis) → Essencial R$97/mo (50 credits) → Acelerador R$297/mo (200) → Autoridade R$497/mo (unlimited)
- **Content templates**: blog-post, ultimate-guide, comparison, faq, landing-page, case-study, schema
- **CMS integrations**: WordPress, Notion, HubSpot, Webflow, Ghost, Joomla, Wix, Squarespace
- **naia-skills**: Claude Code skill (SKILL.md, 168 lines, MIT license, 3 workflows)
- **KEY INSIGHT**: Remote MCP SaaS pattern = proven monetization. Free reads, paid writes/generation.
- **NOT competitive** with us — complementary (GEO analytics vs our web/crypto/social/finance)
- **LEARN FROM**: Credit system, remote HTTP transport, Smithery+npm+Skills 3-channel distribution

## Potential Collaboration/Competition
- **Naia MCP Server** = direct competitor to our openclaw-webtools in GEO space
- **Gotas gamification** = potential partnership for our ZION agents (loyalty integration)
- **O Meu Banco** = fintech patterns we can reuse (Hono + Drizzle + Expo)
- **Ariel's stack evolution** mirrors ours: Solidity → NFTs → TypeScript → AI/MCP
