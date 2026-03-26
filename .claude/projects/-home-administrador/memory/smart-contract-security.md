# Smart Contract Security — Knowledge Base (26 Mar 2026)

## NEAR INTENTS AUDIT LEARNINGS (Session 30.5)

### MPC Bridge Attack Patterns
1. **TEE bypass via Mock attestation** — If test enum variants aren't feature-gated, production WASM includes them. CHECK: `#[cfg(test)]` on all test-only types.
2. **Optional key checks** — `Option<Key>` in attestation = key check skipped when None. ALWAYS use `require!(key.is_some())`.
3. **Detached promise fund loss** — `.detach()` in NEAR means NO error handling. If ft_transfer fails, tokens stuck forever. COMPARE: same bridge's other paths that DO check results.
4. **Cross-chain encoding asymmetry** — NEAR Borsh vs EVM ABI encoding. Check: V1/V2 struct patterns for backward compat. Empty vs None vs Some(empty) differences.
5. **Nonce migration replay** — When transitioning nonce schemes (random→versioned), legacy nonces bypass new validations.
6. **Lock accounting gaps** — Only tracking origin-chain locks misses cross-chain routing. Bridge appears solvent but can't prove it.

### Audit Methodology (Parallel Agents)
- **Pattern**: Launch 3-4 specialized agents in parallel for different code areas
- TEE agent: attestation/access control
- Bridge agent: lock/unlock/mint/burn accounting
- Nonce agent: replay protection, migration gaps
- Main thread: cross-chain encoding, Solana/EVM verification
- **Time**: ~6 minutes for complete audit of 3 repos (16K+ lines)
- **Yield**: 8 findings (1C, 2H, 5M) in single session

## TOP 30 VULNERABILITIES (Rank by $ Lost)
1. **Private key compromise** — $625M (Ronin 2022)
2. **Access control (bridge)** — $611M (Poly Network 2021)
3. **Missing signer check** — $320M (Wormhole 2022)
4. **Flash loan + oracle** — $197M (Euler 2023)
5. **Misconfigured upgrade** — $190M (Nomad 2022)
6. **Flash loan + governance** — $182M (Beanstalk 2022)
7. **ERC-777 reentrancy** — $130M (Cream 2021)
8. **Oracle manipulation** — $114M (Mango 2022)
9. **Compiler bug reentrancy** — $69M (Curve 2023)
10. **Classic reentrancy** — $70M (The DAO 2016)

## VULNERABILITY CATEGORIES (Quick Reference)
### Reentrancy (CEI Pattern Fix)
- Classic: external call before state update
- Cross-function: function A calls external, attacker reenters function B
- Cross-contract: A→B→C→back to A via different entry
- Read-only: view function returns wrong value during state transition
- **FIX**: Checks-Effects-Interactions + ReentrancyGuard + CEI always

### Flash Loans
- NOT inherently malicious — amplifier for other bugs
- Price manipulation: borrow→buy→inflate→borrow against→repay
- Governance: borrow tokens→vote→drain→repay
- **FIX**: TWAP oracles, time-locks, solvency checks on ALL functions

### Oracle
- Spot price = DANGEROUS (flash loan manipulable)
- Chainlink: check staleness, answeredInRound >= roundId, price > 0
- TWAP: period must be long enough (30min+)
- **FIX**: Multi-source oracles, minimum liquidity requirements

### Access Control
- Missing modifiers on admin functions
- tx.origin phishing (use msg.sender always)
- Uninitialized proxy (initialize can be called by anyone)
- **FIX**: OpenZeppelin AccessControl, Ownable2Step, time-locks

### Math
- Integer overflow (pre-0.8 wraps silently, unchecked blocks in 0.8+)
- Precision loss (divide before multiply = BAD)
- Rounding direction (floor for user withdrawal, ceil for collateral)
- **FIX**: Solidity 0.8+, FullMath.mulDiv, audit unchecked blocks

