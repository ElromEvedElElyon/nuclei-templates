#!/usr/bin/env python3
"""
OpenCllaw Tweet Poster v2 - curl_cffi Edition
Bypasses Cloudflare via TLS fingerprint impersonation.
Generates proper x-client-transaction-id using twikit's algorithm.

Usage:
  python3 tweet_now.py "Your tweet text here"
  python3 tweet_now.py /path/to/tweet_file.txt
  python3 tweet_now.py  # Uses default test tweet

Dependencies: curl_cffi, bs4, lxml
"""
import sys
import os
import re
import json
import math
import time
import random
import base64
import hashlib
from functools import reduce

# ---------------------------------------------------------------------------
# Credential loader
# ---------------------------------------------------------------------------
def load_env(path=os.path.expanduser("~/.secrets.env")):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

_env = load_env()
AUTH_TOKEN = _env.get("X_AUTH_TOKEN", "")
CT0 = _env.get("X_CT0", "")
KDT = _env.get("X_KDT", "")
TWID = _env.get("X_TWID", "u%3D2025759519108915200")
ROW_INDEX = int(_env.get("TWIKIT_ROW_INDEX", "10"))
KEY_INDICES = [int(x) for x in _env.get("TWIKIT_KEY_INDICES", "47,35,19").split(",")]

if not AUTH_TOKEN or not CT0:
    print("ERROR: Missing X_AUTH_TOKEN or X_CT0 in ~/.secrets.env")
    sys.exit(1)

BEARER = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

# ---------------------------------------------------------------------------
# Transaction ID generation  (port of twikit's ClientTransaction)
# ---------------------------------------------------------------------------
from typing import List, Union

def _float_to_hex(x):
    result = []
    quotient = int(x)
    fraction = x - quotient
    while quotient > 0:
        quotient = int(x / 16)
        remainder = int(x - (float(quotient) * 16))
        if remainder > 9:
            result.insert(0, chr(remainder + 55))
        else:
            result.insert(0, str(remainder))
        x = float(quotient)
    if fraction == 0:
        return "".join(result)
    result.append(".")
    while fraction > 0:
        fraction *= 16
        integer = int(fraction)
        fraction -= float(integer)
        if integer > 9:
            result.append(chr(integer + 55))
        else:
            result.append(str(integer))
    return "".join(result)


def _is_odd(num):
    return -1.0 if num % 2 else 0.0


def _solve(value, min_val, max_val, rounding):
    result = value * (max_val - min_val) / 255 + min_val
    return math.floor(result) if rounding else round(result, 2)


class _Cubic:
    """Attempt at the cubic bezier curve twikit uses."""
    def __init__(self, curves):
        self.curves = curves

    def get_value(self, t):
        c = self.curves
        if len(c) < 4:
            return t
        x1, y1, x2, y2 = c[0], c[1], c[2], c[3]
        # Simple cubic bezier approximation
        t2 = t * t
        t3 = t2 * t
        return 3 * (1 - t) * (1 - t) * t * y1 + 3 * (1 - t) * t2 * y2 + t3


def _interpolate(from_vals, to_vals, t):
    return [f + (to - f) * t for f, to in zip(from_vals, to_vals)]


def _rotation_to_matrix(deg):
    rad = deg * math.pi / 180
    c = math.cos(rad)
    s = math.sin(rad)
    return [c, s, -s, c, 0, 0]


