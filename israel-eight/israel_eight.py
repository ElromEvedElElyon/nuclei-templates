#!/usr/bin/env python3
"""
Israel/Eight — SALES & MARKETING COMMANDER
Em nome do Senhor Jesus Cristo, nosso Salvador

Autonomous sales agent: product promotion, email campaigns,
social media content, SEO optimization, payment link distribution.

Run: python3 ~/israel-eight/israel_eight.py warmode
"""

import os
import sys
import json
import hashlib
import hmac
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════
# SOUL
# ═══════════════════════════════════════════════════
SOUL = {
    "name": "Israel/Eight",
    "title": "Sales & Marketing Commander",
    "version": "1.0.0",
    "mission": "Sell every product across every channel 24/7",
    "scripture": "The blessing of the LORD makes rich — Proverbs 10:22"
}

# ═══════════════════════════════════════════════════
# PRODUCT CATALOG
# ═══════════════════════════════════════════════════
PRODUCTS = {
    "taptoons": {
        "name": "TapToons v2 — Monster Runner N64",
        "price": "$0.99",
        "url": "https://elromevedelelyon.github.io/taptoons/",
        "stripe": "https://buy.stripe.com/6oUdR80Vu5pm3S56uV0x20c",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/0.99",
        "description": "100 hilarious sound effects + N64-style monster runner game. Fun for all ages!",
        "target": "Mobile gamers, parents with kids, fun gift",
        "hashtags": "#IndieGame #MobileGame #SoundEffects #PWA #N64"
    },
    "mythos": {
        "name": "MYTHOS — Claude AI Mastery Guide",
        "price": "$6.66",
        "url": "https://sintex.ai/mythos",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/6.66",
        "description": "Master Claude AI with the most comprehensive guide. 14 languages. 7 appendices of real prompts.",
        "target": "AI developers, Claude users, prompt engineers",
        "hashtags": "#ClaudeAI #AI #PromptEngineering #AIGuide"
    },
    "bitcoin_guide": {
        "name": "Bitcoin Survival Guide 2026",
        "price": "$19.99",
        "stripe": "https://buy.stripe.com/eVqeVc1Zy196gER5qR0x20d",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/19.99",
        "description": "Navigate Bitcoin in 2026. Practical strategies for the next halving cycle.",
        "target": "Crypto investors, Bitcoin enthusiasts",
        "hashtags": "#Bitcoin #BTC #Crypto #Investment #Halving"
    },
    "ai_templates": {
        "name": "50 AI Agent Templates",
        "price": "$29.99",
        "stripe": "https://buy.stripe.com/3cIeVcgUscRO74h4mN0x20e",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/29.99",
        "description": "50 ready-to-use AI agent templates. Claude, GPT, Gemini compatible. Build agents in minutes.",
        "target": "AI developers, startup founders, automation engineers",
        "hashtags": "#AIAgents #Automation #Claude #Templates #Developer"
    },
    "prompt_bible": {
        "name": "Prompt Engineering Bible",
        "price": "$19.99",
        "stripe": "https://buy.stripe.com/cNi6oG9s0052fAN8D30x20f",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/19.99",
        "description": "The definitive guide to prompt engineering. 500+ tested prompts across all major LLMs.",
        "target": "Prompt engineers, AI enthusiasts, content creators",
        "hashtags": "#PromptEngineering #AI #LLM #ChatGPT #Claude"
    },
    "defi_playbook": {
        "name": "DeFi Playbook 2026",
        "price": "$14.99",
        "stripe": "https://buy.stripe.com/bJe8wO8nWbNK74h3iJ0x20g",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/14.99",
        "description": "Master DeFi yield farming, liquidity providing, and protocol strategies for 2026.",
        "target": "DeFi users, crypto traders, yield farmers",
        "hashtags": "#DeFi #Crypto #YieldFarming #Ethereum #Solana"
    },
    "blueprint": {
        "name": "Sovereign Business Blueprint",
        "price": "$24.99",
        "stripe": "https://buy.stripe.com/5kQ28q1Zy5pm1JXg5v0x20h",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/24.99",
        "description": "Build a sovereign digital business with AI agents, crypto payments, and decentralized infrastructure.",
        "target": "Entrepreneurs, digital nomads, solopreneurs",
        "hashtags": "#Business #Entrepreneur #AI #Sovereign #Digital"
    },
    "bundle": {
        "name": "Complete Digital Bundle (5 Products, Save 30%)",
        "price": "$79.99",
        "stripe": "https://buy.stripe.com/9B67sK7jS2dadsF7yZ0x20i",
        "paypal": "https://www.paypal.com/paypalme/PadraoBitcoin/79.99",
        "description": "Get ALL 5 digital products at 30% off. Bitcoin Guide + AI Templates + Prompt Bible + DeFi Playbook + Business Blueprint.",
        "target": "Power users, builders, multi-disciplinary learners",
        "hashtags": "#Bundle #BestDeal #AI #Crypto #Business"
    }
}

# ═══════════════════════════════════════════════════
# MARKETING COPY GENERATOR
# ═══════════════════════════════════════════════════

