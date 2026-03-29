# HackenProof Submission: MEDIUM — Dev TCB Measurements Accepted in Production

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/mpc
**Severity**: MEDIUM
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**Development TEE Measurements (tcb_info_dev.json) Accepted as Valid in Production, Weakening Enclave Verification**

---

## Severity Justification

- **MEDIUM**: Weakens the TEE security model by accepting development environment attestations in production
- Tracked internally as TODO(#1433) but remains in production code
- Compounds with Finding 1 (MockAttestation) to further degrade TEE trust guarantees
- A node running a development build (with potentially relaxed security) passes production attestation

---

## Vulnerability Details

### Affected File

`crates/mpc-attestation/src/attestation.rs` (lines 123-129)

### Root Cause

The production measurements array includes BOTH production and development TCB configurations:

```rust
static MEASUREMENTS: [ExpectedMeasurements; 2] = [
    include_measurements!("assets/tcb_info.json"),       // Production
    // TODO(#1433): Security - remove dev measurements
    include_measurements!("assets/tcb_info_dev.json"),   // Development -- SHOULD NOT BE HERE
];
```

When verifying a DCAP attestation, the system checks the attested measurements against ALL entries in the `MEASUREMENTS` array. If the attestation matches EITHER the production OR the development measurements, it passes verification.

### What This Means

1. A node running the **development build** of the MPC software produces TEE attestations with development measurements
2. These development measurements are accepted as valid by the production verification logic
3. Development builds may have:
   - Debug logging enabled (leaking sensitive data)
   - Relaxed security checks
   - Additional attack surface from dev tooling
   - Different (potentially weaker) enclave configurations

---

## Proof of Concept

**Step 1**: Build the MPC node software in development mode:

```bash
cargo build --features dev  # or equivalent dev configuration
```

**Step 2**: Run the dev-build node inside a TEE (or any environment that produces attestations matching `tcb_info_dev.json`).

**Step 3**: The node generates a DCAP attestation with measurements from the dev build.

**Step 4**: Submit the attestation to the MPC contract:

```bash
near call <mpc_contract> submit_participant_info '{
  "attestation": {"Dcap": "<dev_build_attestation>"},
  ...
}'
```

**Step 5**: The verification checks attestation measurements against `MEASUREMENTS[0]` (prod) -- no match. Then checks against `MEASUREMENTS[1]` (dev) -- MATCH. Attestation accepted.

**Step 6**: The dev-build node is now a registered MPC participant with potentially weaker security guarantees.

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | TEE security guarantees for the MPC network |
| **Attack Complexity** | MEDIUM -- requires deploying a dev build in a TEE-like environment |
| **Scope** | Degrades trust in the entire MPC participant set |
| **Compound Risk** | Combined with Finding 1 (MockAttestation), this creates a layered TEE bypass |

---

## Recommended Fix

1. **Remove dev measurements from production** (as the TODO already indicates):

```rust
static MEASUREMENTS: [ExpectedMeasurements; 1] = [
    include_measurements!("assets/tcb_info.json"),
    // Dev measurements removed -- only allowed in test builds
];

#[cfg(any(test, feature = "dev"))]
static DEV_MEASUREMENTS: [ExpectedMeasurements; 1] = [
    include_measurements!("assets/tcb_info_dev.json"),
];
```

2. **Feature-gate dev measurements**:

```rust
fn get_expected_measurements() -> &'static [ExpectedMeasurements] {
    #[cfg(any(test, feature = "dev"))]
    {
        static ALL: [ExpectedMeasurements; 2] = [
            include_measurements!("assets/tcb_info.json"),
            include_measurements!("assets/tcb_info_dev.json"),
        ];
        &ALL
    }
    #[cfg(not(any(test, feature = "dev")))]
    {
        static PROD: [ExpectedMeasurements; 1] = [
            include_measurements!("assets/tcb_info.json"),
        ];
        &PROD
    }
}
```

3. **Close TODO(#1433)**: This should be treated as a security issue, not a cleanup task.

---

## References

- NEAR MPC Repository: https://github.com/near/mpc
- Internal tracking: TODO(#1433)
- Related: Finding 1 (MockAttestation in production) -- same pattern of test code in production
