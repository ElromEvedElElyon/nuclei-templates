#!/usr/bin/env python3
"""
AGENT ROSTER — Assign 300 Valentes to Task Groups with specializations.
Em nome do Senhor Jesus Cristo, nosso Salvador.

Each valente keeps ALL existing data (name, soul, skills, MCPs, wallets, memory).
We ONLY ADD task_group + specialization fields. NOTHING is deleted.

Usage:
    python3 agent_roster.py assign     # Assign all valentes to groups
    python3 agent_roster.py verify     # Verify assignments
    python3 agent_roster.py status     # Show group distribution
"""

import json
import os
import sys
from pathlib import Path

VALENTES_DIR = Path.home() / ".zion" / "valentes"
AGENTS_DIR = Path.home() / ".zion" / "agents"

# Group definitions with sizes and specializations
GROUPS = {
    "bounty_hunter": {
        "count": 50,
        "interval_min": 120,
        "agents_per_cycle": 3,
        "specializations": [
            {"name": "immunefi", "count": 10, "focus_areas": ["smart_contract", "defi"]},
            {"name": "c4", "count": 10, "focus_areas": ["solidity", "audit"]},
            {"name": "hackenproof", "count": 10, "focus_areas": ["web3", "bridges"]},
            {"name": "algora", "count": 10, "focus_areas": ["typescript", "python", "mcp"]},
            {"name": "nuclei_cves", "count": 10, "focus_areas": ["cve", "web", "network"]},
        ],
    },
    "pr_monitor": {
        "count": 30,
        "interval_min": 240,
        "agents_per_cycle": 2,
        "specializations": [
            {"name": "default", "count": 30, "repos": [
                "projectdiscovery/nuclei-templates",
                "nosana-ci/agent-challenge",
                "1712n/dn-institute",
                "docker/docs",
                "TensorBlock/awesome-mcp-servers",
                "badkk/awesome-crypto-mcp-servers",
                "royyannick/awesome-blockchain-mcps",
                "demcp/awesome-web3-mcp-servers",
                "ravitemer/mcp-registry",
            ]},
        ],
    },
    "revenue_watcher": {
        "count": 20,
        "interval_min": 60,
        "agents_per_cycle": 2,
        "specializations": [
            {"name": "wallet_eth", "count": 4, "chain": "ETH"},
            {"name": "wallet_sol", "count": 4, "chain": "SOL"},
            {"name": "wallet_btc", "count": 4, "chain": "BTC"},
            {"name": "email", "count": 4},
            {"name": "platform", "count": 4, "platform": "immunefi"},
        ],
    },
    "market_intel": {
        "count": 50,
        "interval_min": 120,
        "agents_per_cycle": 3,
        "specializations": [
            {"name": "price", "count": 20, "coins": [
                "bitcoin", "ethereum", "solana", "chainlink", "uniswap",
                "tao-network", "fetch-ai", "render-token", "injective-protocol", "celestia",
                "near", "polkadot", "avalanche-2", "arbitrum", "optimism",
                "polygon-ecosystem-token", "stacks", "sei-network", "sui", "aptos",
            ]},
            {"name": "fear_greed", "count": 10},
            {"name": "defi_tvl", "count": 10},
            {"name": "trending", "count": 10},
        ],
    },
    "tweet_army": {
        "count": 50,
        "interval_min": 180,
        "agents_per_cycle": 2,
        "specializations": [
            {"name": "generate", "count": 35, "pillars": [
                "ai_agent_alpha", "crypto_ai_convergence", "builder_ethos",
                "sovereignty", "market_data", "open_source", "defi_alpha",
            ]},
            {"name": "research", "count": 15},
        ],
    },
    "security_squad": {
        "count": 30,
        "interval_min": 240,
        "agents_per_cycle": 2,
        "specializations": [
            {"name": "ports", "count": 10},
            {"name": "permissions", "count": 10},
            {"name": "processes", "count": 10},
        ],
    },
    "product_evangelist": {
        "count": 40,
        "interval_min": 360,
        "agents_per_cycle": 2,
        "specializations": [
            {"name": "github", "count": 25, "repos": [
                "ElromEvedElElyon/claw-mcp-toolkit",
                "ElromEvedElElyon/chainlink-sentinel",
                "ElromEvedElElyon/flash-payment-system",
                "ElromEvedElElyon/revenue-mcp",
                "ElromEvedElElyon/sovereign-agent-chain",
                "ElromEvedElElyon/sovereign-agent-market",
                "ElromEvedElElyon/sovereign-pay",
                "ElromEvedElElyon/sovereign-pay-lite",
                "ElromEvedElElyon/lido-mcp-server",
                "ElromEvedElElyon/openclaw-webtools-mcp",
                "ElromEvedElElyon/commerce-pay-mcp",
                "ElromEvedElElyon/mcp-crypto-prices",
                "ElromEvedElElyon/washwatch",
            ]},
            {"name": "npm", "count": 15, "packages": [
                "claw-mcp-toolkit",
                "@anthropic-ai/sdk",
            ]},
        ],
    },
    "git_warrior": {
        "count": 30,
        "interval_min": 360,
        "agents_per_cycle": 2,
        "specializations": [
            {"name": "issues", "count": 10, "languages": ["python", "typescript", "solidity", "rust"]},
            {"name": "cves", "count": 10},
            {"name": "nuclei", "count": 10},
        ],
    },
}


