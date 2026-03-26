#!/usr/bin/env python3
"""
ISRAEL/ONE — Thread Generator for @opencllaw
Em nome do Senhor Jesus Cristo, nosso Salvador.

Converts solo tweets into 5-7 part Twitter/X threads.
Style: builder-authority | ZERO emojis | ZERO hashtags | Technical credibility

Usage:
    python3 thread_generator.py generate
    python3 thread_generator.py list
    python3 thread_generator.py preview INDEX
    python3 thread_generator.py post INDEX
"""

import json
import os
import sys
import hashlib
import random
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import urllib.request

# ─── CONFIG ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
HOME_DIR = Path.home()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

QUEUED_TWEETS_PATH = BASE_DIR / "queued_tweets.json"
OPENCLLAW_TWEETS_PATH = HOME_DIR / "opencllaw_tweets.json"
THREADS_OUTPUT_PATH = BASE_DIR / "queued_threads.json"

BRT = timezone(timedelta(hours=-3))
MAX_TWEET_CHARS = 280
THREAD_MIN = 5
THREAD_MAX = 7
CTA_LINE = "Follow @opencllaw for daily alpha"

# ─── STYLE DNA (proven +774% impressions) ────────────────────────────
STYLE_RULES = [
    "Lead with product name or entity, never I or questions",
    "Short punchy sentences, fragments OK, under 12 words each",
    "Heavy line breaks, each point on its own line",
    "ZERO emojis, ZERO hashtags, ZERO exclamation marks",
    "No period at the end of the tweet",
    "One ALL-CAPS data point maximum per tweet",
    "Arrow lists for features, dash lists for data",
    "Sound like intelligence briefing, not motivational speaker",
]

VOCAB = [
    "ship", "sovereign", "permissionless", "agent", "execute", "infra",
    "stack", "deploy", "vault", "protocol", "rails", "primitive",
    "composable", "trustless", "on-chain", "self-custody", "alpha",
    "convergence", "merge", "build", "output", "pipeline",
]

# ─── PRODUCTS ─────────────────────────────────────────────────────────
PRODUCTS = {
    "ClawChat": "PWA AI assistant, 4 providers racing, zero cost",
    "claw-mcp-toolkit": "29 tools for crypto, social, finance via Claude",
    "chainlink-sentinel": "Autonomous security scanner for smart contracts",
    "SintexOS": "Web-based AI operating system with 8 apps",
    "OpenClaw": "AI agent that runs on your machine, fully sovereign",
    "flash-payment-system": "Instant crypto payment rails for AI agents",
    "Solana Vault Standard": "ERC-4626 on Solana, streaming yield",
    "commerce-pay-mcp": "Commerce payment processing via MCP protocol",
}

# ─── EXPANSION STRATEGIES ─────────────────────────────────────────────
# Maps tweet categories/types to thread expansion patterns.
# Each pattern defines what each tweet slot should contain.

EXPANSION_PATTERNS = {
    "metric_drop": {
        "hook": "Lead with the most surprising number. Create tension between data and narrative",
        "body": [
            "Break down what the metrics actually mean. Add context most miss",
            "Compare to a historical parallel. Show the pattern",
            "Explain what smart money is doing right now vs retail",
            "Present the contrarian read. Why the obvious take is wrong",
        ],
        "counter": "Acknowledge the bear case or risk. Show intellectual honesty",
        "closer": "Distill into one actionable thesis. End with conviction",
    },
    "convergence": {
        "hook": "Name the convergence. Make it feel inevitable",
        "body": [
            "Explain what each technology does alone vs together",
            "Give a concrete example of the convergence in production",
            "Show the market size or opportunity most underestimate",
            "Reference a product or system that proves the thesis",
        ],
        "counter": "Address the skeptic argument directly. Then dismantle it",
        "closer": "Project forward 12-18 months. State what becomes obvious",
    },
    "builder_log": {
        "hook": "Drop the output number. Raw results, no commentary",
        "body": [
            "Break down the stack that made this possible",
            "Share one specific technical decision and why",
            "Compare the builder approach to the corporate approach",
            "Show what this unlocks next. The compound effect",
        ],
        "counter": "Admit what did not work or what you would change",
        "closer": "Restate the builder thesis. Output over optics",
    },
    "insider_alpha": {
        "hook": "State the insight most people will disagree with",
        "body": [
            "Provide the evidence. Data, not opinion",
            "Show why the mainstream view is incomplete",
            "Give a specific example from the trenches",
            "Connect it to a larger structural shift",
        ],
        "counter": "Present the strongest counter-argument fairly",
        "closer": "Deliver the final verdict. Clear and convicted",
    },
    "sovereignty": {
        "hook": "Frame sovereignty as non-negotiable. State the stakes",
        "body": [
            "Define what sovereignty means in practice, not theory",
            "Give a real example of sovereignty violated",
            "Show the technical solution. Keys, protocols, agents",
            "Explain why this matters more in 2026 than ever",
        ],
        "counter": "Address the convenience argument. Why people choose custody",
        "closer": "End with the principle. Sovereignty is not optional",
    },
    "hot_take": {
        "hook": "Drop the contrarian statement. No preamble",
        "body": [
            "Support with first-principles reasoning",
            "Add data or historical precedent",
            "Show what happens if this thesis plays out",
            "Reference builders already proving the point",
        ],
        "counter": "Steel-man the opposing view. Then explain why it fails",
        "closer": "Restate with more precision. Leave no ambiguity",
    },
    "default": {
        "hook": "Reframe the core idea as a provocation or bold claim",
        "body": [
            "Provide the strongest supporting evidence",
            "Add a concrete example or data point",
            "Connect to a broader trend or structural shift",
            "Show what this means for builders and operators",
        ],
        "counter": "Present the nuanced counter-view. Show depth",
        "closer": "Deliver the conclusion with conviction. Add CTA",
    },
}


