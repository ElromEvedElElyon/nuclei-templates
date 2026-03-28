# Layer3 CUBE Security Findings — HackenProof Submission Package
# Em nome do Senhor Jesus Cristo
# Date: 27 Mar 2026
# Target: Layer3 Foundation Smart Contracts (layer3xyz/cubes)
# Platform: HackenProof (zero-rep program, $500K bounty)
# Researcher: ElromSecurity / inteligenciaartificial.now@gmail.com

---

## FINDING 1 [CRITICAL]: ERC1155 Parameter Swap in Factory.withdrawFunds — Permanent Fund Loss

**File**: `src/escrow/Factory.sol` line 188
**Type**: Logic Error / Parameter Swap
**CWE**: CWE-683 (Function Call With Incorrect Order of Arguments)

### Description
In `Factory.withdrawFunds()`, the ERC1155 withdrawal call passes `tokenId` in the `amount` position and `erc1155Amount` in the `tokenId` position. The parameters are SWAPPED compared to the interface definition.

### Vulnerable Code
```solidity
// Factory.sol line 188 — WRONG parameter order
IEscrow(escrow).withdrawERC1155(token, to, tokenId, erc1155Amount);
//                                              ^tokenId  ^amount  ← SWAPPED!

// IEscrow.sol line 7 — CORRECT interface
function withdrawERC1155(address token, address to, uint256 amount, uint256 tokenId) external;
//                                                         ^amount  ^tokenId
```

### Impact
- Admin calls `withdrawFunds(questId, to, token, 5, TokenType.ERC1155)` to recover 1000 tokens of tokenId 5
- `escrowERC1155Reserves(token, 5)` returns 1000
- Call becomes `withdrawERC1155(token, to, 5, 1000)` — "transfer 5 of tokenId 1000"
- If tokenId 1000 doesn't exist → revert → **tokens permanently locked in escrow**
- If tokenId 1000 exists → **WRONG tokens transferred**

Note: `distributeRewards` (line 231) correctly passes parameters. Bug is isolated to admin withdrawal.

### Severity
CRITICAL — Direct permanent loss of ERC1155 funds in escrow. No recovery mechanism.

---

## FINDING 2 [HIGH]: withdraw() Permanently Breaks Treasury Sweep Accounting

**File**: `src/CUBE.sol` lines 750-757, 761-786
**Type**: Accounting Desynchronization

### Description
`withdraw()` drains ALL native ETH but does NOT reset `s_treasuryBalanceNative`. After withdrawal, `sweepToTreasury()` tries to send more ETH than the contract holds, permanently reverting.

### Attack Path
1. Users mint CUBEs → `s_treasuryBalanceNative = 10 ETH`
2. Admin calls `withdraw()` → drains 10 ETH, but counter stays at 10
3. More minting → `s_treasuryBalanceNative = 15 ETH`, contract only has 5 ETH
4. `sweepToTreasury()` tries to send 15 ETH → **REVERTS permanently**

### Severity
HIGH — Treasury sweep permanently bricked after any `withdraw()` call.

---

## FINDING 3 [MEDIUM]: Excess Native ETH Not Refunded in mintCube

**File**: `src/CUBE.sol` lines 358-362
**Type**: Missing Refund

User overpaying (msg.value > cubeData.price) loses excess ETH. Contract keeps it, admin extracts via withdraw().

---

## FINDING 4 [MEDIUM]: Missing Reentrancy Guard on TaskEscrow.claimReward

**File**: `src/escrow/TaskEscrow.sol` lines 66-107
**Type**: Missing Protection

`claimReward` makes external calls (treasury forwarding, ERC721/ERC1155 safeTransfer callbacks) without nonReentrant modifier. CUBE.mintCube correctly uses it, but TaskEscrow does not.

---

## SUMMARY

| # | Severity | Finding | Est. Bounty |
|---|----------|---------|-------------|
| 1 | CRITICAL | ERC1155 parameter swap — fund loss | $5K-$15K |
| 2 | HIGH | withdraw() breaks treasury sweep | $3K-$8K |
| 3 | MEDIUM | Excess ETH not refunded | $1K-$3K |
| 4 | MEDIUM | Missing reentrancy guard | $1K-$3K |

**TOTAL POTENTIAL: $10K-$29K + reputation points for NEAR access**
