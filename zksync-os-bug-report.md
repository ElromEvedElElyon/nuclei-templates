# ZKsync OS EVM Interpreter — Callstack Depth Off-By-One

## Summary

The EVM interpreter in `zksync-os` allows a callstack depth of 1025 instead of the standard EVM limit of 1024. This is caused by an off-by-one error in the depth comparison (`> 1024` instead of `>= 1024`).

## Vulnerability Details

**File:** `evm_interpreter/src/ee_trait_impl.rs`, line 351

**Current code:**
```rust
fn before_executing_frame<'a, 'i: 'ee, 'h: 'ee>(
    system: &mut System<S>,
    frame_state: &mut ExecutionEnvironmentLaunchParams<'i, S>,
    tracer: &mut impl Tracer<S>,
) -> Result<bool, Self::SubsystemError>
where
    S::IO: IOSubsystemExt,
{
    if frame_state.environment_parameters.callstack_depth > 1024 {
        // ... reject call
    }
    // ...
}
```

**Expected:**
```rust
    if frame_state.environment_parameters.callstack_depth >= 1024 {
```

### Root Cause

The Ethereum Yellow Paper (Section 9.4.2) specifies:

> The depth of the call stack is limited to 1024.

The `before_executing_frame` function checks whether a new frame can be launched. With the `> 1024` comparison:

- Depth 0 through 1024: allowed (1025 total frames)
- Depth 1025: rejected

The correct check should use `>= 1024` to limit to exactly 1024 frames (depths 0 through 1023).

### EVM Specification Reference

From the Yellow Paper:
- `I_e` (call depth) must satisfy `I_e < 1024` for the call to proceed
- This means maximum depth is 1023, giving 1024 total frames

Every major EVM implementation (geth, erigon, reth, revm) enforces a strict 1024-frame limit.

## Impact

### State Divergence
ZKsync OS is a ZK rollup that generates validity proofs of EVM execution. If the EVM interpreter produces different results from the canonical EVM specification, the ZK proofs would attest to incorrect state transitions. This is the fundamental correctness property that a ZK-EVM must uphold.

### Concrete Exploitation Scenario
1. A smart contract uses recursive calls that intentionally hit the 1024 depth limit
2. On Ethereum L1, the 1025th call fails → contract behaves one way
3. On ZKsync OS, the 1025th call succeeds → contract behaves differently
4. This creates a state that cannot be reproduced on L1, breaking the equivalence guarantee

### Affected Patterns
- Reentrancy guards that test depth limits
- Gas estimation contracts that probe callstack boundaries
- Proxy contracts with deep delegation chains
- Any contract that uses `CALL` in a loop approaching 1024 iterations

## Proof of Concept

The following Solidity contract demonstrates the issue:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CallDepthTest {
    uint256 public maxDepthReached;

    function testDepth(uint256 depth) external {
        maxDepthReached = depth;
        // Try to call deeper
        try this.testDepth(depth + 1) {} catch {
            // Call failed - we've hit the limit
            // On standard EVM: maxDepthReached = 1023
            // On ZKsync OS:    maxDepthReached = 1024
        }
    }
}
```

On standard EVM: `maxDepthReached` = 1023 (1024 total frames including the initial call).
On ZKsync OS: `maxDepthReached` = 1024 (1025 total frames).

## Recommended Fix

```diff
- if frame_state.environment_parameters.callstack_depth > 1024 {
+ if frame_state.environment_parameters.callstack_depth >= 1024 {
```

## Classification

- **Severity:** Medium
- **Type:** Undocumented deviation from EVM behavior
- **Component:** evm_interpreter (ZKsync OS)
- **Scope:** All EVM contracts executing on ZKsync OS