# ─── CRYPTO DATA ──────────────────────────────────────────────────────
def fetch_crypto_data():
    """Fetch real-time crypto data from CoinGecko. Lightweight, no deps."""
    data = {}
    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum,solana"
            "&vs_currencies=usd"
            "&include_24hr_change=true"
            "&include_market_cap=true"
        )
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "IsraelOne/1.0"},
        )
        resp = urllib.request.urlopen(req, timeout=10)
        prices = json.loads(resp.read())

        data["btc_price"] = f"{prices['bitcoin']['usd']:,.0f}"
        data["eth_price"] = f"{prices['ethereum']['usd']:,.0f}"
        data["sol_price"] = f"{prices['solana']['usd']:,.2f}"
        data["btc_change"] = f"{prices['bitcoin'].get('usd_24h_change', 0):.1f}"
        data["eth_change"] = f"{prices['ethereum'].get('usd_24h_change', 0):.1f}"
        data["sol_change"] = f"{prices['solana'].get('usd_24h_change', 0):.1f}"
        btc_mcap = prices["bitcoin"].get("usd_market_cap", 0)
        data["total_mcap"] = (
            f"{btc_mcap / 1e12:.2f}T" if btc_mcap > 1e12 else f"{btc_mcap / 1e9:.0f}B"
        )
    except Exception:
        pass

    try:
        url = "https://api.alternative.me/fng/?limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "IsraelOne/1.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        fng = json.loads(resp.read())["data"][0]
        data["fear_greed"] = fng["value"]
        data["fear_greed_label"] = fng["value_classification"]
    except Exception:
        pass

    return data


def fetch_trending_coins():
    """Fetch top trending coins from CoinGecko."""
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "IsraelOne/1.0"},
        )
        resp = urllib.request.urlopen(req, timeout=10)
        d = json.loads(resp.read())
        coins = []
        for item in d.get("coins", [])[:5]:
            c = item["item"]
            coins.append({
                "name": c["name"],
                "symbol": c["symbol"],
                "rank": c.get("market_cap_rank", "?"),
            })
        return coins
    except Exception:
        return []


# ─── TWEET SOURCES ────────────────────────────────────────────────────
def load_source_tweets():
    """Load tweets from both source files. Returns list of dicts."""
    tweets = []

    # Load queued_tweets.json
    if QUEUED_TWEETS_PATH.exists():
        try:
            raw = json.loads(QUEUED_TWEETS_PATH.read_text())
            for t in raw:
                tweets.append({
                    "text": t.get("text", ""),
                    "type": t.get("type", "default"),
                    "source": "queued",
                    "category": t.get("type", "default"),
                    "engagement_type": t.get("type", "default"),
                })
        except Exception:
            pass

    # Load opencllaw_tweets.json
    if OPENCLLAW_TWEETS_PATH.exists():
        try:
            raw = json.loads(OPENCLLAW_TWEETS_PATH.read_text())
            for t in raw:
                tweets.append({
                    "text": t.get("tweet", ""),
                    "type": t.get("engagement_type", t.get("category", "default")),
                    "source": "opencllaw",
                    "category": t.get("category", "default"),
                    "engagement_type": t.get("engagement_type", "default"),
                })
        except Exception:
            pass

    return tweets


