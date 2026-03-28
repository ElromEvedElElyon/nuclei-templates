# NEAR Intents Security Findings — Full Report

**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-26
**Programs**: NEAR Intents: Bridges + Smart Contracts on HackenProof

---

## FINDING 1 [CRITICAL]: MockAttestation Bypasses ALL TEE Verification in Production

**Target**: https://github.com/near/mpc
**Files**: `crates/mpc-attestation/src/attestation.rs` (lines 26-29, 47-60, 200-211, 274-281), `crates/near-mpc-contract-interface/src/types/attestation.rs` (lines 29-32, 164-178)

**Description**: The `Attestation` enum includes `Mock(MockAttestation)` variant compiled into production WASM with NO `#[cfg(test)]` or feature flag. `MockAttestation::Valid` unconditionally returns `Ok(())`, bypassing ALL TEE verification: DCAP quote, TLS key binding, Docker image hash, launcher compose hash, and all OS measurements.

**Attack**: Call `submit_participant_info` with `Attestation::Mock(MockAttestation::Valid)`. Node runs outside TEE, extracts key share. Threshold collusion = reconstruct master key = steal ALL funds.

**Impact**: Complete bypass of TEE security model. All cross-chain funds at risk.
**Severity**: CRITICAL

**See separate detailed report: near-intents-finding1-critical-report.md**

---

## FINDING 2 [HIGH]: account_public_key None Bypass in TEE Attestation Check

**Target**: https://github.com/near/mpc
**File**: `contract/src/tee/tee_state.rs` (lines 474-478)

**Description**: `is_caller_an_attested_participant()` skips key check when `account_public_key` is `None`:

```rust
if let Some(node_pk) = &attestation.node_id.account_public_key {
    if node_pk != &signer_pk { return Err(AttestationKeyMismatch); }
}
// None → CHECK SKIPPED → Ok(())
```

Initial participants (from `with_mocked_participant_attestations`) have `account_public_key: None`. If their NEAR account is compromised (new access key added via social engineering or phishing), an attacker signs with any key and passes verification.

**Impact**: Account takeover leads to MPC participant impersonation. Tracked as TODO(#823) but UNPATCHED.
**Severity**: HIGH

---

## FINDING 3 [HIGH]: Detached Promise Token Loss in Fast Transfer Finalization

**Target**: https://github.com/near/omni-bridge (or equivalent bridge repo)
**File**: `omni-bridge/src/lib.rs` (lines 2016-2028)

**Description**: In `process_fin_transfer_to_other_chain` fast transfer path:

```rust
self.send_tokens(token, relayer, amount_without_fee, "").detach();
self.mark_fast_transfer_as_finalised(&fast_transfer.id());
```

`.detach()` means if `ft_transfer` fails, tokens are permanently stuck. Fast transfer is marked finalized (irreversible), but relayer never gets reimbursed.

Compare with `process_fin_transfer_to_near` (lines 1709-1723) which PROPERLY handles refund via `is_refund_required`.

**Impact**: Relayer fund loss. Fast transfer finalized but tokens lost on failure.
**Severity**: HIGH (loss of funds for relayer, inconsistent error handling)

---

## FINDING 4 [MEDIUM]: Legacy Nonces Bypass All Validation + No Revocation

**Target**: https://github.com/near/intents
**Files**: `defuse/core/src/engine/mod.rs` (lines 88-91), `defuse/core/src/nonce/versioned.rs` (line 21), `defuse/src/contract/garbage_collector.rs` (lines 32-36)

**Description**: Legacy nonces (random 32-byte) skip ALL nonce-level validation:

```rust
let Some(nonce) = VersionedNonce::maybe_from(nonce) else {
    return Ok(()); // NO salt/deadline/expiry checks
};
```

Additionally:
- Legacy nonces CANNOT be garbage collected (permanent storage bloat)
- Legacy nonces have NO revocation mechanism (salt rotation only works for versioned)
- Key compromise: signed intents with legacy nonces remain valid until deadline

**Impact**: Irrevocable intents during migration, storage DoS potential.
**Severity**: MEDIUM

---

## FINDING 5 [MEDIUM]: Silent Lock Skip for Cross-Chain Token Routing

**Target**: https://github.com/near/omni-bridge
**File**: `omni-bridge token_lock.rs` (lines 55-57)

**Description**: `lock_tokens()` silently returns `Unchanged` when no entry exists:

```rust
let Some(current_amount) = self.locked_tokens.get(&key) else {
    return LockAction::Unchanged;
};
```

Cross-chain routing (e.g., Eth->NEAR->Base) bypasses lock tracking for non-origin chains. Only origin chain locks are initialized in `bind_token_callback`.

**Impact**: Incomplete solvency tracking for cross-chain routed tokens.
**Severity**: MEDIUM

---

## FINDING 6 [MEDIUM]: Dev TCB Measurements in Production

**Target**: https://github.com/near/mpc
**File**: `crates/mpc-attestation/src/attestation.rs` (lines 123-129)

**Description**:
```rust
static MEASUREMENTS: [ExpectedMeasurements; 2] = [
    include_measurements!("assets/tcb_info.json"),
    // TODO(#1433): Security - remove dev measurements
    include_measurements!("assets/tcb_info_dev.json"),
];
```

Dev environment TEE measurements are accepted as valid in production. This weakens TEE guarantees. Tracked as TODO(#1433).

**Impact**: Reduced TEE security guarantees.
**Severity**: MEDIUM (known issue, compounds with Finding 1)

---

## FINDING 7 [MEDIUM]: Silent Error Swallowing in Key Conversion

**Target**: https://github.com/near/mpc
**File**: `contract/src/tee/tee_state.rs` (lines 173-182)

**Description**: `.ok()` silently converts non-Ed25519 key errors to `None`, which cascades to `[0u8; 32]` zero-bytes fallback in `report_data` hash. This means a participant with a non-Ed25519 key would have their key converted to all-zeros in the attestation binding, potentially creating collisions.

**Impact**: Defense-in-depth weakness in key binding.
**Severity**: MEDIUM

---

## FINDING 8 [MEDIUM]: Potential Decimal Underflow DoS

**Target**: https://github.com/near/omni-bridge
**File**: `omni-bridge/src/lib.rs` (line 2732)

**Description**: `denormalize_amount` performs `origin_decimals - decimals` which panics on underflow (`overflow-checks=true`). If a token is registered with incorrect decimals metadata, all transfers for that token are permanently DoS'd.

**Impact**: Permanent DoS for affected token transfers.
**Severity**: MEDIUM (requires bad token registration, but irrecoverable once triggered)

---

## Summary Table

| # | Finding | Severity | Est. Payout |
|---|---------|----------|-------------|
| 1 | MockAttestation in prod | CRITICAL | $100K-$500K |
| 2 | account_public_key None bypass | HIGH | $20K-$100K |
| 3 | Detached promise token loss | HIGH | $20K-$100K |
| 4 | Legacy nonce no-revocation | MEDIUM | $5K-$20K |
| 5 | Silent lock skip cross-chain | MEDIUM | $5K-$10K |
| 6 | Dev measurements in prod | MEDIUM | $2K-$5K |
| 7 | Silent key conversion error | MEDIUM | $2K-$5K |
| 8 | Decimal underflow DoS | MEDIUM | $2K-$5K |

**TOTAL POTENTIAL: $154K-$665K**
