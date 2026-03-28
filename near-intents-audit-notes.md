# NEAR Intents Security Audit — COMPLETE (26 Mar 2026)

## Target: HackenProof $100K-$500K (Critical), $20K-$100K (High)

## Repos Audited:
- `/tmp/near-intents/` — Verifier/Defuse contract (Rust)
- `/tmp/near-omni-bridge/` — Multi-chain bridge (Rust + Solidity + Solana)
- `/tmp/near-mpc/` — MPC chain signatures (Rust, 16K lines)

---

## FINDING 1 [CRITICAL]: MockAttestation Bypasses ALL TEE Verification in Production

**Files:**
- `mpc-attestation/src/attestation.rs:26-60,274-281`
- `contract/src/dto_mapping.rs:54-65`
- `near-mpc-contract-interface/src/types/attestation.rs:29-32`

**Description:** The `Attestation` enum includes `Mock(MockAttestation)` variant with NO `#[cfg(test)]` or feature flag. It's compiled into the production WASM contract. `MockAttestation::Valid` bypasses ALL verification:
- DCAP quote verification
- TLS key binding via report_data
- Docker image hash verification
- All measurements verification

**Attack:** Any participant calls `submit_participant_info` with `Attestation::Mock(MockAttestation::Valid)`. They can run MPC node OUTSIDE TEE, extract key shares. Threshold collusion = steal ALL funds.

**Impact:** Complete undermining of TEE security model.
**Severity:** CRITICAL — $100K-$500K if exploitable on mainnet.

---

## FINDING 2 [HIGH]: account_public_key None Bypass in TEE Attestation Check

**File:** `contract/src/tee/tee_state.rs:474-478`

**Description:** `is_caller_an_attested_participant()` skips key check when `account_public_key` is None:
```rust
if let Some(node_pk) = &attestation.node_id.account_public_key {
    if node_pk != &signer_pk { return Err(AttestationKeyMismatch); }
}
// None → CHECK SKIPPED → Ok(())
```

Initial participants (from `with_mocked_participant_attestations`) have `account_public_key: None`. If their NEAR account is compromised (new access key added), attacker signs with any key.

