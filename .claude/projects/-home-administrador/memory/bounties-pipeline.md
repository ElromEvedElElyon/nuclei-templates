# Bounties Pipeline — 26 Mar 2026 (Session 35 Update)

## TIER 0: BLOCKED / NEEDS MANUAL ACTION

### C4 Chainlink $65K — DEADLINE PASSED (27 Mar) — CLOSED
- **H-01**: SUBMETIDO DUAS VEZES (erro de duplicacao), usou 2/2 slots
- **0/2 submissions restantes** — locked after 2 hours, NAO pode retirar
- **H-02 e H-03**: PRONTOS mas NAO PODEM ser submetidos (slots esgotados)
- **PERDA CONFIRMADA**: ~$5K-15K em potencial H-02 + H-03 rewards
- **STATUS**: Contest ENCERRADO 27 Mar 20:00 UTC. Aguardar resultado H-01

### Immunefi — REPORT #71022 SUBMITTED! ZKsync OS Bug
- **Email VERIFICADO**: inteligenciaartificial.now@gmail.com
- **Password**: ImmElrom2026!Bug#99
- **REPORT #71022**: SUBMITTED 26 Mar 2026 at 11:16 UTC — Status: **Reported**
  - URL: https://bugs.immunefi.com/dashboard/submission/71022
  - Severity: Medium | Program: ZKsync OS (project 947) | Asset: evm_interpreter
  - Wallet: 0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B (Verified, Primary)
- **Discord RESOLVED**: wagner7978 (ID 771534250368565298) connected — NOT elromauditor
- **Discord (OLD/BLOCKED)**: elromauditor_86701 — still linked to different Immunefi account
- **Zendesk tickets**: #8002 and #8008 OPEN — for Discord unlink request (may no longer matter)
- **Email submissions**: security@matterlabs.dev (05:34+13:33 UTC) + security@zksync.io (12:36 UTC)
- **NEXT**: Monitor report #71022 every 24-48h, follow up if no response by 2 Apr

### Guardian Defender $150K — BLOQUEADO HARDWARE + EXPIRED TOKENS
- **Login API funciona**: token em `~/.guardian_defender_token.json`
- **Conta**: elromaud1774361187@sharebot.net / GuardElrom2026Sec#99
- **BLOQUEIO 1**: SPA requer WebGL2 (THREE.js), GPU Intel HD 1st gen NAO suporta
- **BLOQUEIO 2**: Password reset tokens EXPIRED (Session 35)
- **KYC API**: POST /api/kyc/access-token retorna 500 (Sumsub integration issue)
- **ACAO**: Precisa machine com WebGL2 OU Guardian fix backend. Re-request password reset

## TIER 1: HIGH PRIORITY (Confirmed Payment)

### nuclei-templates $150-$250/merged PR (Algora) — 7 PRs OPEN = $1,050-$1,750
- **CLOSED BY MAINTAINERS (Session 36)**: #15695, #15698, #15699 — "detection only, not full exploit"
- **FIXED (Session 36)**: #15696 (Array+Struts converted to vuln testing), #15700 (all 5 templates — WebLogic/Roundcube/Nagios/Plex/Pi-hole with version extraction)
- **CLEAN (awaiting review)**: #15675, #15676, #15697, #15701, #15705
- **AT RISK**: #15697, #15701 — same "detection only" pattern, may need proactive fix
- **CRITICAL LESSON**: Maintainers (pussycat0x, DhiyaneshGeek) REJECT templates that only detect product presence. Must: (1) test vulnerable endpoint, (2) extract version, (3) compare against vulnerable range
- **~31 uncovered KEV CVEs remain** in issue #7549
- **ACAO**: Proactively fix #15697, #15701 before reviewers close them

### INITIATE Hackathon (Initia) $25K — DoraHacks
- URL: dorahacks.io/hackathon/initiate
- Deadline: Apr 15
- **APENAS 3 SUBMISSIONS** — competicao BAIXISSIMA
- Tracks: Web3, DeFi, Gaming, Appchain
- **ACAO**: Registrar + build project com security+MCP+AI

### Nosana ElizaOS Challenge $3K — Superteam Earn
- PR #18 SUBMETIDO (unico PR open!)
- 4 repos starred
- **FALTA**: Frontend/UI, deploy Nosana, video <1min, social post
- Deadline: Apr 14
- **ACAO**: Build frontend, deploy, record video

### Guardian LimitBreak $150K — P1 (see TIER 0 blockers)
- Deadline: 9 Abr
- 1 finding pronto (`~/limitbreak-amm/findings/C-01-operator-precedence-createPool.md`)
- **BLOQUEIO**: Email verification + KYC Sumsub pendente + password reset tokens EXPIRED

