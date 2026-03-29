# HackenProof Submission: MEDIUM — Silent Error Swallowing in Key Conversion Creates Zero-Byte Fallback

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/mpc
**Severity**: MEDIUM
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**Silent .ok() on Non-Ed25519 Key Conversion Cascades to [0u8; 32] Zero-Byte Fallback in Attestation report_data Hash**

---

## Severity Justification

- **MEDIUM**: Defense-in-depth weakness in cryptographic key binding
- Non-Ed25519 keys are silently converted to `None`, which then becomes `[0u8; 32]` in the hash
- Multiple participants with non-Ed25519 keys would share the same zero-byte representation
- Creates potential for attestation collision or confusion

---

## Vulnerability Details

### Affected File

`contract/src/tee/tee_state.rs` (lines 173-182)

### Root Cause

The key conversion logic uses `.ok()` to silently discard errors:

```rust
// Simplified flow:
let account_pk_bytes = attestation.node_id.account_public_key
    .as_ref()
    .and_then(|pk| pk.try_to_ed25519().ok())  // .ok() SWALLOWS the error
    .map(|ed25519_key| ed25519_key.to_bytes())
    .unwrap_or([0u8; 32]);  // Fallback: all zeros
```

The chain of operations:
1. If `account_public_key` is `None` -> result is `None`
2. If `account_public_key` is `Some` but NOT Ed25519 (e.g., secp256k1) -> `.ok()` converts the error to `None`
3. `None` -> `.unwrap_or([0u8; 32])` -> all zeros used in the hash

This means **any non-Ed25519 key is treated identically to a missing key**, and all such keys map to the same `[0u8; 32]` value in the `report_data` hash used for attestation binding.

### The Collision Problem

If two participants both have non-Ed25519 keys (or one has `None` and another has a non-Ed25519 key), their `report_data` hashes use the same `[0u8; 32]` input. This creates:

1. **Ambiguous attestation binding**: The attestation cannot distinguish between these participants based on key material
2. **Potential attestation reuse**: Under specific conditions, an attestation generated for one participant could be valid for another

---

## Proof of Concept

**Step 1**: Participant A registers with an Ed25519 key. Their `report_data` hash includes their actual key bytes. Unique and correct.

**Step 2**: Participant B registers with a secp256k1 key (e.g., from an Ethereum-style account). The `.ok()` swallows the conversion error. `report_data` hash includes `[0u8; 32]`.

**Step 3**: Participant C also registers with a non-Ed25519 key. Same result: `[0u8; 32]` in the hash.

**Step 4**: Participant B and Participant C now have the SAME key-derived component in their attestation hashes, despite having different actual keys.

**Step 5**: Depending on how `report_data` is constructed, this could allow attestation confusion between B and C.

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | Attestation binding integrity |
| **Attack Complexity** | HIGH -- requires specific key type conditions |
| **Scope** | Defense-in-depth weakness |
| **Likelihood** | LOW in current deployment (most participants use Ed25519) |

---

## Recommended Fix

1. **Fail loudly on unsupported key types**:

```rust
let account_pk_bytes = match attestation.node_id.account_public_key.as_ref() {
    Some(pk) => {
        pk.try_to_ed25519()
            .map(|key| key.to_bytes())
            .map_err(|e| {
                log!("SECURITY: Non-Ed25519 key in attestation: {:?}", e);
                AttestationError::UnsupportedKeyType
            })?
    }
    None => {
        return Err(AttestationError::MissingPublicKey);
    }
};
```

2. **Support multiple key types explicitly**:

```rust
let account_pk_bytes = match attestation.node_id.account_public_key.as_ref() {
    Some(pk) => match pk {
        PublicKey::Ed25519(key) => key.to_bytes(),
        PublicKey::Secp256k1(key) => {
            // Use a different but deterministic representation
            let mut hasher = Sha256::new();
            hasher.update(b"secp256k1:");
            hasher.update(key.to_bytes());
            hasher.finalize().into()
        }
    },
    None => return Err(AttestationError::MissingPublicKey),
};
```

3. **Never use zero-byte fallbacks for cryptographic operations**.

---

## References

- NEAR MPC Repository: https://github.com/near/mpc
- Related: Finding 2 (account_public_key None bypass) -- same key handling area
