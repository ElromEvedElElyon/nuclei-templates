# DeFi Development — Knowledge Base (25 Mar 2026)

## ERC-4626 VAULT (Core Pattern)
### Rounding Rules (CRITICAL — protects vault from manipulation)
```
deposit(assets) → shares  : Floor  (fewer shares → protects vault)
mint(shares)    → assets  : Ceil   (more assets  → protects vault)
withdraw(assets)→ shares  : Ceil   (more shares burned → protects vault)
redeem(shares)  → assets  : Floor  (fewer assets out → protects vault)
```
- Virtual shares offset: CRITICAL anti-inflation-attack (add 1e6 virtual shares)
- Exchange rate: starts at 1:1, grows with accrued interest
- From our codebase: v4lend/src/vault/V4Vault.sol, solana-vault-standard/programs/svs-1

## AMM MATHEMATICS
### Constant Product (x*y=k)
```
Δy = y · Δx / (x + Δx)                    # basic
Δy = y · (Δx · (1-f)) / (x + Δx · (1-f))  # with fee f
priceImpact ≈ Δx / x                       # for small trades
```

### Concentrated Liquidity (Uniswap V3/V4)
- sqrtPriceX96 = sqrt(price) * 2^96
- Tick: price(tick) = 1.0001^tick (~0.01% per tick)
- Capital efficiency: up to 4000x vs V2 (same liquidity, tighter range)
- amount0 = L * (sqrtUpper - sqrtCurrent) / (sqrtCurrent * sqrtUpper / 2^96)
- amount1 = L * (sqrtCurrent - sqrtLower) / 2^96

### StableSwap (Curve)
- Combines constant-sum + constant-product
- A = amplification coefficient (higher = more stable)
- Solved iteratively via Newton-Raphson
- 4A(x+y) + D = 4AD + D³/(4xy)

### Impermanent Loss
```
IL = 2*sqrt(P') / (1 + P') - 1
P' = new_price / initial_price
P'=2.0 → IL = -5.72%
P'=4.0 → IL = -20%
```
- Concentrated liquidity: IL is AMPLIFIED within range

## LENDING PROTOCOLS
### Interest Rate Model (Two-Slope / Kink)
```
Below kink: borrowRate = baseRate + utilization * multiplier
Above kink: borrowRate = baseRate + kink*multiplier + (util-kink)*jumpMultiplier
supplyRate = borrowRate * utilization
```
- Typical: base=0%, multiplier=5%, jumpMultiplier=109%, kink=80%
- At 50% util: borrow≈2.5%/yr | At 90%: borrow≈14.9%/yr

### Health Factor & Liquidation
```
healthFactor = collateralValue * collateralFactor / debtValue
if healthFactor < 1.0 → liquidatable
liquidationPenalty: 2-10% (incentive for liquidators)
```
- Flash loan liquidation: borrow→liquidate→swap collateral→repay→profit

## FIXED-POINT ARITHMETIC
| Notation | Bits | Use |
|----------|------|-----|
| Q64 | 64 fractional | Interest rates per second |
| Q96 | 96 fractional | Uniswap sqrtPrice, exchange rates |
| Q32 | 32 fractional | Collateral factors, fees |
| BPS | 1/10000 | Fee percentages (300 BPS = 3%) |
- ALWAYS use FullMath.mulDiv() for Q-notation (prevents phantom overflow)

## SOLANA/RUST PATTERNS
### Anchor Constraints (Account Validation)
```rust
#[account(mut)] pub user: Signer<'info>,     // MUST sign
#[account(seeds=[b"vault", user.key().as_ref()], bump=vault.bump)]  // PDA
#[account(has_one=authority)]                  // field match
#[account(constraint=!vault.paused)]           // custom
```
- ALWAYS store canonical bump in account
- Reload accounts after CPI: `ctx.accounts.vault.reload()?`
- Use checked math: `a.checked_add(b).ok_or(ErrorCode::Overflow)?`
- Token-2022: transfer hooks, confidential transfers, interest-bearing

### CPI (Cross-Program Invocation)
```rust
// PDA-signed CPI for vault operations
let signer_seeds: &[&[&[u8]]] = &[&[VAULT_SEED, mint.as_ref(), &[bump]]];
token_2022::mint_to(CpiContext::new_with_signer(program, accounts, signer_seeds), amount)?;
```

## MCP SERVER DEVELOPMENT
### TypeScript Pattern (claw-mcp-toolkit)
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
srv.tool("tool_name", "description", { param: z.string() }, async ({param}) => {
    return { content: [{ type: "text", text: result }] };
});
```
### Python Pattern (polymarket-mcp-server)
```python
@server.list_tools() → list[types.Tool]
@server.call_tool() → list[types.TextContent]
```
- Glama AAA: tools+descriptions, error handling, input validation
- Publishing: npm, configure in ~/.claude.json mcpServers

## FOUNDRY TESTING
### Key Cheatcodes
- `vm.prank(addr)` — next call from addr
- `deal(token, user, amount)` — set balance
- `vm.warp(time)` — advance time
- `vm.expectRevert()` — expect revert
- `bound(x, min, max)` — constrain fuzz input
- `vm.createFork(rpc, block)` — fork mainnet

### Testing Patterns
- Unit: test specific function behavior
- Fuzz: `testFuzz_X(uint amount)` with `bound()`
- Invariant: `invariant_X()` — random call sequences, verify property holds
- Fork: test against real deployed contracts

## GAS OPTIMIZATION
- Storage packing: multiple vars in 32-byte slot (uint128+uint128)
- calldata > memory for read-only params
- unchecked {} where overflow impossible (loop counters)
- ++i > i++ (saves 5 gas)
- TSTORE/TLOAD (EIP-1153): 100 gas vs 20000 for transient storage
- Storage reference vs memory copy for struct modification

## CROSS-CHAIN / BRIDGES
- Lock-and-mint: risky (locked funds = honeypot)
- Burn-and-mint: better (Circle CCTP pattern)
- LayerZero: OApp standard, _lzSend/_lzReceive
- CCIP (Chainlink): router.ccipSend(), CCIPReceiver
- Security: finality, replay (nonces), value caps, oracle independence, upgrade timelocks

## KEY FILES IN OUR CODEBASE
- `v4lend/src/vault/V4Vault.sol` — ERC-4626 lending vault
- `v4lend/src/vault/InterestRateModel.sol` — two-slope model
- `v4lend/src/vault/liquidation/FlashloanLiquidator.sol` — flash loan liquidator
- `limitbreak-amm/lbamm-core/src/` — modular AMM with hooks
- `limitbreak-amm/.../FullMath.sol` — 512-bit math
- `solana-vault-standard/programs/svs-1/` — ERC-4626 on Solana
- `polymarket-mcp-server/` — Python MCP, 45+ tools
- `claw-mcp-toolkit/` — TypeScript MCP, 29 tools
