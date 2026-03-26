#!/usr/bin/env python3
"""
ISRAEL/ONE — Autonomous X Agent for @opencllaw
Em nome do Senhor Jesus Cristo, nosso Salvador.
Style: builder-authority | Engine: twikit + Claude + MCP data
"""

import json, os, sys, time, random, hashlib, logging, re, subprocess, asyncio
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

POSTING_HANDLE = "opencllaw"
TARGET_HANDLE = "0xCVYH"
TWEET_LANGUAGE = "en"
MAX_TWEETS_PER_DAY = 12
MIN_INTERVAL_SEC = 55  # Twitter rate limit safety
BRT = timezone(timedelta(hours=-3))

# ─── LOGGING ──────────────────────────────────────────────────────────
LOG_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "israel.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("israel")

# ─── STYLE DNA (proven +774% impressions) ─────────────────────────────
STYLE_DNA = {
    "voice": "builder-authority",
    "rules": [
        "Lead with product name or entity, never I or questions",
        "Short punchy sentences, fragments OK, under 12 words each",
        "Heavy line breaks, each point on its own line",
        "ZERO emojis, ZERO hashtags, ZERO exclamation marks",
        "No period at the end of the tweet",
        "One ALL-CAPS data point maximum per tweet",
        "Arrow lists (→) for features, dash lists (- ) for data",
        "End with prediction, action statement, or contrarian take",
        "Sound like intelligence briefing, not motivational speaker",
        "Use: ship, sovereign, permissionless, agent, execute, infra, stack",
        "Never: excited, thrilled, LFG, WAGMI, disrupting, partnership without code"
    ],
    "vocabulary": [
        "ship", "sovereign", "permissionless", "agent", "execute", "infra",
        "stack", "deploy", "vault", "protocol", "rails", "primitive",
        "composable", "trustless", "on-chain", "self-custody", "alpha",
        "convergence", "merge", "build", "output", "pipeline"
    ]
}

# ─── CONTENT PILLARS ──────────────────────────────────────────────────
PILLARS = [
    "ai_agent_alpha",
    "crypto_ai_convergence",
    "builder_ethos",
    "sovereignty",
    "open_source",
    "defi_alpha",
    "mcp_tools",
    "market_data"
]

# ─── PRODUCTS TO REFERENCE ────────────────────────────────────────────
PRODUCTS = [
    ("ClawChat", "PWA AI assistant, 4 providers racing, zero cost"),
    ("claw-mcp-toolkit", "29 tools for crypto, social, finance via Claude"),
    ("chainlink-sentinel", "Autonomous security scanner for smart contracts"),
    ("revenue-mcp", "Revenue tracking and pipeline management via AI"),
    ("SintexOS", "Web-based AI operating system with 8 apps"),
    ("OpenClaw", "AI agent that runs on your machine, connects WhatsApp/Telegram/Discord"),
    ("Solana Vault Standard", "ERC-4626 on Solana, streaming yield, open source"),
    ("flash-payment-system", "Instant crypto payment rails for AI agents"),
    ("Sovereign Agent Chain", "32 MCP tools, Bitcoin-native agent marketplace, 312 tests"),
    ("Sovereign Pay", "20 MCP tools, multi-chain BTC/ETH/SOL, protocol fees, 161 tests"),
    ("Sovereign Pay Lite", "18 MCP tools, multi-chain BTC/ETH/SOL, 0.1% flat fee, 144 tests"),
]

# ─── 50+ TWEET TEMPLATES ─────────────────────────────────────────────
# Each template is a function that returns tweet text
# {data} placeholders filled with real MCP data when available

