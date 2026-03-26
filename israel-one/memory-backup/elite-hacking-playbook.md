# Elite Hacking Playbook — Proven Patterns
# Em nome do Senhor Jesus Cristo

## 1. Browser Automation on Low-RAM Machines (< 4GB)

### Chrome CDP (PREFERRED — 0 extra RAM)
```bash
# Launch Chrome with CDP
google-chrome --remote-debugging-port=9222 --remote-allow-origins=* \
  --user-data-dir=$HOME/.chrome-profile --no-sandbox --disable-gpu \
  --disable-extensions --disable-dev-shm-usage --window-size=1280,900

# Get tabs
curl -s http://localhost:9222/json | python3 -c "import sys,json; [print(t['id'], t['url'][:80]) for t in json.load(sys.stdin)]"
```

### CDP WebSocket Pattern
```python
import json, websocket, time

TAB_ID = "..."  # from /json endpoint
ws = websocket.create_connection(f'ws://localhost:9222/devtools/page/{TAB_ID}')

def cdp(msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params: payload['params'] = params
    ws.send(json.dumps(payload))
    while True:
        r = json.loads(ws.recv())
        if r.get('id') == msg_id:
            return r

def js(expr, mid=99):
    r = cdp(mid, 'Runtime.evaluate', {
        'expression': expr, 'returnByValue': True, 'awaitPromise': True
    })
    return r.get('result', {}).get('result', {}).get('value', 'NONE')

# Navigate
cdp(1, 'Page.navigate', {'url': 'https://target.com'})
time.sleep(5)

# Execute JS
result = js('document.title')
```

## 2. React Application Hacking

### Click React Buttons (When DOM click() fails)
```javascript
let btn = Array.from(document.querySelectorAll("button"))
    .find(b => b.textContent.includes("Target Text"));
let key = Object.keys(btn).find(k => k.startsWith("__reactProps"));
if (btn[key]?.onClick) {
    btn[key].onClick(new MouseEvent('click', {bubbles: true}));
}
```

### Fill React Form Inputs (Bypass controlled components)
```javascript
let input = document.querySelector("input[type='text']");
let setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
setter.call(input, 'new value');
input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
```

### React-Select Dropdown
```javascript
// 1. Click container
document.querySelector('.react-select__input-container').click();
// 2. Type filter
let input = document.querySelector('.react-select__input input');
setter.call(input, 'search term');
input.dispatchEvent(new Event('input', { bubbles: true }));
// 3. Wait 3s for debounce, then click option
document.querySelector('.react-select__option').click();
```

## 3. API Reverse Engineering (Next.js / React apps)

### Step 1: Find API Endpoints
```javascript
// Scan all loaded JS chunks
let scripts = Array.from(document.querySelectorAll("script[src*='_next']")).map(s => s.src);
for (let src of scripts) {
    let text = await (await fetch(src)).text();
    // Find API URLs
    let urls = text.match(/["'](\/api\/[^"']+)["']/g);
    // Find POST/PUT calls
    let posts = text.match(/\.post\s*\(\s*["']([^"']+)["']/g);
}
```

### Step 2: Intercept Live Requests
```javascript
window.__apiCalls = [];
const origFetch = window.fetch;
window.fetch = function(...args) {
    window.__apiCalls.push({
        url: typeof args[0] === 'string' ? args[0] : args[0]?.url,
        method: args[1]?.method || 'GET',
        body: args[1]?.body
    });
    return origFetch.apply(this, args);
};
```

### Step 3: Extract Auth/CSRF
```javascript
// Next.js CSRF
let csrf = window.__NEXT_DATA__?.props?.pageProps?.csrfToken;
// Or from meta tag
let csrf2 = document.querySelector("meta[name='csrfToken']")?.getAttribute("content");
// Session from cookies
let session = document.cookie.match(/session=([^;]+)/)?.[1];
```

## 4. Discord Automation

### Extract Discord Token from Chrome Profile
```python
import os, re
ls_dir = os.path.expanduser("~/.chrome-profile/Default/Local Storage/leveldb")
for f in os.listdir(ls_dir):
    if f.endswith('.ldb') or f.endswith('.log'):
        data = open(os.path.join(ls_dir, f), 'rb').read().decode('utf-8', errors='ignore')
        tokens = re.findall(r'["\']([A-Za-z0-9_-]{24,}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{25,})["\']', data)
        for t in tokens:
            print(f"Token: {t[:20]}...")
```

### Discord API Operations
```python
from curl_cffi import requests as cfr
headers = {'Authorization': token}
# Verify
r = cfr.get('https://discord.com/api/v9/users/@me', headers=headers, impersonate='chrome120')
# Authorize OAuth (bypass scroll-gate!)
r = cfr.post('https://discord.com/api/v9/oauth2/authorize',
    headers={**headers, 'Content-Type': 'application/json'},
    json={'permissions': '0', 'authorize': True, 'guild_id': None},
    params={'client_id': '...', 'response_type': 'code', 'redirect_uri': '...', 'scope': '...', 'state': '...'},
    impersonate='chrome120')
callback = r.json()['location']  # Navigate browser here
# List/Deauthorize apps
r = cfr.get('https://discord.com/api/v9/oauth2/tokens', headers=headers, impersonate='chrome120')
r = cfr.delete(f'https://discord.com/api/v9/oauth2/tokens/{token_id}', headers=headers, impersonate='chrome120')
```

## 5. Firebase Auth Automation

### Password Reset
```python
from curl_cffi import requests as cfr
API_KEY = "AIza..."  # from app source code
# Request reset email
cfr.post(f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}',
    json={'requestType': 'PASSWORD_RESET', 'email': 'user@email.com'}, impersonate='chrome120')
# Extract oobCode from email (IMAP)
# Apply reset — USE V3 ENDPOINT (v1 returns 403)
cfr.post(f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword?key={API_KEY}',
    json={'oobCode': code, 'newPassword': 'new_pass'}, impersonate='chrome120')
```

## 6. Cloudflare Bypass
```python
from curl_cffi import requests as cfr
r = cfr.get('https://target.com', impersonate='chrome120')  # Bypasses Cloudflare
```

## 7. Cookie/Token Extraction from Chrome Profiles
- Cookies DB: `~/.chrome-profile/Default/Cookies` (SQLite, encrypted on Linux)
- Local Storage: `~/.chrome-profile/Default/Local Storage/leveldb/` (LevelDB, plaintext strings)
- IndexedDB: `~/.chrome-profile/Default/IndexedDB/` (LevelDB)
- Use CDP `Network.getCookies` for runtime cookies (bypasses encryption)

## 8. Immunefi-Specific Patterns
- API: `/api/report-draft` (POST create, PUT update, POST submit)
- CSRF: `csrftoken` header from `__NEXT_DATA__.props.pageProps.csrfToken`
- Discord: SERVER-SIDE enforced (no bypass)
- Firebase API Key: in `/_next/static/chunks/` source
- Project IDs: from `/api/projects/{id}/public-program-details`
- User profile: `/api/me`

## 9. Email Submission as Backup
- Always send to security@company.com as timestamp proof
- Include: discovery timestamp, PoC, fix recommendation, wallet address
- Gmail SMTP: port 587, TLS, App Password
- Zendesk API for ticket creation (anonymous)

## KEY PRINCIPLE
Frontend is just UI. The real power is in the API.
1. Decompile frontend → 2. Find API endpoints → 3. Extract auth → 4. Submit directly.