def load_threads():
    """Load existing generated threads."""
    if THREADS_OUTPUT_PATH.exists():
        try:
            return json.loads(THREADS_OUTPUT_PATH.read_text())
        except Exception:
            return []
    return []


def save_threads(threads):
    """Save threads to output file."""
    THREADS_OUTPUT_PATH.write_text(
        json.dumps(threads, indent=2, ensure_ascii=False)
    )


# ─── THREAD GENERATION ENGINE ─────────────────────────────────────────
def get_pattern(tweet_type):
    """Get expansion pattern for a tweet type."""
    # Map various types to pattern keys
    type_map = {
        "metric_drop": "metric_drop",
        "data_point": "metric_drop",
        "convergence": "convergence",
        "builder_log": "builder_log",
        "statement": "insider_alpha",
        "insider_alpha": "insider_alpha",
        "sovereignty": "sovereignty",
        "hot_take": "hot_take",
        "question": "hot_take",
        "call_to_action": "convergence",
        "stack_reveal": "builder_log",
        "binary_frame": "hot_take",
        "prediction": "insider_alpha",
        "anti_pattern": "hot_take",
        "mcp_tools": "convergence",
        "defi_alpha": "insider_alpha",
        "two_word": "default",
        "promo": "convergence",
    }
    key = type_map.get(tweet_type, "default")
    return EXPANSION_PATTERNS.get(key, EXPANSION_PATTERNS["default"])


def sanitize_tweet(text):
    """Enforce style rules on a single tweet part."""
    # Remove emojis
    text = re.sub(
        r"[\U0001F600-\U0001F9FF\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        r"\U0001F900-\U0001F9FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
        r"\U0001FA00-\U0001FAFF]",
        "",
        text,
    )
    # Remove hashtags
    text = re.sub(r"#\w+", "", text)
    # Remove trailing period
    text = text.rstrip(".")
    # Remove trailing whitespace per line
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    # Collapse triple+ newlines to double
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate_tweet(text, max_chars=MAX_TWEET_CHARS):
    """Truncate tweet to fit character limit while keeping meaning."""
    if len(text) <= max_chars:
        return text
    # Try to cut at last complete line that fits
    lines = text.split("\n")
    result = ""
    for line in lines:
        test = (result + "\n" + line).strip() if result else line
        if len(test) <= max_chars:
            result = test
        else:
            break
    if not result:
        # Single long line — cut at word boundary
        result = text[: max_chars - 3].rsplit(" ", 1)[0] + "..."
    return result


def extract_core_thesis(tweet_text):
    """Extract the central claim or thesis from a tweet."""
    lines = [l.strip() for l in tweet_text.strip().split("\n") if l.strip()]
    # Skip list items, find declarative lines
    candidates = []
    for line in lines:
        if line.startswith(("-", "->", "=>")) or line.startswith(("- ", "-> ")):
            continue
        if len(line) > 15:
            candidates.append(line)
    if candidates:
        # Prefer longer lines as more likely to be thesis
        return max(candidates, key=len)
    return lines[0] if lines else tweet_text[:100]


def extract_data_points(tweet_text):
    """Extract any numbers, percentages, or metrics from the tweet."""
    points = []
    # Find dollar amounts
    for m in re.finditer(r"\$[\d,]+\.?\d*[TBMK]?", tweet_text):
        points.append(m.group())
    # Find percentages
    for m in re.finditer(r"\d+\.?\d*%", tweet_text):
        points.append(m.group())
    # Find plain large numbers
    for m in re.finditer(r"\b\d{2,}[+]?\b", tweet_text):
        if m.group() not in ["24", "2026", "2025", "2024"]:
            points.append(m.group())
    return points


def extract_list_items(tweet_text):
    """Extract bulleted or dashed list items from tweet text."""
    items = []
    for line in tweet_text.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif line.startswith("-> "):
            items.append(line[3:].strip())
        elif line.startswith("=> "):
            items.append(line[3:].strip())
    return items


