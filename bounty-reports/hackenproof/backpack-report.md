# Backpack Exchange Security Report — HackenProof Submission

---

## Finding 1: Critical Security Header Deficiency on Main Exchange Frontend (backpack.exchange)

**Severity:** High

**Target:** `https://backpack.exchange`

**Category:** OWASP A05:2021 — Security Misconfiguration

### Description

The main Backpack Exchange frontend at `https://backpack.exchange` is missing nearly all recommended security response headers. This is the primary user-facing application where users manage cryptocurrency assets, execute trades, and access their wallets. The security header score is **1/9** (only `X-Frame-Options` is present), which is critically insufficient for a financial application handling real funds.

The API subdomain (`api.backpack.exchange`) correctly implements most security headers including HSTS and X-Content-Type-Options, which makes the frontend deficiency a clear inconsistency in the security posture -- the API is protected but the page that loads it is not.

### Missing Headers (Verified)

| Header | Frontend (backpack.exchange) | API (api.backpack.exchange) | Risk |
|--------|------------------------------|----------------------------|------|
| `Strict-Transport-Security` | **MISSING** | Present (31536000) | **HIGH** — SSL stripping |
| `Content-Security-Policy` | **MISSING** | N/A | **HIGH** — XSS escalation |
| `X-Content-Type-Options` | **MISSING** | Present (nosniff) | **MEDIUM** — MIME sniffing |
| `Referrer-Policy` | **MISSING** | N/A | **MEDIUM** — URL leakage |
| `X-XSS-Protection` | **MISSING** | Present | **LOW** — Legacy XSS filter |
| `Permissions-Policy` | **MISSING** | N/A | **MEDIUM** — Feature abuse |
| `Cross-Origin-Opener-Policy` | **MISSING** | N/A | **MEDIUM** — Spectre-class |
| `Cross-Origin-Resource-Policy` | **MISSING** | N/A | **LOW** — Cross-origin reads |

Headers present: Only `X-Frame-Options: SAMEORIGIN`.

Additionally, the frontend leaks `X-Powered-By: Next.js`, disclosing the framework.

### Steps to Reproduce

1. Verify the absence of HSTS on the main exchange:

```bash
curl -sI https://backpack.exchange | grep -i "strict-transport-security"
```

Result: **No output** (header is missing).

2. Compare with the API:

```bash
curl -sI https://api.backpack.exchange/api/v1/tickers | grep -i "strict-transport-security"
```

Result: `strict-transport-security: max-age=31536000; includeSubDomains`

3. Verify missing CSP:

```bash
curl -sI https://backpack.exchange | grep -i "content-security-policy"
```

Result: **No output**.

4. Verify missing X-Content-Type-Options:

```bash
curl -sI https://backpack.exchange | grep -i "x-content-type-options"
```

Result: **No output**.

5. Verify framework disclosure:

```bash
curl -sI https://backpack.exchange | grep -i "x-powered-by"
```

Result: `x-powered-by: Next.js`

6. View the complete header set (showing the deficiency):

```bash
curl -sI https://backpack.exchange
```

Result:
```
HTTP/2 200
content-type: text/html; charset=utf-8
content-length: 435845
date: Fri, 27 Mar 2026 02:30:38 GMT
vary: Accept-Encoding
x-frame-options: SAMEORIGIN
x-nextjs-cache: HIT
cache-control: s-maxage=60, stale-while-revalidate=31535940
x-powered-by: Next.js
etag: "..."
x-cache: Miss from cloudfront
via: 1.1 ....cloudfront.net (CloudFront)
```

No security headers beyond `x-frame-options`.

### Impact

**This is a cryptocurrency exchange handling real user funds.** The missing headers create the following attack vectors:

1. **SSL Stripping (No HSTS):** An attacker on a shared network can intercept the initial HTTP connection to `backpack.exchange` (before the CloudFront 301 redirect to HTTPS) and serve a malicious version of the exchange. Users would enter credentials and 2FA codes on the attacker's site. The HTTP-to-HTTPS redirect exists but without HSTS, browsers will not enforce HTTPS on subsequent visits.

   ```bash
   # Verify HTTP redirect exists but lacks HSTS enforcement
   curl -sI http://backpack.exchange | head -3
   # HTTP/1.1 301 Moved Permanently
   # Location: https://backpack.exchange/
   ```

