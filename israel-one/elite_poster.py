#!/usr/bin/env python3
"""
ELITE POSTER — Posts tweets following @0xCVYH Style DNA exactly.
Em nome do Senhor Jesus Cristo, nosso Salvador.

Usage:
    python3 elite_poster.py post          # Post next tweet from queue
    python3 elite_poster.py preview       # Preview next tweet
    python3 elite_poster.py schedule      # Show what to post when
    python3 elite_poster.py validate TEXT  # Check if tweet follows rules
    python3 elite_poster.py generate      # Generate new tweets with real data

RULES (from elite_tweet_rules.md):
    - ZERO emojis, hashtags, exclamation marks
    - NEVER "follow me for more"
    - Lead with product/data, never "I"
    - Short punchy lines, fragments OK
    - End with prediction or contrarian take
    - Max 5-8 tweets/day, prefer singles over threads
"""

import json
import sys
import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
QUEUE_FILE = "/tmp/elite_tweets_queue.json"
PRODUCT_QUEUE = "/tmp/product_tweets_queue.txt"
POSTED_LOG = Path.home() / ".zion" / "posted_tweets.json"
RULES_FILE = Path.home() / "israel-one" / "elite_tweet_rules.md"

# Banned patterns — instant rejection
BANNED = [
    r'[^\w\s]*([\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0000FE0F])',  # emojis
    r'#\w+',  # hashtags
    r'!',  # exclamation marks
    r'(?i)follow.*for.*alpha',
    r'(?i)follow.*for.*more',
    r'(?i)follow @opencllaw',
    r'(?i)breaking this down',
    r'(?i)is not a random data point',
    r'(?i)the noise is temporary',
    r'(?i)excited to announce',
    r'(?i)we.re thrilled',
    r'(?i)\bLFG\b',
    r'(?i)\bWAGMI\b',
    r'(?i)disrupting',
    r'(?i)game.changing',
]


def validate_tweet(text):
    """Returns (is_valid, list_of_violations)"""
    violations = []

    for pattern in BANNED:
        if re.search(pattern, text):
            violations.append(f"BANNED: matches '{pattern}'")

    if len(text) > 500:
        violations.append(f"TOO LONG: {len(text)} chars (max 500 for single tweet)")

    if text.strip().startswith(("I ", "I'm", "I've")):
        violations.append("STYLE: starts with 'I' — lead with product/data instead")

    # Check for good signals
    good_words = ['ship', 'sovereign', 'agent', 'execute', 'open source',
                  'builder', 'stack', 'deploy', 'infra', 'permissionless']
    has_good = any(w in text.lower() for w in good_words)
    if not has_good:
        violations.append("WARNING: no on-brand vocabulary detected")

    return len(violations) == 0, violations


def get_time_slot():
    """Return current time slot for posting"""
    now = datetime.now(BRT)
    hour = now.hour
    if 2 <= hour < 4:
        return "2-4 AM"
    elif 7 <= hour < 9:
        return "7-9 AM"
    elif 11 <= hour < 13:
        return "11 AM-1 PM"
    elif 15 <= hour < 17:
        return "3-5 PM"
    elif 21 <= hour < 23:
        return "9-11 PM"
    else:
        return "off-peak"


def load_queue():
    """Load tweet queue"""
    tweets = []
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE) as f:
            data = json.load(f)
            tweets = data.get('tweets', []) if isinstance(data, dict) else data
    return tweets


def preview_next():
    """Preview the next tweet to post"""
    slot = get_time_slot()
    tweets = load_queue()

    print(f"Current time slot: {slot}")
    print(f"Tweets in queue: {len(tweets)}")
    print()

    # Find matching tweet for current slot
    for t in tweets:
        if isinstance(t, dict) and t.get('time_slot') == slot:
            print(f"NEXT TWEET ({t.get('type', '?')}):")
            print("-" * 40)
            print(t.get('tweet', ''))
            print("-" * 40)
            valid, violations = validate_tweet(t.get('tweet', ''))
            if valid:
                print("VALIDATION: PASSED")
            else:
                print("VALIDATION: FAILED")
                for v in violations:
                    print(f"  - {v}")
            return

    # No match for current slot, show next available
    if tweets:
        t = tweets[0]
        print(f"No tweet for current slot. Next available ({t.get('type', '?')}):")
        print("-" * 40)
        print(t.get('tweet', ''))
        print("-" * 40)


def schedule():
    """Show posting schedule"""
    tweets = load_queue()
    slots = {}
    for t in tweets:
        if isinstance(t, dict):
            slot = t.get('time_slot', 'unscheduled')
            if slot not in slots:
                slots[slot] = []
            slots[slot].append(t)

    print("POSTING SCHEDULE")
    print("=" * 50)
    for slot in ["2-4 AM", "7-9 AM", "11 AM-1 PM", "3-5 PM", "9-11 PM"]:
        items = slots.get(slot, [])
        print(f"\n{slot} BRT:")
        if items:
            for t in items:
                tweet_text = t.get('tweet', '')[:60]
                print(f"  [{t.get('type', '?')}] {tweet_text}...")
        else:
            print("  (empty)")


def validate_cmd(text):
    """Validate a tweet from command line"""
    valid, violations = validate_tweet(text)
    if valid:
        print("PASSED — Tweet follows elite rules")
    else:
        print("FAILED — Violations found:")
        for v in violations:
            print(f"  - {v}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 elite_poster.py [preview|schedule|validate TEXT]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "preview":
        preview_next()
    elif cmd == "schedule":
        schedule()
    elif cmd == "validate":
        text = " ".join(sys.argv[2:])
        validate_cmd(text)
    else:
        print(f"Unknown command: {cmd}")
        print("Available: preview, schedule, validate")