def generate_thread_from_tweet(tweet_data, crypto_data=None):
    """
    Generate a 5-7 part thread from a single solo tweet.

    Thread structure:
        1. Hook -- attention-grabbing opener
        2-5. Supporting points with data/logic
        6. Counter-argument or nuance
        7. Strong closer with CTA
    """
    text = tweet_data["text"]
    tweet_type = tweet_data.get("type", "default")
    category = tweet_data.get("category", "default")
    pattern = get_pattern(tweet_type)

    thesis = extract_core_thesis(text)
    data_points = extract_data_points(text)
    list_items = extract_list_items(text)

    # Decide thread length: shorter tweets get 5, longer/richer get 6-7
    if len(text) < 100 or (not data_points and not list_items):
        thread_len = THREAD_MIN
    elif len(list_items) >= 3 or len(data_points) >= 2:
        thread_len = THREAD_MAX
    else:
        thread_len = 6

    parts = []

    # ── TWEET 1: HOOK ──
    hook = _build_hook(text, thesis, tweet_type, crypto_data)
    parts.append(sanitize_tweet(hook))

    # ── TWEETS 2-N-2: BODY ──
    body_count = thread_len - 2  # minus hook and closer
    if thread_len >= 7:
        body_count -= 1  # reserve one for counter

    body_slots = pattern["body"][:body_count]

    for i, slot_hint in enumerate(body_slots):
        body_tweet = _build_body_tweet(
            text, thesis, tweet_type, category, slot_hint,
            i, list_items, data_points, crypto_data,
        )
        parts.append(sanitize_tweet(body_tweet))

    # ── COUNTER-ARGUMENT (if 7-part thread) ──
    if thread_len >= 7:
        counter = _build_counter(text, thesis, tweet_type, category)
        parts.append(sanitize_tweet(counter))

    # If we got a 6-part thread, add counter as part of the flow
    if thread_len == 6:
        counter = _build_counter(text, thesis, tweet_type, category)
        parts.append(sanitize_tweet(counter))

    # ── CLOSER WITH CTA ──
    closer = _build_closer(text, thesis, tweet_type, category, crypto_data)
    parts.append(sanitize_tweet(closer))

    # Enforce char limits
    parts = [truncate_tweet(p) for p in parts]

    # Trim to target length if we somehow over-generated
    parts = parts[:thread_len]

    return parts


# ─── THREAD PART BUILDERS ─────────────────────────────────────────────
# These construct each tweet in the thread from the source material.
# They use deterministic expansion, not LLM generation, to stay lightweight.

