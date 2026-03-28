#!/usr/bin/env python3
"""
Gemini Free Engine — Google AI Studio API (100% FREE, no credit card)
Unlimited access to Gemini 2.5 Flash with 1M token context
For viral content generation for @opencllaw
"""
import os
import json
import requests
from datetime import datetime

# Google AI Studio API key — get FREE at https://aistudio.google.com/apikey
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def ask_gemini(prompt: str) -> str:
    """Ask Gemini a question — completely free"""
    if not GEMINI_API_KEY:
        return "ERROR: Set GEMINI_API_KEY env var. Get free key at https://aistudio.google.com/apikey"

    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.9,
                    "maxOutputTokens": 1024
                }
            },
            timeout=30
        )
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"ERROR: {e}"

def generate_viral_tweet(topic: str) -> str:
    """Generate viral tweet via Gemini"""
    prompt = f"""Generate ONE viral tweet about: {topic}

Rules:
- Max 280 chars
- Zero emojis, zero hashtags
- Builder/hacker voice, direct, technical
- Strong opinion or surprising data
- Provocative enough to get replies
- English language

Output ONLY the tweet text."""

    return ask_gemini(prompt).strip().strip('"')

def generate_thread(topic: str, count: int = 5) -> list:
    """Generate thread via Gemini"""
    prompt = f"""Write a {count}-tweet thread about: {topic}

Rules:
- Tweet 1: Strong hook (max 10 words)
- Each tweet max 280 chars
- Zero emojis, zero hashtags
- Builder authority voice
- Separate with ---

Output ONLY tweets separated by ---"""

    resp = ask_gemini(prompt)
    return [t.strip().strip('"') for t in resp.split("---") if t.strip()]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gemini Free Engine")
    parser.add_argument("action", choices=["tweet", "thread", "ask"])
    parser.add_argument("--topic", "-t", default="AI agents and MCP")
    parser.add_argument("--count", "-c", type=int, default=5)
    args = parser.parse_args()

    if args.action == "tweet":
        print(generate_viral_tweet(args.topic))
    elif args.action == "thread":
        for i, t in enumerate(generate_thread(args.topic, args.count), 1):
            print(f"[{i}] {t}\n")
    elif args.action == "ask":
        print(ask_gemini(args.topic))
