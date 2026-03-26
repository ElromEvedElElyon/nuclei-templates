# Bounties Pipeline — 26 Mar 2026 (Session 31 Browser Automation)

## TIER 0: BLOCKED / NEEDS MANUAL ACTION

### C4 Chainlink $65K — DEADLINE 27 MAR 20:00 UTC — BLOCKED
- **H-01**: SUBMETIDO DUAS VEZES (erro de duplicacao), usou 2/2 slots
- **0/2 submissions restantes** — locked after 2 hours, NAO pode retirar
- **H-02 e H-03**: PRONTOS mas NAO PODEM ser submetidos
- **Login funciona**: ElromAuditor / C4_LVnFWosBgxQSQwJP!Ax
- **PERDA**: ~$5K-15K em potencial H-02 + H-03 rewards

### Immunefi — PARCIALMENTE ATIVADO
- **Email VERIFICADO**: inteligenciaartificial.now@gmail.com
- **Password**: ImmunefiElrom2026#Sec99
- **BLOQUEIO**: Discord required para submeter reports (Discord OAuth)
- **ZKsync bug** pronto: `~/zksync-os-bug-report.md` (callstack off-by-one)
- **ACAO**: Criar conta Discord → conectar → submeter ZKsync

### Guardian Defender $150K — BLOQUEADO HARDWARE
- **Login API funciona**: token em `~/.guardian_defender_token.json`
- **Conta**: elromaud1774361187@sharebot.net / GuardElrom2026Sec#99
- **BLOQUEIO**: SPA requer WebGL2 (THREE.js), GPU Intel HD 1st gen NAO suporta
- **KYC API**: POST /api/kyc/access-token retorna 500 (Sumsub integration issue)
- **ACAO**: Precisa machine com WebGL2 OU Guardian fix backend

## TIER 1: HIGH PRIORITY (Confirmed Payment)

### INITIATE Hackathon (Initia) $25K — DoraHacks (NOVO!)
- URL: dorahacks.io/hackathon/initiate
- Deadline: Apr 15
- **APENAS 3 SUBMISSIONS** — competicao BAIXISSIMA
- Tracks: Web3, DeFi, Gaming, Appchain
- **ACAO**: Registrar + build project com security+MCP+AI
- Background research agent running

### Nosana ElizaOS Challenge $3K — Superteam Earn
- PR #18 SUBMETIDO (unico PR open!)
- 4 repos starred
- **FALTA**: Frontend/UI, deploy Nosana, video <1min, social post
- Deadline: Apr 14
- **ACAO**: Build frontend, deploy, record video

### Guardian LimitBreak $150K — P1
- Deadline: 9 Abr
- 1 finding pronto (`~/limitbreak-amm/findings/C-01-operator-precedence-createPool.md`)
- **BLOQUEIO**: Email verification + KYC Sumsub pendente

### NEAR Intents $300K — HackenProof (NEW!)
- Smart contracts + MPC bridges
- Cross-chain = top payout category historicamente
- KYC HackenProof required

### Immunefi Variational $100K max — P2
- Perps DEX, ~500 assets, smart contracts
- URL: immunefi.com/bug-bounty/variational/

## TIER 2: MEDIUM PRIORITY

