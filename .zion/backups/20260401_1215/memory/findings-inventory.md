# Security Findings Inventory — Session 42 (27 Mar 2026)
# Em nome do Senhor Jesus Cristo

## TOTAL: 28 findings across 5 targets = $213K-$764K potential

---

## huntr.com — OLLAMA (11 findings, $31,500)
**Reports**: ~/huntr-reports/ollama-findings.md
**Status**: READY TO SUBMIT (need huntr.com registration)

| # | Finding | Severity | Category | Bounty |
|---|---------|----------|----------|--------|
| 1 | GGUF V1 String Panic (zero-length) | HIGH | Model File | $4,000 |
| 2 | Tensor Dims OOM (unbounded uint32) | HIGH | Model File | $4,000 |
| 3 | String Allocation OOM/Panic | HIGH | Model File | $4,000 |
| 4 | Safetensors Header OOM | HIGH | Model File | $4,000 |
| 5 | Tensor Size Integer Overflow | HIGH | Model File | $4,000 |
| 6 | discardGGUFString Sign Overflow | HIGH | Model File | $4,000 |
| 7 | BashTool RCE (prompt injection) | HIGH | Other | $1,500 |
| 8 | DNS Rebinding Host Bypass | MEDIUM | Other | $1,500 |
| 9 | TLS Bypass (https+insecure) | MEDIUM | Other | $1,500 |
| 10 | No Auth on Non-Loopback | MEDIUM | Other | $1,500 |
| 11 | Quantization Buffer Over-Read | HIGH | Other | $1,500 |

## huntr.com — MLFLOW (2 findings, $3,000)
**Reports**: ~/huntr-reports/mlflow-findings.md
**Status**: READY TO SUBMIT (need huntr.com registration)

| # | Finding | Severity | Bounty |
|---|---------|----------|--------|
| 1 | SSRF via DNS Rebinding in Webhooks | HIGH | $1,500 |
| 2 | Hardcoded Default Encryption Key | HIGH | $1,500 |

## HackenProof — NEAR INTENTS (8 findings, $154K-$660K)
**Reports**: ~/near-intents-all-findings-report.md
**Status**: BLOCKED — needs 100+ HackenProof reputation

| # | Finding | Severity | Est. Payout |
|---|---------|----------|-------------|
| 1 | MockAttestation in production | CRITICAL | $100K-$500K |
| 2 | account_public_key None bypass | HIGH | $20K-$100K |
| 3 | Detached promise token loss | HIGH | $20K-$100K |
| 4 | Legacy nonce no-revocation | MEDIUM | $5K-$20K |
| 5 | Silent lock skip cross-chain | MEDIUM | $5K-$10K |
| 6 | Dev measurements in prod | MEDIUM | $2K-$5K |
| 7 | Silent key conversion error | MEDIUM | $2K-$5K |
| 8 | Decimal underflow DoS | MEDIUM | $2K-$5K |

## HackenProof — LAYER3 (4 findings, $10K-$29K)
**Reports**: ~/huntr-reports/layer3-hackenproof-findings.md
**Status**: READY TO SUBMIT (zero-rep program, no rep needed!)

| # | Finding | Severity | Est. Bounty |
|---|---------|----------|-------------|
| 1 | ERC1155 parameter swap (fund loss) | CRITICAL | $5K-$15K |
| 2 | withdraw() breaks treasury sweep | HIGH | $3K-$8K |
| 3 | Excess ETH not refunded | MEDIUM | $1K-$3K |
| 4 | Missing reentrancy guard | MEDIUM | $1K-$3K |

## HackenProof — CETUS (5 findings, $14.5K-$44K)
**Reports**: ~/huntr-reports/cetus-hackenproof-findings.md
**Status**: READY TO SUBMIT (zero-rep program)

| # | Finding | Severity | Est. Bounty |
|---|---------|----------|-------------|
| 1 | Unchecked shlw() overflow | MEDIUM | $5K-$15K |
| 2 | checked_shlw() fragile API | MEDIUM | $5K-$15K |
| 3 | Deprecated mul_shl() still public | MEDIUM | $3K-$10K |
| 4 | Signed shl() sign flip | LOW | $1K-$3K |
| 5 | Missing mul_shr_ceil | INFO | $500-$1K |

---

## SUBMISSION PRIORITY (highest ROI first)

1. **Layer3 Finding 1** (CRITICAL, HackenProof zero-rep) — submit NOW via browser
2. **huntr.com Ollama Findings 1-6** (model file $4K each) — register + submit
3. **Cetus Findings 1-2** ($223M exploit pattern) — submit via HackenProof
4. **MLflow Findings** (huntr.com) — submit after registration
5. **Ollama Findings 7-11** (huntr.com other) — submit batch
6. **Layer3 Findings 2-4** — submit after Finding 1 accepted
7. **NEAR Findings** — after building 100+ rep from Layer3/Cetus/huntr
