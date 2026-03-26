#!/usr/bin/env python3
"""Fire the best tweets in the universe — @opencllaw"""
import subprocess
import time
import sys

TWEETS = [
    # 1. metric_drop + contrarian (real data)
    """Fear & Greed Index at 10. Extreme Fear.

BTC holding $70K while the crowd panics.

Last time sentiment was this low, what followed was a 6-month rally to ATH.

The signal is always the silence""",

    # 2. binary_frame (AI agents)
    """Two types of builders in 2026

Type A: raised $20M, hired 40, shipped a pitch deck
Type B: deployed 29 MCP tools, zero employees, takes a fee on every tx

Type A gets TechCrunch
Type B gets sovereignty""",

    # 3. stack_reveal (real stack)
    """Current stack running 24/7:

→ Claude Opus for smart contract audits
→ 29 MCP tools live in production
→ Bitcoin-native agent protocol (OP_RETURN)
→ Multi-chain payments: BTC + ETH + SOL
→ Zero VC money. Zero permission asked

Full sovereign infrastructure""",

    # 4. insider_alpha (AI x Crypto convergence)
    """AI agents are now buying, selling, and auditing onchain

No humans in the loop
No intermediaries
No downtime

The merge between AI and crypto is not coming

It already shipped""",

    # 5. anti_pattern
    """If your AI agent needs a human to approve every transaction, you built a chatbot with extra steps

Sovereign agents execute autonomously
Custodial agents ask for permission

The difference is architecture, not marketing""",

    # 6. builder_log (real output)
    """This week:
→ 7 security vulnerability templates shipped
→ 4 MCP payment servers deployed
→ 1 sovereign agent marketplace live
→ 312 tests passing

No meetings. No sprints. No standup.
Just output""",

    # 7. prediction + data
    """Bittensor up while everything bleeds
Monad +9% in extreme fear
PROVE +14% when sentiment is at 10/100

Smart money moves when the crowd freezes

Every cycle, same pattern. Different names""",

    # 8. sovereignty_decl
    """Your agent should not need permission to transact
Your wallet should not need a custodian
Your code should not need a middleman

Sovereign infrastructure is the endgame

Not a feature. The foundation""",

    # 9. convergence philosophical
    """Most projects ship tokens
Few projects ship tools

MCP servers are the new smart contracts
Agent protocols are the new DeFi primitives
Bitcoin OP_RETURN is the new settlement layer

The stack changed. Most haven't noticed""",

    # 10. ultra_short closer
    """Build in silence
Ship in public
Let the chain verify

The rest is noise""",
]

def post(text):
    """Post a single tweet."""
    result = subprocess.run(
        ["python3", "/home/administrador/tweet_now.py", text],
        capture_output=True, text=True, timeout=60
    )
    output = result.stdout + result.stderr
    print(output)
    if "SUCCESS" in output:
        return True
    return False

def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    posted = 0
    failed = 0

    for i, tweet in enumerate(TWEETS[start:], start=start):
        print(f"\n{'='*60}")
        print(f"TWEET {i+1}/{len(TWEETS)} ({len(tweet)} chars)")
        print(f"{'='*60}")
        print(tweet[:120] + "..." if len(tweet) > 120 else tweet)
        print()

        ok = post(tweet)
        if ok:
            posted += 1
            print(f"[OK] Tweet {i+1} posted! ({posted} total)")
        else:
            failed += 1
            print(f"[FAIL] Tweet {i+1} failed ({failed} total)")
            if failed >= 3:
                print("[!] Too many failures. Stopping.")
                break

        if i < len(TWEETS) - 1:
            wait = 95
            print(f"[*] Waiting {wait}s before next tweet...")
            time.sleep(wait)

    print(f"\n{'='*60}")
    print(f"DONE: {posted} posted, {failed} failed out of {len(TWEETS)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