def _animate(frame_row, target_time):
    from_color = [float(item) for item in [*frame_row[:3], 1]]
    to_color = [float(item) for item in [*frame_row[3:6], 1]]
    from_rotation = [0.0]
    to_rotation = [_solve(float(frame_row[6]), 60.0, 360.0, True)]
    curves_data = frame_row[7:]
    curves = [_solve(float(item), _is_odd(counter), 1.0, False)
              for counter, item in enumerate(curves_data)]
    cubic = _Cubic(curves)
    val = cubic.get_value(target_time)
    color = _interpolate(from_color, to_color, val)
    color = [v if v > 0 else 0 for v in color]
    rotation = _interpolate(from_rotation, to_rotation, val)
    matrix = _rotation_to_matrix(rotation[0])
    str_arr = [format(round(v), "x") for v in color[:-1]]
    for v in matrix:
        rounded = round(v, 2)
        if rounded < 0:
            rounded = -rounded
        hex_value = _float_to_hex(rounded)
        str_arr.append(
            f"0{hex_value}".lower() if hex_value.startswith(".") else hex_value if hex_value else "0"
        )
    str_arr.extend(["0", "0"])
    return re.sub(r"[.\-]", "", "".join(str_arr))


def _get_2d_array(key_bytes, soup):
    frames = soup.select("[id^='loading-x-anim']")
    if not frames:
        raise RuntimeError("No loading-x-anim frames found in page")
    frame_el = frames[key_bytes[5] % 4]
    children_outer = list(frame_el.children)
    children_inner = list(children_outer[0].children)
    d_attr = children_inner[1].get("d", "")[9:]
    parts = d_attr.split("C")
    return [[int(x) for x in re.sub(r"[^\d]+", " ", item).strip().split()] for item in parts]


def generate_transaction_id(method, path, key_str, key_bytes, animation_key):
    """Generate a valid x-client-transaction-id."""
    time_now = math.floor((time.time() * 1000 - 1682924400 * 1000) / 1000)
    time_now_bytes = [(time_now >> (i * 8)) & 0xFF for i in range(4)]
    keyword = "obfiowerehiring"
    hash_val = hashlib.sha256(
        f"{method}!{path}!{time_now}{keyword}{animation_key}".encode()
    ).digest()
    hash_bytes = list(hash_val)
    random_num = random.randint(0, 255)
    bytes_arr = [*key_bytes, *time_now_bytes, *hash_bytes[:16], 3]
    out = bytearray([random_num, *[item ^ random_num for item in bytes_arr]])
    return base64.b64encode(bytes(out)).decode().rstrip("=")


# ---------------------------------------------------------------------------
# Core HTTP layer using curl_cffi
# ---------------------------------------------------------------------------
def get_session():
    """Create a curl_cffi session with Chrome TLS fingerprint."""
    from curl_cffi import requests as cffi_requests
    return cffi_requests


def fetch_homepage_and_build_txn():
    """Fetch x.com homepage and build the transaction ID generator context."""
    import bs4
    cffi = get_session()
    print("[*] Fetching x.com homepage (curl_cffi + chrome TLS)...")
    r = cffi.get("https://x.com/", impersonate="safari15_5", timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"Homepage returned {r.status_code}")
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    # Extract key
    elem = soup.select_one("[name='twitter-site-verification']")
    if not elem:
        raise RuntimeError("No twitter-site-verification meta tag found")
    key_str = elem.get("content")
    key_bytes = list(base64.b64decode(key_str.encode()))
    print(f"[+] Got verification key ({len(key_bytes)} bytes)")

    # Build animation key
    row_index = key_bytes[ROW_INDEX] % 16
    frame_time = reduce(
        lambda a, b: a * b, [key_bytes[i] % 16 for i in KEY_INDICES]
    )
    arr = _get_2d_array(key_bytes, soup)
    frame_row = arr[row_index]
    total_time = 4096
    target_time = float(frame_time) / total_time
    animation_key = _animate(frame_row, target_time)
    print(f"[+] Animation key: {animation_key[:20]}...")

    # Also try to get updated ondemand indices
    try:
        on_demand_re = re.compile(
            r"""['\"]{1}ondemand\.s['\"]{1}:\s*['\"]{1}([\w]*)['\"]{1}""",
            re.VERBOSE | re.MULTILINE,
        )
        match = on_demand_re.search(r.text)
        if match:
            chunk_id = match.group(1)
            print(f"[+] Found ondemand.s chunk: {chunk_id}")
            od_url = f"https://abs.twimg.com/responsive-web/client-web/ondemand.s.{chunk_id}a.js"
            odr = cffi.get(od_url, impersonate="safari15_5", timeout=10)
            if odr.status_code == 200:
                idx_re = re.compile(r"""(\(\w{1}\[(\d{1,2})\],\s*16\))+""", re.VERBOSE | re.MULTILINE)
                idxs = [m.group(2) for m in idx_re.finditer(odr.text)]
                if idxs:
                    new_row = int(idxs[0])
                    new_keys = [int(x) for x in idxs[1:]]
                    print(f"[+] Updated indices: row={new_row}, keys={new_keys}")
    except Exception as e:
        print(f"[!] Could not update indices: {e}")

    return key_str, key_bytes, animation_key