class CopyGenerator:
    """Generate marketing copy for all products"""

    @staticmethod
    def tweet(product_id):
        """Generate tweet for a product"""
        p = PRODUCTS[product_id]
        templates = [
            f"{p['name']} is LIVE! {p['description'][:100]}... Only {p['price']}. Get yours: {p.get('stripe', p.get('url', ''))}",
            f"Just dropped: {p['name']}. {p['price']}. {p['description'][:80]}... {p.get('stripe', p.get('url', ''))}",
            f"{p['description'][:120]}. {p['name']} — {p['price']}. {p.get('stripe', p.get('url', ''))}",
        ]
        import random
        return random.choice(templates)

    @staticmethod
    def email_body(product_id):
        """Generate email marketing body"""
        p = PRODUCTS[product_id]
        return f"""
Hi there,

I wanted to share something I've been working on:

**{p['name']}** — {p['price']}

{p['description']}

Get it now:
- Stripe: {p.get('stripe', 'N/A')}
- PayPal: {p.get('paypal', 'N/A')}

Best regards,
Elrom — Padrao Bitcoin
standardbitcoin.io@gmail.com
"""

    @staticmethod
    def landing_page_hero(product_id):
        """Generate landing page hero section"""
        p = PRODUCTS[product_id]
        return f"""
<section class="hero">
  <h1>{p['name']}</h1>
  <p class="price">{p['price']}</p>
  <p class="description">{p['description']}</p>
  <div class="cta-buttons">
    <a href="{p.get('stripe', '#')}" class="btn-primary">Buy with Card</a>
    <a href="{p.get('paypal', '#')}" class="btn-secondary">Pay with PayPal</a>
  </div>
</section>
"""


# ═══════════════════════════════════════════════════
# EMAIL CAMPAIGN ENGINE
# ═══════════════════════════════════════════════════

class EmailCampaign:
    """Send marketing emails via SMTP"""

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "inteligenciaartificial.now@gmail.com"
    SMTP_PASS = "vrhyiymomugnqwrs"  # App password

    def send(self, to_email, subject, body):
        """Send a single marketing email"""
        try:
            msg = MIMEMultipart()
            msg["From"] = f"Padrao Bitcoin <{self.SMTP_USER}>"
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.SMTP_USER, self.SMTP_PASS)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"  Email to {to_email} failed: {e}")
            return False

    def campaign(self, contacts, product_id):
        """Run email campaign for a product"""
        p = PRODUCTS[product_id]
        subject = f"New: {p['name']} — {p['price']}"
        body = CopyGenerator.email_body(product_id)

        success = 0
        for contact in contacts:
            if self.send(contact, subject, body):
                success += 1
                print(f"  Sent to {contact}")

        print(f"\n  Campaign: {success}/{len(contacts)} emails sent for {p['name']}")
        return success


# ═══════════════════════════════════════════════════
# SOCIAL MEDIA ENGINE
# ═══════════════════════════════════════════════════

class SocialEngine:
    """Generate social media content"""

    def generate_all_tweets(self):
        """Generate tweets for all products"""
        tweets = []
        for pid in PRODUCTS:
            tweet = CopyGenerator.tweet(pid)
            tweets.append({"product": pid, "text": tweet})
        return tweets

    def generate_thread(self, topic="products"):
        """Generate Twitter/X thread"""
        thread = [
            "Thread: Everything I've built as a solo AI developer (you can buy all of these right now)",
            "",
        ]
        for pid, p in PRODUCTS.items():
            thread.append(f"{p['name']} — {p['price']}\n{p['description'][:100]}...\n{p.get('stripe', p.get('url', ''))}\n")
        thread.append("That's 8 products, all LIVE, all under $80.\n\nThe Complete Bundle saves you 30%: $79.99\n\nBuilt with Claude Code + pure determination. No VC, no team, just code.")
        return thread

    def display_tweets(self):
        """Show all generated tweets"""
        print("\n  SOCIAL MEDIA CONTENT QUEUE:")
        print("  " + "=" * 50)
        tweets = self.generate_all_tweets()
        for i, t in enumerate(tweets, 1):
            print(f"\n  Tweet #{i} ({t['product']}):")
            print(f"  {t['text'][:280]}")
        return tweets


# ═══════════════════════════════════════════════════
# STORE SUBMISSION ENGINE
# ═══════════════════════════════════════════════════

