# HackenProof Submission: HIGH — account_public_key None Bypass in TEE Attestation Check

**Program**: NEAR Intents: Bridges + Smart Contracts
**Target Repository**: https://github.com/near/mpc
**Severity**: HIGH
**Reporter**: Elrom (standardbitcoin.io@gmail.com)
**Date**: 2026-03-29

---

## Title

**account_public_key None Value Allows Attestation Key Check Bypass Enabling MPC Participant Impersonation**

---

## Severity Justification

- **HIGH**: Enables MPC participant impersonation if a NEAR account is compromised
- A compromised initial participant account (via social engineering, phishing, or access key addition) allows signing with ANY key
- The verification check is completely skipped when `account_public_key` is `None`
- Tracked internally as TODO(#823) but remains UNPATCHED in production

---

## Vulnerability Details

### Affected File

`contract/src/tee/tee_state.rs` (lines 474-478)

### Root Cause

The function `is_caller_an_attested_participant()` contains a conditional key check that is trivially bypassed:

```rust
if let Some(node_pk) = &attestation.node_id.account_public_key {
    if node_pk != &signer_pk {
        return Err(AttestationKeyMismatch);
    }
}
// When account_public_key is None:
// CHECK IS SKIPPED ENTIRELY
// Function continues and returns Ok(())
```

Initial participants created via `with_mocked_participant_attestations` have `account_public_key: None`. This means:

1. The attestation exists and is considered valid
2. But NO key binding exists between the attestation and the signing account
3. ANY key that can sign for that NEAR account passes verification

### Attack Scenario

1. Attacker identifies an initial MPC participant whose `account_public_key` is `None`
2. Attacker compromises the participant's NEAR account (social engineering, phishing, or exploiting weak key management)
3. Attacker adds a new access key to the compromised NEAR account
4. Attacker signs `submit_participant_info` or other attested calls using the new key
5. The `if let Some(node_pk)` check sees `None` and skips verification
6. Attacker impersonates the legitimate MPC participant

---

## Proof of Concept

**Step 1**: Identify initial participants with `account_public_key: None` by querying the contract state:

```bash
near view <mpc_contract> get_participants '{}'
```

**Step 2**: After compromising the target NEAR account, add a new full-access key:

```bash
near add-key <target_account> <attacker_pubkey> --masterAccount <target_account>
```

**Step 3**: Call attested functions using the compromised account with the attacker's key:

```bash
near call <mpc_contract> submit_participant_info '{
  "attestation": <valid_attestation>,
  "node_info": { ... }
}' --accountId <target_account> --publicKey <attacker_pubkey>
```

**Step 4**: The key mismatch check is skipped because `account_public_key` is `None`, and the call succeeds.

---

## Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| **Assets at Risk** | MPC key shares held by the impersonated participant |
| **Attack Complexity** | MEDIUM -- requires compromising a NEAR account |
| **Privileges Required** | Access to the compromised NEAR account |
| **Scope** | MPC participant impersonation, potential key share extraction |

---

## Recommended Fix

1. **Require `account_public_key` for all participants**: Reject attestations with `None` as the public key:

```rust
let node_pk = attestation.node_id.account_public_key
    .as_ref()
    .ok_or(AttestationError::MissingPublicKey)?;

if node_pk != &signer_pk {
    return Err(AttestationError::AttestationKeyMismatch);
}
```

2. **Migration**: Update all existing participants with `None` keys to bind their current signing keys.

3. **Close TODO(#823)**: This tracked issue should be prioritized as a security fix.

---

## References

- NEAR MPC Repository: https://github.com/near/mpc
- Internal tracking: TODO(#823)
- Compounds with Finding 1 (MockAttestation) for full TEE bypass chain
