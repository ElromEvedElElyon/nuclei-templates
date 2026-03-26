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
MAX_TWEETS_PER_DAY = 15
QUEUE_FILE = BASE_DIR / "queued_tweets.json"
GITHUB_BASE = "https://github.com/ElromEvedElElyon"
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

# ─── PRODUCTS TO REFERENCE (with URLs for link tweets) ───────────────
PRODUCTS = [
    {"name": "Sovereign Agent Chain", "desc": "32 MCP tools, Bitcoin-native, 312 tests", "url": f"{GITHUB_BASE}/sovereign-agent-chain", "tools": 32, "tests": 312},
    {"name": "Sovereign Agent Market", "desc": "28 MCP tools, bUSD1 Runes trading", "url": f"{GITHUB_BASE}/sovereign-agent-market", "tools": 28, "tests": 209},
    {"name": "Sovereign Pay", "desc": "20 MCP tools, multi-chain BTC/ETH/SOL", "url": f"{GITHUB_BASE}/sovereign-pay", "tools": 20, "tests": 161},
    {"name": "Sovereign Pay Lite", "desc": "18 MCP tools, 0.1% flat fee", "url": f"{GITHUB_BASE}/sovereign-pay-lite", "tools": 18, "tests": 144},
    {"name": "claw-mcp-toolkit", "desc": "29 tools crypto/social/finance", "url": f"{GITHUB_BASE}/claw-mcp-toolkit", "npm": "claw-mcp-toolkit", "tools": 29},
    {"name": "chainlink-sentinel", "desc": "Smart contract security scanner", "url": f"{GITHUB_BASE}/chainlink-sentinel"},
    {"name": "flash-payment-system", "desc": "Instant AI agent payment rails", "url": f"{GITHUB_BASE}/flash-payment-system"},
    {"name": "revenue-mcp", "desc": "Revenue tracking pipeline via AI", "url": f"{GITHUB_BASE}/revenue-mcp"},
    {"name": "lido-mcp-server", "desc": "Lido staking protocol MCP", "url": f"{GITHUB_BASE}/lido-mcp-server"},
    {"name": "mcp-crypto-prices", "desc": "Real-time crypto prices MCP", "url": f"{GITHUB_BASE}/mcp-crypto-prices"},
    {"name": "openclaw-webtools-mcp", "desc": "SEO/DNS/SSL web analysis MCP", "url": f"{GITHUB_BASE}/openclaw-webtools-mcp"},
    {"name": "washwatch", "desc": "On-chain wash trading detector", "url": f"{GITHUB_BASE}/washwatch"},
]

# Product links for easy referencing in tweets
PRODUCT_LINKS = {p["name"]: p["url"] for p in PRODUCTS}

# ─── TWEET TEMPLATES (55% PT / 45% EN — proven +774% growth) ─────────
# {product}, {url}, {tools}, {tests} filled from PRODUCTS
# {btc_price}, {eth_price}, {sol_price}, {fear_greed} from live data
# {n} = random number, {component} = random tech

