# Chainstack Security Report — HackenProof Submission

---

## Finding 1: Missing HSTS Header on Main Domain (chainstack.com) Enables SSL Stripping Attacks

**Severity:** Medium

**Target:** `https://chainstack.com`

**Category:** OWASP A05:2021 — Security Misconfiguration

### Description

The main domain `chainstack.com` is missing the `Strict-Transport-Security` (HSTS) response header. This is especially concerning because the authenticated application at `console.chainstack.com` correctly implements HSTS (`max-age=31536000; includeSubDomains`), but the main marketing/login domain does not.

This inconsistency means that an attacker performing a man-in-the-middle (MITM) attack can intercept the initial HTTP request to `chainstack.com` before the 301 redirect to HTTPS, potentially injecting malicious content or redirecting users to a phishing site. Since `chainstack.com` links to `console.chainstack.com` for login/signup, this can be used as an entry point for credential theft.

Additionally, the following critical security headers are missing from `chainstack.com`:

| Header | Status |
|--------|--------|
| `Strict-Transport-Security` | **MISSING** |
| `Content-Security-Policy` | **MISSING** |
| `Permissions-Policy` | **MISSING** |
| `Cross-Origin-Opener-Policy` | **MISSING** |
| `Cross-Origin-Resource-Policy` | **MISSING** |

Headers that ARE present: `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`.

### Steps to Reproduce

1. Run the following command to verify missing HSTS on the main domain:

```bash
curl -sI https://chainstack.com | grep -i "strict-transport-security"
```

Result: **No output** (header is missing).

2. Compare with the console subdomain:

```bash
curl -sI https://console.chainstack.com | grep -i "strict-transport-security"
```

Result: `strict-transport-security: max-age=31536000; includeSubDomains`

3. Verify that HTTP requests are redirected without HSTS protection:

```bash
curl -sI http://chainstack.com | head -5
```

Result: `HTTP/1.1 301 Moved Permanently` with `Location: https://chainstack.com/` but no HSTS header to prevent future downgrades.

4. Confirm missing Content-Security-Policy:

```bash
curl -sI https://chainstack.com | grep -i "content-security-policy"
```

Result: **No output** (header is missing). Note that `docs.chainstack.com` (Vercel/Mintlify) does implement CSP.

### Impact

- **SSL Stripping:** An attacker on a shared network (Wi-Fi, corporate LAN) can intercept the initial HTTP connection to `chainstack.com` and prevent the HTTPS redirect, serving a malicious version of the site.
- **Credential Harvesting:** Since users navigate from `chainstack.com` to `console.chainstack.com` to log in, intercepting the initial navigation allows phishing.
- **Session Hijacking:** Without HSTS, cookies sent over the initial HTTP request (before redirect) can be captured.
- **No CSP Mitigation:** The absence of Content-Security-Policy on the main domain means any XSS vulnerability would have no defense-in-depth protection. Inline scripts, eval, and third-party script injection are all unrestricted.

### Affected Infrastructure

- Primary domain: `chainstack.com` (Cloudflare + SiteGround/WordPress)
- The console (`console.chainstack.com`) and docs (`docs.chainstack.com`) correctly implement HSTS, making this an inconsistency in the security posture.

### Remediation

1. Add HSTS to `chainstack.com` via Cloudflare or the origin server:
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   ```

2. Add Content-Security-Policy to restrict script sources, preventing XSS escalation:
   ```
   Content-Security-Policy: default-src 'self'; script-src 'self' https://js.hs-analytics.net https://js.hsforms.net; ...
   ```

3. Add Permissions-Policy to restrict browser feature access:
   ```
   Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
   ```

4. Submit the domain to the HSTS preload list at https://hstspreload.org/ once the header is confirmed working.

---

## Finding 2: WordPress REST API User Enumeration via _embed Parameter Bypass

**Severity:** Medium

**Target:** `https://chainstack.com/wp-json/wp/v2/posts?_embed`

**Category:** OWASP A01:2021 — Broken Access Control

### Description

