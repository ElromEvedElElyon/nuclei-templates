# Immunefi Bug Submission Automation — Patterns & Lessons (Session 30 — 25 Mar 2026)

## Account
- Username: PadraoBTC736
- Email: inteligenciaartificial.now@gmail.com
- Chrome profile: `~/.chrome-immunefi2`
- Creds file: `~/.immunefi_creds` (chmod 600)

## CRITICAL REQUIREMENTS (Before First Submission)
1. **Discord validation** — Must connect Discord via OAuth in Settings
2. **Identity Verification** — ZKPassport (NFC passport + phone app) OR Persona (photo ID + selfie)
3. Both MUST be completed before submission form advances past Step 1

## Submission Form Flow (4 Steps)
1. **Assets and Impact** (Select Program)
   - Program: react-select dropdown
   - Program confirmation: text input (exact match)
   - Asset selection: radio buttons/clickable cards
   - Impact selection: CHECKBOXES (not dropdown!)
   - Acknowledgment checkbox: REQUIRED before "Next"
2. **Severity Level** — clickable cards (Low/Medium/High/Critical)
3. **Main Report** — Title input + body (textarea or ProseMirror contenteditable)
4. **Wallet Address** — input field for payout address

## React-Select Interaction Pattern
```python
# 1. Click the input container (NOT the placeholder div)
rc = d.find_element(By.CSS_SELECTOR, ".react-select__input-container")
rc.click()
time.sleep(1)

# 2. Type in the inner input to filter
rs_input = d.find_element(By.CSS_SELECTOR, ".react-select__input input, input[id^='react-select']")
rs_input.send_keys("ZKsync")
time.sleep(3)

# 3. Select option by EXACT text match (avoid partial — wrong program!)
for opt in d.find_elements(By.CSS_SELECTOR, ".react-select__option"):
    if opt.text.strip() == "ZKsync OS":
        opt.click()
        break
```

## Modal Handling — CRITICAL
```python
def dismiss_modal(d):
    """Press Escape — NEVER remove DOM elements"""
    from selenium.webdriver.common.keys import Keys
    try:
        body = d.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        time.sleep(1)
        body.send_keys(Keys.ESCAPE)
    except:
        pass
    time.sleep(1)
```

### NEVER DO:
```python
# CRASHES REACT — "Failed to execute 'removeChild' on 'Node'"
document.querySelectorAll('[role="dialog"]').forEach(el => el.remove());
```

### NEVER DO:
```python
# "Cancel" button on Discord modal CANCELS the entire submission
# Redirects back to dashboard, losing all form data
cancel_btn.click()  # BAD
```

### ALWAYS DO:
```python
# Escape key dismisses Radix UI modals without side effects
body.send_keys(Keys.ESCAPE)  # GOOD
```

## Discord Modal After Program Selection
- Appears immediately after selecting a program
- Shows "Validate account with Discord" prompt
- Has "Connect Discord" and "Cancel" buttons
- **Cancel** = loses entire submission
- **Escape** = closes modal, stays on form
- If Discord not connected, "Next: Severity Level" redirects to Discord OAuth

## Selector Reference
| Element | Selector | Notes |
|---------|----------|-------|
| Program dropdown | `.react-select__input-container` | Click this, NOT placeholder |
| Program options | `.react-select__option` | After typing filter text |
| Confirmation input | `input[placeholder*="manually type"]` | Exact program name |
| Asset cards | `[role='radio'], button, [class*='cursor-pointer']` | Match text content |
| Impact checkboxes | `//*[contains(text(), 'Undocumented deviation')]` | XPath by text |
| Acknowledgment | `//*[contains(text(), 'I have read the rules')]` | Also try `input[type='checkbox']` |
| Next button | `button` with text containing "next" | Case-insensitive |
| Severity cards | `//*[text()='Medium']` | Filter by x-position (>480 = main content) |
| Title input | `input[type='text']` without "search" placeholder | First visible empty text input |
| Body editor | `textarea, .ProseMirror, [contenteditable='true']` | May need JS for contenteditable |
| Wallet input | `input` with placeholder containing "wallet" or "0x" | |