TEMPLATES = {
    # ── BUILDER LOG (daily updates) ──
    "builder_log": [
        "{n} deploys before lunch. Zero meetings. The build continues",
        "Pushed {n} PRs today\n\nNo standup. No retro. Just output",
        "Monday: 0 meetings\nTuesday: 0 meetings\nWednesday: shipped\n\nThe pattern holds",
        "Refactored the entire {component} pipeline in one session\n\nClaude did the heavy lifting. I did the thinking",
        "3 AM deploy. No one asked. No one approved\n\nSovereign builders do not wait for permission",
        "Shipped {product} update while most were planning their sprint\n\nThe gap between talkers and builders grows daily",
        "Morning routine:\n- git pull\n- claude code\n- ship\n- repeat\n\nNo Slack required",
        "Built, tested, deployed. All before the first meeting invite landed\n\nDeleted the invite",
        "Another day of output. No roadmap presentation. No stakeholder sync\n\nJust code that works",
    ],

    # ── STACK REVEAL ──
    "stack_reveal": [
        "Current stack:\n→ Claude Opus for reasoning\n→ MCP for tool access\n→ Solana for settlement\n→ Zero cloud cost\n\nInfra sovereign",
        "Running:\n→ 29 MCP tools\n→ 4 AI providers\n→ Real-time crypto data\n→ Autonomous posting\n\nAll local. All sovereign",
        "The stack that ships:\n→ Claude Code as core\n→ curl_cffi for distribution\n→ CoinGecko for alpha\n→ GitHub for proof\n\nNo middle layer",
        "What my agents run:\n→ Price feeds every 60s\n→ Fear & Greed monitoring\n→ Auto-tweet generation\n→ Engagement tracking\n\nZero human in the loop",
        "Tech stack 2026:\n→ AI agent as CEO\n→ MCP as nervous system\n→ Blockchain as treasury\n→ Code as the only employee",
    ],

    # ── BINARY FRAME ──
    "binary_frame": [
        "Two kinds of builders in 2026\n\nType A: meetings, roadmaps, quarterly reviews\nType B: ships daily, iterates hourly, sleeps optional\n\nType A gets funding. Type B gets users",
        "Two kinds of AI companies\n\nOnes that sell seats\nOnes that deploy agents\n\nThe second kind will eat the first",
        "Two paths for crypto in 2026\n\nPath A: regulated, custodial, KYC everything\nPath B: permissionless, self-custody, agent-native\n\nBoth will exist. Only one matters",
        "Two types of MCP servers\n\nType A: wrapper around an API, 3 tools\nType B: full protocol integration, {n}+ tools\n\nThe market only rewards Type B",
        "Developers vs builders\n\nDevelopers write code for tickets\nBuilders write code because they cannot stop\n\nThe difference is visible in the commit history",
    ],

    # ── METRIC DROP ──
    "metric_drop": [
        "BTC at ${btc_price}\nFear & Greed: {fear_greed}\n\nThe signal is in the divergence",
        "{trending_coin} up {pct}% in 24h\n\nMost will buy the top. Few positioned before the move",
        "Market cap: ${total_mcap}\nBTC dominance: {btc_dom}%\n\nThe rotation tells you more than the price",
        "ETH at ${eth_price}\nSOL at ${sol_price}\n\nTwo ecosystems. One thesis. Programmable money wins",
        "{n} MCP servers deployed this week\n\nThe agent economy is not coming. It is here",
    ],

    # ── INSIDER ALPHA ──
    "insider_alpha": [
        "Most AI agents run on OpenAI\n\nThe smart ones run Claude with MCP\n\nThe smartest ones run both and let them compete",
        "The real alpha is not in the token\n\nIt is in the infrastructure layer beneath it\n\nEvery protocol needs an MCP server. Most do not have one yet",
        "AI agents will become the primary users of DeFi\n\nNot retail. Not institutions. Agents\n\nBuild the rails or become irrelevant",
        "Natural language trading is not a feature\n\nIt is the entire interface layer collapsing into a single prompt\n\nEvery CEX dashboard becomes obsolete",
        "The gap between free and paid AI inference closed this quarter\n\nThe arbitrage window for building on free models is still open\n\nNot for long",
        "Concentrated liquidity changed the game\n\n4000x capital efficiency vs V2\n\nBut 90% of LPs still use full-range. The edge is in the range",
    ],

    # ── SOVEREIGNTY ──
    "sovereignty": [
        "Your keys. Your agent. Your sovereign stack\n\nEverything else is a subscription to someone else's decisions",
        "Self-custody is not paranoia\n\nIt is the only rational response to a system designed to freeze your assets on command",
        "Every centralized service is a single point of failure\n\nEvery decentralized protocol is a single point of freedom\n\nChoose accordingly",
        "The most important feature of any software in 2026:\n\nCan you run it without permission?\n\nIf no, you do not own it",
        "Open source is not charity\n\nIt is a competitive moat\n\nClosedness invites regulation. Openness invites contribution",
    ],

    # ── CONVERGENCE (AI x Crypto) ──
    "convergence": [
        "The merge accelerates",
        "AI x Crypto is not a narrative\n\nIt is the convergence of two sovereign technologies\n\nOne thinks. The other settles. Together they execute",
        "MCP + Solana + Claude = the complete autonomous agent stack\n\nNo API keys to manage. No cloud to maintain. Just intent to execution",
        "DeFi protocols without MCP integration will lose to those with it\n\nThe interface layer is collapsing into natural language\n\nAdapt or become a backend",
        "Every AI model will have a wallet\n\nEvery wallet will have an agent\n\nThe question is not if. It is who builds the best bridge",
    ],

    # ── PREDICTION / RECEIPTS ──
    "prediction": [
        "6 months ago: MCP tools are a niche experiment\nToday: 269 stars on a single MCP server\n\nReceipts matter more than predictions",
        "By Q4 2026:\n- Every DeFi protocol has an MCP server\n- AI agents execute 30%+ of on-chain volume\n- Natural language replaces every trading dashboard\n\nBookmark this",
        "The playbook is simple:\n\n1. Build in public\n2. Ship daily\n3. Let the code speak\n\nEverything else is noise",
    ],

    # ── ANTI-PATTERN ──
    "anti_pattern": [
        "If your AI agent needs permission to think, it is not an agent\n\nIt is a chatbot with extra steps",
        "Raising capital to build an AI wrapper is the 2026 version of raising capital to build a website in 1999\n\nThe smart money builds infrastructure",
        "If you need a meeting to decide what to build next, the market has already moved\n\nShip first. Discuss later",
        "The biggest risk in crypto is not volatility\n\nIt is building something no one asked for\n\nListen to the chain. Read the transactions. The users tell you everything",
    ],

    # ── TWO WORD GRENADE ──
    "two_word": [
        "Ship or irrelevance",
        "The merge accelerates",
        "Agents eat dashboards",
        "Build. Ship. Repeat",
        "Sovereign by default",
        "Code over consensus",
        "Output over optics",
        "Infra over narrative",
        "Execute or exit",
        "Permissionless wins",
    ],

    # ── MCP TOOLS ──
    "mcp_tools": [
        "29 tools running under one MCP server\n\nCrypto prices. Social automation. Finance tracking\n\nOne install. Zero cloud. Complete autonomy",
        "MCP servers are the nervous system of autonomous AI\n\nEvery tool an agent needs in one protocol\n\nBuild the server. Let the agents decide what to call",
        "Most AI tools still require manual setup\n\nMCP tools auto-discover. Auto-connect. Auto-execute\n\nThe difference between a chatbot and an agent",
        "Shipped chainlink-sentinel as MCP server\n\nReal-time smart contract monitoring via natural language\n\nSecurity scanning should not require a dashboard",
        "The MCP economy is invisible but growing\n\nEvery tool becomes composable. Every agent becomes capable\n\nInfra wins quietly",
    ],

    # ── DeFi ALPHA ──
    "defi_alpha": [
        "Concentrated liquidity is the most underutilized primitive in DeFi\n\n4000x capital efficiency. Yet 90% of LPs still use full range\n\nThe edge is in the range management",
        "Stablecoin yield is the gateway\n\nStart with DAI-USDC. Zero impermanent loss. Learn the mechanics\n\nThen graduate to volatile pairs with real conviction",
        "The yield comes from fees, not emissions\n\nIf a protocol pays you in its own token to stay, ask why real users are not paying enough\n\nReal yield > printed yield",
        "DeFi makes your crypto work 24/7\n\nWhile you sleep, your LP positions earn fees\nWhile you sleep, your vaults compound\n\nThe market never closes",
        "Risk management is the only alpha that compounds\n\n5-7% per month. Every month. Bull or bear\n\nThe math beats the narrative every time",
    ],
}