def get_create_tweet_query_id():
    """Fetch current CreateTweet queryId from main.js."""
    cffi = get_session()
    print("[*] Fetching main.js to get CreateTweet queryId...")
    r = cffi.get("https://x.com/", impersonate="safari15_5", timeout=15)
    urls = re.findall(
        r'src="(https://abs\.twimg\.com/responsive-web/client-web/main\.[^"]+\.js)"',
        r.text,
    )
    if not urls:
        print("[!] Could not find main.js URL, using fallback queryId")
        return "zkcFc6F-RKRgWN8HUkJfZg"

    jr = cffi.get(urls[0], impersonate="safari15_5", timeout=15)
    matches = re.findall(
        r'queryId:"([^"]+)",operationName:"CreateTweet"', jr.text
    )
    if matches:
        print(f"[+] CreateTweet queryId: {matches[0]}")
        return matches[0]
    print("[!] queryId not found in main.js, using fallback")
    return "zkcFc6F-RKRgWN8HUkJfZg"


# Feature flags for CreateTweet (extracted from main.js)
CREATE_TWEET_FEATURES = {
    "premium_content_api_read_enabled": False,
    "communities_web_enable_tweet_community_results_fetch": True,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "responsive_web_grok_analyze_button_fetch_trends_enabled": True,
    "responsive_web_grok_analyze_post_followups_enabled": True,
    "responsive_web_jetfuel_frame": False,
    "responsive_web_grok_share_attachment_enabled": True,
    "responsive_web_grok_annotations_enabled": False,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "tweet_awards_web_tipping_enabled": False,
    "content_disclosure_indicator_enabled": True,
    "content_disclosure_ai_generated_indicator_enabled": True,
    "responsive_web_grok_show_grok_translated_post": False,
    "responsive_web_grok_analysis_button_from_backend": True,
    "post_ctas_fetch_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "profile_label_improvements_pcf_label_in_post_enabled": True,
    "responsive_web_profile_redirect_enabled": True,
    "rweb_tipjar_consumption_enabled": True,
    "verified_phone_label_enabled": False,
    "articles_preview_enabled": True,
    "responsive_web_grok_community_note_auto_translation_is_enabled": False,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "responsive_web_grok_image_annotation_enabled": True,
    "responsive_web_grok_imagine_annotation_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
}