def _build_hook(text, thesis, tweet_type, crypto_data):
    """Build the opening hook tweet. Must grab attention immediately."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Strategy 1: If tweet has a strong opening line, use it with amplification
    first_line = lines[0] if lines else thesis
    if len(first_line) < 80 and not first_line.startswith("-"):
        # Short punchy opener -- amplify it
        hooks = [
            f"{first_line}\n\nThis changes everything. Here is why",
            f"{first_line}\n\nMost people are not paying attention\n\nThread",
            f"{first_line}\n\nBreaking this down",
            f"{first_line}\n\nThe data tells a different story",
        ]
        # For metric tweets, lead with numbers
        if tweet_type in ("metric_drop", "data_point") and crypto_data:
            btc = crypto_data.get("btc_price", "")
            fg = crypto_data.get("fear_greed", "")
            if btc and fg:
                hooks.append(
                    f"BTC ${btc}\nFear and Greed: {fg}\n\n{first_line}"
                )
        return random.choice(hooks)

    # Strategy 2: Extract thesis and frame as hook
    hooks = [
        f"{thesis}\n\nA thread on what most are missing",
        f"Unpopular take:\n\n{thesis}",
        f"The signal everyone is ignoring:\n\n{thesis}",
    ]
    return random.choice(hooks)


def _build_body_tweet(text, thesis, tweet_type, category, slot_hint,
                      index, list_items, data_points, crypto_data):
    """Build a supporting body tweet based on slot position and content."""

    # ── SLOT 0: Evidence / Breakdown ──
    if index == 0:
        if list_items and len(list_items) >= 2:
            # Expand list items into a structured breakdown
            items_str = "\n".join(f"- {item}" for item in list_items[:4])
            return f"Breaking it down:\n\n{items_str}"

        if data_points:
            dp = data_points[0]
            return (
                f"The numbers:\n\n{dp} is not a random data point\n\n"
                f"It is the result of structural shifts happening beneath the surface"
            )

        # Generic evidence frame
        evidence_frames = [
            f"The evidence is in the output\n\nNot the pitch deck\nNot the roadmap\nNot the Twitter thread\n\nThe deployed code",
            f"Here is what most analysis misses:\n\nThe surface narrative and the structural reality are diverging\n\nOne tells you what happened\nThe other tells you what is coming",
            f"First principles:\n\nStrip away the noise\nIgnore the sentiment\nFollow the on-chain data\n\nThe fundamentals have not changed",
        ]
        return random.choice(evidence_frames)

    # ── SLOT 1: Historical parallel or comparison ──
    if index == 1:
        if crypto_data and category in ("crypto", "convergence", "metric_drop"):
            btc = crypto_data.get("btc_price", "")
            sol = crypto_data.get("sol_price", "")
            eth = crypto_data.get("eth_price", "")
            fg_label = crypto_data.get("fear_greed_label", "")

            if btc and fg_label:
                return (
                    f"Current state:\n\n"
                    f"BTC: ${btc}\n"
                    f"ETH: ${eth}\n"
                    f"SOL: ${sol}\n"
                    f"Sentiment: {fg_label}\n\n"
                    f"The last time sentiment was here, the setup lasted weeks\n\nNot months"
                )

        parallel_frames = [
            "Every major technological shift follows the same pattern:\n\nDismissal\nCuriosity\nPanic adoption\n\nWe are between stages 2 and 3",
            "The internet in 1997\nMobile in 2009\nCrypto in 2015\nAI agents in 2026\n\nSame pattern. Different infrastructure\n\nThe builders who showed up early captured the decade",
            "History does not repeat but it rhymes\n\nThe last cycle rewarded infrastructure builders who ignored the noise\n\nThis cycle will do the same",
        ]
        return random.choice(parallel_frames)

    # ── SLOT 2: What smart money / builders are doing ──
    if index == 2:
        if category in ("ai", "building", "mcp_tools", "stack_reveal"):
            builder_frames = [
                "What the serious builders are doing right now:\n\n- Deploying MCP servers for every protocol\n- Building agent-native interfaces\n- Replacing dashboards with natural language\n\nQuietly. Without announcements",
                "The gap between builders and talkers:\n\nTalkers: 50 tweets per day, zero commits\nBuilders: 50 commits per day, zero excuses\n\nThe market always figures out which is which",
                "Smart operators are not waiting for permission\n\nThey are shipping autonomous systems that generate revenue while they sleep\n\nThe 24/7 economy demands 24/7 infrastructure",
            ]
            return random.choice(builder_frames)

        smart_money_frames = [
            "Retail watches the price\nSmart money watches the infrastructure\n\nNew protocols. New primitives. New rails\n\nThe alpha is in what gets built, not what gets bought",
            "The institutions filing quietly\nThe protocols deploying without announcements\nThe agents executing without human input\n\nThis is where the signal lives",
            "Follow the developers, not the influencers\n\nGitHub commits tell you more than Twitter threads\n\nThe code does not lie",
        ]
        return random.choice(smart_money_frames)

    # ── SLOT 3: Product reference or concrete proof ──
    if index == 3:
        product_name = random.choice(list(PRODUCTS.keys()))
        product_desc = PRODUCTS[product_name]

        product_frames = [
            f"This is why we built {product_name}\n\n{product_desc}\n\nNot theory. Deployed. Running. Verifiable",
            f"Proof of work:\n\n{product_name} — {product_desc}\n\nOpen source. Auditable. No permission required\n\nShipping is the only credential that matters",
            f"We did not write a whitepaper about this\n\nWe shipped {product_name}\n\n{product_desc}\n\nCode over consensus",
        ]
        return random.choice(product_frames)

    # ── FALLBACK for any extra body slots ──
    fallback_frames = [
        "The compound effect of daily output:\n\nDay 1: invisible\nDay 30: noticed\nDay 90: undeniable\nDay 365: unreachable\n\nMost quit at day 14",
        "Infrastructure wins are quiet\n\nNo viral moment\nNo trending topic\nNo celebrity endorsement\n\nJust adoption curves that start slow and go vertical",
        "The best opportunities hide in complexity\n\nIf it were easy, everyone would do it\nIf everyone did it, there would be no edge\n\nDifficulty is the moat",
    ]
    return random.choice(fallback_frames)


def _build_counter(text, thesis, tweet_type, category):
    """Build the counter-argument / nuance tweet."""
    counters = {
        "crypto": [
            "The bear case is real:\n\nRegulation is tightening\nRetail interest is cyclical\nMost projects will fail\n\nBut the protocols that survive will define the next financial system",
            "Fair criticism: most crypto projects ship nothing of value\n\n95% are vaporware\n\nBut the 5% that execute are building unstoppable financial infrastructure\n\nSeparate the signal from the noise",
        ],
        "ai": [
            "The honest counter:\n\nMost AI agents today are fragile. They break in production. They hallucinate\n\nBut so did the first websites. The first mobile apps. The first smart contracts\n\nInfrastructure matures. The thesis does not change",
            "Valid concern: autonomous agents making financial decisions creates real risk\n\nThe answer is not to stop building\n\nThe answer is verifiable behavior, open-source code, and transparent execution\n\nTrust through transparency",
        ],
        "building": [
            "The uncomfortable truth:\n\nShipping fast means shipping broken sometimes\n\nThe difference between amateurs and professionals is not avoiding mistakes\n\nIt is fixing them in minutes, not months",
            "Counter-point: not everything should be shipped fast\n\nSecurity. Custody. Settlement\n\nThese demand precision over speed\n\nKnow which mode you are in. That is the real skill",
        ],
    }

    # Get category-specific counters or use general
    category_counters = counters.get(category, [])

    general_counters = [
        "The strongest counter-argument:\n\nMaybe it is too early. Maybe the market is not ready\n\nBut every builder who changed the world heard the same thing\n\nToo early is better than too late. Always",
        "Honest assessment:\n\nNot every thesis plays out on schedule\nNot every build finds product-market fit\nNot every deployment survives contact with users\n\nBut the ones that do change everything",
        "The risk is real\n\nExecution risk. Market risk. Timing risk\n\nBut the biggest risk of all is building nothing while waiting for certainty\n\nCertainty is a luxury. Conviction is a choice",
    ]

    pool = category_counters + general_counters
    return random.choice(pool)


def _build_closer(text, thesis, tweet_type, category, crypto_data):
    """Build the closing tweet with CTA."""
    # Extract a short restatement
    short_thesis = thesis[:80].rstrip(".")

    closers = [
        f"{short_thesis}\n\nThis is not a prediction. It is a build log\n\n{CTA_LINE}",
        f"The thesis is simple:\n\nBuild sovereign infrastructure. Ship daily. Let the output speak\n\n{CTA_LINE}",
        f"Summary:\n\nThe noise is temporary. The infrastructure is permanent\n\nWe ship every day. The receipts are public\n\n{CTA_LINE}",
        f"Bottom line:\n\n{short_thesis}\n\nWe are not debating this. We are building it\n\n{CTA_LINE}",
        f"The signal is clear for those paying attention\n\nOutput over optics. Code over consensus. Execution over everything\n\n{CTA_LINE}",
        f"Final word:\n\nShip or become irrelevant. The market rewards builders, not commentators\n\n{CTA_LINE}",
    ]

    return random.choice(closers)


# ─── THREAD SCORING (pick best tweet to thread) ───────────────────────
def score_tweet_for_threading(tweet_data):
    """Score a tweet on how well it would expand into a thread. Higher = better."""
    text = tweet_data["text"]
    score = 0

    # Length: longer tweets have more material to expand
    if len(text) > 150:
        score += 3
    elif len(text) > 80:
        score += 2
    else:
        score += 1

    # Data points: numbers make threads more credible
    data_points = extract_data_points(text)
    score += len(data_points) * 2

    # List items: expandable structure
    list_items = extract_list_items(text)
    score += len(list_items)

    # Multiple lines: already has structure
    line_count = len([l for l in text.split("\n") if l.strip()])
    if line_count >= 3:
        score += 2

    # Certain types thread better
    good_types = ["hot_take", "convergence", "insider_alpha", "metric_drop", "data_point", "statement"]
    if tweet_data.get("type", "") in good_types:
        score += 2
    if tweet_data.get("engagement_type", "") in good_types:
        score += 1

    # Penalize very short tweets (two_word grenades are bad thread candidates)
    if len(text) < 40:
        score -= 5

    return score


def select_best_tweet(tweets, existing_threads):
    """Select the best tweet to convert into a thread, avoiding duplicates."""
    # Get hashes of already-threaded source tweets
    used_hashes = set()
    for t in existing_threads:
        used_hashes.add(t.get("source_hash", ""))

    # Score and filter
    candidates = []
    for tweet in tweets:
        h = hashlib.md5(tweet["text"].encode()).hexdigest()[:12]
        if h in used_hashes:
            continue
        score = score_tweet_for_threading(tweet)
        if score > 0:
            candidates.append((score, tweet, h))

    if not candidates:
        return None, None

    # Sort by score descending, pick top
    candidates.sort(key=lambda x: -x[0])
    best = candidates[0]
    return best[1], best[2]


# ─── CLI COMMANDS ──────────────────────────────────────────────────────
def cmd_generate():
    """Pick the best solo tweet and generate a thread from it."""
    print("ISRAEL/ONE Thread Generator")
    print("=" * 50)

    # Load sources
    tweets = load_source_tweets()
    if not tweets:
        print("[ERROR] No source tweets found")
        print(f"  Checked: {QUEUED_TWEETS_PATH}")
        print(f"  Checked: {OPENCLLAW_TWEETS_PATH}")
        sys.exit(1)

    existing_threads = load_threads()
    print(f"Source tweets: {len(tweets)}")
    print(f"Existing threads: {len(existing_threads)}")

    # Select best candidate
    tweet, source_hash = select_best_tweet(tweets, existing_threads)
    if tweet is None:
        print("\n[INFO] All source tweets have already been threaded")
        print("       Add new tweets to queued_tweets.json or opencllaw_tweets.json")
        sys.exit(0)

    print(f"\nSelected tweet (score: {score_tweet_for_threading(tweet)}):")
    print(f"  Type: {tweet.get('type', '?')}")
    print(f"  Source: {tweet.get('source', '?')}")
    print(f"  Text: {tweet['text'][:80]}...")

    # Fetch live data
    print("\nFetching crypto data...")
    crypto_data = fetch_crypto_data()
    if crypto_data:
        btc = crypto_data.get("btc_price", "?")
        fg = crypto_data.get("fear_greed", "?")
        print(f"  BTC: ${btc} | Fear&Greed: {fg}")
    else:
        print("  (offline mode — no live data)")

    # Generate thread
    print("\nGenerating thread...")
    parts = generate_thread_from_tweet(tweet, crypto_data)

    # Build thread object
    thread = {
        "id": len(existing_threads) + 1,
        "source_text": tweet["text"],
        "source_hash": source_hash,
        "source_type": tweet.get("type", "default"),
        "source_file": tweet.get("source", "unknown"),
        "thread_parts": parts,
        "thread_length": len(parts),
        "status": "generated",
        "created": datetime.now(BRT).isoformat(),
        "crypto_data": crypto_data if crypto_data else None,
    }

    existing_threads.append(thread)
    save_threads(existing_threads)

    print(f"\nThread #{thread['id']} generated ({len(parts)} parts)")
    print("=" * 50)
    for i, part in enumerate(parts, 1):
        label = "HOOK" if i == 1 else ("CLOSER" if i == len(parts) else f"PART {i}")
        print(f"\n[{label}] ({len(part)} chars):")
        print(part)
        print("-" * 40)

    print(f"\nSaved to: {THREADS_OUTPUT_PATH}")


def cmd_list():
    """List all generated threads."""
    threads = load_threads()
    if not threads:
        print("No threads generated yet")
        print(f"Run: python3 {Path(__file__).name} generate")
        return

    print(f"Generated Threads: {len(threads)}")
    print("=" * 60)
    for t in threads:
        status_marker = "POSTED" if t.get("status") == "posted" else "READY"
        source_preview = t["source_text"][:60].replace("\n", " ")
        print(
            f"\n  [{t['id']}] [{status_marker}] {t['thread_length']} parts | "
            f"{t.get('source_type', '?')}"
        )
        print(f"      {source_preview}...")
        print(f"      Created: {t.get('created', '?')}")


def cmd_preview(index):
    """Preview a specific thread by index."""
    threads = load_threads()
    if not threads:
        print("No threads generated yet")
        return

    # Find thread by ID
    thread = None
    for t in threads:
        if t["id"] == index:
            thread = t
            break

    if thread is None:
        print(f"Thread #{index} not found")
        print(f"Available: {[t['id'] for t in threads]}")
        return

    print(f"Thread #{thread['id']} — {thread['thread_length']} parts")
    print(f"Source type: {thread.get('source_type', '?')}")
    print(f"Status: {thread.get('status', '?')}")
    print(f"Created: {thread.get('created', '?')}")
    print("=" * 60)
    print(f"Source tweet:\n  {thread['source_text'][:120]}...")
    print("=" * 60)

    total_chars = 0
    for i, part in enumerate(thread["thread_parts"], 1):
        if i == 1:
            label = "HOOK"
        elif i == len(thread["thread_parts"]):
            label = "CLOSER + CTA"
        elif i == len(thread["thread_parts"]) - 1 and thread["thread_length"] >= 6:
            label = "COUNTER"
        else:
            label = f"BODY {i - 1}"

        print(f"\n  [{i}/{thread['thread_length']}] {label} ({len(part)} chars):")
        print(f"  {'─' * 40}")
        for line in part.split("\n"):
            print(f"    {line}")
        total_chars += len(part)

    print(f"\n{'=' * 60}")
    print(f"Total characters: {total_chars}")
    print(f"Avg per tweet: {total_chars // len(thread['thread_parts'])}")


def cmd_post(index):
    """Post a thread via tweet_now.py (sequential posting)."""
    threads = load_threads()
    thread = None
    for t in threads:
        if t["id"] == index:
            thread = t
            break

    if thread is None:
        print(f"Thread #{index} not found")
        return

    if thread.get("status") == "posted":
        print(f"Thread #{index} already posted")
        return

    script = os.path.expanduser("~/tweet_now.py")
    if not os.path.exists(script):
        print("[ERROR] tweet_now.py not found at ~/tweet_now.py")
        print("Cannot post without the posting script")
        sys.exit(1)

    import subprocess
    import time

    print(f"Posting thread #{index} ({thread['thread_length']} parts)")
    print("=" * 50)

    posted = 0
    for i, part in enumerate(thread["thread_parts"], 1):
        label = "HOOK" if i == 1 else ("CLOSER" if i == len(thread["thread_parts"]) else f"PART {i}")
        print(f"\n  Posting [{label}] ({len(part)} chars)...")

        try:
            result = subprocess.run(
                ["python3", script, part],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0 and "SUCCESS" in result.stdout:
                print(f"    POSTED")
                posted += 1
            else:
                print(f"    FAILED: {result.stdout[:100]}")
                print(f"    Stopping thread to avoid gaps")
                break
        except Exception as e:
            print(f"    ERROR: {e}")
            break

        # Rate limit safety between thread parts
        if i < len(thread["thread_parts"]):
            wait = random.randint(8, 15)
            print(f"    Waiting {wait}s before next part...")
            time.sleep(wait)

    if posted == len(thread["thread_parts"]):
        thread["status"] = "posted"
        thread["posted_at"] = datetime.now(BRT).isoformat()
        save_threads(threads)
        print(f"\nThread #{index} fully posted ({posted}/{thread['thread_length']})")
    else:
        thread["status"] = f"partial_{posted}"
        save_threads(threads)
        print(f"\nThread #{index} partially posted ({posted}/{thread['thread_length']})")


def cmd_help():
    """Print usage."""
    print("ISRAEL/ONE Thread Generator")
    print("Em nome do Senhor Jesus Cristo, nosso Salvador")
    print()
    print("Usage:")
    print(f"  python3 {Path(__file__).name} generate       Pick best tweet, generate thread")
    print(f"  python3 {Path(__file__).name} list            List all generated threads")
    print(f"  python3 {Path(__file__).name} preview INDEX   Preview thread by ID")
    print(f"  python3 {Path(__file__).name} post INDEX      Post thread via tweet_now.py")
    print()
    print("Sources:")
    print(f"  {QUEUED_TWEETS_PATH}")
    print(f"  {OPENCLLAW_TWEETS_PATH}")
    print()
    print("Output:")
    print(f"  {THREADS_OUTPUT_PATH}")


# ─── MAIN ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "generate":
        cmd_generate()
    elif command == "list":
        cmd_list()
    elif command == "preview":
        if len(sys.argv) < 3:
            print("Usage: preview INDEX")
            sys.exit(1)
        try:
            idx = int(sys.argv[2])
        except ValueError:
            print("INDEX must be a number")
            sys.exit(1)
        cmd_preview(idx)
    elif command == "post":
        if len(sys.argv) < 3:
            print("Usage: post INDEX")
            sys.exit(1)
        try:
            idx = int(sys.argv[2])
        except ValueError:
            print("INDEX must be a number")
            sys.exit(1)
        cmd_post(idx)
    elif command in ("help", "--help", "-h"):
        cmd_help()
    else:
        print(f"Unknown command: {command}")
        cmd_help()
        sys.exit(1)
