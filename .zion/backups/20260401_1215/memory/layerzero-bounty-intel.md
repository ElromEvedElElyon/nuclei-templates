# LayerZero V2 Bounty Intelligence — 31 Mar 2026

## Program: Immunefi | Account: PadraoBTC736 | Max: $15M | ~$1M paid historically
## ALSO: USDT0 separate bounty ($6M max) — built on LayerZero OFT

## TOP ATTACK VECTORS (Session 79 Research)

### PRIORITY 1: _clearPayload DoS ($250K+)
- EndpointV2.sol loops through nonces in _clearPayload
- Attack: Send 500+ messages to create nonce gap → execution becomes permanently impossible (OOG)
- Ordered execution OApps especially vulnerable — single revert blocks ALL
- PoC: Foundry test with mock DVN, demonstrate gas exceeds block limit
- Risk of rejection: MEDIUM (LayerZero knows about it but "clear/skip" mitigation insufficient)

### PRIORITY 2: _toSD uint64 Truncation ($250K+)
- OFTCore._toSD() casts to uint64 SILENTLY — no revert on overflow
- When sharedDecimals == localDecimals == 18, amounts > 18.4 quintillion truncate
- Source debits full amount, destination credits truncated value → fund loss
- Risk of rejection: MEDIUM-HIGH (may classify as "OApp misconfiguration")
- ALSO applies to USDT0 bounty ($6M)

### PRIORITY 3: lzCompose Validation Bypass ($25K-$250K)
- lzCompose callback needs DUAL validation: msg.sender == Endpoint AND _from == expected OApp
- Missing either allows unauthorized composed message execution
- Must find this in LayerZero-maintained contract (not third-party)

### PRIORITY 4: Ordered Execution Freeze ($10K-$25K)
- Reverting lzReceive at nonce N permanently blocks N+1, N+2... forever
- Cheap attack, expensive recovery. Asymmetric griefing.

## KEY INTEL
- LayerZero DOWNGRADES severity (Trust-Security got $5K for HIGH)
- "OApp misconfiguration" is main rejection reason — focus on PROTOCOL contracts
- KYC required, PoC mandatory, local testing only
- Primacy of Impact allows any LayerZero-managed contract for Critical/High
- Previous findings: Prestwich ZeroValidation, Cobo MPT proof, Dedaub DVN-AVS

## REPOS TO CLONE
- https://github.com/LayerZero-Labs/LayerZero-v2
- Key files: EndpointV2.sol, OFTCore.sol, SendUln302.sol, ReceiveUln302.sol

## NEXT STEPS
1. Clone LayerZero-v2 repo
2. Build Foundry PoC for Vector B (_clearPayload DoS)
3. Build Foundry PoC for Vector A (_toSD truncation)
4. Audit LayerZero-maintained composers for Vector C
5. Submit strongest finding first on Immunefi