2. **XSS Escalation (No CSP):** If any XSS vulnerability is discovered (even a minor reflected XSS), the absence of Content-Security-Policy means there is zero defense-in-depth. An attacker could:
   - Inject arbitrary JavaScript that executes in the exchange context
   - Access session tokens and authentication state
   - Initiate withdrawal transactions on behalf of the user
   - Exfiltrate API keys if the user has created any

3. **MIME Type Confusion (No X-Content-Type-Options):** Without `nosniff`, the browser may interpret uploaded/served content with incorrect MIME types, potentially executing user-controlled content as JavaScript.

4. **Referrer Leakage (No Referrer-Policy):** When users click external links from the exchange, the full URL (which may contain account information, transaction IDs, or internal paths) is sent to the destination in the `Referer` header.

5. **Spectre-Class Attacks (No COOP/CORP):** Without `Cross-Origin-Opener-Policy` and `Cross-Origin-Resource-Policy`, the page is vulnerable to cross-origin attacks that could read sensitive data from the exchange interface via Spectre-class side-channel attacks.

### Severity Justification

This is rated **High** because:
- Backpack is a cryptocurrency exchange with real financial impact
- The main frontend is the attack surface for all user interactions
- Missing HSTS on a financial application is widely considered a Medium-High issue
- Missing CSP on a financial application is widely considered High
- The combination of ALL missing headers compounds the risk significantly
- The API correctly implements these headers, proving the team is aware of them but did not apply them to the frontend

### Remediation