While Chainstack has correctly disabled the direct WordPress user enumeration endpoint (`/wp-json/wp/v2/users` returns 404, and `/wp-json/wp/v2/users/{id}` returns "Not Allowed"), the `_embed` parameter on the posts endpoint bypasses this restriction and embeds full author information including user IDs, full names, URL slugs, and avatar image URLs.

This allows an attacker to enumerate all WordPress user accounts that have published content, including the administrator account.

### Verified User Accounts Enumerated

| User ID | Name | Slug | Role Indicator |
|---------|------|------|----------------|
| 1 | Chainstack | **admin** | Administrator (slug = "admin") |
| 33 | Developer Hub Guest | developerhub | Contributor |
| 50 | Nikita Ilin | nikita-ilin | Author |
| 54 | Ana Levidze | ana-levidze | Author |
| 55 | Alexey Obukhov | alexey-obukhov | Author |
| 57 | Alex Usachev | alex-usachev | Author |
| 58 | Anton Sauchyk | anton-sauchyk | Author |

### Steps to Reproduce

1. Confirm that the direct users endpoint is blocked:

```bash
curl -s "https://chainstack.com/wp-json/wp/v2/users"
# Returns: {"code":"rest_no_route","message":"No route was found matching the URL and request method.","data":{"status":404}}

curl -s "https://chainstack.com/wp-json/wp/v2/users/57"
# Returns: Not Allowed
```

2. Bypass the restriction using the `_embed` parameter on posts:

```bash
curl -s "https://chainstack.com/wp-json/wp/v2/posts?_embed&per_page=100" | \
  python3 -c "
import sys,json
data = json.load(sys.stdin)
authors = set()
for p in data:
    for a in p.get('_embedded',{}).get('author',[]):
        authors.add((a.get('id'), a.get('name'), a.get('slug')))
for a in sorted(authors):
    print(f'ID: {a[0]}, Name: {a[1]}, Slug: {a[2]}')
"
```

Result:
```
ID: 1, Name: Chainstack, Slug: admin
ID: 33, Name: Developer Hub Guest, Slug: developerhub
ID: 50, Name: Nikita Ilin, Slug: nikita-ilin
ID: 54, Name: Ana Levidze, Slug: ana-levidze
ID: 55, Name: Alexey Obukhov, Slug: alexey-obukhov
ID: 57, Name: Alex Usachev, Slug: alex-usachev
ID: 58, Name: Anton Sauchyk, Slug: anton-sauchyk
```

3. The slug `admin` for user ID 1 reveals this is the primary administrator account.

### Impact

- **Targeted Brute Force:** Knowing the exact username slugs (especially `admin`) allows targeted credential stuffing and brute-force attacks against `wp-login.php` or the application-passwords authentication endpoint.
- **Social Engineering:** Full names and roles of team members can be used for spear-phishing campaigns targeting Chainstack employees.
- **OSINT Enrichment:** Combined with LinkedIn and other sources, this provides a verified employee list for the engineering/content team.
- **Access Control Bypass:** The restriction on `/wp-json/wp/v2/users` is rendered ineffective by the `_embed` bypass, indicating incomplete access control implementation.

### Remediation

1. Disable the `_embed` functionality for unauthenticated requests, or strip author data from embedded responses:

```php
// In functions.php or a security plugin
add_filter('rest_prepare_post', function($response, $post, $request) {
    if (!is_user_logged_in()) {
        unset($response->data['author']);
        if (isset($response->data['_embedded']['author'])) {
            unset($response->data['_embedded']['author']);
        }
    }
    return $response;
}, 10, 3);
```

2. Alternatively, use a security plugin like Wordfence or iThemes Security to disable REST API access for unauthenticated users.

3. Change the admin account slug from `admin` to a non-obvious value.

---

## Finding 3: Excessive WordPress REST API and Plugin Namespace Exposure

**Severity:** Low

**Target:** `https://chainstack.com/wp-json/`

**Category:** OWASP A05:2021 — Security Misconfiguration

### Description

