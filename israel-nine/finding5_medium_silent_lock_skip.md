# HackenProof Submission: MEDIUM — Silent Lock Skip for Cross-Chain Token Routing

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/omni-bridge
**Severity**: MEDIUM
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**lock_tokens() Silently Returns Unchanged for Non-Origin Chain Tokens, Bypassing Solvency Tracking in Cross-Chain Routes**

---

## Severity Justification

- **MEDIUM**: Incomplete solvency tracking weakens bridge accounting integrity
- Cross-chain routed tokens (e.g., ETH -> NEAR -> Base) bypass lock tracking on intermediate chains
- The silent `Unchanged` return hides the accounting gap from monitoring systems
- Could lead to insolvency if exploited in combination with other vulnerabilities

---

## Vulnerability Details

### Affected File

`omni-bridge token_lock.rs` (lines 55-57)

### Root Cause

The `lock_tokens()` function silently returns when no lock entry exists for a token:

```rust
let Some(current_amount) = self.locked_tokens.get(&key) else {
    return LockAction::Unchanged;  // SILENT: No lock entry, no error, no event
};
```

Lock entries are only initialized during `bind_token_callback` for the token's ORIGIN chain. When a token is routed through an intermediate chain (e.g., an ERC-20 going from Ethereum -> NEAR -> Base), the intermediate chain has no lock entry.

### The Accounting Gap

Consider a token flow: ETH (origin: Ethereum) routed via NEAR to Base.

1. **Ethereum side**: Lock entry exists (origin chain). Lock tracking works correctly.
2. **NEAR side (intermediate)**: No lock entry. `lock_tokens()` returns `Unchanged`. The bridge wraps/unwraps the token on NEAR but the solvency tracker does not record this.
3. **Base side**: No lock entry. Same silent skip.

This means the bridge's solvency accounting only tracks tokens on their origin chain, not across the full routing path. The total locked amount may not reflect the actual obligations across all chains.

---

## Proof of Concept

**Step 1**: Deploy a token on Chain A and bridge it to NEAR via omni-bridge.
- `bind_token_callback` creates a lock entry on Chain A.

**Step 2**: From NEAR, initiate a cross-chain transfer of this token to Chain B.
- NEAR calls `lock_tokens()` for the Chain A token.
- No lock entry exists on NEAR for this token.
- `lock_tokens()` returns `LockAction::Unchanged`.
- The transfer proceeds without any lock accounting update.

**Step 3**: Query the bridge's locked token state.
- Chain A shows the original locked amount.
- NEAR and Chain B show NO locked amount for this token.
- The total reported locked tokens undercount the actual obligations.

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | Bridge solvency accounting integrity |
| **Attack Complexity** | LOW -- occurs naturally in any cross-chain routing |
| **Detection Difficulty** | HIGH -- silent return produces no errors or events |
| **Scope** | All cross-chain routed tokens (non-origin-chain transfers) |

### Cascading Risk

If the bridge relies on `locked_tokens` for solvency checks (e.g., ensuring it holds enough backing assets), the undercount could allow over-withdrawal. This is especially dangerous if combined with the detached promise bug (Finding 3), which can silently lose tokens.

---

## Recommended Fix

1. **Initialize lock entries for all chains during routing**:

```rust
pub fn lock_tokens(&mut self, key: &TokenLockKey, amount: u128) -> LockAction {
    let current_amount = self.locked_tokens.get(&key).unwrap_or(0);
    let new_amount = current_amount.checked_add(amount)
        .expect("Lock amount overflow");
    self.locked_tokens.insert(key, &new_amount);
    LockAction::Locked { previous: current_amount, new: new_amount }
}
```

2. **Alternatively, return an explicit error** instead of silently skipping:

```rust
let Some(current_amount) = self.locked_tokens.get(&key) else {
    return LockAction::Error(LockError::NoLockEntryForToken);
};
```

3. **Add events/logging** for lock operations so monitoring can detect gaps.

---

## References

- NEAR Omni Bridge Repository: https://github.com/near/omni-bridge
- Token binding flow: `bind_token_callback`
- Related: Finding 3 (detached promise) and Finding 8 (decimal underflow) in the same bridge
