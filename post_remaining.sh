#!/bin/bash
# Post remaining tweets after tweet 2 lands
# Run this AFTER tweet 2 is confirmed posted
# Each tweet waits 95s between posts

DELAY=95

tweets=(
'Current stack running 24/7:

→ Claude Opus for smart contract audits
→ 29 MCP tools live in production
→ Bitcoin-native agent protocol (OP_RETURN)
→ Multi-chain payments: BTC + ETH + SOL
→ Zero VC money. Zero permission asked

Full sovereign infrastructure'

'AI agents are now buying, selling, and auditing onchain

No humans in the loop
No intermediaries
No downtime

The merge between AI and crypto is not coming

It already shipped'

'If your AI agent needs a human to approve every transaction, you built a chatbot with extra steps

Sovereign agents execute autonomously
Custodial agents ask for permission

The difference is architecture, not marketing'

'This week:
→ 7 security vulnerability templates shipped
→ 4 MCP payment servers deployed
→ 1 sovereign agent marketplace live
→ 312 tests passing

No meetings. No sprints. No standup.
Just output'

'Bittensor up while everything bleeds
Monad +9% in extreme fear
PROVE +14% when sentiment is at 10/100

Smart money moves when the crowd freezes

Every cycle, same pattern. Different names'

'Your agent should not need permission to transact
Your wallet should not need a custodian
Your code should not need a middleman

Sovereign infrastructure is the endgame

Not a feature. The foundation'

'Most projects ship tokens
Few projects ship tools

MCP servers are the new smart contracts
Agent protocols are the new DeFi primitives
Bitcoin OP_RETURN is the new settlement layer

The stack changed. Most have not noticed'

'Build in silence
Ship in public
Let the chain verify

The rest is noise'
)

posted=0
failed=0

for i in "${!tweets[@]}"; do
    num=$((i + 3))
    echo ""
    echo "============================================================"
    echo "TWEET $num/10"
    echo "============================================================"

    python3 ~/tweet_now.py "${tweets[$i]}" 2>&1

    if [ $? -eq 0 ]; then
        posted=$((posted + 1))
        echo "[OK] Tweet $num posted! ($posted total)"
    else
        failed=$((failed + 1))
        echo "[FAIL] Tweet $num failed ($failed total)"
        if [ $failed -ge 3 ]; then
            echo "[!] Too many failures. Stopping."
            break
        fi
    fi

    if [ $i -lt $((${#tweets[@]} - 1)) ]; then
        echo "[*] Waiting ${DELAY}s..."
        sleep $DELAY
    fi
done

echo ""
echo "============================================================"
echo "DONE: $posted posted, $failed failed"
echo "============================================================"