### NEAR Intents $164K-$880K+ — HackenProof (MASSIVE!)
- **3 separate programs**: Smart Contracts, Bridges (MPC+Omni), SDK
- **CRITICAL**: $100K-$500K per finding | HIGH: $20K-$100K | MEDIUM: $1K-$20K
- **Our 8 findings**: 1 CRITICAL ($100K-$500K) + 2 HIGH ($40K-$200K) + 5 MEDIUM ($5K-$100K)
- **CRITICAL finding**: MockAttestation in production WASM bypasses ALL TEE verification
- **Registration**: NO KYC upfront! Email + verify only. KYC only at withdrawal
- **Payouts**: USDC on Base, BTC, or ETH. 3% commission. Min $100 withdrawal
- **NO API**: Browser-only submission, each finding = separate report
- **IMPORTANT**: security@near.org DEPRECATED — must use HackenProof.com only
- **NEAR paid $1.8M to hackers historically** — they PAY
- Findings: `~/near-intents-all-findings-report.md`
- Guide: `/tmp/hackenproof_registration_guide.txt`
- **ACAO URGENTE**: Register hackenproof.com → submit CRITICAL first → then HIGHs → then MEDIUMs

### Immunefi Variational $100K max — P2
- Perps DEX, ~500 assets, smart contracts
- URL: immunefi.com/bug-bounty/variational/
- **Discord RESOLVED** — wagner7978 connected, can now submit to ANY Immunefi program

## TIER 2: MEDIUM PRIORITY

### C4 Chainlink Rewards $200K — (~mid-April)
- Pool ENORME $200K, 30-day window
- Precisa mesma KYC do C4 (ALREADY APPROVED)
- **ACAO**: Auditar when contest opens

