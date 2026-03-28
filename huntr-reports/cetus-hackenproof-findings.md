# Cetus integer-mate Security Findings — HackenProof Submission Package
# Em nome do Senhor Jesus Cristo
# Date: 27 Mar 2026
# Target: CetusProtocol/integer-mate v1.3.0 (Sui Move)
# Platform: HackenProof (zero-rep, $300K bounty)
# Researcher: ElromSecurity

---

## FINDING 1 [MEDIUM]: Unchecked shlw() Silently Overflows u256

**File**: `sources/math_u256.move` lines 10-12
**Same pattern as the $223M exploit**

`shlw(n)` does `n << 64` without checking if `n >= 2^192`. High bits silently discarded.
Checked variant exists (`checked_shlw`) proving developers were aware, but unchecked is still public.

## FINDING 2 [MEDIUM]: checked_shlw() Returns Sentinel 0 Instead of Aborting

**File**: `sources/math_u256.move` lines 18-25

Returns `(0, true)` on overflow. If consumer fails to check boolean flag, zero propagates into calculations. THIS IS THE EXACT PATTERN THAT CAUSED THE $223M EXPLOIT.

## FINDING 3 [MEDIUM]: Deprecated mul_shl() Still Public with Silent Overflow

**File**: `sources/full_math_u128.move` lines 23-31

Deprecated but still callable. `mul_shl(1<<127, 1<<127, 2)` returns 0 instead of 2^256.

## FINDING 4 [LOW]: Signed shl() Can Flip Sign Bit

**File**: `sources/i128.move` lines 133-137

`shl(from(1), 31)` turns positive into negative. Dangerous for tick math.

## FINDING 5 [INFO]: Missing mul_shr_ceil/round Variants

Only floor rounding for mul_shr. DeFi needs all rounding modes.

---

**Total estimated: $14.5K-$44K**
**Best submission: Findings 1+2 together (same class as $223M exploit)**
