# NEAR Intents HackenProof Submission Package -- Master Index

**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Program**: NEAR Intents: Bridges + Smart Contracts (HackenProof)
**Date**: 2026-03-29
**Total Findings**: 8

---

## Submission Order (Submit CRITICAL first, then HIGH, then MEDIUM)

### Priority 1: CRITICAL

| # | File | Title | Severity | Est. Payout |
|---|------|-------|----------|-------------|
| 1 | `near_critical_submission.md` | MockAttestation::Valid Bypasses ALL TEE Verification in Production | CRITICAL | $100K-$500K |

### Priority 2: HIGH

| # | File | Title | Severity | Est. Payout |
|---|------|-------|----------|-------------|
| 2 | `finding2_high_account_pubkey_bypass.md` | account_public_key None Bypass in TEE Attestation | HIGH | $20K-$100K |
| 3 | `finding3_high_detached_promise_token_loss.md` | Detached Promise Token Loss in Fast Transfer | HIGH | $20K-$100K |

### Priority 3: MEDIUM

| # | File | Title | Severity | Est. Payout |
|---|------|-------|----------|-------------|
| 4 | `finding4_medium_legacy_nonce_bypass.md` | Legacy Nonces Bypass All Validation + No Revocation | MEDIUM | $5K-$20K |
| 5 | `finding5_medium_silent_lock_skip.md` | Silent Lock Skip for Cross-Chain Routing | MEDIUM | $5K-$10K |
| 6 | `finding6_medium_dev_measurements_prod.md` | Dev TCB Measurements in Production | MEDIUM | $2K-$5K |
| 7 | `finding7_medium_silent_key_conversion.md` | Silent Key Conversion Error to Zero-Bytes | MEDIUM | $2K-$5K |
| 8 | `finding8_medium_decimal_underflow_dos.md` | Decimal Underflow DoS in denormalize_amount | MEDIUM | $2K-$5K |

---

## Total Estimated Payout: $154K - $665K

---

## Target Repositories

- **NEAR MPC**: https://github.com/near/mpc (Findings 1, 2, 6, 7)
- **NEAR Omni Bridge**: https://github.com/near/omni-bridge (Findings 3, 5, 8)
- **NEAR Intents**: https://github.com/near/intents (Finding 4)

---

## Cross-References Between Findings

Findings 1 + 2 + 6 + 7 form a compound TEE security degradation chain:
- Finding 1 (MockAttestation) completely bypasses TEE
- Finding 6 (Dev measurements) weakens TEE even for real attestations
- Finding 2 (None key bypass) removes key binding after TEE check
- Finding 7 (Zero-byte fallback) weakens key binding cryptographically

Findings 3 + 5 + 8 form a compound bridge accounting/safety chain:
- Finding 3 (Detached promise) loses relayer funds silently
- Finding 5 (Silent lock skip) hides solvency gaps
- Finding 8 (Decimal underflow) permanently DoS's token transfers

---

## Submission Checklist

- [ ] Submit Finding 1 (CRITICAL) first -- highest priority
- [ ] Wait for acknowledgment before submitting others (avoids duplicate flags)
- [ ] Submit Finding 2 (HIGH) -- reference Finding 1 as compound
- [ ] Submit Finding 3 (HIGH) -- independent bridge issue
- [ ] Submit Findings 4-8 (MEDIUM) -- can batch or submit individually
- [ ] Track all submission IDs in this document
- [ ] Follow up at 48h, 7d, 14d intervals

## Submission IDs (fill after submission)

| Finding | HackenProof ID | Date Submitted | Status |
|---------|---------------|----------------|--------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
