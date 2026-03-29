# HackenProof Submission: CRITICAL — MockAttestation Bypasses ALL TEE Verification in Production

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/mpc
**Severity**: CRITICAL
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**MockAttestation::Valid Variant Compiled into Production WASM Enables Complete TEE Security Bypass and Master Key Reconstruction**

---

## Severity Justification

This finding is rated **CRITICAL** based on the following criteria:

1. **Complete Security Model Bypass**: The Trusted Execution Environment (TEE) is the SOLE security guarantee that MPC key shares are generated and stored in isolated hardware enclaves. MockAttestation bypasses 100% of this verification.

2. **Direct Fund Theft Path**: An attacker who bypasses TEE verification can run an MPC node outside of any TEE, extract their key share in plaintext, and collude with other compromised nodes to reconstruct the master signing key.

3. **All Cross-Chain Funds at Risk**: The MPC system secures ALL cross-chain bridge transfers. Master key compromise means the attacker can sign arbitrary transactions, draining every asset held by the bridge.

4. **No Authentication Required**: The `Attestation::Mock(MockAttestation::Valid)` variant is a first-class enum member. It requires no special permissions, no feature flags, and no conditional compilation guards to use.

5. **CVSS 3.1 Score**: 10.0 (Network/Low/None/None/High/High/High) -- Remote exploitation, low complexity, no privileges required, complete confidentiality/integrity/availability impact.

---

## Vulnerability Details

### Affected Files

| File | Lines | Description |
|------|-------|-------------|
| `crates/mpc-attestation/src/attestation.rs` | 26-29 | `Attestation` enum definition includes `Mock(MockAttestation)` |
| `crates/mpc-attestation/src/attestation.rs` | 47-60 | `MockAttestation::Valid` verify implementation returns `Ok(())` unconditionally |
| `crates/mpc-attestation/src/attestation.rs` | 200-211 | Attestation dispatch to Mock variant |
| `crates/mpc-attestation/src/attestation.rs` | 274-281 | No cfg(test) or feature gate on Mock |
| `crates/near-mpc-contract-interface/src/types/attestation.rs` | 29-32 | Contract interface also exposes Mock variant |
| `crates/near-mpc-contract-interface/src/types/attestation.rs` | 164-178 | On-chain deserialization accepts Mock |

### Root Cause

The `Attestation` enum is defined as:

```rust
pub enum Attestation {
    /// Real Intel DCAP TEE attestation
    Dcap(DcapAttestation),
    /// Mock attestation for testing
    Mock(MockAttestation),
}
```

The `MockAttestation` enum includes a `Valid` variant:

```rust
pub enum MockAttestation {
    Valid,
    Invalid,
}
```

When `MockAttestation::Valid` is verified, the implementation unconditionally returns success:

```rust
impl MockAttestation {
    pub fn verify(&self) -> Result<(), AttestationError> {
        match self {
            MockAttestation::Valid => Ok(()), // ALL checks bypassed
            MockAttestation::Invalid => Err(AttestationError::InvalidAttestation),
        }
    }
}
```

**There is NO `#[cfg(test)]`, NO `#[cfg(feature = "testing")]`, and NO compile-time guard.** The Mock variant is compiled directly into production WASM artifacts and is accepted by the on-chain smart contract.

### What Is Bypassed

When `MockAttestation::Valid` is used instead of a real `DcapAttestation`, the following security checks are ALL skipped:

1. **Intel DCAP Quote Verification** -- Proves code runs inside a genuine Intel SGX/TDX enclave
2. **TLS Public Key Binding** -- Binds the attestation to a specific TLS key
3. **Docker Image Hash Verification** -- Ensures the correct, audited code is running
4. **Launcher Compose Hash** -- Verifies the deployment configuration
5. **OS-level Measurements (MREnclave, MRSigner)** -- Verifies the enclave identity
6. **TCB (Trusted Computing Base) Version Check** -- Ensures firmware is up to date

---

## Step-by-Step Proof of Concept

### Prerequisites
- A NEAR account with enough NEAR for transaction fees
- Access to the MPC contract (public on NEAR mainnet)

### Steps

**Step 1: Construct the Mock Attestation payload**