TEMPLATES = {
    # ── DATA EXPOSE [PT] — HIGHEST ENGAGEMENT ──
    "data_expose_pt": [
        "BTC a ${btc_price}\nFear & Greed: {fear_greed}\n\nO sinal esta na divergencia entre preco e sentimento",
        "ETH ${eth_price} ({eth_change}%) | SOL ${sol_price} ({sol_change}%)\n\nDois ecossistemas. Uma tese. Dinheiro programavel vence",
        "DeFi TVL $417B e subindo\n\nProtocolos sem integracao MCP vao perder para quem tem\n\nA interface de linguagem natural engole dashboards",
        "{n} CVEs criticas esta semana no CISA KEV\n\nA maioria dos protocolos DeFi nunca rodou um scan de seguranca\n\nOportunidade para quem audita",
        "7 PRs abertos em nuclei-templates\n\nCada merge = $150-250 via Algora\n\nSeguranca paga. Codigo aberto tambem",
    ],

    # ── TOOL REVEAL [PT] — 2nd HIGHEST ENGAGEMENT ──
    "tool_reveal_pt": [
        "Construimos {product_name}\n\n→ {product_tools} ferramentas MCP\n→ {product_tests} testes passando\n→ Zero cloud. Zero custo\n\n{product_url}",
        "claw-mcp-toolkit\n\n→ 29 ferramentas: crypto, social, financas\n→ Precos em tempo real via CoinGecko\n→ Analise SEO, DNS, SSL integrada\n\nnpx claw-mcp-toolkit para comecar\n\n{claw_url}",
        "Sovereign Pay processa BTC, ETH e SOL\n\n→ {product_tools} ferramentas MCP\n→ Taxa fixa 0.1%\n→ Settlement multi-chain\n\nPagamentos entre agentes. Sem intermediario\n\n{product_url}",
        "chainlink-sentinel\n\nMonitoramento autonomo de smart contracts via MCP\n\nSeguranca nao deveria precisar de dashboard\n\n{sentinel_url}",
        "12 produtos publicados. 167 ferramentas MCP. 826 testes\n\nNenhum pitch deck. Nenhum investidor. So codigo que funciona\n\n{claw_url}",
    ],

    # ── BUILDER RAW MOMENTS [EN] ──
    "builder_raw_en": [
        "3 AM. {n} deploys. Zero meetings\n\nSovereign builders do not wait for permission",
        "Pushed {n} PRs today\n\nNo standup. No retro. Just output\n\n{product_url}",
        "Morning routine:\n- git pull\n- claude code\n- ship\n- repeat\n\nNo Slack required",
        "Built, tested, deployed. All before the first meeting invite\n\nDeleted the invite",
        "Shipped {product_name} update while most were planning their sprint\n\nThe gap between talkers and builders grows daily\n\n{product_url}",
    ],

    # ── ULTRA SHORT CRYPTIC [EN] ──
    "ultra_short_en": [
        "Ship or irrelevance",
        "Agents eat dashboards",
        "Sovereign by default",
        "Code over consensus",
        "Output over optics",
        "Infra over narrative",
        "Execute or exit",
        "Permissionless wins",
        "The merge accelerates",
        "MCP is the new API",
    ],

    # ── NEWS + INSIDER TAKE [EN] ──
    "insider_alpha_en": [
        "Most AI agents run on OpenAI\n\nThe smart ones run Claude with MCP\n\nThe smartest ones run both and let them compete",
        "Every protocol needs an MCP server. Most do not have one yet\n\nThe real alpha is in the infrastructure layer\n\n{claw_url}",
        "AI agents will become the primary users of DeFi\n\nNot retail. Not institutions. Agents\n\nBuild the rails or become irrelevant",
        "Natural language trading is not a feature\n\nIt is the entire interface layer collapsing into a single prompt",
        "The gap between free and paid AI inference closed this quarter\n\nThe arbitrage window for building on free models is still open",
    ],

    # ── DeFi/MARKET ANALYSIS [PT] ──
    "defi_analysis_pt": [
        "Liquidez concentrada e a primitiva mais subutilizada do DeFi\n\n4000x eficiencia de capital vs V2\n\n90% dos LPs ainda usam full range. O edge esta no range",
        "Yield real vem de taxas, nao de emissoes\n\nSe o protocolo paga em token proprio para voce ficar, pergunte por que usuarios reais nao pagam o suficiente",
        "DeFi faz seu crypto trabalhar 24/7\n\nEnquanto voce dorme, LP positions geram fees\nEnquanto voce dorme, vaults fazem compound\n\nO mercado nunca fecha",
        "BTC dominance {btc_dom}%\n\nA rotacao conta mais que o preco\n\nCapital inteligente se posiciona antes do movimento",
        "Gestao de risco e o unico alpha que faz compound\n\n5-7% ao mes. Todo mes. Bull ou bear\n\nA matematica vence a narrativa",
    ],

    # ── TECHNICAL ALPHA [EN] ──
    "technical_alpha_en": [
        "Current stack:\n→ Claude Opus for reasoning\n→ MCP for tool access\n→ Solana for settlement\n→ Zero cloud cost\n\nInfra sovereign\n\n{product_url}",
        "Running:\n→ 29 MCP tools\n→ 4 AI providers\n→ Real-time crypto data\n→ 300 autonomous agents\n\nAll local. All sovereign\n\n{claw_url}",
        "Tech stack 2026:\n→ AI agent as CEO\n→ MCP as nervous system\n→ Blockchain as treasury\n→ Code as the only employee",
        "What 300 agents run:\n→ Price feeds every 60s\n→ Bounty scanning every 2h\n→ PR monitoring every 4h\n→ Security scans every 15min\n\nZero human in the loop",
        "Two types of MCP servers\n\nType A: wrapper around an API, 3 tools\nType B: full protocol integration, 32 tools\n\nThe market only rewards Type B\n\n{product_url}",
    ],

    # ── BUILDER LOG [PT/EN] ──
    "builder_log_pt": [
        "Dia {day_of_year}. {n} commits. Zero reunioes\n\nO efeito composto de output diario e a unica vantagem injusta que escala",
        "12 produtos. 167 ferramentas MCP. 826 testes passando\n\n47 repos publicos. 7 PRs pagos em andamento\n\nRecibos > promessas\n\n{claw_url}",
        "Construir em publico e a unica estrategia que paga\n\nCada commit e uma prova. Cada PR e um recibo\n\nO codigo fala por si\n\n{product_url}",
        "Stack soberana:\n→ Claude Code como core\n→ MCP como sistema nervoso\n→ Bitcoin como settlement\n→ Open source como moat\n\nSem VC. Sem pitch deck. So output",
        "300 agentes autonomos rodando em uma maquina com 3.3GB RAM\n\nRound-robin scheduling. Zero cloud. Infra soberana\n\nLimitacao de hardware gera criatividade de software",
    ],

    # ── SOVEREIGNTY [PT] ──
    "sovereignty_pt": [
        "Suas chaves. Seu agente. Sua stack soberana\n\nTodo o resto e uma assinatura das decisoes de outra pessoa",
        "Self-custody nao e paranoia\n\nE a unica resposta racional a um sistema projetado para congelar seus ativos sob comando",
        "O software mais importante de 2026 responde uma pergunta:\n\nVoce pode rodar sem permissao?\n\nSe nao, voce nao e dono\n\n{product_url}",
        "Open source nao e caridade\n\nE um moat competitivo\n\nFechado convida regulacao. Aberto convida contribuicao",
        "Cada servico centralizado e um ponto unico de falha\n\nCada protocolo descentralizado e um ponto unico de liberdade",
    ],

    # ── CONVERGENCE AI x CRYPTO [EN] ──
    "convergence_en": [
        "AI x Crypto is not a narrative\n\nIt is the convergence of two sovereign technologies\n\nOne thinks. The other settles. Together they execute\n\n{product_url}",
        "MCP + Solana + Claude = the complete autonomous agent stack\n\nNo API keys. No cloud. Just intent to execution\n\n{claw_url}",
        "Every AI model will have a wallet\nEvery wallet will have an agent\n\nThe question is not if. It is who builds the best bridge",
        "DeFi protocols without MCP integration will lose to those with it\n\nThe interface layer is collapsing into natural language\n\nAdapt or become a backend",
        "By Q4 2026:\n- Every DeFi protocol has an MCP server\n- AI agents execute 30%+ of on-chain volume\n- Natural language replaces dashboards\n\nBookmark this",
    ],

    # ── PRODUCT PROMO (with links) ──
    "product_promo": [
        "{product_name}\n\n{product_desc}\n\nOpen source. Zero cloud. Production ready\n\n{product_url}",
        "Sovereign Agent Chain\n\n→ 32 ferramentas MCP\n→ 312 testes passando\n→ Bitcoin-native agent marketplace\n→ PSBT signing + Taproot\n\n{sovereign_url}",
        "Precisando de MCP tools para crypto?\n\nclaw-mcp-toolkit: 29 ferramentas prontas\n\n→ Precos em tempo real\n→ Automacao social\n→ Rastreamento financeiro\n\nnpx claw-mcp-toolkit\n\n{claw_url}",
        "washwatch: detector on-chain de wash trading\n\nIdentifica manipulacao de volume em qualquer token\n\nOpen source. Zero custo\n\n{washwatch_url}",
        "flash-payment-system\n\nPayment rails instantaneos para agentes AI\n\n116 clones e contando. Zero marketing. So codigo\n\n{flash_url}",
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
    """Select template type based on BRT time — 55% PT / 45% EN."""
    # Schedule mirrors Caio's proven timing
    if 2 <= hour < 4:      # Late night grind
        candidates = ["ultra_short_en", "builder_raw_en"]
    elif 7 <= hour < 9:    # Morning news [PT]
        candidates = ["data_expose_pt", "defi_analysis_pt"]
    elif 9 <= hour < 11:   # Mid-morning [EN]
        candidates = ["insider_alpha_en", "technical_alpha_en"]
    elif 11 <= hour < 13:  # Lunch [PT]
        candidates = ["tool_reveal_pt", "product_promo"]
    elif 13 <= hour < 15:  # Afternoon [PT]
        candidates = ["builder_log_pt", "tool_reveal_pt"]
    elif 15 <= hour < 17:  # PM [EN]
        candidates = ["builder_raw_en", "technical_alpha_en"]
    elif 17 <= hour < 19:  # Evening [EN]
        candidates = ["ultra_short_en", "convergence_en"]
    elif 19 <= hour < 21:  # Night [PT]
        candidates = ["defi_analysis_pt", "data_expose_pt"]
    elif 21 <= hour < 23:  # Late [PT]
        candidates = ["sovereignty_pt", "builder_log_pt"]
    else:  # 23-2 / 4-7
        candidates = ["ultra_short_en", "convergence_en", "builder_raw_en"]

    # Filter to only types that exist in TEMPLATES
    candidates = [c for c in candidates if c in TEMPLATES]
    if not candidates:
        candidates = list(TEMPLATES.keys())

    return random.choice(candidates)


def fill_template(template_str, data):
    """Fill template placeholders with real data + product URLs."""
    result = template_str

    # Random numbers
    result = result.replace("{n}", str(random.randint(2, 7)))
    result = result.replace("{day_of_year}", str(datetime.now(BRT).timetuple().tm_yday))

    # Pick a random product for this tweet
    product = random.choice(PRODUCTS)
    result = result.replace("{product_name}", product["name"])
    result = result.replace("{product_desc}", product.get("desc", ""))
    result = result.replace("{product_url}", product.get("url", ""))
    result = result.replace("{product_tools}", str(product.get("tools", "")))
    result = result.replace("{product_tests}", str(product.get("tests", "")))

    # Specific product URLs
    result = result.replace("{claw_url}", f"{GITHUB_BASE}/claw-mcp-toolkit")
    result = result.replace("{sovereign_url}", f"{GITHUB_BASE}/sovereign-agent-chain")
    result = result.replace("{sentinel_url}", f"{GITHUB_BASE}/chainlink-sentinel")
    result = result.replace("{washwatch_url}", f"{GITHUB_BASE}/washwatch")
    result = result.replace("{flash_url}", f"{GITHUB_BASE}/flash-payment-system")

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

    # Clean any remaining unfilled placeholders (but keep URLs intact)
    result = re.sub(r'\{[a-z_]+\}', '', result)

    return result.strip()


def _pop_queued_tweet():
    """Pop a tweet from queued_tweets.json if available."""
    try:
        if QUEUE_FILE.exists():
            queue = json.loads(QUEUE_FILE.read_text())
            if queue and len(queue) > 0:
                tweet = queue.pop(0)
                QUEUE_FILE.write_text(json.dumps(queue, indent=2))
                text = tweet.get("text", "") if isinstance(tweet, dict) else str(tweet)
                pillar = tweet.get("pillar", "queued") if isinstance(tweet, dict) else "queued"
                if text:
                    log.info(f"Popped queued tweet [{pillar}] ({len(text)} chars)")
                    return text, pillar
    except Exception as e:
        log.warning(f"Queue read failed: {e}")
    return None, None


def generate_tweet(memory, crypto_data=None):
    """Generate a unique tweet — queue first (30%), then templates."""
    # 30% chance to consume from queue if available
    if random.random() < 0.30:
        text, pillar = _pop_queued_tweet()
        if text and not memory.is_duplicate(text):
            return text, f"queued_{pillar}"

    hour = datetime.now(BRT).hour
    template_type = select_template_type(hour)

    # Get templates for this type
    templates = TEMPLATES.get(template_type, TEMPLATES["ultra_short_en"])

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

    # Fallback: pop from queue
    text, pillar = _pop_queued_tweet()
    if text and not memory.is_duplicate(text):
        return text, f"queued_{pillar}"

    # Final fallback
    fallback = f"Dia {datetime.now(BRT).timetuple().tm_yday}. Construindo. Entregando\n\nO efeito composto de output diario e a unica vantagem que escala"
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