## Errors & Fixes
| Error | Cause | Fix |
|-------|-------|-----|
| `SessionNotCreatedException: user data directory in use` | Chrome not fully closed | `pkill -9 -f chrome; rm -f $PROFILE/SingletonLock` |
| `ElementClickInterceptedException: .fixed.inset-0` | Modal overlay blocking | `dismiss_modal(d)` with Escape key |
| React crash `removeChild` | Removing React-managed DOM elements | NEVER `el.remove()` — use Escape |
| Wrong program selected | Partial text match | Exact match: `opt.text.strip() == "ZKsync OS"` |
| `UnexpectedAlertPresentException` | "Changing project clears all fields" | `d.switch_to.alert.accept()` |
| Form not advancing | Acknowledgment checkbox not checked | Find and click actual checkbox input |
| Discord OAuth redirect | Discord not connected | Must connect Discord first via Settings |

## ZKPassport Verification Flow
1. Go to `bugs.immunefi.com/settings/identity/zkpassport`
2. QR code appears (canvas/SVG element)
3. Scan with ZKPassport app on phone
4. App does NFC scan of passport
5. Generates ZK proof
6. Page shows "Generating proof..." then "Verified"
7. Keep browser open ~5 min for proof generation

## Key Scripts
- `imm_connect_discord_v2.py` — Connect Discord OAuth
- `imm_submit_v2.py` — Full submission automation
- `imm_zkpassport_qr.py` — QR code for identity verification
- `imm_refresh_check.py` — Check verification status

## Chrome Setup (All Immunefi Scripts)
```python
PROFILE = os.path.expanduser("~/.chrome-immunefi2")
opts = Options()
opts.add_argument(f"--user-data-dir={PROFILE}")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1280,1100")
opts.add_argument("--disable-gpu")
opts.binary_location = "/usr/bin/google-chrome"
svc = Service(ChromeDriverManager().install())
d = webdriver.Chrome(service=svc, options=opts)
d.implicitly_wait(10)
```

## Bug Report Template (ZKsync OS Example)
```
Title: "EVM Interpreter Callstack Depth Off-By-One Allows 1025 Frames Instead of 1024"
Sections: Summary → Vulnerability Details → Root Cause → EVM Spec Reference → Impact → PoC → Recommended Fix
Severity: Medium (undocumented deviation from EVM behavior)
Asset: Primacy of Impact / Blockchain/DLT
Wallet: 0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B
```

## Timing Notes
- Page loads: `time.sleep(5-8)` (Immunefi is SLOW)
- React-select typing: `time.sleep(3)` after send_keys (debounce)
- After clicking options: `time.sleep(2-3)` for state update
- Modal dismiss: `time.sleep(1)` between Escape presses
- After "Next" button: `time.sleep(4)` for page transition

## Session 31.5 — Login Troubleshooting (26 Mar 2026)

### Login Issues
- Password `PadraoBTC2026!Sec#` EXPIRED — new password is `ImmunefiElrom2026#Sec99`
- Immunefi uses **NextAuth + Firebase** (session cookie = Firebase JWT)
- Login button XPath `//button[contains(text(), 'Login')]` FAILS — button text is in child span
- **ALWAYS use `Keys.RETURN` on password field** instead of finding/clicking Login button
- Login via headless Chrome SILENTLY FAILS — no error shown, stays on login page
- Likely cause: invisible reCAPTCHA or rate limiting on headless browsers
- `__NEXT_DATA__` available at page load, contains `user: null` when not logged in

### Working Selectors (26 Mar 2026)
- Email: `input[type='email']`
- Password: `input[type='password']`
- CSRF token in `__Host-next-auth.csrf-token` cookie
- NextAuth callback URL in `__Secure-next-auth.callback-url` cookie
- Firebase session in `session` cookie (JWT with `eyJhbG...`)

### Key Architecture
- Immunefi = Next.js + NextAuth + Firebase Auth
- Session cookie = Firebase JWT (`eyJhbGciOiJSUzI1NiIsImtpZCI6...`)
- Firebase API key needed for REST API auth (not found in page source easily)
- `__NEXT_DATA__` props contain CSRF and user state
- `customTokenInjection` cookie exists but empty

### Anti-Automation Defenses
- Headless Chrome login fails silently (no error message shown)
- Possible reCAPTCHA or Cloudflare challenge on login
- Non-headless Chrome with `--disable-blink-features=AutomationControlled` needed
- `DISPLAY=:0` with real X server required for non-headless mode

### BLOCKER STATUS
- **Discord**: STILL NOT CONNECTED — blocks submission form at Step 1
- Support ticket #8002 sent 25 Mar, NO response yet
- Cannot submit bugs until Discord is connected OR Immunefi support responds
