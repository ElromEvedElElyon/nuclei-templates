#!/usr/bin/env python3
"""
Grok Free Engine — Uses Grok WITHOUT API key
Generates viral content for @opencllaw via grok.com web interface
Zero cost. Zero API key. Full Grok 4 access.
"""
import sys
import json
import os
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/grok-api-free"))

def ask_grok(prompt: str, model: str = "grok-3-auto") -> str:
    """Ask Grok a question without any API key"""
    try:
        from core import Grok
        result = Grok(model).start_convo(prompt, extra_data=None)
        if isinstance(result, dict) and "response" in result:
            return result["response"]
        return str(result)
    except Exception as e:
        return f"ERROR: {e}"

def generate_viral_tweet(topic: str) -> str:
    """Generate a viral tweet using Grok for free"""
    prompt = f"""Generate a single viral tweet about: {topic}

Rules:
- Maximum 280 characters
- Zero emojis, zero hashtags
- Builder/hacker voice, direct and technical
- Include a strong opinion or data point
- Make it provocative enough to get replies (replies = 13.5x engagement)
- English language
- No quotes around the tweet

Just output the tweet text, nothing else."""

    return ask_grok(prompt)

def generate_thread(topic: str, tweets: int = 5) -> list:
    """Generate a viral thread using Grok"""
    prompt = f"""Generate a Twitter/X thread about: {topic}

Rules:
- {tweets} tweets total
- Tweet 1: Hook (max 10 words, grab attention)
- Tweet 2-{tweets-1}: Data + insights + strong opinions
- Tweet {tweets}: Call to action or powerful conclusion
- Each tweet max 280 characters
- Zero emojis, zero hashtags
- Builder/hacker authority voice
- Separate each tweet with ---

Output only the tweets separated by ---, nothing else."""

    response = ask_grok(prompt)
    return [t.strip() for t in response.split("---") if t.strip()]

def search_x_trends(topic: str) -> str:
    """Use Grok to search X/Twitter trends (Grok has native X access)"""
    prompt = f"""Search X/Twitter for the latest trending discussions about: {topic}

What are people saying? What's getting the most engagement?
Give me 5 key insights from current X discussions about this topic.
Include specific usernames or tweets if possible."""

    return ask_grok(prompt)

def generate_batch_tweets(count: int = 10) -> list:
    """Generate a batch of diverse viral tweets"""
    pillars = [
        "MCP servers and AI agent infrastructure",
        "Bitcoin self-custody and sovereignty",
        "DeFi alpha and concentrated liquidity",
        "Open source as competitive moat",
        "AI agents replacing SaaS",
        "Smart contract security and auditing",
        "Crypto market data and fear/greed analysis",
        "Building in public with zero funding",
        "MCP tools for autonomous AI agents",
        "The convergence of AI and crypto"
    ]

    tweets = []
    for i in range(min(count, len(pillars))):
        tweet = generate_viral_tweet(pillars[i])
        if tweet and not tweet.startswith("ERROR"):
            tweets.append({
                "text": tweet,
                "pillar": pillars[i].replace(" ", "_").lower()[:30],
                "created": datetime.now().strftime("%Y-%m-%d"),
                "source": "grok_free_engine"
            })
            print(f"[{i+1}/{count}] Generated: {tweet[:60]}...")

    return tweets

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Grok Free Engine")
    parser.add_argument("action", choices=["tweet", "thread", "trends", "batch", "ask"],
                       help="Action to perform")
    parser.add_argument("--topic", "-t", default="AI agents and MCP tools",
                       help="Topic for content generation")
    parser.add_argument("--count", "-c", type=int, default=5,
                       help="Number of items to generate")
    parser.add_argument("--model", "-m", default="grok-3-auto",
                       help="Grok model to use")
    parser.add_argument("--save", "-s", action="store_true",
                       help="Save to queued_tweets.json")
    args = parser.parse_args()

    if args.action == "tweet":
        tweet = generate_viral_tweet(args.topic)
        print(f"\n=== VIRAL TWEET ===\n{tweet}\n")

    elif args.action == "thread":
        thread = generate_thread(args.topic, args.count)
        print(f"\n=== THREAD ({len(thread)} tweets) ===")
        for i, t in enumerate(thread, 1):
            print(f"\n[{i}] {t}")

    elif args.action == "trends":
        trends = search_x_trends(args.topic)
        print(f"\n=== X TRENDS ===\n{trends}\n")

    elif args.action == "batch":
        tweets = generate_batch_tweets(args.count)
        print(f"\n=== BATCH ({len(tweets)} tweets) ===")
        for t in tweets:
            print(f"  [{t['pillar']}] {t['text'][:80]}...")

        if args.save and tweets:
            queue_file = os.path.expanduser("~/israel-one/queued_tweets.json")
            existing = []
            if os.path.exists(queue_file):
                with open(queue_file) as f:
                    existing = json.load(f)
            existing.extend(tweets)
            with open(queue_file, "w") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            print(f"\nSaved {len(tweets)} tweets to queue ({len(existing)} total)")

    elif args.action == "ask":
        response = ask_grok(args.topic, args.model)
        print(f"\n=== GROK RESPONSE ===\n{response}\n")
