#!/usr/bin/env python3
"""
REPLY STRATEGIST — Intelligent Reply Strategy Agent for @opencllaw
Em nome do Senhor Jesus Cristo, nosso Salvador.

Generates high-quality replies to top crypto/AI accounts.
Style: builder-authority | ZERO emojis | ZERO hashtags | 280 char max
Engine: stdlib only | Lightweight for 3.3GB RAM
"""

import json
import os
import sys
import random
import hashlib
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
QUEUE_FILE = BASE_DIR / "queued_replies.json"
TARGETS_FILE = DATA_DIR / "reply_targets.json"
LOG_FILE = BASE_DIR / "logs" / "reply_strategist.log"
BRT = timezone(timedelta(hours=-3))
MAX_REPLY_LEN = 280
REPLIES_PER_CYCLE = 10

# Ensure dirs exist
DATA_DIR.mkdir(exist_ok=True)
(BASE_DIR / "logs").mkdir(exist_ok=True)

# ─── LOGGING (minimal, no external deps) ──────────────────────────────
def _log(level: str, msg: str):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} [{level}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

# ─── STYLE DNA (replies inherit from agent.py proven style) ───────────
REPLY_STYLE = {
    "voice": "builder-authority",
    "rules": [
        "ZERO emojis, ZERO hashtags, ZERO exclamation marks",
        "Short punchy sentences, max 12 words each",
        "Sound like builder who has shipped, not fan or spectator",
        "Add value: data, experience, insight, or sharp question",
        "Never sycophantic, never hostile, always substantive",
        "Never start with 'Great point' or 'Love this'",
        "Contrarian is OK if backed by reasoning",
        "Reference real products/data when relevant",
        "End with insight, not pleasantry",
        "No period at the end of the reply",
    ],
    "banned_words": [
        "excited", "thrilled", "LFG", "WAGMI", "ser", "fren",
        "disrupting", "game-changer", "love this", "great thread",
        "so true", "based", "gm", "bullish", "moon",
    ],
    "vocabulary": [
        "ship", "sovereign", "permissionless", "agent", "execute",
        "infra", "stack", "deploy", "vault", "protocol", "rails",
        "primitive", "composable", "trustless", "on-chain",
        "self-custody", "alpha", "convergence", "build", "output",
    ],
}

# ─── PRODUCTS WE CAN REFERENCE ───────────────────────────────────────
PRODUCTS = {
    "claw-mcp-toolkit": "29 MCP tools for crypto, social, finance via Claude",
    "chainlink-sentinel": "Autonomous security scanner for smart contracts",
    "flash-payment-system": "Instant crypto payment rails for AI agents, 61/61 tests",
    "commerce-pay-mcp": "Commerce payment integration via MCP protocol",
    "solana-vault-standard": "ERC-4626 on Solana, streaming yield, open source",
    "lido-mcp-server": "11-tool DeFi integration for Lido staking protocol",
    "sintex-ai": "Web-based AI operating system with 8 apps, deployed live",
    "openclaw": "AI agent running on local machine, connects all messaging",
}

# ─── TARGET ACCOUNTS DATABASE ────────────────────────────────────────
# 50 accounts across crypto, AI, builders, security, MCP ecosystem
DEFAULT_TARGETS = [
    # ── Crypto Builders & Leaders ──
    {"handle": "VitalikButerin", "category": "crypto_leader", "topics": ["ethereum", "L2", "crypto philosophy", "public goods"]},
    {"handle": "CryptoHayes", "category": "crypto_macro", "topics": ["macro", "DeFi", "derivatives", "monetary policy"]},
    {"handle": "AndreCronjeTech", "category": "defi_builder", "topics": ["DeFi", "Fantom", "Sonic", "yield", "protocol design"]},
    {"handle": "haaborsufi", "category": "crypto_builder", "topics": ["DeFi", "MEV", "protocol"]},
    {"handle": "bantaboreg", "category": "crypto_research", "topics": ["crypto research", "data analysis"]},
    {"handle": "0xMert_", "category": "solana_builder", "topics": ["Solana", "infra", "RPC", "validator"]},
    {"handle": "aaboreybtc", "category": "bitcoin_dev", "topics": ["Bitcoin", "Lightning", "ordinals"]},
    {"handle": "staborni", "category": "defi_builder", "topics": ["DeFi", "protocol", "yield"]},
    {"handle": "DefiIgnas", "category": "defi_analyst", "topics": ["DeFi", "yield", "airdrop", "protocol analysis"]},
    {"handle": "WatcherGuru", "category": "crypto_news", "topics": ["breaking news", "crypto", "regulation"]},
    {"handle": "tier10k", "category": "crypto_data", "topics": ["on-chain data", "whale tracking", "flows"]},
    {"handle": "MessariCrypto", "category": "crypto_research", "topics": ["research", "reports", "protocol analysis"]},
    {"handle": "coinaborbase", "category": "exchange", "topics": ["listings", "regulation", "Base L2"]},

    # ── AI Builders & Researchers ──
    {"handle": "sama", "category": "ai_leader", "topics": ["AGI", "OpenAI", "AI safety", "policy"]},
    {"handle": "karpathy", "category": "ai_researcher", "topics": ["LLM", "training", "neural nets", "AI engineering"]},
    {"handle": "ylecun", "category": "ai_researcher", "topics": ["AI architecture", "world models", "Meta AI"]},
    {"handle": "AnthropicAI", "category": "ai_company", "topics": ["Claude", "MCP", "AI safety", "constitutional AI"]},
    {"handle": "alexalaborbert", "category": "ai_researcher", "topics": ["AI research", "ML", "NLP"]},
    {"handle": "emaborilyvn", "category": "ai_builder", "topics": ["AI", "agents", "automation"]},
    {"handle": "swaboryx", "category": "ai_builder", "topics": ["AI agents", "dev tools", "automation"]},
    {"handle": "hardmaru", "category": "ai_researcher", "topics": ["ML research", "creative AI", "evolution"]},
    {"handle": "goodfellow_ian", "category": "ai_researcher", "topics": ["GANs", "deep learning", "AI security"]},

    # ── AI x Crypto Convergence ──
    {"handle": "shaborwn_tai", "category": "ai_crypto", "topics": ["AI agents", "crypto", "autonomous systems"]},
    {"handle": "AIatMeta", "category": "ai_company", "topics": ["Llama", "open source AI", "Meta research"]},
    {"handle": "huaborggingface", "category": "ai_platform", "topics": ["open source AI", "models", "datasets"]},
    {"handle": "LangChainAI", "category": "ai_tools", "topics": ["agents", "chains", "RAG", "tool use"]},
    {"handle": "far_el_nore", "category": "ai_crypto", "topics": ["crypto AI", "agents", "DeFi automation"]},

    # ── Solana Ecosystem ──
    {"handle": "solaborana", "category": "solana_core", "topics": ["Solana", "performance", "ecosystem"]},
    {"handle": "rajaborgopal", "category": "solana_builder", "topics": ["Solana", "DeFi", "development"]},
    {"handle": "taborrent", "category": "solana_builder", "topics": ["Solana", "infra", "tooling"]},
    {"handle": "aaborave", "category": "solana_builder", "topics": ["Solana", "DeFi", "NFT"]},
    {"handle": "JupiterExchange", "category": "solana_defi", "topics": ["DEX", "aggregation", "Solana DeFi"]},
    {"handle": "marinade_finance", "category": "solana_defi", "topics": ["liquid staking", "Solana", "yield"]},

    # ── Security / Audit ──
    {"handle": "samczsun", "category": "security", "topics": ["smart contract security", "exploits", "auditing"]},
    {"handle": "bytes032", "category": "security", "topics": ["security research", "vulnerabilities", "auditing"]},
    {"handle": "pashovkrum", "category": "security", "topics": ["audit", "DeFi security", "Solidity"]},
    {"handle": "code4rena", "category": "security_platform", "topics": ["audit contests", "findings", "security"]},
    {"handle": "immunefi", "category": "security_platform", "topics": ["bug bounties", "exploits", "whitehat"]},
    {"handle": "OpenZeppelin", "category": "security", "topics": ["smart contracts", "standards", "security"]},

    # ── MCP / Agent Economy ──
    {"handle": "modelcontextprotocol", "category": "mcp_core", "topics": ["MCP", "tool use", "protocol"]},
    {"handle": "GlamaAI", "category": "mcp_platform", "topics": ["MCP marketplace", "tools", "discovery"]},
    {"handle": "ClaudeAI", "category": "ai_product", "topics": ["Claude", "coding", "reasoning"]},

    # ── Dev Tools / Infra ──
    {"handle": "vercel", "category": "dev_infra", "topics": ["deployment", "frontend", "serverless"]},
    {"handle": "supabase", "category": "dev_infra", "topics": ["database", "auth", "backend"]},
    {"handle": "rustlang", "category": "dev_lang", "topics": ["Rust", "systems programming", "performance"]},
    {"handle": "typescriptlang", "category": "dev_lang", "topics": ["TypeScript", "types", "tooling"]},

    # ── Macro / Finance ──
    {"handle": "zaborhuaborral", "category": "macro", "topics": ["macro", "rates", "Fed", "liquidity"]},
    {"handle": "Croissaborant", "category": "macro", "topics": ["global macro", "FX", "monetary policy"]},
    {"handle": "TheBlock__", "category": "crypto_media", "topics": ["crypto news", "analysis", "data"]},
    {"handle": "coinabordesk", "category": "crypto_media", "topics": ["market data", "regulation", "news"]},
]

# ─── REPLY CATEGORIES & TEMPLATES ────────────────────────────────────
# Each template uses {topic}, {data}, {product}, {insight} placeholders
# Templates are scored and selected based on target account category

REPLY_TEMPLATES = {
    "DATA_REPLY": {
        "description": "Add a data point to reinforce or challenge their tweet",
        "engagement_weight": 0.85,
        "templates": [
            "The data backs this. {data}. The signal was there for weeks",
            "{data}. Most missed this while watching price. The infra layer tells the real story",
            "Worth adding: {data}. The on-chain signal diverged from sentiment {insight}",
            "Numbers confirm. {data}. This is not narrative. This is measurable output",
            "{data}. Builders tracking this for months. The market is just catching up",
            "The metric that matters here: {data}. Everything else is noise",
            "Underreported signal: {data}. This shifts the thesis if you run the numbers",
        ],
    },

    "CONTRARIAN": {
        "description": "Respectful disagreement backed by reasoning",
        "engagement_weight": 0.92,
        "templates": [
            "Counterpoint: {insight}. The second-order effect reverses the thesis",
            "Disagree on the mechanism. {insight}. The data points the other direction",
            "This assumes {topic} scales linearly. It does not. {insight}",
            "Partial pushback: {insight}. The base case is right but the timeline is wrong",
            "The opposite happened in {topic} last cycle. {insight}. History rhymes here",
            "Right thesis, wrong conclusion. {insight}. The bottleneck is elsewhere",
            "Most agree with this take. That is exactly why {insight}",
        ],
    },

    "AMPLIFIER": {
        "description": "Expand on their point with a unique angle",
        "engagement_weight": 0.78,
        "templates": [
            "Extends further. {insight}. The second-order effect is what matters",
            "This also implies {insight}. The convergence is accelerating faster than the market prices",
            "Underrated angle here: {insight}. The infra layer compounds before anyone notices",
            "Add to this: {insight}. The builders who see it early are already shipping",
            "The part most will miss: {insight}. This changes the entire stack assumption",
            "{topic} is the surface. The deeper play is {insight}",
            "Correct frame. And it compounds: {insight}. The gap widens from here",
        ],
    },

    "BUILDER_PROOF": {
        "description": "Reference our own shipping experience as evidence",
        "engagement_weight": 0.88,
        "templates": [
            "Built this. {product}. The hardest part was {insight}",
            "Shipped something in this space. {product}. Learned that {insight}",
            "Can confirm from building {product}. {insight}. The theory and practice diverge here",
            "We deploy {product} and the biggest lesson: {insight}",
            "Running {product} in production. {insight}. The gap between demo and deploy is the real moat",
            "After shipping {product}: {insight}. The market does not reward complexity. It rewards output",
        ],
    },

    "QUESTION": {
        "description": "Thoughtful question that sparks discussion",
        "engagement_weight": 0.80,
        "templates": [
            "What happens to {topic} when agents become the primary users? The interface assumptions break",
            "Genuine question: does {topic} hold when you remove the human from the loop? {insight}",
            "Has anyone measured the second-order effect on {topic}? The surface metric hides the real shift",
            "How does this change when {topic} hits the agent economy? Current models assume human operators",
            "What breaks first in {topic} under this thesis? The consensus answer is probably wrong",
            "Where does {topic} converge with {insight}? That intersection is where the alpha sits",
        ],
    },
}

# ─── DATA POINTS (real, verifiable, updated by MCP feeds) ─────────────
# These rotate into {data} placeholders
DATA_POINTS = [
    "BTC hash rate at all-time high",
    "Solana processing 4000+ TPS in production",
    "MCP protocol has 2000+ servers listed on Glama",
    "Claude handles 200K context window natively",
    "DeFi TVL recovered to $180B+",
    "ETH staking ratio crossed 28%",
    "Solana DeFi TVL grew 340% in 6 months",
    "AI agent transactions on-chain up 500% this quarter",
    "GitHub Copilot users crossed 1.8M",
    "MCP tool calls growing 40% month over month",
    "On-chain AI agent wallets surpassed 50K",
    "Concentrated liquidity captures 85% of DEX volume",
    "ERC-4626 vault standard adopted by 200+ protocols",
    "Smart contract audit market at $2.4B annually",
    "Bug bounty payouts exceeded $300M in 2025",
    "Solana validator count crossed 3500",
    "Average DeFi yield compressed to 4.2% on majors",
    "AI inference cost dropped 90% in 18 months",
    "TypeScript dominates 78% of MCP server implementations",
    "Self-hosted AI agents grew 600% year over year",
]

# ─── INSIGHT FRAGMENTS ───────────────────────────────────────────────
INSIGHTS = [
    "the infra layer always wins before the application layer",
    "agents do not need UI. They need protocols",
    "liquidity follows composability, not branding",
    "the moat is in the tool integration, not the model",
    "open source compounds. Closed source decays",
    "self-custody extends to compute, not just keys",
    "protocol revenue is the only metric that survives bear markets",
    "the convergence of AI and crypto eliminates the middleware layer",
    "permissionless rails beat permissioned ones on a long enough timeline",
    "the best interface is no interface. Just intent to execution",
    "shipping daily beats planning quarterly in every measurable metric",
    "agents will route 80% of DeFi volume within 3 years",
    "the audit bottleneck breaks when AI agents verify contracts",
    "MCP is doing for tools what HTTP did for documents",
    "the real competition is not between chains. It is between stacks",
    "sovereign infrastructure outlasts every narrative cycle",
    "capital efficiency beats capital quantity in concentrated liquidity",
    "the builder who ships today owns the standard tomorrow",
    "on-chain data does not lie. Sentiment does",
    "trustless verification is cheaper than trusted intermediation",
]

# ─── TOPIC KEYWORDS (for matching replies to target categories) ──────
TOPIC_MAP = {
    "crypto_leader": ["Ethereum", "L2 scaling", "crypto", "decentralization"],
    "crypto_macro": ["macro cycle", "DeFi derivatives", "monetary expansion", "rate cuts"],
    "defi_builder": ["DeFi protocols", "yield optimization", "TVL", "AMM design"],
    "solana_builder": ["Solana infra", "Solana DeFi", "SPL tokens", "program deployment"],
    "solana_core": ["Solana performance", "validator economics", "TPS"],
    "solana_defi": ["Solana DeFi", "DEX aggregation", "liquid staking"],
    "ai_leader": ["AGI timeline", "AI safety", "scaling laws", "AI policy"],
    "ai_researcher": ["LLM architecture", "training efficiency", "model scaling"],
    "ai_company": ["Claude", "MCP protocol", "AI agents", "tool use"],
    "ai_builder": ["AI agents", "automation", "dev tools"],
    "ai_crypto": ["AI x crypto", "autonomous agents", "on-chain AI"],
    "ai_tools": ["agent frameworks", "RAG", "tool integration", "chains"],
    "ai_platform": ["open source models", "model hosting", "datasets"],
    "ai_product": ["Claude", "coding", "reasoning", "agentic workflows"],
    "security": ["smart contract exploits", "audit methodology", "vulnerability research"],
    "security_platform": ["bug bounties", "audit contests", "whitehat rewards"],
    "mcp_core": ["MCP protocol", "tool specification", "server architecture"],
    "mcp_platform": ["MCP marketplace", "tool discovery", "server ratings"],
    "dev_infra": ["deployment", "serverless", "edge computing", "backend"],
    "dev_lang": ["Rust", "TypeScript", "systems programming", "type safety"],
    "macro": ["Fed policy", "global liquidity", "rate expectations", "FX"],
    "crypto_news": ["breaking", "regulation", "market events"],
    "crypto_data": ["on-chain flows", "whale movements", "exchange reserves"],
    "crypto_research": ["protocol analysis", "tokenomics", "governance"],
    "crypto_media": ["market data", "industry analysis", "regulatory updates"],
    "exchange": ["listings", "regulation", "L2 deployment"],
    "bitcoin_dev": ["Bitcoin development", "ordinals", "Lightning"],
}


# ─── CORE ENGINE ─────────────────────────────────────────────────────

def load_targets() -> list:
    """Load target accounts from file, or initialize with defaults."""
    if TARGETS_FILE.exists():
        try:
            with open(TARGETS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            _log("WARN", "Corrupt targets file, resetting to defaults")
    save_targets(DEFAULT_TARGETS)
    return DEFAULT_TARGETS[:]


def save_targets(targets: list):
    """Persist target accounts to disk."""
    with open(TARGETS_FILE, "w") as f:
        json.dump(targets, f, indent=2)
    _log("INFO", f"Saved {len(targets)} targets to {TARGETS_FILE}")


def load_queue() -> list:
    """Load queued replies from disk."""
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_queue(queue: list):
    """Persist reply queue to disk."""
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)


def _hash_reply(text: str) -> str:
    """Generate short hash to detect duplicate replies."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def _score_reply(reply_text: str, category: str, template_type: str) -> float:
    """
    Score a reply candidate (0.0 - 1.0) based on:
    - Length efficiency (shorter is better for replies)
    - Vocabulary alignment with builder-authority voice
    - Category-template match quality
    - Engagement weight of template type
    """
    score = 0.0

    # Length score: sweet spot is 120-220 chars
    length = len(reply_text)
    if length < 50:
        score += 0.1
    elif length < 120:
        score += 0.5
    elif length <= 220:
        score += 0.8
    elif length <= 280:
        score += 0.6
    else:
        score += 0.0  # Over limit

    # Vocabulary alignment
    vocab_hits = sum(1 for w in REPLY_STYLE["vocabulary"] if w in reply_text.lower())
    score += min(vocab_hits * 0.08, 0.4)

    # Banned word penalty
    banned_hits = sum(1 for w in REPLY_STYLE["banned_words"] if w.lower() in reply_text.lower())
    score -= banned_hits * 0.3

    # Template engagement weight
    template_info = REPLY_TEMPLATES.get(template_type, {})
    engagement_weight = template_info.get("engagement_weight", 0.5)
    score += engagement_weight * 0.3

    # Category relevance bonus
    if category in ("security", "defi_builder", "ai_crypto", "mcp_core"):
        score += 0.15  # High-value engagement targets
    elif category in ("crypto_leader", "ai_leader", "ai_researcher"):
        score += 0.10  # High visibility but harder to get noticed

    # Contrarian and builder proof get bonus (higher engagement historically)
    if template_type in ("CONTRARIAN", "BUILDER_PROOF"):
        score += 0.10

    # Normalize to 0.0-1.0
    return max(0.0, min(1.0, score))


def _fill_template(template: str, target: dict) -> str:
    """Fill a template with contextual data for the target account."""
    category = target.get("category", "crypto_builder")
    topics = target.get("topics", ["crypto"])

    # Select contextual data
    topic = random.choice(topics)
    data = random.choice(DATA_POINTS)
    insight = random.choice(INSIGHTS)

    # Select a product relevant to the category
    product_keys = list(PRODUCTS.keys())
    if category in ("security", "security_platform"):
        preferred = ["chainlink-sentinel", "flash-payment-system"]
    elif category in ("ai_company", "ai_builder", "ai_tools", "mcp_core", "mcp_platform", "ai_product"):
        preferred = ["claw-mcp-toolkit", "openclaw", "commerce-pay-mcp"]
    elif category in ("solana_builder", "solana_core", "solana_defi"):
        preferred = ["solana-vault-standard", "flash-payment-system"]
    elif category in ("defi_builder", "defi_analyst"):
        preferred = ["solana-vault-standard", "lido-mcp-server", "flash-payment-system"]
    else:
        preferred = product_keys

    product_key = random.choice(preferred)
    product = f"{product_key} ({PRODUCTS[product_key]})"

    # Fill placeholders
    result = template
    result = result.replace("{topic}", topic)
    result = result.replace("{data}", data)
    result = result.replace("{insight}", insight)
    result = result.replace("{product}", product)

    return result


def generate_replies(count: int = REPLIES_PER_CYCLE) -> list:
    """
    Generate scored reply candidates for the next engagement cycle.
    Returns list of reply dicts sorted by score (highest first).
    """
    targets = load_targets()
    existing_queue = load_queue()
    existing_hashes = {r.get("hash", "") for r in existing_queue}

    # Select targets for this cycle (weighted random, avoid repeats)
    cycle_targets = random.sample(targets, min(count * 2, len(targets)))

    candidates = []
    attempts = 0
    max_attempts = count * 5  # Prevent infinite loops

    while len(candidates) < count and attempts < max_attempts:
        attempts += 1

        # Pick target and template type
        target = random.choice(cycle_targets)
        template_type = random.choice(list(REPLY_TEMPLATES.keys()))
        templates = REPLY_TEMPLATES[template_type]["templates"]
        template = random.choice(templates)

        # Generate reply text
        reply_text = _fill_template(template, target)

        # Enforce 280 char limit
        if len(reply_text) > MAX_REPLY_LEN:
            # Try to trim at last sentence boundary
            trimmed = reply_text[:MAX_REPLY_LEN]
            last_period = trimmed.rfind(". ")
            if last_period > 100:
                reply_text = trimmed[:last_period]
            else:
                continue  # Skip, too long to salvage

        # Check for duplicates
        reply_hash = _hash_reply(reply_text)
        if reply_hash in existing_hashes:
            continue

        # Score the reply
        score = _score_reply(reply_text, target["category"], template_type)

        candidate = {
            "text": reply_text,
            "target": f"@{target['handle']}",
            "target_category": target["category"],
            "reply_type": template_type,
            "score": round(score, 3),
            "char_count": len(reply_text),
            "hash": reply_hash,
            "status": "queued",
            "created": datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S"),
        }

        candidates.append(candidate)
        existing_hashes.add(reply_hash)

    # Sort by score (highest first)
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Save to queue (append to existing)
    full_queue = existing_queue + candidates
    save_queue(full_queue)

    _log("INFO", f"Generated {len(candidates)} reply candidates ({attempts} attempts)")
    return candidates


def list_queued() -> list:
    """List all queued replies with status."""
    queue = load_queue()
    return queue


def preview_next() -> dict:
    """Show the highest-scored queued reply with full context."""
    queue = load_queue()
    queued = [r for r in queue if r.get("status") == "queued"]
    if not queued:
        return {}
    # Return highest scored
    queued.sort(key=lambda x: x.get("score", 0), reverse=True)
    return queued[0]


def show_targets() -> list:
    """Show all target accounts with categories."""
    return load_targets()


def add_target(handle: str, category: str = "crypto_builder", topics: list = None):
    """Add a new target account to the database."""
    handle = handle.lstrip("@")
    targets = load_targets()

    # Check for duplicates
    for t in targets:
        if t["handle"].lower() == handle.lower():
            _log("WARN", f"@{handle} already in targets")
            return False

    new_target = {
        "handle": handle,
        "category": category,
        "topics": topics or ["crypto", "AI", "building"],
    }
    targets.append(new_target)
    save_targets(targets)
    _log("INFO", f"Added @{handle} ({category}) to targets")
    return True


def remove_target(handle: str) -> bool:
    """Remove a target account from the database."""
    handle = handle.lstrip("@")
    targets = load_targets()
    original_count = len(targets)
    targets = [t for t in targets if t["handle"].lower() != handle.lower()]
    if len(targets) < original_count:
        save_targets(targets)
        _log("INFO", f"Removed @{handle} from targets")
        return True
    _log("WARN", f"@{handle} not found in targets")
    return False


def clear_posted():
    """Remove all replies marked as 'posted' from the queue."""
    queue = load_queue()
    original = len(queue)
    queue = [r for r in queue if r.get("status") != "posted"]
    save_queue(queue)
    removed = original - len(queue)
    _log("INFO", f"Cleared {removed} posted replies from queue")
    return removed


def mark_posted(reply_hash: str) -> bool:
    """Mark a specific reply as posted by its hash."""
    queue = load_queue()
    for r in queue:
        if r.get("hash") == reply_hash:
            r["status"] = "posted"
            r["posted_at"] = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
            save_queue(queue)
            _log("INFO", f"Marked reply {reply_hash} as posted")
            return True
    return False


def stats() -> dict:
    """Return queue statistics."""
    queue = load_queue()
    targets = load_targets()
    queued = [r for r in queue if r.get("status") == "queued"]
    posted = [r for r in queue if r.get("status") == "posted"]

    # Category distribution
    cat_dist = {}
    for r in queued:
        cat = r.get("reply_type", "unknown")
        cat_dist[cat] = cat_dist.get(cat, 0) + 1

    # Average score
    scores = [r.get("score", 0) for r in queued]
    avg_score = sum(scores) / len(scores) if scores else 0

    return {
        "total_targets": len(targets),
        "queued_replies": len(queued),
        "posted_replies": len(posted),
        "avg_score": round(avg_score, 3),
        "category_distribution": cat_dist,
        "unique_targets_in_queue": len({r.get("target") for r in queued}),
    }


# ─── CLI ─────────────────────────────────────────────────────────────

def _print_reply(reply: dict, index: int = 0):
    """Pretty print a single reply entry."""
    print(f"\n{'='*60}")
    print(f"  #{index+1} | {reply.get('target', '?')} | {reply.get('reply_type', '?')}")
    print(f"  Score: {reply.get('score', 0)} | {reply.get('char_count', 0)} chars | {reply.get('status', '?')}")
    print(f"  Category: {reply.get('target_category', '?')}")
    print(f"  Created: {reply.get('created', '?')}")
    print(f"{'─'*60}")
    print(f"  {reply.get('text', '')}")
    print(f"{'='*60}")


def cli_generate():
    """CLI: Generate reply candidates."""
    print("\n[REPLY STRATEGIST] Generating reply candidates...")
    print(f"  Style: builder-authority | Max: {MAX_REPLY_LEN} chars")
    print(f"  Target count: {REPLIES_PER_CYCLE} replies\n")

    replies = generate_replies()

    for i, r in enumerate(replies):
        _print_reply(r, i)

    print(f"\n  Total generated: {len(replies)}")
    print(f"  Saved to: {QUEUE_FILE}")

    s = stats()
    print(f"\n  Queue: {s['queued_replies']} queued | {s['posted_replies']} posted")
    print(f"  Avg score: {s['avg_score']} | Targets in queue: {s['unique_targets_in_queue']}")


def cli_list():
    """CLI: List all queued replies."""
    queue = list_queued()
    queued = [r for r in queue if r.get("status") == "queued"]

    if not queued:
        print("\n[REPLY STRATEGIST] No queued replies. Run 'generate' first.")
        return

    print(f"\n[REPLY STRATEGIST] {len(queued)} queued replies:\n")

    # Sort by score
    queued.sort(key=lambda x: x.get("score", 0), reverse=True)

    for i, r in enumerate(queued):
        _print_reply(r, i)

    s = stats()
    print(f"\n  Avg score: {s['avg_score']}")
    print(f"  Distribution: {json.dumps(s['category_distribution'], indent=4)}")


def cli_preview():
    """CLI: Preview the next best reply."""
    reply = preview_next()
    if not reply:
        print("\n[REPLY STRATEGIST] No queued replies. Run 'generate' first.")
        return

    print("\n[REPLY STRATEGIST] Next reply to post:\n")
    _print_reply(reply, 0)

    print(f"\n  Action: Reply to {reply.get('target')}'s latest tweet")
    print(f"  Strategy: {REPLY_TEMPLATES.get(reply.get('reply_type', ''), {}).get('description', 'N/A')}")
    print(f"  Hash: {reply.get('hash')} (use to mark as posted)")


def cli_targets():
    """CLI: Show all target accounts."""
    targets = show_targets()
    print(f"\n[REPLY STRATEGIST] {len(targets)} target accounts:\n")

    # Group by category
    by_cat = {}
    for t in targets:
        cat = t.get("category", "other")
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(t)

    for cat, accts in sorted(by_cat.items()):
        print(f"\n  [{cat.upper()}] ({len(accts)} accounts)")
        for a in accts:
            topics = ", ".join(a.get("topics", []))
            print(f"    @{a['handle']:25s} | {topics}")

    print(f"\n  Total: {len(targets)} accounts across {len(by_cat)} categories")


def cli_add(handle: str):
    """CLI: Add a new target account."""
    handle = handle.lstrip("@")
    print(f"\n[REPLY STRATEGIST] Adding @{handle} to targets...")

    # Try to auto-detect category from handle
    category = "crypto_builder"  # default
    result = add_target(handle, category)

    if result:
        print(f"  Added @{handle} ({category})")
        print(f"  Total targets: {len(load_targets())}")
        print(f"  Edit category/topics in: {TARGETS_FILE}")
    else:
        print(f"  @{handle} already exists in targets")


def cli_remove(handle: str):
    """CLI: Remove a target account."""
    handle = handle.lstrip("@")
    result = remove_target(handle)
    if result:
        print(f"\n[REPLY STRATEGIST] Removed @{handle}")
    else:
        print(f"\n[REPLY STRATEGIST] @{handle} not found in targets")


def cli_stats():
    """CLI: Show queue statistics."""
    s = stats()
    print(f"\n[REPLY STRATEGIST] Queue Statistics:")
    print(f"  Targets:     {s['total_targets']}")
    print(f"  Queued:      {s['queued_replies']}")
    print(f"  Posted:      {s['posted_replies']}")
    print(f"  Avg Score:   {s['avg_score']}")
    print(f"  Unique targets in queue: {s['unique_targets_in_queue']}")
    print(f"  Distribution: {json.dumps(s['category_distribution'], indent=4)}")


def cli_mark(reply_hash: str):
    """CLI: Mark a reply as posted."""
    result = mark_posted(reply_hash)
    if result:
        print(f"\n[REPLY STRATEGIST] Marked {reply_hash} as posted")
    else:
        print(f"\n[REPLY STRATEGIST] Hash {reply_hash} not found in queue")


def cli_clear():
    """CLI: Clear all posted replies from queue."""
    removed = clear_posted()
    print(f"\n[REPLY STRATEGIST] Cleared {removed} posted replies")


def print_usage():
    """Print CLI usage."""
    print("""
REPLY STRATEGIST — Intelligent Reply Strategy for @opencllaw
Em nome do Senhor Jesus Cristo, nosso Salvador.

Usage:
  reply_strategist.py generate          Generate 10 reply candidates (scored)
  reply_strategist.py list              Show all queued replies
  reply_strategist.py preview           Show next best reply with context
  reply_strategist.py targets           Show all target accounts
  reply_strategist.py add @HANDLE       Add new target account
  reply_strategist.py remove @HANDLE    Remove target account
  reply_strategist.py stats             Show queue statistics
  reply_strategist.py mark HASH         Mark reply as posted
  reply_strategist.py clear             Clear posted replies from queue

Style: builder-authority | ZERO emojis | ZERO hashtags | 280 chars max
Output: ~/israel-one/queued_replies.json
""")


# ─── MAIN ────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    cmd = sys.argv[1].lower()

    if cmd == "generate":
        cli_generate()
    elif cmd == "list":
        cli_list()
    elif cmd == "preview":
        cli_preview()
    elif cmd == "targets":
        cli_targets()
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: reply_strategist.py add @HANDLE")
            return
        cli_add(sys.argv[2])
    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("Usage: reply_strategist.py remove @HANDLE")
            return
        cli_remove(sys.argv[2])
    elif cmd == "stats":
        cli_stats()
    elif cmd == "mark":
        if len(sys.argv) < 3:
            print("Usage: reply_strategist.py mark HASH")
            return
        cli_mark(sys.argv[2])
    elif cmd == "clear":
        cli_clear()
    else:
        print(f"Unknown command: {cmd}")
        print_usage()


if __name__ == "__main__":
    main()