### dn-institute $3,500-$4,500
- 10 PRs (#694-#703), CI green
- 0 reviews, maintainers inativos — NAO pingar mais

### Superteam Vault Standard $4,000
- SVS-8 construido, deploy pendente (faucet)
- Deadline: 31 Mar

### Algora Twenty CRM $2,500 (NEW!)
- URL: app.algora.io/twentyhq/bounties/g6i2c8YSNV9nHogT
- TypeScript CRM, IMAP email sync
- Plataforma com escrow — pagamento garantido se aceito

### bolivian-peru $100-$400
- Issue #77 claimed (LinkedIn API)
- Tambem: X/Twitter API #73 ($100), Trend Intel #70 ($100), Google SERP #149 ($200)
- Paga em $SX token — RISCO de token sem valor

### Nosana Builders Challenge $3,000 USDC — MOVIDO para TIER 1 (PR #18 SUBMITTED)

### NAVI Protocol $300K — HackenProof (NOVO Session 30!)
- Smart contracts + web frontend
- Critical smart contract: ate $300K | Web: ate $10K
- Requer conta HackenProof ativa
- **ACAO**: Ativar conta, auditar

### C4 Chainlink Rewards $200K — NOVO! (~mid-April)
- Pool ENORME $200K, 30-day window
- Precisa mesma KYC do C4
- **ACAO**: Se KYC resolver, auditar

### Activepieces MCP $200/each — Algora (NOVO Session 30!)
- Build MCP integrations para Activepieces platform
- SEM KYC, escrow payment
- Stack multiples rapidamente
- URL: algora.io/challenges/activepieces

### HackenProof New Programs
- Flipcash Reserve: Smart contracts
- NEAR Bridges: MPC cross-chain
- Ember EVM: Tokenized assets
- Multipli ZK: ZK yield protocol
- **NAVI Protocol**: Smart contracts ate $300K (NOVO!)

### Deploy-Gate Ed25519 Bypass $200 — P1 (NEW 25 Mar!)
- URL: github.com/permission-protocol/deploy-gate/issues/36
- Task: Find flaw in Ed25519 signature verification
- Opened: 24 Mar 2026 (FRESH)
- Skill match: PERFECT (security + MCP — mcp-guard is MCP server)
- Repos: deploy-gate + mcp-guard

### Lido MCP Server $5,000 — P1 (NEW!)
- $3K first / $2K second
- Task: Build MCP server for Lido staking (stake, unstake, wrap, unwrap, balances)
- Skill match: EXCELLENT (MCP is our specialty)
- ~435 lines new code, ~8 hours
- Reference: MorkeethHQ/delegated-agent-treasury#2

### huntr.com AI/ML Vulns $1,500-$4,000/finding — P1
- Targets: ollama ($1,500), llama_index ($1,500), transformers ($1,500), mlflow ($1,500)
- Model file format vulns: up to $4,000 (TensorRT, GGUF, ONNX)
- Skill match: EXCELLENT (security auditing)
- Register at huntr.com

### nuclei-templates $150-$250/merged PR (Algora)
- **#15675**: 5 KEV CVEs, rebased clean, Neo bot approved, awaiting @DhiyaneshGeek
- **#15676**: CVE-2020-5849, CI SUCCESS, Neo approved, awaiting @theamanrawat
- **#15696** (Session 31): 5 KEV CVEs — Telerik, Array Networks, Apache Struts, Langflow, Cisco FMC
- **#15697** (Session 33 NEW): 5 KEV CVEs — GPON, Telerik RadAsyncUpload, SAP NetWeaver, Struts S2-008, ManageEngine
- **#15698** (Session 33 NEW): 5 KEV CVEs — Fortinet SSL VPN x2 (XORtigate), SonicWall x2, Qlik Sense
- **5 PRs open = $750-$1,250 potential** if all merge
- **84 unchecked KEV CVEs remain** in issue #7549 — can write ~16 more batches
- **Next batch targets**: CVE-2024-23113 (Fortinet fgfmd), CVE-2024-20353 (Cisco ArcaneDoor), CVE-2024-8190 (Ivanti CSA), CVE-2024-53677 (Struts S2-067), CVE-2024-11667 (Zyxel)

### Endgame Hackathon (Bittensor) $10K+ — DoraHacks (NOVO!)
- Deadline: Apr 24
- Decentralized AI tools
- URL: dorahacks.io/hackathon/endgame/detail

### Vertex Swarm Challenge $27K — DoraHacks (NOVO!)
- Deadline: Apr 6
- AI agent coordination (C, Rust, ROS 2)
- URL: dorahacks.io/hackathon/global-vertex-swarm-challenge

## TIER 3: SKIP / LOW VALUE / CLOSED
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
| Code4rena | Solidity audits | Web only, KYC needed |
| Immunefi | Smart contract bugs | $8M+ pipeline permanente |
| HackenProof | Web3 security | 200+ programas |
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

### ZKsync Era $1.1M — Immunefi (NOVO Session 30!)
- Critical: $100K min (10% of funds at risk)
- High: $20K min
- Payment: USDC on zkSync Era
- Mesma plataforma Immunefi — same KYC

## PRs STATUS (32+ open, 26 Mar — Session 33)
- **nosana-ci/agent-challenge #18**: ZION agent — ONLY PR OPEN
- **nuclei-templates #15675**: 5 KEV CVEs, clean, Neo approved — awaiting @DhiyaneshGeek
- **nuclei-templates #15676**: CVE-2020-5849, CI SUCCESS — awaiting @theamanrawat
- **nuclei-templates #15696**: 5 KEV CVEs batch 3 (Session 31)
- **nuclei-templates #15697**: 5 KEV CVEs batch 4 (Session 33 NEW)
- **nuclei-templates #15698**: 5 KEV CVEs batch 5 (Session 33 NEW)
- **docker/mcp-registry #1960**: MERGEABLE, 0 reviews
- **awesome-crypto-mcp #39,40,42**: 1 comment each, waiting
- **ravitemer/mcp-registry #10-13**: 4 PRs, 0 comments
- **awesome-web3-mcp #45, Awesome-MCP #82, TensorBlock #228**: 0 comments
- **dn-institute #694-703**: 10 PRs, only OUR comments — maintainers DEAD
- **PrivacyLayer #117-118**: OPEN, 0 comments, API 404 — SUSPICIOUS
- **sorosave #130-132**: OPEN, API 404 — PROBABLY DEAD
- **rustchain #2336-2339**: ALL CLOSED ("wrong repo, see #2516")

## GRANTS & CREDITS
- **Alibaba Cloud $120K**: DEADLINE 31 MAR — form ready
- **xAI $150/mo**: console.x.ai signup
- **Together AI $15K**: together.ai/startup-accelerator
- **Claude for OSS $1,200**: claude.com/contact-sales/claude-for-oss
- **Anthropic $25K**: menlovc.com/anthology-fund-application

## TOTAL PIPELINE: $8M+ (Immunefi) + $300K+ (active bounties/hackathons) + $160K (grants)

## SESSION 30.5 ACTIONS COMPLETED (26 Mar 2026)
- Nosana ZION agent built + PR #18 (only submission)
- 4 Nosana repos starred
- 2 tweets posted (@opencllaw) — daily limit hit
- C4 findings consolidated in /tmp/c4_submission_ready.txt
- INITIATE hackathon identified ($25K, only 3 submissions!)
- Endgame + Vertex hackathons identified
- Bounty pipeline fully updated
- 4 tweets queued for tomorrow in /tmp/tweets_queue.txt
- Swarm daemon running continuously (PID 102462, 92% success)