**Tracked as:** TODO(#823) but unpatched.
**Severity:** HIGH — $20K-$100K.

---

## FINDING 3 [HIGH]: Detached Promise Token Loss in Fast Transfer Finalization

**File:** `omni-bridge/src/lib.rs:2016-2028`

**Description:** In `process_fin_transfer_to_other_chain` fast transfer path:
```rust
self.send_tokens(token, relayer, amount_without_fee, "").detach();
self.mark_fast_transfer_as_finalised(&fast_transfer.id());
```

`.detach()` means if ft_transfer fails, tokens are permanently stuck. Fast transfer is marked finalized (irreversible), but relayer never gets reimbursed.

Compare with `process_fin_transfer_to_near` (line 1709-1723) which PROPERLY handles refund via `is_refund_required`.

**Impact:** Relayer fund loss. Bridge accounting intact but relayer loses fronted tokens.
**Severity:** HIGH (loss of funds for relayer, inconsistent error handling vs other paths).

---

## FINDING 4 [MEDIUM]: Legacy Nonces Bypass All Validation + No Revocation

**Files:**
- `defuse/core/src/engine/mod.rs:88-91`
- `defuse/core/src/nonce/versioned.rs:21`
- `defuse/src/contract/garbage_collector.rs:32-36`

**Description:** Legacy nonces (random 32-byte) skip ALL nonce-level validation:
```rust
let Some(nonce) = VersionedNonce::maybe_from(nonce) else {
    return Ok(()); // NO salt/deadline/expiry checks
};
```

Additionally:
- Legacy nonces CANNOT be garbage collected (permanent storage bloat)
- Legacy nonces have NO revocation mechanism (salt rotation only works for versioned)
- Key compromise scenario: signed intents with legacy nonces remain valid until deadline

**Impact:** Irrevocable intents during migration, storage DoS.
**Severity:** MEDIUM — $5K-$20K.

---

## FINDING 5 [MEDIUM]: Silent Lock Skip for Cross-Chain Token Routing

**File:** `omni-bridge token_lock.rs:55-57`

**Description:** `lock_tokens()` silently returns `Unchanged` when no entry exists in `locked_tokens`:
```rust
let Some(current_amount) = self.locked_tokens.get(&key) else {
    return LockAction::Unchanged;
};
```

Cross-chain routing (e.g., Eth→NEAR→Base) bypasses lock tracking for non-origin chains. Only origin chain locks are initialized in `bind_token_callback`. This creates incomplete accounting.

**Impact:** Incomplete solvency tracking for cross-chain routed tokens.
**Severity:** MEDIUM.

---

## FINDING 6 [MEDIUM]: Dev TCB Measurements in Production

**File:** `mpc-attestation/src/attestation.rs:123-129`

**Description:**
```rust
static MEASUREMENTS: [ExpectedMeasurements; 2] = [
    include_measurements!("assets/tcb_info.json"),
    // TODO(#1433): Security - remove dev measurements
    include_measurements!("assets/tcb_info_dev.json"),
];
```

Dev environment TEE accepted as valid in production.
**Tracked as:** TODO(#1433). **Severity:** MEDIUM.

---

## FINDING 7 [MEDIUM]: Silent Error Swallowing in Key Conversion

**File:** `contract/src/tee/tee_state.rs:173-182`

**Description:** `.ok()` silently converts non-Ed25519 key errors to `None`, which cascades to `[0u8; 32]` zero-bytes fallback in report_data hash.

**Severity:** MEDIUM (defense-in-depth weakness).

---

## FINDING 8 [MEDIUM]: Potential Decimal Underflow DoS

**File:** `omni-bridge/src/lib.rs:2732`

**Description:** `denormalize_amount` does `origin_decimals - decimals` which panics on underflow (overflow-checks=true). If a token is registered with bad decimals, all transfers for that token are permanently DoS'd.

**Severity:** MEDIUM (requires bad token registration).

---

## FINDINGS NOT EXPLOITABLE (Investigated & Dismissed):

### P1: Message Encoding Asymmetry — NOT A BUG
- NEAR uses `TransferMessagePayloadV1` (no message field) when message is empty
- EVM uses `bytes("")` (nothing) when message is empty
- Encoding IS symmetric. Confirmed in `omni-types/src/lib.rs:638-644`.

### Solana Bridge — SOLID
- Signature verification: secp256k1_recover + malleability check (`!signature.s.is_high()`)
- Mint/recipient included in signed hash (can't be swapped)
- Nonce replay: BitArray per nonce range, solid
- Chain IDs prevent cross-chain replay (different address sizes)
- Minor: `amount.try_into().unwrap()` panics for u128>u64::MAX (liveness only)

### EVM OmniBridge — SOLID
- Nonce checked before external calls (reentrancy safe)
- Borsh encoding matches NEAR encoding
- Wormhole used only for outbound (Solana→NEAR), not inbound verification

---

## SUBMISSION PRIORITY:

| # | Finding | Severity | Est. Payout | Ready |
|---|---------|----------|-------------|-------|
| 1 | MockAttestation in prod | CRITICAL | $100K-$500K | YES |
| 2 | account_public_key None bypass | HIGH | $20K-$100K | YES |
| 3 | Detached promise token loss | HIGH | $20K-$100K | YES |
| 4 | Legacy nonce no-revocation | MEDIUM | $5K-$20K | YES |
| 5 | Silent lock skip cross-chain | MEDIUM | $5K-$10K | YES |
| 6 | Dev measurements in prod | MEDIUM | Known issue | INFO |
| 7 | Silent key conversion error | MEDIUM | $2K-$5K | YES |
| 8 | Decimal underflow DoS | MEDIUM | $2K-$5K | YES |

**TOTAL POTENTIAL: $154K-$660K**

## NEXT STEP: Activate HackenProof account + submit Finding 1 (Critical) ASAP