The WordPress REST API root endpoint publicly exposes 17 API namespaces, revealing the complete list of installed plugins and internal infrastructure components. While individual endpoints require authentication, the namespace listing and route enumeration provide significant reconnaissance value.

### Exposed Namespaces

```
oembed/1.0
wp/v2
abd/v1
leadin/v1              (HubSpot integration)
llms/v1                (LMS plugin)
nab/v1                 (A/B testing - Nelio)
redirection/v1         (Redirection plugin - exposes route schema)
siteground-settings/v1 (SiteGround hosting config)
siteground-optimizer/v1 (SiteGround optimizer - 40+ routes exposed)
yoast/v1               (Yoast SEO)
amp/v1                 (AMP plugin)
weglot/v1              (Translation plugin)
wp-rollback/v1         (Plugin rollback capability)
wp-site-health/v1      (Site health diagnostics)
wp-block-editor/v1     (Gutenberg editor)
wp-abilities/v1        (Capabilities)
chainstack              (Custom namespace)
```

### Additional Information Disclosed

1. **WordPress Version:** The RSS feed at `/feed/` exposes the exact version:
   ```
   <generator>https://wordpress.org/?v=6.9.4</generator>
   ```

2. **PHP Handler Configuration:** The response header `x-httpd-modphp: 1` reveals the PHP execution mode.

3. **SiteGround CDN Identifier:** The header `host-header: 6b7412fb82ca5edfd0917e3957f05d89` exposes an internal SiteGround CDN token.

4. **Platform Disclosure:** `cf-edge-cache: cache,platform=wordpress` confirms the CMS.

5. **SiteGround Optimizer Routes:** The `siteground-optimizer/v1` namespace alone exposes 40+ routes including cache purge, SSL configuration, database optimization, image optimization, and memcached control endpoints. While they require authentication, the route schema reveals the exact infrastructure management capabilities.

### Steps to Reproduce

```bash
# List all namespaces
curl -s "https://chainstack.com/wp-json/" | python3 -c "
import sys,json
data = json.load(sys.stdin)
for ns in data.get('namespaces', []):
    print(ns)
"

# Check WordPress version
curl -s "https://chainstack.com/feed/" | grep -i "generator"

# Check leaking headers
curl -sI https://chainstack.com | grep -iE "x-httpd-modphp|host-header|cf-edge-cache"
```

### Impact

- **Attack Surface Mapping:** Knowing the exact WordPress version (6.9.4), PHP configuration (mod_php), hosting provider (SiteGround), CDN (Cloudflare), and all installed plugins allows targeted exploit development.
- **Plugin Vulnerability Targeting:** Each identified plugin (Redirection, Yoast, HubSpot Leadin, WP Rollback, etc.) can be cross-referenced with known CVE databases for version-specific vulnerabilities.
- **Infrastructure Intelligence:** The SiteGround optimizer route schema reveals cache, SSL, database, and memcached management capabilities that could be targeted if authentication is ever bypassed.

### Remediation

1. Restrict REST API access for unauthenticated users:
```php
add_filter('rest_authentication_errors', function($result) {
    if (!is_user_logged_in()) {
        return new WP_Error('rest_disabled', 'REST API restricted.', ['status' => 401]);
    }
    return $result;
});
```

2. Remove the WordPress version from the RSS feed:
```php
remove_action('wp_head', 'wp_generator');
add_filter('the_generator', '__return_empty_string');
```

3. Remove unnecessary response headers (`x-httpd-modphp`, `host-header`) at the Cloudflare or server level.

4. Disable REST API discovery link in HTML headers if the API is not needed publicly.

---

## Summary

| # | Finding | Severity | CVSS Est. |
|---|---------|----------|-----------|
| 1 | Missing HSTS + CSP on main domain | Medium | 5.3 |
| 2 | User enumeration via _embed bypass | Medium | 5.3 |
| 3 | Excessive REST API/plugin namespace exposure + version disclosure | Low | 3.7 |

**Researcher:** ElromAuditor
**Date:** 2026-03-27
**Program:** Chainstack on HackenProof
