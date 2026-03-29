# HackenProof Submission: MEDIUM — Legacy Nonces Bypass All Validation and Cannot Be Revoked

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/intents
**Severity**: MEDIUM
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**Legacy 32-Byte Nonces Skip All Nonce-Level Validation, Cannot Be Garbage Collected, and Lack Revocation Mechanism**

---

## Severity Justification

- **MEDIUM**: Combination of validation bypass, storage DoS vector, and irrevocable signed intents
- Legacy nonces skip salt, deadline, and expiry checks that protect versioned nonces
- No garbage collection possible for legacy nonces (permanent storage bloat)
- No revocation mechanism during key compromise events
- Affects the migration period from legacy to versioned nonce format

---

## Vulnerability Details

### Affected Files

| File | Lines | Description |
|------|-------|-------------|
| `defuse/core/src/engine/mod.rs` | 88-91 | Legacy nonce early return bypasses validation |
| `defuse/core/src/nonce/versioned.rs` | 21 | `maybe_from` returns None for legacy format |
| `defuse/src/contract/garbage_collector.rs` | 32-36 | GC cannot process legacy nonces |

### Root Cause

The intent execution engine uses `VersionedNonce::maybe_from()` to parse nonces. Legacy nonces (raw 32-byte values) return `None`:

```rust
let Some(nonce) = VersionedNonce::maybe_from(nonce) else {
    return Ok(()); // EARLY RETURN: No salt check, no deadline check, no expiry check
};
```

This means:
1. **No salt validation**: Salt rotation (used to revoke nonces in bulk) is skipped
2. **No deadline enforcement**: Legacy nonces have no expiration deadline
3. **No expiry check**: Time-based expiration is not applied

### Three Compounding Issues

**Issue A -- Validation Bypass**: All nonce-level security checks are skipped for legacy format. Only the basic "has this exact nonce been used before" check remains.

**Issue B -- No Garbage Collection**: The garbage collector cannot process legacy nonces:

```rust
// garbage_collector.rs lines 32-36
// Only processes VersionedNonce format
// Legacy nonces remain in storage permanently
```

This means every legacy nonce consumed permanently occupies contract storage, creating a storage cost that grows monotonically.

**Issue C -- No Revocation**: Versioned nonces support salt rotation for bulk revocation. If a signing key is compromised, the user rotates their salt to invalidate all pending intents. Legacy nonces lack this mechanism entirely -- signed intents with legacy nonces remain valid until executed or until a potential deadline (which is also not enforced).

---

## Proof of Concept

**Scenario: Key Compromise During Migration**

**Step 1**: User has signed intents using legacy nonces (pre-migration).

**Step 2**: User's signing key is compromised.

**Step 3**: User rotates their nonce salt to invalidate all pending versioned nonces -- this works correctly for new-format nonces.

**Step 4**: Attacker replays the legacy-nonce signed intents. The salt rotation has NO effect because legacy nonces skip the salt check entirely.

**Step 5**: The intents execute successfully, causing unintended token transfers from the compromised user.

**Storage DoS Scenario**:

**Step 1**: Attacker creates many intents with unique legacy 32-byte nonces.

**Step 2**: Each consumed nonce permanently occupies storage.

**Step 3**: Legacy nonces cannot be garbage collected, so storage grows without bound.

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | User funds (irrevocable intents after key compromise) |
| **Attack Complexity** | MEDIUM -- requires key compromise plus legacy nonces |
| **Storage Impact** | Permanent storage bloat from non-GC-able nonces |
| **Affected Period** | Migration window from legacy to versioned nonce format |

---

## Recommended Fix

1. **Reject legacy nonces or enforce minimum checks**:

```rust
let Some(nonce) = VersionedNonce::maybe_from(nonce) else {
    // Option A: Reject legacy nonces after migration deadline
    if env::block_timestamp() > LEGACY_NONCE_DEADLINE {
        return Err(DefuseError::LegacyNonceExpired);
    }
    // Option B: At minimum, check against user's current salt
    if !self.is_legacy_nonce_valid_for_salt(account_id, nonce) {
        return Err(DefuseError::NonceSaltMismatch);
    }
    return Ok(());
};
```

2. **Add legacy nonce garbage collection**: Implement a migration path that converts legacy nonces to versioned format or allows their cleanup.

3. **Add legacy nonce revocation**: Allow users to invalidate all legacy nonces via a dedicated `revoke_legacy_nonces` function.

---

## References

- NEAR Intents Repository: https://github.com/near/intents
- Nonce versioning design: `defuse/core/src/nonce/versioned.rs`
