# HackenProof Submission: MEDIUM — Potential Decimal Underflow DoS in Token Denormalization

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/omni-bridge
**Severity**: MEDIUM
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**Unchecked Subtraction in denormalize_amount Panics on Decimal Underflow, Permanently DoS-ing Token Transfers**

---

## Severity Justification

- **MEDIUM**: Permanent denial of service for affected token transfers
- The WASM binary is compiled with `overflow-checks=true`, so underflow causes a panic (not a wrap)
- Once triggered, ALL transfers for the affected token are permanently blocked
- Recovery requires contract upgrade or manual state intervention
- The trigger condition (incorrect token decimals metadata) is plausible in cross-chain contexts

---

## Vulnerability Details

### Affected File

`omni-bridge/src/lib.rs` (line 2732)

### Root Cause

The `denormalize_amount` function performs an unchecked subtraction:

```rust
fn denormalize_amount(amount: u128, origin_decimals: u8, decimals: u8) -> u128 {
    let diff = origin_decimals - decimals;  // PANICS if origin_decimals < decimals
    amount * 10u128.pow(diff as u32)
}
```

If `origin_decimals < decimals`, the subtraction underflows. With `overflow-checks=true` in the WASM build profile, this causes a **panic** (not a silent wraparound), which aborts the entire transaction.

### How Incorrect Decimals Can Occur

1. **Cross-chain decimal mismatch**: Token A on Chain X has 6 decimals, but on Chain Y the wrapped version is registered with 18 decimals. If the bridge stores `origin_decimals=6` and `decimals=18`, every denormalization panics.

2. **Manual token registration error**: An admin registers a token with incorrect decimal metadata. The error is not caught at registration time.

3. **Token upgrade**: A token contract on the origin chain upgrades and changes its decimals value. The bridge's stored metadata becomes stale.

### Permanent DoS

Once a token has mismatched decimals in the bridge's metadata:
- EVERY transfer of that token calls `denormalize_amount`
- EVERY call panics
- The token is permanently frozen in the bridge
- No user can transfer, withdraw, or interact with that token
- Fix requires a contract upgrade to correct the metadata or add underflow protection

---

## Proof of Concept

**Step 1**: Identify (or create, if in a test environment) a token registered in omni-bridge with decimal metadata where `origin_decimals < decimals`.

Example scenario:
- Token USDC on origin chain: 6 decimals
- Incorrectly registered in bridge metadata as: `decimals = 18`

**Step 2**: Initiate a transfer of this token through the bridge. The transfer reaches `denormalize_amount`.

**Step 3**: `denormalize_amount(1000000, 6, 18)` executes:

```
diff = 6 - 18 = underflow!
```

**Step 4**: WASM panics with `attempt to subtract with overflow`. Transaction fails.

**Step 5**: Every subsequent transfer of this token hits the same panic. The token is permanently DoS'd.

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | All tokens of the affected denomination locked in the bridge |
| **Attack Complexity** | LOW (if attacker can influence token registration) / MEDIUM (if relies on admin error) |
| **Reversibility** | Requires contract upgrade -- NOT recoverable through normal operations |
| **Scope** | All users holding or transferring the affected token |
| **Availability Impact** | HIGH -- permanent DoS for the affected token |

---

## Recommended Fix

1. **Use checked subtraction with proper error handling**:

```rust
fn denormalize_amount(amount: u128, origin_decimals: u8, decimals: u8) -> Result<u128, BridgeError> {
    if origin_decimals >= decimals {
        let diff = origin_decimals - decimals;
        amount.checked_mul(10u128.checked_pow(diff as u32)
            .ok_or(BridgeError::DecimalOverflow)?)
            .ok_or(BridgeError::AmountOverflow)
    } else {
        // Reverse: divide instead of multiply
        let diff = decimals - origin_decimals;
        Ok(amount / 10u128.pow(diff as u32))
    }
}
```

2. **Validate decimals at token registration time**:

```rust
fn bind_token(&mut self, token: &TokenId, origin_decimals: u8, bridge_decimals: u8) {
    require!(
        origin_decimals >= bridge_decimals || self.allow_upscaling,
        "Origin decimals must be >= bridge decimals to prevent denormalization panic"
    );
    // ... rest of binding logic
}
```

3. **Add integration tests** that cover cross-chain tokens with varying decimal configurations, including edge cases where `origin_decimals < decimals`.

---

## References

- NEAR Omni Bridge Repository: https://github.com/near/omni-bridge
- Rust overflow-checks: https://doc.rust-lang.org/cargo/reference/profiles.html#overflow-checks
- Related: Finding 5 (silent lock skip) and Finding 3 (detached promise) in the same bridge