def load_valentes():
    """Load all valente JSON files."""
    valentes = []
    if not VALENTES_DIR.exists():
        return valentes
    for f in sorted(VALENTES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            data["_file"] = str(f)
            valentes.append(data)
        except:
            continue
    return valentes


def assign_groups():
    """Assign task groups to valentes. PRESERVES all existing data."""
    valentes = load_valentes()
    if not valentes:
        print("ERROR: No valentes found")
        return

    print(f"Found {len(valentes)} valentes")

    # Sort by name for deterministic assignment
    valentes.sort(key=lambda v: v.get("name", ""))

    idx = 0
    assignments = {}

    for group_name, group_cfg in GROUPS.items():
        spec_idx = 0
        for spec in group_cfg["specializations"]:
            for i in range(spec["count"]):
                if idx >= len(valentes):
                    break

                v = valentes[idx]
                filepath = v.pop("_file")

                # ADD task_group and specialization — NEVER delete existing fields
                v["task_group"] = group_name
                v["specialization"] = {
                    "name": spec["name"],
                }

                # Copy specialization params
                for key in ["focus_areas", "chain", "platform", "repos", "coins",
                            "pillars", "packages", "languages"]:
                    if key in spec:
                        val = spec[key]
                        # For lists, rotate through items for variety
                        if isinstance(val, list) and len(val) > 1:
                            # Each agent gets a different item from the list
                            v["specialization"][key] = val[i % len(val)] if not isinstance(val[0], str) or key in ("coins", "repos", "languages", "pillars") else val
                            if key in ("coins", "repos") and len(val) > spec["count"]:
                                v["specialization"][key] = val[i % len(val)]
                            elif key in ("coins",):
                                v["specialization"]["coin"] = val[i % len(val)]
                            elif key in ("repos",):
                                v["specialization"]["repo"] = val[i % len(val)]
                            elif key in ("languages",):
                                v["specialization"]["language"] = val[i % len(val)]
                            elif key in ("pillars",):
                                v["specialization"]["pillar"] = val[i % len(val)]
                        else:
                            v["specialization"][key] = val

                # Ensure agent has memory dict
                if "memory" not in v:
                    v["memory"] = {}
                v["memory"]["assigned_at"] = __import__("datetime").datetime.now().isoformat()

                # Ensure inviolable/permanent flags (NEVER remove)
                v.setdefault("permanent", True)
                v.setdefault("inviolable", True)
                v.setdefault("never_delete", True)

                # Save back
                with open(filepath, "w") as f:
                    json.dump(v, f, indent=2)

                group_key = f"{group_name}:{spec['name']}"
                assignments.setdefault(group_key, []).append(v.get("name", "?"))
                idx += 1
            spec_idx += 1

    # Summary
    print(f"\nAssigned {idx}/{len(valentes)} valentes to {len(GROUPS)} groups:")
    for group_name, group_cfg in GROUPS.items():
        count = sum(len(v) for k, v in assignments.items() if k.startswith(group_name))
        print(f"  {group_name}: {count}/{group_cfg['count']} agents")
        for spec in group_cfg["specializations"]:
            key = f"{group_name}:{spec['name']}"
            agents = assignments.get(key, [])
            print(f"    {spec['name']}: {len(agents)} agents")

    # Any unassigned?
    if idx < len(valentes):
        remaining = len(valentes) - idx
        print(f"\n  {remaining} valentes unassigned (overflow → bounty_hunter default)")
        # Assign overflow to bounty_hunter
        for v in valentes[idx:]:
            filepath = v.pop("_file")
            v["task_group"] = "bounty_hunter"
            v["specialization"] = {"name": "immunefi", "focus_areas": ["smart_contract", "defi"]}
            v.setdefault("memory", {})
            v.setdefault("permanent", True)
            v.setdefault("inviolable", True)
            v.setdefault("never_delete", True)
            with open(filepath, "w") as f:
                json.dump(v, f, indent=2)

    print(f"\nDONE. All {len(valentes)} valentes assigned. No data deleted.")


def verify():
    """Verify all valentes have task_group assigned."""
    valentes = load_valentes()
    assigned = sum(1 for v in valentes if v.get("task_group"))
    unassigned = [v.get("name", "?") for v in valentes if not v.get("task_group")]
    print(f"Total: {len(valentes)}, Assigned: {assigned}, Unassigned: {len(unassigned)}")
    if unassigned:
        print(f"Unassigned: {', '.join(unassigned[:20])}")


def status():
    """Show group distribution."""
    valentes = load_valentes()
    groups = {}
    for v in valentes:
        g = v.get("task_group", "UNASSIGNED")
        groups.setdefault(g, 0)
        groups[g] += 1

    print("=== VALENTE GROUP DISTRIBUTION ===")
    for g, count in sorted(groups.items()):
        print(f"  {g}: {count}")
    print(f"  TOTAL: {len(valentes)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "assign":
        assign_groups()
    elif cmd == "verify":
        verify()
    elif cmd == "status":
        status()
    else:
        print(f"Usage: {sys.argv[0]} assign|verify|status")