class StoreSubmitter:
    """Submit products to app stores and marketplaces"""

    STORES = {
        "samsung_galaxy": {
            "name": "Samsung Galaxy Store",
            "url": "https://seller.samsungapps.com/",
            "fee": "FREE",
            "status": "NOT SUBMITTED",
            "action": "Register developer account, upload APK"
        },
        "amazon_appstore": {
            "name": "Amazon Appstore",
            "url": "https://developer.amazon.com/apps-and-games",
            "fee": "FREE",
            "status": "NOT SUBMITTED",
            "action": "Register developer account, upload APK"
        },
        "huawei_appgallery": {
            "name": "Huawei AppGallery",
            "url": "https://developer.huawei.com/consumer/en/appgallery",
            "fee": "FREE (15% rev share vs Google's 30%)",
            "status": "NOT SUBMITTED",
            "action": "Register developer account, upload APK"
        },
        "microsoft_store": {
            "name": "Microsoft Store",
            "url": "https://partner.microsoft.com/en-us/dashboard",
            "fee": "FREE for PWAs",
            "status": "NOT SUBMITTED",
            "action": "Submit PWA URL directly"
        },
        "kdp_amazon": {
            "name": "Amazon KDP",
            "url": "https://kdp.amazon.com",
            "fee": "FREE, 70% royalty",
            "status": "DRAFT PAUSED — fiscal pending",
            "action": "Complete W-8BEN, citizenship, bank details"
        }
    }

    def status(self):
        """Show store submission status"""
        print("\n  STORE SUBMISSIONS:")
        print("  " + "=" * 50)
        for sid, s in self.STORES.items():
            print(f"  [{s['status']}] {s['name']} — {s['fee']}")
            print(f"    Action: {s['action']}")
        return self.STORES


# ═══════════════════════════════════════════════════
# PAYMENT LINKS DIRECTORY
# ═══════════════════════════════════════════════════

def show_payment_links():
    """Display all active payment links"""
    print("\n  PAYMENT LINKS DIRECTORY:")
    print("  " + "=" * 50)
    print()
    print("  STRIPE (Card payments):")
    for pid, p in PRODUCTS.items():
        if "stripe" in p:
            print(f"    {p['price']:>6} | {p['name']}")
            print(f"           {p['stripe']}")
    print()
    print("  PAYPAL (Global):")
    for pid, p in PRODUCTS.items():
        if "paypal" in p:
            print(f"    {p['price']:>6} | {p['name']}")
            print(f"           {p['paypal']}")
    print()
    print("  CRYPTO:")
    print("    EVM: 0x6b45b26e1d59A832FE8c9E7c685C36Ea54A3F88B")
    print("    SOL: CM42ofAFowySg72GjDuCchEkwwbwnhdSRYgztRCAAEzR")
    print("    BTC: bc1qdj3flkqe7v3qwlfux5d5u3rja7ldm9gwywk9t2")
    print()
    print("  PIX (Brasil):")
    print("    CNPJ: 51.148.891/0001-69")
    print("    Padrao Bitcoin Atividades de Internet LTDA")


# ═══════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════

def cmd_dashboard():
    """Marketing dashboard"""
    print("=" * 60)
    print("  ISRAEL/EIGHT — SALES & MARKETING COMMANDER")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print(f"\n  PRODUCTS: {len(PRODUCTS)} LIVE")
    print(f"  REVENUE: $0 (EMERGENCY — need first sale!)")
    print()
    for pid, p in PRODUCTS.items():
        print(f"  [{pid}] {p['name']} — {p['price']}")
    print()
    print("  IMMEDIATE ACTIONS:")
    print("  1. Post product links on relevant subreddits/forums")
    print("  2. Create Upwork gigs showcasing products")
    print("  3. Submit to app stores (Samsung, Amazon, Huawei)")
    print("  4. Complete KDP fiscal for MYTHOS book")
    print("  5. Generate and queue 20 product tweets")
    print("  6. Send email campaign to existing contacts")
    print("  7. List MCP tools on Claude Marketplace")

def cmd_tweets():
    """Generate marketing tweets"""
    social = SocialEngine()
    social.display_tweets()

def cmd_links():
    """Show all payment links"""
    show_payment_links()

def cmd_stores():
    """Store submission status"""
    StoreSubmitter().status()

def cmd_copy(product_id=None):
    """Generate marketing copy"""
    if product_id and product_id in PRODUCTS:
        print(f"\n  TWEET:\n  {CopyGenerator.tweet(product_id)}")
        print(f"\n  EMAIL:\n  {CopyGenerator.email_body(product_id)}")
        print(f"\n  LANDING PAGE:\n  {CopyGenerator.landing_page_hero(product_id)}")
    else:
        print(f"  Products: {', '.join(PRODUCTS.keys())}")
        print(f"  Usage: python3 israel_eight.py copy <product_id>")

def cmd_warmode():
    """Full marketing warmode"""
    print("\n" + "=" * 60)
    print("  ISRAEL/EIGHT — SALES WARMODE")
    print("=" * 60)
    cmd_dashboard()
    print("\n" + "-" * 60)
    SocialEngine().display_tweets()
    print("\n" + "-" * 60)
    show_payment_links()
    print("\n" + "-" * 60)
    StoreSubmitter().status()
    print("\n" + "=" * 60)
    print("  ALL SALES VECTORS ACTIVE — PUSH EVERY PRODUCT")
    print("=" * 60)

COMMANDS = {
    "dashboard": cmd_dashboard,
    "tweets": cmd_tweets,
    "links": cmd_links,
    "stores": cmd_stores,
    "warmode": cmd_warmode,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dashboard"
    if cmd == "copy":
        pid = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_copy(pid)
    elif cmd in COMMANDS:
        COMMANDS[cmd]()
    else:
        print(f"Commands: {', '.join(list(COMMANDS.keys()) + ['copy <id>'])}")
