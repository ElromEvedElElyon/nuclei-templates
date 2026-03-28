# CRITICAL: MockAttestation Bypasses ALL TEE Verification in Production

## Vulnerability Report — NEAR Intents: Bridges (MPC Chain Signatures)

**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-26
**Program**: NEAR Intents: Bridges on HackenProof
**Severity**: CRITICAL
**Target**: https://github.com/near/mpc

---

## Summary

The `Attestation` enum in the MPC chain signatures codebase includes a `Mock(MockAttestation)` variant that is compiled into **production WASM** without any `#[cfg(test)]` or feature-flag gating. The `MockAttestation::Valid` variant unconditionally returns `Ok(())` during attestation verification, allowing any participant to **bypass ALL TEE (Trusted Execution Environment) verification** — including DCAP quote verification, TLS key binding, Docker image hash verification, and all OS measurements verification.

This effectively **destroys the entire TEE security model** of the MPC network. A malicious participant can submit `Attestation::Mock(MockAttestation::Valid)` via `submit_participant_info` and run an MPC node completely outside a TEE, with the ability to extract key shares. If a threshold number of participants collude using this bypass, they can reconstruct the master key and **steal ALL funds** secured by the MPC network.

---

## Affected Files

1. **`crates/mpc-attestation/src/attestation.rs` (lines 26-29, 47-60, 200-211, 274-281)**
2. **`crates/near-mpc-contract-interface/src/types/attestation.rs` (lines 29-32, 164-178)**

---

## Vulnerability Details

### 1. Mock variant compiled into production (no feature gate)

In `crates/mpc-attestation/src/attestation.rs`:

```rust
// Lines 25-29 — NO #[cfg(test)] or #[cfg(feature = "test")] attribute
#[derive(Clone, Debug, Serialize, Deserialize, BorshSerialize, BorshDeserialize)]
pub enum Attestation {
    Dstack(DstackAttestation),
    Mock(MockAttestation),  // <-- COMPILED INTO PRODUCTION WASM
}
```

The `MockAttestation` enum (lines 42-60):

```rust
#[derive(Debug, Default, Clone, Serialize, Deserialize, BorshDeserialize, BorshSerialize)]
pub enum MockAttestation {
    #[default]
    /// Always pass validation
    Valid,            // <-- UNCONDITIONALLY PASSES ALL CHECKS
    /// Always fails validation
    Invalid,
    /// Pass validation depending on the set constraints
    WithConstraints { ... },
}
```

### 2. MockAttestation::Valid bypasses ALL verification

In `crates/mpc-attestation/src/attestation.rs` lines 274-281:

```rust
pub(crate) fn verify_mock_attestation(
    mock_attestation: &MockAttestation,
    allowed_mpc_docker_image_hashes: &[NodeImageHash],
    allowed_launcher_docker_compose_hashes: &[LauncherDockerComposeHash],
    timestamp_seconds: u64,
) -> Result<(), VerificationError> {
    match mock_attestation {
        MockAttestation::Valid => Ok(()),  // <-- BYPASSES EVERYTHING
        MockAttestation::Invalid => Err(VerificationError::InvalidMockAttestation),
        ...
    }
}
```

### 3. Both initial verification AND re-verification are bypassed

Initial verification (`Attestation::verify`, lines 200-211):
```rust
Self::Mock(mock_attestation) => {
    // Override attestation verification for this case
    let () = verify_mock_attestation(...)?;
    Ok(VerifiedAttestation::Mock(mock_attestation.clone()))
}
```

Re-verification (`VerifiedAttestation::re_verify`, lines 112-117):
```rust
Self::Mock(mock_attestation) => verify_mock_attestation(...),
```

### 4. The contract interface also includes Mock in production

In `crates/near-mpc-contract-interface/src/types/attestation.rs` lines 29-32:
```rust
pub enum Attestation {
    Dstack(DstackAttestation),
    Mock(MockAttestation),  // <-- Also in the contract interface, no feature gate
}
```

This means the NEAR smart contract ABI accepts Mock attestations as valid input.

### 5. Submit path accepts Mock attestation

The `SubmitParticipantInfoArgs` struct (line 349-353) accepts any `Attestation` variant:
```rust
pub struct SubmitParticipantInfoArgs {
    pub proposed_participant_attestation: Attestation,  // <-- Can be Mock(Valid)
    pub tls_public_key: Ed25519PublicKey,
}
```

### 6. Additional: Dev measurements in production (compounding issue)

Lines 123-130:
```rust
static MEASUREMENTS: [ExpectedMeasurements; 2] = [
    include_measurements!("assets/tcb_info.json"),
    // TODO(#1433): Security - remove dev measurements from production builds
    include_measurements!("assets/tcb_info_dev.json"),  // <-- DEV ENV ACCEPTED
];
```

---

## Attack Scenario

1. Attacker runs a standard (non-TEE) node
2. Calls `submit_participant_info` with:
   ```json
   {
     "proposed_participant_attestation": { "Mock": "Valid" },
     "tls_public_key": "<attacker_key>"
   }
   ```
3. Attestation verification succeeds (returns `Ok(())`)
4. Attacker is registered as a valid MPC participant without any TEE
5. Attacker extracts their key share (no TEE protection)
6. If threshold number of participants collude via same attack, master key is reconstructed
7. **All funds secured by chain signatures are stolen**

---

## What is Bypassed

| Security Check | Normal (Dstack) | Mock(Valid) |
|---|---|---|
| DCAP Quote Verification | YES | SKIPPED |
| TLS Key Binding (report_data) | YES | SKIPPED |
| Docker Image Hash | YES | SKIPPED |
| Launcher Compose Hash | YES | SKIPPED |
| OS Measurements (mrtd, rtmr0-2) | YES | SKIPPED |
| Expiration Check | YES | SKIPPED |
| Re-verification | YES | SKIPPED |

---

## Impact

- **Severity**: CRITICAL
- **Type**: Authentication/Authorization Bypass
- **Affected Asset**: Entire MPC chain signatures network
- **Funds at Risk**: ALL funds secured by NEAR chain signatures (cross-chain bridges, all chains connected via MPC)
- **Attack Complexity**: LOW — requires only a single contract call with a crafted Borsh-encoded payload
- **Prerequisites**: Must be (or become) an MPC participant candidate

---

## Recommended Fix

Gate the `Mock` variant behind a test-only feature flag:

```rust
pub enum Attestation {
    Dstack(DstackAttestation),
    #[cfg(any(test, feature = "test-utils"))]
    Mock(MockAttestation),
}
```

Apply the same gating to:
- `VerifiedAttestation::Mock` variant
- `MockAttestation` enum definition
- `verify_mock_attestation` function
- The contract interface `Attestation` enum

Additionally, remove dev measurements from production builds (TODO #1433).

---

## References

- Repository: https://github.com/near/mpc
- Primary file: `crates/mpc-attestation/src/attestation.rs`
- Contract interface: `crates/near-mpc-contract-interface/src/types/attestation.rs`
- Related TODO: #1433 (dev measurements in production)
