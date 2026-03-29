# HackenProof Submission: HIGH — Detached Promise Token Loss in Fast Transfer Finalization

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/omni-bridge
**Severity**: HIGH
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**Detached Promise in Fast Transfer Finalization Causes Permanent Token Loss for Relayers When ft_transfer Fails**

---

## Severity Justification

- **HIGH**: Direct loss of funds for relayers
- The `.detach()` call severs the promise chain, making failure undetectable
- Fast transfer is irreversibly marked as finalized BEFORE token transfer succeeds
- No refund mechanism exists for this code path (unlike the NEAR transfer path which handles refunds properly)
- Relayers who front liquidity for fast transfers lose their reimbursement permanently

---

## Vulnerability Details

### Affected File

`omni-bridge/src/lib.rs` (lines 2016-2028)

### Root Cause

In `process_fin_transfer_to_other_chain`, the fast transfer finalization path:

```rust
// Fast transfer finalization (VULNERABLE)
self.send_tokens(token, relayer, amount_without_fee, "").detach();
self.mark_fast_transfer_as_finalised(&fast_transfer.id());
```

The `.detach()` call means:
1. `send_tokens` (which calls `ft_transfer`) is fired as a detached promise
2. If `ft_transfer` fails (e.g., relayer account not registered for the token, storage deposit insufficient, or contract paused), the failure is SILENTLY IGNORED
3. `mark_fast_transfer_as_finalised` executes regardless, marking the transfer as complete
4. The finalization is IRREVERSIBLE -- there is no mechanism to retry or refund

### Comparison with Correct Implementation

The NEAR transfer path (`process_fin_transfer_to_near`, lines 1709-1723) handles this correctly:

```rust
// NEAR transfer finalization (CORRECT)
// Uses is_refund_required callback to detect failures
// Implements refund logic for failed transfers
```

This inconsistency proves the developers are aware of the failure scenario but did not implement the same safeguard in the cross-chain path.

---

## Proof of Concept

**Step 1**: Relayer executes a fast transfer, fronting liquidity for a user's cross-chain transfer.

**Step 2**: The canonical (slow) transfer arrives and triggers `process_fin_transfer_to_other_chain`.

**Step 3**: The bridge calls `send_tokens` to reimburse the relayer, but the relayer's account lacks storage deposit for the token:

```
ft_transfer fails: "The account relayer.near is not registered"
```

**Step 4**: Because `.detach()` was used, the bridge contract never learns about the failure.

**Step 5**: `mark_fast_transfer_as_finalised` marks the transfer as complete.

**Step 6**: The relayer's reimbursement is permanently lost. There is no retry, no refund, and no event emitted to alert anyone.

### Failure Scenarios That Trigger This Bug

- Relayer account not registered for the fungible token
- Insufficient storage deposit on the relayer's account
- Token contract is paused or upgraded mid-transfer
- Token contract runs out of gas during execution
- Any `ft_transfer` revert for any reason

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | Relayer funds (reimbursement for fronted liquidity) |
| **Attack Complexity** | LOW -- can occur naturally without adversarial action |
| **Frequency** | Every time `ft_transfer` fails during fast transfer finalization |
| **Reversibility** | IRREVERSIBLE -- finalization cannot be undone |
| **Affected Parties** | All relayers participating in fast transfers |

### Economic Impact

Relayers are critical infrastructure for fast transfers. If relayers lose funds to this bug, they will stop providing fast transfer liquidity, degrading the bridge's user experience and throughput.

---

## Recommended Fix

Replace the detached promise with a proper callback chain:

```rust
// FIXED: Use callback to handle ft_transfer failures
let promise = self.send_tokens(token.clone(), relayer.clone(), amount_without_fee, "");

promise.then(
    Self::ext(env::current_account_id())
        .with_static_gas(Gas::from_tgas(5))
        .on_fast_transfer_finalization(
            fast_transfer.id(),
            token,
            relayer,
            amount_without_fee,
        )
);
```

```rust
#[private]
pub fn on_fast_transfer_finalization(
    &mut self,
    transfer_id: TransferId,
    token: AccountId,
    relayer: AccountId,
    amount: U128,
) {
    if env::promise_results_count() == 1 {
        match env::promise_result(0) {
            PromiseResult::Successful(_) => {
                self.mark_fast_transfer_as_finalised(&transfer_id);
            }
            PromiseResult::Failed => {
                // Log the failure, store for retry, or refund
                log!("Fast transfer finalization failed for {}, scheduling retry", transfer_id);
                self.pending_fast_transfer_refunds.insert(&transfer_id, &PendingRefund {
                    token, relayer, amount
                });
            }
        }
    }
}
```

---

## References

- NEAR Omni Bridge Repository: https://github.com/near/omni-bridge
- Correct implementation for comparison: `process_fin_transfer_to_near` (lines 1709-1723)
- NEAR Promise documentation: https://docs.near.org/sdk/rust/promises/intro
