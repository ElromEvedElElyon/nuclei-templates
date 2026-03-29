#!/usr/bin/env python3
"""
Israel/Nine — BOUNTY SUBMISSION COMMANDER
Em nome do Senhor Jesus Cristo, nosso Salvador

Autonomous agent for finding, analyzing, and submitting bug bounties.
Tracks all platforms, generates reports, and manages submissions.

Run: python3 ~/israel-nine/israel_nine.py warmode
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

SOUL = {
    "name": "Israel/Nine",
    "title": "Bounty Submission Commander",
    "version": "1.0.0",
    "mission": "Find and submit bugs to every bounty platform",
    "scripture": "The diligent hand makes rich — Proverbs 10:4"
}

# ═══════════════════════════════════════════════════
# ACTIVE BOUNTY PLATFORMS
# ═══════════════════════════════════════════════════

PLATFORMS = {
    "immunefi": {
        "url": "https://immunefi.com/bug-bounty/",
        "account": "PadraoBTC736 (VERIFIED)",
        "wallet": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
        "active_report": "#71022 ZKsync OS ($5K-$100K)",
        "targets": {
            "layerzero": {"max": "$15M", "medium": "$10K-$25K", "priority": "HIGH"},
            "chainlink": {"max": "$3M", "medium": "$5K-$25K"},
            "polygon": {"max": "$2M", "medium": "$2K-$10K"},
            "optimism": {"max": "$2M", "medium": "$5K-$20K"},
            "zksync_era": {"max": "$1.1M", "medium": "$5K-$20K"},
            "immutable": {"max": "$1M", "medium": "$5K-$20K"},
            "injective": {"max": "$500K"},
            "stacks": {"max": "$250K"},
        }
    },
    "hackenproof": {
        "url": "https://hackenproof.com/programs",
        "account": "ElromSecurity (ACTIVE)",
        "wallet": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
        "ready_findings": {
            "near_intents": {
                "count": 8,
                "critical": 1,
                "high": 2,
                "medium": 5,
                "total_value": "$164K-$880K",
                "file": "~/near-intents-all-findings-report.md",
                "status": "READY — SUBMIT VIA BROWSER"
            }
        },
        "zero_rep_targets": [
            {"name": "Cetus Protocol", "max": "$300K"},
            {"name": "Layer3", "max": "$500K"},
            {"name": "Backpack", "max": "$20K"},
            {"name": "Coinstore", "max": "$10K"},
            {"name": "BitDelta", "max": "$10K"},
            {"name": "Bluefin", "max": "$10K"},
            {"name": "BTSE", "max": "$5K"},
            {"name": "Chainstack", "max": "$10K"},
        ]
    },
    "code4rena": {
        "url": "https://code4rena.com/audits",
        "account": "ElromAuditor (KYC APPROVED)",
        "wallet": "0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B",
        "note": "Check for new audits daily — C4 takes ZERO CUT now",
        "recent": "Chainlink H-01 submitted, judging"
    },
    "openai_bugcrowd": {
        "url": "https://bugcrowd.com/openai",
        "status": "NOT REGISTERED — NEW PROGRAM Mar 25, 2026!",
        "max_payout": "$100K critical",
        "medium": "$7,500 high-severity",
        "focus": "Agentic AI abuse/safety risks",
        "action": "REGISTER ON BUGCROWD NOW"
    },
    "anthropic_hackerone": {
        "url": "https://www.anthropic.com/news/model-safety-bug-bounty",
        "status": "NOT APPLIED",
        "max_payout": "$35K per universal jailbreak",
        "action": "Apply on HackerOne for invitation"
    },
    "gray_swan": {
        "url": "https://app.grayswan.ai/arena/challenge/safeguards/rules",
        "status": "NOT REGISTERED",
        "prize_pool": "$140K",
        "deadline": "May 6, 2026",
        "action": "REGISTER and compete in attack/defense"
    },
    "microsoft_msrc": {
        "url": "https://www.microsoft.com/en-us/msrc/bounty-ai",
        "status": "NOT REGISTERED",
        "max_payout": "$30K+",
        "focus": "Copilot AI safety",
        "action": "REGISTER on MSRC portal"
    },
    "ethereum_foundation": {
        "url": "https://ethereum.org/bug-bounty/",
        "status": "NOT REGISTERED",
        "max_payout": "$1M (RAISED 4x in Mar 2026!)",
        "attackathon": "$500K pool for mediums",
        "action": "REGISTER and HUNT"
    },
    "sherlock": {
        "url": "https://audits.sherlock.xyz/contests",
        "status": "NOT REGISTERED",
        "pools": "$47K-$126K per contest",
        "action": "REGISTER and join active contests"
    },
    "hats_finance": {
        "url": "https://app.hats.finance/",
        "status": "NOT REGISTERED",
        "note": "NO KYC required! On-chain payments + NFTs",
        "action": "REGISTER — first reporter gets full reward"
    },
    "cantina": {
        "url": "https://cantina.xyz/competitions",
        "status": "NOT REGISTERED",
        "pools": "$1M+ (Euler v2 $1.25M, Blast $1.2M)",
        "action": "REGISTER and compete"
    },
    "guardian": {
        "url": "https://guardianaudits.com",
        "status": "KYC BROKEN (500 error)",
        "active": "LimitBreak $150K — deadline Apr 9",
        "action": "Retry KYC daily, try Telegram t.me/guardianaudits"
    },
    "huntr": {
        "url": "https://huntr.com",
        "status": "NOT REGISTERED",
        "targets": "ollama, llama_index, transformers, mlflow ($1.5K-$4K each)",
        "action": "REGISTER with GitHub OAuth"
    },
    "cyfrin_codehawks": {
        "url": "https://codehawks.cyfrin.io/",
        "status": "NOT REGISTERED",
        "note": "Competitive audits + First Flights (practice). Eagles Elite tier for top performers.",
        "action": "REGISTER and join active audits"
    }
}

# ═══════════════════════════════════════════════════
# ACTIVE AUDIT CONTESTS (Session 54 — 29 Mar 2026)
# ═══════════════════════════════════════════════════

ACTIVE_CONTESTS = {
    "cantina_revert": {
        "platform": "Cantina",
        "name": "Revert Finance",
        "prize": "$50,000 USDC",
        "url": "https://cantina.xyz/competitions/efb6f308-f13b-4110-aff8-0d67181608dd",
        "deadline": "~Apr 3 (5 DAYS!)",
        "protocol": "DeFi lending for AMM LPs, Aerodrome Slipstream",
        "priority": "HIGH — ending soon!"
    },
    "sherlock_fluid": {
        "platform": "Sherlock",
        "name": "Fluid DEX v2",
        "prize": "$200,000+ USDC",
        "url": "https://audits.sherlock.xyz/contests/1225",
        "deadline": "Check live status",
        "protocol": "Liquidity Layer DEX + lending",
        "priority": "HIGHEST — biggest active pool"
    },
    "sherlock_inverse": {
        "platform": "Sherlock",
        "name": "Inverse Finance Junior Tranche",
        "prize": "$50,000 USDC",
        "url": "https://audits.sherlock.xyz/contests/1202",
        "protocol": "Insurance mechanism, bad debt buffer"
    },
    "sherlock_dhedge": {
        "platform": "Sherlock",
        "name": "dHEDGE Update",
        "prize": "$47,000 USDC",
        "url": "https://audits.sherlock.xyz/contests/1070",
        "protocol": "Aave + Pendle integration (Optimism)"
    },
    "sherlock_current": {
        "platform": "Sherlock",
        "name": "Current Finance",
        "prize": "$41,500 USDC",
        "url": "https://audits.sherlock.xyz/contests/1256",
        "protocol": "Capital efficiency on Sui, 16x leveraged yield"
    },
    "sherlock_superdca": {
        "platform": "Sherlock",
        "name": "Super DCA Liquidity Network",
        "prize": "$26,400 USDC",
        "url": "https://audits.sherlock.xyz/contests/1171",
        "protocol": "Uniswap V4 Hooks, DCA emission"
    },
    "sherlock_usual": {
        "platform": "Sherlock",
        "name": "Usual Money Bug Bounty",
        "prize": "$16,000,000 USDC (CRITICAL ONLY!)",
        "url": "https://audits.sherlock.xyz/bug-bounties",
        "deadline": "PERMANENT",
        "protocol": "Decentralized stablecoin — LARGEST bounty in crypto"
    },
    "c4_blend_v2": {
        "platform": "Code4rena",
        "name": "Blend V2 Mitigation Review",
        "prize": "$20,000 USDC",
        "url": "https://code4rena.com/audits",
        "deadline": "Apr 7-11",
        "protocol": "Liquidity protocol on Stellar (Rust)"
    },
    "hackenproof_rain": {
        "platform": "HackenProof",
        "name": "Rain Smart Contract Audit",
        "prize": "Up to $10,000/finding",
        "url": "https://hackenproof.com/audit-programs/rain-smart-contract-audit-contest",
        "protocol": "Prediction Markets"
    },
    "hackenproof_ignite": {
        "platform": "HackenProof",
        "name": "Ignite Market Audit",
        "prize": "Up to $10,000/finding",
        "url": "https://hackenproof.com/audit-programs/ignite-market-audit-contest"
    },
    "hackenproof_blockz": {
        "platform": "HackenProof",
        "name": "Blockz Smart Contract Audit",
        "prize": "Up to $10,000/finding",
        "url": "https://hackenproof.com/audit-programs/blockz-smart-contract-audit-contest",
        "protocol": "Core blockchain NFT marketplace"
    }
}

# ═══════════════════════════════════════════════════
# FINDINGS DATABASE
# ═══════════════════════════════════════════════════

FINDINGS = {
    "submitted": [
        {
            "platform": "Immunefi",
            "report": "#71022",
            "target": "ZKsync OS",
            "severity": "Medium",
            "bug": "Callstack depth off-by-one in ee_trait_impl.rs:351",
            "value": "$5K-$100K",
            "status": "Triage responded 26 Mar",
            "next": "Follow up if no response by 2 Apr"
        },
        {
            "platform": "Code4rena",
            "target": "Chainlink Payment Abstraction V2",
            "severity": "High",
            "bug": "H-01",
            "status": "Live Judging",
            "next": "Wait for results"
        }
    ],
    "ready_to_submit": [
        {
            "platform": "HackenProof",
            "target": "NEAR Intents",
            "severity": "CRITICAL",
            "bug": "MockAttestation in production WASM bypasses ALL TEE verification",
            "value": "$100K-$500K",
            "file": "~/near-intents-all-findings-report.md",
            "action": "SUBMIT VIA BROWSER — HIGHEST PRIORITY"
        },
        {
            "platform": "HackenProof",
            "target": "NEAR Intents",
            "severity": "HIGH",
            "count": 2,
            "value": "$40K-$200K",
            "action": "Submit after CRITICAL"
        },
        {
            "platform": "HackenProof",
            "target": "NEAR Intents",
            "severity": "MEDIUM",
            "count": 5,
            "value": "$5K-$100K each",
            "action": "Submit after HIGH"
        },
        {
            "platform": "Guardian",
            "target": "LimitBreak",
            "severity": "Mixed (8 findings)",
            "value": "$150K",
            "status": "KYC BROKEN — emailed backup",
            "deadline": "Apr 9"
        }
    ]
}

# ═══════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════

def cmd_dashboard():
    """Bounty dashboard"""
    print("=" * 60)
    print("  ISRAEL/NINE — BOUNTY SUBMISSION COMMANDER")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    print(f"\n  PLATFORMS: {len(PLATFORMS)} tracked")
    registered = sum(1 for p in PLATFORMS.values() if "ACTIVE" in str(p.get("account", "")) or "VERIFIED" in str(p.get("account", "")) or "APPROVED" in str(p.get("account", "")))
    print(f"  REGISTERED: {registered} | NOT REGISTERED: {len(PLATFORMS) - registered}")
    print(f"  SUBMITTED: {len(FINDINGS['submitted'])} reports")
    print(f"  READY TO SUBMIT: {len(FINDINGS['ready_to_submit'])} findings")
    print()

    print("  HIGHEST VALUE TARGETS:")
    print("  1. NEAR CRITICAL on HackenProof — $100K-$500K [8 REPORTS READY!]")
    print("  2. Sherlock Usual Money — $16M PERMANENT [critical only]")
    print("  3. Sherlock Fluid DEX v2 — $200K+ [ACTIVE NOW]")
    print("  4. Ethereum Foundation — $1M max [NEW 4x raise!]")
    print("  5. Gray Swan Arena — $140K pool [REGISTER!]")
    print("  6. LayerZero mediums — $10K-$25K each on Immunefi")
    print("  7. OpenAI Safety — $100K critical [NEW Bugcrowd!]")
    print("  8. Cantina Revert Finance — $50K [ENDS IN 5 DAYS!]")
    print("  9. Guardian LimitBreak — $150K [KYC broken]")
    print(" 10. ZKsync #71022 — $5K-$100K [IN TRIAGE]")
    print()
    print("  ACTIVE AUDIT CONTESTS:")
    for cid, c in ACTIVE_CONTESTS.items():
        deadline = c.get("deadline", "Check live")
        print(f"    [{c['platform']}] {c['name']} — {c['prize']} | {deadline}")

def cmd_platforms():
    """List all platforms"""
    print("\n  ALL BOUNTY PLATFORMS:")
    print("  " + "=" * 50)
    for pid, p in PLATFORMS.items():
        status = p.get("status", p.get("account", "Unknown"))
        url = p["url"]
        max_pay = p.get("max_payout", p.get("prize_pool", ""))
        print(f"\n  [{pid.upper()}] {status}")
        print(f"    URL: {url}")
        if max_pay:
            print(f"    Max: {max_pay}")

def cmd_findings():
    """List all findings"""
    print("\n  SUBMITTED REPORTS:")
    for f in FINDINGS["submitted"]:
        print(f"  [{f['platform']}] {f['target']} — {f.get('severity', '')} — {f.get('value', '')}")
        print(f"    Status: {f['status']} | Next: {f.get('next', '')}")

    print("\n  READY TO SUBMIT:")
    for f in FINDINGS["ready_to_submit"]:
        print(f"  [{f['platform']}] {f['target']} — {f['severity']} — {f.get('value', '')}")
        print(f"    Action: {f.get('action', '')}")

def cmd_register():
    """Show platforms needing registration"""
    print("\n  PLATFORMS NEEDING REGISTRATION:")
    print("  " + "=" * 50)
    for pid, p in PLATFORMS.items():
        status = str(p.get("status", p.get("account", "")))
        if "NOT REGISTERED" in status or "NOT APPLIED" in status:
            print(f"\n  [{pid.upper()}]")
            print(f"    URL: {p['url']}")
            print(f"    Action: {p.get('action', 'Register')}")
            if "max_payout" in p:
                print(f"    Max payout: {p['max_payout']}")

def cmd_warmode():
    """Full bounty warmode"""
    print("\n" + "=" * 60)
    print("  ISRAEL/NINE — BOUNTY WARMODE")
    print("=" * 60)
    cmd_dashboard()
    print("\n" + "-" * 60)
    cmd_findings()
    print("\n" + "-" * 60)
    cmd_register()
    print("\n" + "=" * 60)
    print("  EXECUTE: Register on ALL platforms, submit ALL findings")
    print("=" * 60)

COMMANDS = {
    "dashboard": cmd_dashboard,
    "platforms": cmd_platforms,
    "findings": cmd_findings,
    "register": cmd_register,
    "warmode": cmd_warmode,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dashboard"
    if cmd in COMMANDS:
        COMMANDS[cmd]()
    else:
        print(f"Commands: {', '.join(COMMANDS.keys())}")