### dn-institute $3,500-$4,500
- 10 PRs (#694-#703), CI green
- 0 reviews, maintainers inativos — NAO pingar mais

### Superteam Vault Standard $4,000
- SVS-8 construido, deploy pendente (faucet)
- Deadline: 31 Mar

### Algora Twenty CRM $2,500
- URL: app.algora.io/twentyhq/bounties/g6i2c8YSNV9nHogT
- TypeScript CRM, IMAP email sync
- Plataforma com escrow — pagamento garantido se aceito

### bolivian-peru $100-$400
- Issue #77 claimed (LinkedIn API)
- Tambem: X/Twitter API #73 ($100), Trend Intel #70 ($100), Google SERP #149 ($200)
- Paga em $SX token — RISCO de token sem valor

### NAVI Protocol $300K — HackenProof
- Smart contracts + web frontend
- Critical smart contract: ate $300K | Web: ate $10K
- Requer conta HackenProof ativa

### Activepieces MCP $200/each — Algora
- Build MCP integrations para Activepieces platform
- SEM KYC, escrow payment
- Stack multiples rapidamente
- URL: algora.io/challenges/activepieces

### Deploy-Gate Ed25519 Bypass $200 — P1
- URL: github.com/permission-protocol/deploy-gate/issues/36
- Task: Find flaw in Ed25519 signature verification
- Skill match: PERFECT (security + MCP)

### Lido MCP Server $5,000 — P1
- $3K first / $2K second
- Task: Build MCP server for Lido staking
- Reference: MorkeethHQ/delegated-agent-treasury#2

### huntr.com AI/ML Vulns $1,500-$4,000/finding — P1
- Targets: ollama ($1,500), llama_index ($1,500), transformers ($1,500), mlflow ($1,500)
- Model file format vulns: up to $4,000 (TensorRT, GGUF, ONNX)
- Register at huntr.com

### Endgame Hackathon (Bittensor) $10K+ — DoraHacks
- Deadline: Apr 24
- Decentralized AI tools
- URL: dorahacks.io/hackathon/endgame/detail

### Vertex Swarm Challenge $27K — DoraHacks
- Deadline: Apr 6
- AI agent coordination (C, Rust, ROS 2)
- URL: dorahacks.io/hackathon/global-vertex-swarm-challenge

### HackenProof New Programs
- Flipcash Reserve: Smart contracts
- NEAR Bridges: MPC cross-chain
- Ember EVM: Tokenized assets
- Multipli ZK: ZK yield protocol
- **NAVI Protocol**: Smart contracts ate $300K

## TIER 3: SKIP / LOW VALUE / CLOSED
- **Expensify $250**: ALREADY MERGED — not for us (Session 35 confirmed)
- **C4 Chainlink $65K**: DEADLINE PASSED 27 Mar — H-01 submitted (duplicate), 0 slots left
- **Golem Cloud MCP $3,500**: FECHADO E PAGO
- **Desloppify $1,000**: FECHADO
- **RustChain RTC**: ALL PRs CLOSED 25 Mar (wrong repo) — MORTO
- **Superteam Stablecoin $5K**: CLOSED, winners announced 23 Mar — MISSED
- **PrivacyLayer**: SCAM confirmado (PRs open, 0 comments, 404 on API)
- **sorosave-protocol**: 3 PRs open, 404 on API — PROVAVELMENTE MORTO
- **Hyperlane**: Muito competido

## PLATAFORMAS ATIVAS
| Plataforma | Foco | Nota |
|-----------|------|------|
| Code4rena | Solidity audits | Web only, KYC APPROVED |
| Immunefi | Smart contract bugs | $8M+ pipeline, Discord RESOLVED (wagner7978), Report #71022 active |
| HackenProof | Web3 security | 200+ programas, KYC needed |
| Algora | TypeScript bounties | Escrow, $500-$5K |
| huntr.com | AI/ML bugs | ate $50K |
| Opire | GitHub bounties | 100% payout |
| boss.dev | Aggregator | GitHub bounties |

## IMMUNEFI — PERMANENTE ($8M+)
| Program | Max Payout |
|---------|-----------|
| Chainlink | $3,000,000 |
| Polygon | $2,000,000 |
| Immutable | $1,000,000 |
| Injective | $500,000 |
| Resolv | $500,000 |
| Stacks | $250,000 |
| XION | $250,000 |
| Variational | $100,000 |

### ZKsync Era $1.1M — Immunefi
- Critical: $100K min (10% of funds at risk)
- High: $20K min
- Payment: USDC on zkSync Era
- **Discord RESOLVED** — can submit via wagner7978

## PRs STATUS (35+ open, 26 Mar — Session 35)
- **nosana-ci/agent-challenge #18**: ZION agent — ONLY PR OPEN
- **nuclei-templates**: 9 PRs (#15675, #15676, #15695, #15696, #15697, #15698, #15699, #15700, #15701)
  - CLEAN: #15675, #15676, #15698, #15699, #15701
  - NEEDS FIX: #15695, #15696, #15700
- **docker/mcp-registry #1960**: MERGEABLE, 0 reviews
- **awesome-crypto-mcp #39,40,42**: 1 comment each, waiting
- **ravitemer/mcp-registry #10-13**: 4 PRs, 0 comments
- **awesome-web3-mcp #45, Awesome-MCP #82, TensorBlock #228**: 0 comments
- **dn-institute #694-703**: 10 PRs, only OUR comments — maintainers DEAD
- **PrivacyLayer #117-118**: OPEN, 0 comments, API 404 — SUSPICIOUS
- **sorosave #130-132**: OPEN, API 404 — PROBABLY DEAD
- **rustchain #2336-2339**: ALL CLOSED ("wrong repo, see #2516")

## GRANTS & CREDITS
- **Alibaba Cloud $120K**: Rolling basis (NOT hard March 31 deadline) — form ready
- **xAI $150/mo**: console.x.ai signup
- **Together AI $15K**: together.ai/startup-accelerator
- **Claude for OSS $1,200**: claude.com/contact-sales/claude-for-oss
- **Anthropic $25K**: menlovc.com/anthology-fund-application

## MARKET CONTEXT (26 Mar 2026 — Session 35)
- **BTC**: $70K | **SOL**: $89 | **ETH**: $2.1K
- **Fear & Greed Index**: 10/100 EXTREME FEAR
- **AI agent tokens**: TAO $337, FET $0.24, VIRTUAL $0.70
- **STBTCx**: $3,819 mcap, 7.17 SOL reserves, DORMANT (last trade 17 days ago), NOT graduated from bonding curve
- **Book manuscript**: DOES NOT EXIST on this machine — needs to be written from scratch

## TOTAL PIPELINE: $8M+ (Immunefi) + $300K+ (active bounties/hackathons) + $120K+ (grants)

## SESSION 35 KEY ACTIONS (26 Mar 2026)
- nuclei-templates expanded from 7 to 9 PRs (#15695, #15701 added)
- Identified 3 PRs needing fixes (#15695, #15696, #15700)
- Immunefi Zendesk tickets #8002 and #8008 confirmed — no human response
- Confirmed NEAR security@near.org DEPRECATED — HackenProof only
- Guardian password reset tokens EXPIRED
- Expensify $250 already merged — eliminated from pipeline
- C4 Chainlink deadline PASSED — moved to TIER 3
- Alibaba $120K confirmed rolling (not hard March 31 deadline)
- ~36 KEV CVEs remaining uncovered for nuclei-templates