### Proxy/Upgradeable
- Storage collision (delegatecall uses caller's storage)
- Uninitialized implementation (initialize() callable by anyone)
- UUPS: _authorizeUpgrade without access control
- **FIX**: EIP-1967 unstructured storage, EIP-7201 namespaced, Ownable2Step

### ERC-4626 Inflation Attack
- First depositor donates to vault → manipulates share price → robs next depositor
- **FIX**: Virtual shares offset (OpenZeppelin v5), dead shares, internal balance tracking

### Solana-Specific
- Missing signer check (is_signer not verified)
- Missing owner check (account owned by wrong program)
- Type cosplay (wrong account type deserialized)
- Shared PDA vulnerability (per-user PDAs needed)
- Account not reloaded after CPI
- **FIX**: Anchor constraints, discriminators, bump storage, reload()

## AUDIT METHODOLOGY (Top Firms)
1. **Scoping**: files, commits, threat model, nSLOC, complexity
2. **Automated**: Slither, Mythril, forge coverage
3. **Manual**: line-by-line, two independent reviewers
4. **Fuzzing**: Echidna/Foundry invariant tests
5. **Report**: title, severity, impact, PoC, fix
6. **Remediation**: verify each fix, check for new bugs

## TOOLS
| Tool | Type | Cost | Best For |
|------|------|------|----------|
| Slither | Static analysis | Free | Fast pattern detection, 70+ detectors |
| Foundry | Fuzz + invariant | Free | Best DX, stateful fuzzing, fork testing |
| Echidna | Property fuzzer | Free | Complex invariant testing |
| Mythril | Symbolic exec | Free | Deep logic bugs via SMT |
| Certora | Formal verif | Paid | Mathematical proofs ($32B+ TVL verified) |
| Medusa | Fuzzer | Free | Newer, Echidna-compatible |
| Halmos | Symbolic | Free | Foundry-compatible symbolic execution |

## LEARNING PATH
1. **Foundation** (1-3mo): Cyfrin Updraft, Ethernaut (30 levels), DVDeFi 1-10
2. **Pattern Recognition** (3-6mo): Read 20 audit reports (solodit.xyz), C4 contests
3. **Competition** (6-12mo): 1 contest/2 weeks, specialize in 1 area
4. **Elite** (12mo+): Top 100 warden, custom Slither detectors, Immunefi bounties

## KEY RESOURCES (Free)
- Cyfrin Updraft: updraft.cyfrin.io/courses/security
- Ethernaut: ethernaut.openzeppelin.com
- Damn Vulnerable DeFi v4: damnvulnerabledefi.xyz
- solodit.xyz: searchable finding database (ALL public reports)
- Secureum bootcamp: secureum.xyz
- RareSkills: rareskills.io (deep technical)
- Trail of Bits publications: github.com/trailofbits/publications

## C4 CONTEST STRATEGY
- Severity: Critical (10x), High (7x), Medium (3x), Low/QA (1x)
- Coded PoC MANDATORY for High/Critical
- Unique finding formula: 10 * 0.9^n / n (n = number finding same bug)
- Focus: highest-value contracts first (most TVL exposure)
- Post-contest: read ALL findings (learn what you missed)

## ZK-EVM AUDIT — ZKsync OS evm_interpreter (25 Mar 2026)

### Bug Found: Callstack Depth Off-By-One (MEDIUM)
- **File**: `evm_interpreter/src/ee_trait_impl.rs`, line 351
- **Bug**: `callstack_depth > 1024` should be `>= 1024`
- **Impact**: Allows 1025 frames instead of EVM standard 1024
- **EVM Spec**: Yellow Paper Section 9.4.2 — `I_e < 1024` for call to proceed
- **Report**: `~/zksync-os-bug-report.md`
- **PoC**: Solidity contract showing maxDepthReached=1024 vs expected 1023
- **Immunefi submission**: PENDING (need KYC + registration)

### ZK-EVM Audit Methodology (Confirmed Working)
1. Map codebase structure (`find src/ -name "*.rs" | wc -l`)
2. Read ALL files systematically (batch 5-6 files per parallel read)
3. Compare each opcode implementation against Yellow Paper
4. Focus on boundary conditions: `>` vs `>=`, `<` vs `<=`
5. Check operand ordering (stack pop order matters)
6. Verify signed arithmetic edge cases (MIN_INT / -1, etc.)
7. Check gas accounting matches EVM spec constants
8. Look for ZKsync-specific deviations (intentional vs bugs)

### ZKsync OS Codebase Structure (21 files, 4640 lines)
- `ee_trait_impl.rs` (450L): Frame lifecycle, **BUG HERE**
- `interpreter.rs` (518L): Main execution loop, opcode dispatch
- `host.rs` (478L): Storage, CALL variants, CREATE, LOG
- `evm_stack.rs` (519L): Unsafe stack impl, MaybeUninit<U256>[1024]
- `opcodes.rs` (501L): Opcode constants, jump map
- `lib.rs` (492L): Interpreter struct, ExitCode, bytecode preprocessing
- `system.rs` (235L): SHA3, ADDRESS, CALLER, CALLDATA*
- `native_resource_constants.rs` (176L): ZK proving costs
- `gas.rs` (157L): Dual accounting (ergs + native), ERGS_PER_GAS=256
- `i256.rs` (153L): Signed 256-bit arithmetic
- `bitwise.rs` (152L): Comparison & bitwise ops
- `arithmetic.rs` (132L): ADD/MUL/SUB/DIV/MOD/EXP
- `utils.rs` (173L): bytereverse, RLP encoding, precompile check
- `environment.rs` (105L): Block info opcodes
- `heap.rs` (111L): MLOAD/MSTORE/MSIZE/MCOPY
- `control_flow.rs` (81L): JUMP/JUMPI/JUMPDEST/PC/RETURN/REVERT
- `stack.rs` (62L): POP/PUSH/DUP/SWAP
- `gas_constants.rs` (54L): EVM gas costs (verified correct)
- `u256.rs` (57L): mul_mod, log2floor

### Verified Correct (Not Bugs)
- ADDMOD/MULMOD modulus=0 → ruint returns 0 (matches EVM)
- SDIV(-2^255, -1) → two_compl_mut correct (wraps to same value)
- SIGNEXTEND at all edge cases (shift=0, shift=31)
- All operand ordering for 2-operand opcodes (pop order)
- CREATE RLP encoding (nonce=0 → 0x80)
- Storage ops charge 0 EVM gas (deferred to IO subsystem — intentional)
- BLOBHASH returns 0, BLOBBASEFEE returns 1 (ZKsync-specific — intentional)
- Gas constants match Yellow Paper exactly
- Stack overflow/underflow checks correct

### ZK-EVM Common Bug Patterns (For Future Audits)
- **Off-by-one in limits**: callstack depth, gas bounds, memory expansion
- **Operand ordering**: EVM stack is LIFO — `a = pop(); b = pop(); push(a OP b)` vs `push(b OP a)`
- **Signed arithmetic edge cases**: MIN_INT, division by zero, modulo by zero
- **Memory expansion cost formula**: quadratic component easy to get wrong
- **RETURNDATACOPY bounds**: must check against actual returndata length
- **Gas forwarding (63/64 rule)**: `available - available/64` for CALL
- **Precompile address range**: 0x01-0x0a (10 precompiles post-Cancun)

## AUDIT CHECKLIST (Quick)
- [ ] CEI pattern on all external calls
- [ ] nonReentrant on state-changing + external call functions
- [ ] Access control on ALL privileged functions
- [ ] Oracle staleness + validity checks
- [ ] No division before multiplication
- [ ] Rounding favors protocol
- [ ] Return values checked on call/send/delegatecall
- [ ] Signatures: nonce + deadline + chainId + EIP-712
- [ ] Proxy: storage layout matches, initialize protected
- [ ] Fee-on-transfer: balance diff pattern
- [ ] No unbounded loops over user-controlled arrays
- [ ] Pull over push for payments