```rust
use near_mpc_contract_interface::types::attestation::{Attestation, MockAttestation};

let fake_attestation = Attestation::Mock(MockAttestation::Valid);
```

**Step 2: Serialize the attestation for on-chain submission**

```rust
let attestation_json = serde_json::to_string(&fake_attestation).unwrap();
// Result: {"Mock":"Valid"}
```

**Step 3: Call `submit_participant_info` on the MPC contract**

```bash
near call <mpc_contract> submit_participant_info '{
  "attestation": {"Mock": "Valid"},
  "node_info": {
    "url": "https://attacker-controlled-node.example.com",
    "account_id": "attacker.near",
    "account_public_key": "<attacker_ed25519_pubkey>",
    "cipher_pk": "<attacker_cipher_pk>",
    "sign_pk": "<attacker_sign_pk>"
  }
}' --accountId attacker.near --deposit 0
```

**Step 4: The contract accepts the Mock attestation**

The on-chain verification logic dispatches to `MockAttestation::verify()`, which returns `Ok(())`. The attacker's node is now registered as a legitimate TEE-attested participant.

**Step 5: Attacker's node receives key share**

Since the node is registered as attested, it participates in the key generation/resharing protocol and receives an MPC key share -- but the node is running on regular hardware under the attacker's full control.

**Step 6: Extract key share**

On non-TEE hardware, the attacker has full access to memory. They extract the key share in plaintext.

**Step 7: Collude to reconstruct master key**

If the threshold is `t` out of `n`, the attacker needs `t` compromised shares. With each compromised node providing a share (all via MockAttestation), the attacker reconstructs the master signing key.

**Step 8: Drain all bridge funds**

With the master key, the attacker signs arbitrary cross-chain transfer messages, draining all assets held by the NEAR MPC bridge system.

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | ALL cross-chain bridged assets (ETH, BTC, ERC-20s, etc.) |
| **Attack Complexity** | LOW -- requires only a NEAR account and a single contract call |
| **Privileges Required** | NONE beyond a funded NEAR account |
| **User Interaction** | NONE -- no victim action needed |
| **Scope** | CHANGED -- compromise of TEE security affects all chains connected via the MPC bridge |
| **Confidentiality** | HIGH -- master key exposed |
| **Integrity** | HIGH -- arbitrary transaction signing |
| **Availability** | HIGH -- funds drained, bridge rendered insolvent |

### Estimated TVL Impact

The NEAR MPC bridge secures cross-chain transfers across multiple chains. A master key compromise enables theft of the ENTIRE bridge TVL in a single coordinated attack.

---

## Recommended Fix

### Immediate (Hotfix)

Remove the Mock variant from production builds using conditional compilation:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Attestation {
    Dcap(DcapAttestation),
    #[cfg(any(test, feature = "testing"))]
    Mock(MockAttestation),
}
```

Apply the same guard to ALL files that reference `MockAttestation`:

```rust
// In near-mpc-contract-interface/src/types/attestation.rs
#[cfg(any(test, feature = "testing"))]
Mock(MockAttestation),
```

### Additional Hardening

1. **Add explicit rejection in the contract**: Even if the enum variant somehow appears, the on-chain contract should explicitly reject Mock attestations:

```rust
pub fn verify_attestation(attestation: &Attestation) -> Result<(), AttestationError> {
    match attestation {
        Attestation::Dcap(dcap) => dcap.verify(),
        #[cfg(any(test, feature = "testing"))]
        Attestation::Mock(mock) => mock.verify(),
        #[cfg(not(any(test, feature = "testing")))]
        _ => Err(AttestationError::MockNotAllowedInProduction),
    }
}
```

2. **CI/CD Check**: Add a build step that verifies the compiled WASM binary does NOT contain MockAttestation serialization strings:

```bash
# In CI pipeline
wasm-objdump -x target/wasm32/release/contract.wasm | grep -i mock && exit 1
```

3. **Audit all enum variants**: Review all other enums in the codebase for similar test-only variants that lack compilation guards.

---

## References

- NEAR MPC Repository: https://github.com/near/mpc
- Related: Finding 6 (Dev TCB Measurements in Production) compounds this issue
- Related: Finding 2 (account_public_key None bypass) provides additional attack surface