1. **Add HSTS to the CloudFront distribution** serving `backpack.exchange`:
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   ```
   This can be done via CloudFront response headers policies.

2. **Implement Content-Security-Policy.** Start with a report-only policy to identify violations, then enforce:
   ```
   Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https://api.backpack.exchange wss://ws.backpack.exchange; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; frame-ancestors 'self';
   ```

3. **Add remaining security headers** via Next.js config (`next.config.js`) or CloudFront response headers policy:
   ```javascript
   // next.config.js
   async headers() {
     return [{
       source: '/(.*)',
       headers: [
         { key: 'X-Content-Type-Options', value: 'nosniff' },
         { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
         { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=(), payment=()' },
         { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
         { key: 'X-XSS-Protection', value: '0' }, // Modern recommendation: disable, rely on CSP
       ],
     }];
   }
   ```

4. **Remove the `X-Powered-By` header:**
   ```javascript
   // next.config.js
   poweredByHeader: false,
   ```

5. Submit the domain to the HSTS preload list after confirming the header works.

---

## Finding 2: SPF Record Uses Softfail (~all) Instead of Hardfail (-all)

**Severity:** Medium

**Target:** DNS TXT record for `backpack.exchange`

**Category:** OWASP A05:2021 — Security Misconfiguration (Email Security)

### Description

The SPF (Sender Policy Framework) DNS record for `backpack.exchange` uses the `~all` qualifier (softfail) instead of the recommended `-all` (hardfail). This means that email from unauthorized senders is treated as "suspicious" rather than "rejected," allowing spoofed emails to potentially reach recipients' inboxes.

For a cryptocurrency exchange, this significantly increases the risk of phishing attacks where threat actors send emails appearing to come from `@backpack.exchange` addresses.

### Current DNS Configuration

```
SPF:   v=spf1 include:dc-aa8e722993._spfm.backpack.exchange ~all
DMARC: v=DMARC1; p=quarantine; rua=mailto:incident.report@backpack.exchange
```

Issues:
- **SPF `~all`**: Softfail allows spoofed emails through if the receiving server is lenient
- **DMARC `p=quarantine`**: Quarantine (not reject) means spoofed emails go to spam rather than being dropped

### Steps to Reproduce

```bash
# Check SPF record
dig +short TXT backpack.exchange
```

Result:
```
"v=spf1 include:dc-aa8e722993._spfm.backpack.exchange ~all"
```

```bash
# Check DMARC record
dig +short TXT _dmarc.backpack.exchange
```

Result:
```
"v=DMARC1; p=quarantine; rua=mailto:incident.report@backpack.exchange"
```

### Impact

- **Phishing Escalation:** Attackers can send emails spoofing `@backpack.exchange` addresses. With `~all` softfail, many email providers will deliver these to the inbox (with a warning) or to spam, rather than rejecting outright.
- **Account Takeover:** Phishing emails appearing to come from `support@backpack.exchange` or `security@backpack.exchange` could trick users into:
  - Clicking malicious links to fake login pages
  - Providing 2FA codes
  - Downloading malware disguised as "security updates"
- **Brand Impersonation:** The combination of SPF softfail and DMARC quarantine gives attackers a better success rate for impersonation compared to SPF hardfail + DMARC reject.

### Comparison with Industry Best Practice

| Entity | SPF | DMARC |
|--------|-----|-------|
| Backpack | `~all` (softfail) | `p=quarantine` |
| Coinbase | `-all` (hardfail) | `p=reject` |
| Binance | `-all` (hardfail) | `p=reject` |
| Chainstack | `-all` (hardfail) | `p=reject` |

### Remediation

1. **Upgrade SPF to hardfail:**
   ```
   v=spf1 include:dc-aa8e722993._spfm.backpack.exchange -all
   ```

2. **Upgrade DMARC to reject:**
   ```
   v=DMARC1; p=reject; rua=mailto:incident.report@backpack.exchange; ruf=mailto:incident.report@backpack.exchange; adkim=s; aspf=s
   ```

3. Ensure DKIM is properly configured for all authorized sending sources before upgrading to `-all` and `p=reject`.

4. Monitor DMARC aggregate reports (rua) for at least 2 weeks after the change to verify no legitimate emails are being rejected.

---

## Finding 3: Technology Disclosure via Response Headers

**Severity:** Low

**Target:** `https://backpack.exchange`

**Category:** OWASP A05:2021 — Security Misconfiguration

### Description

The Backpack Exchange frontend exposes several headers that reveal the underlying technology stack, enabling targeted reconnaissance:

| Header | Value | Information Revealed |
|--------|-------|---------------------|
| `X-Powered-By` | `Next.js` | Application framework |
| `X-Nextjs-Cache` | `HIT` | Internal caching state |
| `Via` | `1.1 ....cloudfront.net (CloudFront)` | CDN provider (AWS CloudFront) |
| `X-Amz-Cf-Pop` | `GRU3-P5` | CloudFront edge location (Sao Paulo) |
| `X-Amz-Cf-Id` | `...` | CloudFront request tracing ID |
| `X-Cache` | `Miss from cloudfront` | Cache state |

### Steps to Reproduce

```bash
curl -sI https://backpack.exchange | grep -iE "x-powered-by|x-nextjs|x-amz|x-cache|via"
```

Result:
```
x-powered-by: Next.js
x-nextjs-cache: HIT
x-cache: Miss from cloudfront
via: 1.1 ....cloudfront.net (CloudFront)
x-amz-cf-pop: GRU3-P5
x-amz-cf-id: ...
```

### Impact

- Knowing the exact framework (Next.js) and CDN (CloudFront) allows targeted attacks against known vulnerabilities in those specific technologies.
- The edge location identifier reveals geographic routing information.
- CloudFront request IDs can be used for cache poisoning research.

### Remediation

1. Remove `X-Powered-By` in Next.js config:
   ```javascript
   // next.config.js
   module.exports = { poweredByHeader: false }
   ```

2. Configure CloudFront to strip `X-Amz-*` headers from responses using a CloudFront response headers policy.

3. The `Via` header is required by HTTP specification for proxies, but `X-Cache` can be suppressed.

---

## Summary

| # | Finding | Severity | CVSS Est. |
|---|---------|----------|-----------|
| 1 | Missing HSTS + CSP + 6 other security headers on exchange frontend | High | 7.1 |
| 2 | SPF softfail enables email spoofing | Medium | 5.3 |
| 3 | Technology stack disclosure via response headers | Low | 3.1 |

### Key Risk Factor

Backpack Exchange is a **cryptocurrency exchange** handling real user funds. The absence of Strict-Transport-Security and Content-Security-Policy on the main frontend is significantly more impactful than it would be for a marketing website. Users interacting with this application are managing wallets, executing trades, and accessing financial data -- all without the foundational browser-enforced security headers that modern financial applications require.

The API subdomain (`api.backpack.exchange`) correctly implements HSTS, X-Content-Type-Options, X-XSS-Protection, and X-Frame-Options, demonstrating that the security team is aware of these headers but has not applied them to the frontend where users interact.

**Researcher:** ElromAuditor
**Date:** 2026-03-27
**Program:** Backpack on HackenProof