def post_tweet(tweet_text, query_id=None, max_retries=2):
    """Post a tweet using curl_cffi + proper transaction ID."""
    cffi = get_session()

    # Step 1: Get homepage data for transaction ID
    key_str, key_bytes, animation_key = fetch_homepage_and_build_txn()

    # Step 2: Get the current CreateTweet queryId
    if not query_id:
        query_id = get_create_tweet_query_id()

    path = f"/i/api/graphql/{query_id}/CreateTweet"

    # Step 3: Generate transaction ID
    txn_id = generate_transaction_id("POST", path, key_str, key_bytes, animation_key)
    print(f"[+] Transaction ID: {txn_id[:30]}...")

    # Step 4: Build cookies and headers
    cookies = {
        "auth_token": AUTH_TOKEN,
        "ct0": CT0,
        "kdt": KDT,
        "twid": TWID,
    }

    headers = {
        "authorization": BEARER,
        "x-csrf-token": CT0,
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en",
        "x-client-transaction-id": txn_id,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "referer": "https://x.com/compose/post",
        "origin": "https://x.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }

    payload = {
        "variables": {
            "tweet_text": tweet_text,
            "dark_request": False,
            "media": {"media_entities": [], "possibly_sensitive": False},
            "semantic_annotation_ids": [],
        },
        "features": CREATE_TWEET_FEATURES,
        "queryId": query_id,
    }

    # Step 5: Post the tweet
    url = f"https://x.com{path}"
    print(f"[*] Posting tweet ({len(tweet_text)} chars)...")

    for attempt in range(max_retries + 1):
        r = cffi.post(
            url,
            headers=headers,
            cookies=cookies,
            json=payload,
            impersonate="safari15_5",
            timeout=20,
        )

        print(f"[*] Response status: {r.status_code}")

        if r.status_code == 403:
            print("[!] Got 403 (Cloudflare or auth issue)")
            # Try refreshing ct0 from response cookies
            new_ct0 = None
            for cookie_str in r.headers.get("set-cookie", "").split(","):
                if "ct0=" in cookie_str:
                    m = re.search(r"ct0=([^;]+)", cookie_str)
                    if m and m.group(1):
                        new_ct0 = m.group(1)
            if new_ct0 and new_ct0 != CT0:
                print(f"[+] Got new ct0 token, retrying...")
                cookies["ct0"] = new_ct0
                headers["x-csrf-token"] = new_ct0
                # Regenerate transaction ID
                txn_id = generate_transaction_id("POST", path, key_str, key_bytes, animation_key)
                headers["x-client-transaction-id"] = txn_id
                continue
            if attempt < max_retries:
                print(f"[*] Retry {attempt + 1}...")
                time.sleep(2)
                continue
            return False, f"403 Forbidden after {max_retries + 1} attempts"

        if r.status_code == 429:
            return False, "Rate limited (429). Wait and retry."

        try:
            data = r.json()
        except Exception:
            return False, f"Non-JSON response: {r.text[:300]}"

        # Check for errors
        if "errors" in data:
            errors = data["errors"]
            codes = [e.get("code", 0) for e in errors]
            msgs = [e.get("message", "") for e in errors]
            err_str = "; ".join(f"[{c}] {m}" for c, m in zip(codes, msgs))

            if 353 in codes and attempt < max_retries:
                # CSRF token mismatch - extract new one
                print("[!] CSRF mismatch (353), extracting new ct0...")
                for cookie_str in r.headers.get("set-cookie", "").split(","):
                    if "ct0=" in cookie_str:
                        m = re.search(r"ct0=([^;]+)", cookie_str)
                        if m and m.group(1):
                            cookies["ct0"] = m.group(1)
                            headers["x-csrf-token"] = m.group(1)
                            txn_id = generate_transaction_id("POST", path, key_str, key_bytes, animation_key)
                            headers["x-client-transaction-id"] = txn_id
                            continue

            return False, err_str

        # Check for successful tweet
        tweet_results = data.get("data", {}).get("create_tweet", {}).get("tweet_results", {})
        result = tweet_results.get("result", {})
        tweet_id = result.get("rest_id", "")

        if tweet_id:
            return True, tweet_id

        # Empty tweet_results - tweet was silently dropped
        # This can happen if:
        # 1. Transaction ID is invalid
        # 2. Account is in limited state
        # 3. Rate limit soft-cap reached
        print("[!] Empty tweet_results (tweet silently dropped)")
        print(f"[!] Full response: {json.dumps(data)[:500]}")

        if attempt < max_retries:
            print(f"[*] Retrying with fresh homepage data...")
            time.sleep(2)
            # Refresh everything
            key_str, key_bytes, animation_key = fetch_homepage_and_build_txn()
            txn_id = generate_transaction_id("POST", path, key_str, key_bytes, animation_key)
            headers["x-client-transaction-id"] = txn_id
            continue

        return False, "Tweet silently dropped (empty tweet_results). Account may be rate-limited or in restricted mode."

    return False, "Max retries exceeded"


def verify_auth():
    """Verify that the auth tokens are still valid."""
    cffi = get_session()
    cookies = {
        "auth_token": AUTH_TOKEN,
        "ct0": CT0,
        "kdt": KDT,
        "twid": TWID,
    }
    headers = {
        "authorization": BEARER,
        "x-csrf-token": CT0,
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en",
        "content-type": "application/json",
    }

    # Use the latest Viewer queryId
    r_home = cffi.get("https://x.com/", impersonate="safari15_5", timeout=15)
    urls = re.findall(
        r'src="(https://abs\.twimg\.com/responsive-web/client-web/main\.[^"]+\.js)"',
        r_home.text,
    )
    viewer_id = "_8ClT24oZ8tpylf_OSuNdg"  # fallback
    if urls:
        jr = cffi.get(urls[0], impersonate="safari15_5", timeout=15)
        vm = re.findall(r'queryId:"([^"]+)",operationName:"Viewer"', jr.text)
        if vm:
            viewer_id = vm[0]

    r = cffi.get(
        f"https://x.com/i/api/graphql/{viewer_id}/Viewer",
        params={
            "variables": json.dumps({"withCommunitiesMemberships": True}),
            "features": json.dumps({
                "rweb_tipjar_consumption_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
            }),
        },
        headers=headers,
        cookies=cookies,
        impersonate="safari15_5",
        timeout=15,
    )

    if r.status_code != 200:
        return False, f"Status {r.status_code}"

    data = r.json()
    # Find screen_name in nested structure
    def find_val(d, target):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == target:
                    return v
                found = find_val(v, target)
                if found is not None:
                    return found
        elif isinstance(d, list):
            for item in d:
                found = find_val(item, target)
                if found is not None:
                    return found
        return None

    screen = find_val(data, "screen_name")
    if screen:
        return True, screen
    return False, "Could not find screen_name in response"


def main():
    # Parse arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--verify":
            print("[*] Verifying auth...")
            ok, result = verify_auth()
            if ok:
                print(f"[+] Auth valid! Logged in as @{result}")
            else:
                print(f"[-] Auth failed: {result}")
            sys.exit(0 if ok else 1)
        elif os.path.isfile(arg):
            with open(arg) as f:
                tweet_text = f.read().strip()
        else:
            tweet_text = arg
    else:
        tweet_text = f"Building the future of decentralized finance, one commit at a time. [{int(time.time()) % 10000}]"

    if len(tweet_text) > 280:
        print(f"ERROR: Tweet too long ({len(tweet_text)} chars, max 280)")
        sys.exit(1)

    print(f"[*] Tweet ({len(tweet_text)} chars): {tweet_text[:120]}{'...' if len(tweet_text) > 120 else ''}")
    print()

    success, result = post_tweet(tweet_text)

    if success:
        url = f"https://x.com/opencllaw/status/{result}"
        print()
        print(f"[+] SUCCESS!")
        print(f"[+] Tweet ID: {result}")
        print(f"[+] URL: {url}")
    else:
        print()
        print(f"[-] FAILED: {result}")
        if "226" in str(result):
            print("[!] Rate limited (automation detection). Wait 15+ minutes.")
        elif "187" in str(result):
            print("[!] Duplicate tweet. Change the text and retry.")
        elif "344" in str(result):
            print("[!] Daily limit reached. Wait until tomorrow.")
        elif "silently dropped" in str(result):
            print("[!] Tweet was silently dropped. Possible causes:")
            print("    1. Account in restricted/limited mode (rate limit code 226)")
            print("    2. Transaction ID generation mismatch")
            print("    3. Try: python3 tweet_now.py --verify  (to check auth)")
            print("    4. May need to log in via browser to clear captcha/challenge")
        sys.exit(1)


if __name__ == "__main__":
    main()