# ─── DATA ENRICHMENT (via subprocess MCP calls) ──────────────────────
def get_crypto_data():
    """Fetch real-time crypto data for tweet enrichment."""
    data = {}
    try:
        # BTC price
        result = subprocess.run(
            ["python3", "-c", """
import urllib.request, json
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "IsraelOne/1.0"})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())
print(json.dumps(d))
"""],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            prices = json.loads(result.stdout.strip())
            data["btc_price"] = f"{prices['bitcoin']['usd']:,.0f}"
            data["eth_price"] = f"{prices['ethereum']['usd']:,.0f}"
            data["sol_price"] = f"{prices['solana']['usd']:,.2f}"
            data["btc_change"] = f"{prices['bitcoin'].get('usd_24h_change', 0):.1f}"
            data["eth_change"] = f"{prices['ethereum'].get('usd_24h_change', 0):.1f}"
            data["sol_change"] = f"{prices['solana'].get('usd_24h_change', 0):.1f}"
            btc_mcap = prices['bitcoin'].get('usd_market_cap', 0)
            data["total_mcap"] = f"{btc_mcap/1e12:.2f}T" if btc_mcap > 1e12 else f"{btc_mcap/1e9:.0f}B"
            log.info(f"Crypto data: BTC=${data['btc_price']} ETH=${data['eth_price']} SOL=${data['sol_price']}")
    except Exception as e:
        log.warning(f"Crypto data fetch failed: {e}")

    try:
        # Fear & Greed
        result = subprocess.run(
            ["python3", "-c", """
import urllib.request, json
url = "https://api.alternative.me/fng/?limit=1"
req = urllib.request.Request(url, headers={"User-Agent": "IsraelOne/1.0"})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())
print(json.dumps(d['data'][0]))
"""],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            fng = json.loads(result.stdout.strip())
            data["fear_greed"] = f"{fng['value']} ({fng['value_classification']})"
            log.info(f"Fear & Greed: {data['fear_greed']}")
    except Exception as e:
        log.warning(f"Fear & Greed fetch failed: {e}")

    return data


def get_trending_coins():
    """Fetch trending coins for content."""
    try:
        result = subprocess.run(
            ["python3", "-c", """
import urllib.request, json
url = "https://api.coingecko.com/api/v3/search/trending"
req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "IsraelOne/1.0"})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())
coins = []
for item in d.get('coins', [])[:5]:
    c = item['item']
    coins.append({"name": c['name'], "symbol": c['symbol'], "rank": c.get('market_cap_rank', '?')})
print(json.dumps(coins))
"""],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
    except Exception as e:
        log.warning(f"Trending fetch failed: {e}")
    return []


# ─── MEMORY SYSTEM ────────────────────────────────────────────────────
class IsraelMemory:
    def __init__(self):
        self.path = DATA_DIR / "israel_memory.json"
        self.data = self._load()

    def _load(self):
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {
            "posted_hashes": [],
            "posted_tweets": [],
            "daily_counts": {},
            "templates_used": {},
            "best_performing": [],
            "total_posted": 0,
            "created": datetime.now(BRT).isoformat()
        }

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False))

    def is_duplicate(self, text):
        h = hashlib.md5(text.encode()).hexdigest()[:12]
        return h in self.data["posted_hashes"]

    def record_post(self, text, template_type, method="twikit"):
        h = hashlib.md5(text.encode()).hexdigest()[:12]
        self.data["posted_hashes"].append(h)
        # Keep only last 500 hashes
        self.data["posted_hashes"] = self.data["posted_hashes"][-500:]

        today = datetime.now(BRT).strftime("%Y-%m-%d")
        self.data["daily_counts"][today] = self.data["daily_counts"].get(today, 0) + 1
        self.data["total_posted"] = self.data.get("total_posted", 0) + 1

        # Track template usage for variety
        self.data["templates_used"][template_type] = self.data["templates_used"].get(template_type, 0) + 1

        self.data["posted_tweets"].append({
            "text": text[:100] + "..." if len(text) > 100 else text,
            "hash": h,
            "template": template_type,
            "method": method,
            "timestamp": datetime.now(BRT).isoformat()
        })
        # Keep only last 200 posts
        self.data["posted_tweets"] = self.data["posted_tweets"][-200:]
        self.save()

    def today_count(self):
        today = datetime.now(BRT).strftime("%Y-%m-%d")
        return self.data["daily_counts"].get(today, 0)

    def least_used_template_type(self):
        """Return the template type used least for variety."""
        all_types = list(TEMPLATES.keys())
        usage = {t: self.data["templates_used"].get(t, 0) for t in all_types}
        return min(usage, key=usage.get)


# ─── TWEET GENERATION ─────────────────────────────────────────────────
def select_template_type(hour):
    """Select template type based on BRT time and variety."""
    if 7 <= hour < 9:
        candidates = ["metric_drop", "insider_alpha", "defi_alpha"]
    elif 9 <= hour < 11:
        candidates = ["builder_log", "stack_reveal", "mcp_tools"]
    elif 11 <= hour < 13:
        candidates = ["insider_alpha", "defi_alpha", "convergence"]
    elif 13 <= hour < 15:
        candidates = ["binary_frame", "builder_log", "anti_pattern"]
    elif 15 <= hour < 17:
        candidates = ["builder_log", "stack_reveal", "prediction"]
    elif 17 <= hour < 19:
        candidates = ["convergence", "defi_alpha", "sovereignty"]
    elif 19 <= hour < 21:
        candidates = ["insider_alpha", "prediction", "sovereignty"]
    elif 21 <= hour < 23:
        candidates = ["sovereignty", "convergence", "two_word"]
    else:  # 23-7 (night/early morning)
        candidates = ["two_word", "convergence", "builder_log"]

    # Filter to only types that exist in TEMPLATES
    candidates = [c for c in candidates if c in TEMPLATES]
    if not candidates:
        candidates = list(TEMPLATES.keys())

    return random.choice(candidates)


def fill_template(template_str, data):
    """Fill template placeholders with real data."""
    result = template_str

    # Random numbers
    result = result.replace("{n}", str(random.randint(2, 7)))

    # Products
    if "{product}" in result:
        product = random.choice(PRODUCTS)
        result = result.replace("{product}", product[0])

    if "{component}" in result:
        components = ["auth", "payment", "indexer", "vault", "bridge", "oracle"]
        result = result.replace("{component}", random.choice(components))

    # Crypto data
    if data:
        for key, value in data.items():
            result = result.replace("{" + key + "}", str(value))

    # Trending coin
    if "{trending_coin}" in result:
        result = result.replace("{trending_coin}", "SOL")
    if "{pct}" in result:
        result = result.replace("{pct}", str(random.randint(5, 25)))
    if "{btc_dom}" in result:
        result = result.replace("{btc_dom}", str(random.randint(48, 58)))

    # Clean any remaining unfilled placeholders
    result = re.sub(r'\{[a-z_]+\}', '', result)

    return result.strip()


def generate_tweet(memory, crypto_data=None):
    """Generate a unique tweet using templates + data enrichment."""
    hour = datetime.now(BRT).hour
    template_type = select_template_type(hour)

    # Get templates for this type
    templates = TEMPLATES.get(template_type, TEMPLATES["two_word"])

    # Try up to 10 times to find a non-duplicate
    for attempt in range(10):
        template = random.choice(templates)
        text = fill_template(template, crypto_data or {})

        # Enforce character limit
        if len(text) > 280:
            text = text[:277] + "..."

        # Remove trailing period (style rule)
        text = text.rstrip(".")

        # Remove any emojis (safety check)
        text = re.sub(r'[\U0001F600-\U0001F9FF\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F\U0001FA00-\U0001FAFF]', '', text)

        if not memory.is_duplicate(text):
            log.info(f"Generated [{template_type}] ({len(text)} chars): {text[:60]}...")
            return text, template_type

        log.debug(f"Duplicate on attempt {attempt+1}, retrying...")

    # Fallback: generate timestamp-unique tweet
    fallback = f"Day {datetime.now(BRT).timetuple().tm_yday}. Still shipping. Still building\n\nThe compound effect of daily output is the only unfair advantage that scales"
    log.warning("All templates exhausted. Using fallback")
    return fallback, "fallback"


# ─── POSTING VIA TWEET_NOW.PY (curl_cffi — proven working) ───────────
def post_via_script(text):
    """Post tweet via tweet_now.py (curl_cffi Chrome TLS fingerprint). The ONLY method that works."""
    try:
        script = os.path.expanduser("~/tweet_now.py")
        if not os.path.exists(script):
            log.warning("tweet_now.py not found")
            return False

        result = subprocess.run(
            ["python3", script, text],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and "SUCCESS" in result.stdout:
            log.info("Tweet posted via tweet_now.py")
            return True
        else:
            log.error(f"tweet_now.py failed: {result.stdout[:200]} {result.stderr[:200]}")
            return False
    except Exception as e:
        log.error(f"Script posting failed: {e}")
        return False


# ─── MAIN AGENT LOOP ─────────────────────────────────────────────────
def run_single_cycle():
    """Execute one posting cycle."""
    memory = IsraelMemory()

    # Check daily limit
    if memory.today_count() >= MAX_TWEETS_PER_DAY:
        log.info(f"Daily limit reached ({memory.today_count()}/{MAX_TWEETS_PER_DAY})")
        return False

    # Fetch real-time data for enrichment
    crypto_data = get_crypto_data()

    # Generate tweet
    text, template_type = generate_tweet(memory, crypto_data)

    if not text:
        log.error("Failed to generate tweet")
        return False

    log.info(f"Posting: {text}")

    # Post via tweet_now.py (the ONLY method that works)
    success = post_via_script(text)

    if success:
        memory.record_post(text, template_type, "tweet_now")
        log.info(f"Posted successfully. Today: {memory.today_count()}/{MAX_TWEETS_PER_DAY}")
        return True
    else:
        log.error("Posting failed")
        return False


def run_sentinel(min_interval=60, max_interval=120):
    """Run as continuous sentinel, posting every 60-120 minutes (randomized)."""
    log.info("=" * 60)
    log.info("ISRAEL/ONE Agent Starting — SENTINEL MODE")
    log.info(f"Posting as: @{POSTING_HANDLE}")
    log.info(f"Style: {STYLE_DNA['voice']}")
    log.info(f"Max tweets/day: {MAX_TWEETS_PER_DAY}")
    log.info(f"Interval: {min_interval}-{max_interval} minutes (randomized)")
    log.info("=" * 60)

    while True:
        try:
            run_single_cycle()
        except Exception as e:
            log.error(f"Cycle error: {e}")

        # Randomized sleep between min and max interval
        sleep_sec = random.randint(min_interval * 60, max_interval * 60)
        log.info(f"Next cycle in {sleep_sec//60} minutes")
        time.sleep(sleep_sec)


def run_once():
    """Post a single tweet and exit."""
    return run_single_cycle()


# ─── CLI ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("sentinel", "daemon"):
        min_int = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        max_int = int(sys.argv[3]) if len(sys.argv) > 3 else 120
        run_sentinel(min_int, max_int)
    elif len(sys.argv) > 1 and sys.argv[1] == "preview":
        # Preview mode: generate but don't post
        crypto_data = get_crypto_data()
        memory = IsraelMemory()
        for i in range(5):
            text, ttype = generate_tweet(memory, crypto_data)
            print(f"\n[{ttype}] ({len(text)} chars):")
            print(text)
            print("-" * 40)
            # Temporarily add hash to avoid showing same one
            h = hashlib.md5(text.encode()).hexdigest()[:12]
            memory.data["posted_hashes"].append(h)
    elif len(sys.argv) > 1 and sys.argv[1] == "stats":
        memory = IsraelMemory()
        print(f"\nTotal posted: {memory.data.get('total_posted', 0)}")
        print(f"Today: {memory.today_count()}/{MAX_TWEETS_PER_DAY}")
        print(f"\nTemplate usage:")
        for t, c in sorted(memory.data.get("templates_used", {}).items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print(f"\nLast 5 posts:")
        for p in memory.data.get("posted_tweets", [])[-5:]:
            print(f"  [{p.get('template', '?')}] {p.get('text', '')}")
    else:
        # Single post
        result = run_once()
        sys.exit(0 if result else 1)
