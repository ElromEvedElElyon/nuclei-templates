#!/usr/bin/env python3
"""
ZION Agent Framework — Full autonomous agents with soul, memory, MCPs, and tools.
Em nome do Senhor Jesus Cristo, nosso Salvador.

Agents can:
1. Use MCP tools (crypto prices, social, web analysis)
2. Use skills (tweet generation, thread building, content calendar)
3. Create sub-agents with their own soul/memory
4. Communicate with other agents via shared network
5. Learn from experience and improve over time

Architecture:
    ZionAgent (base class)
    ├── soul: AgentSoul (identity, values, voice)
    ├── memory: AgentMemory (persistent, learning)
    ├── tools: ToolRegistry (MCPs, skills, custom)
    ├── network: AgentNetwork (inter-agent comms)
    └── children: list[ZionAgent] (sub-agents created)
"""

import json, subprocess, os, random, re, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Callable
from agent_soul_architecture import AgentSoul, AgentMemory, AgentNetwork

BRT = timezone(timedelta(hours=-3))


# ─── TOOL REGISTRY ───────────────────────────────────────────────────
class Tool:
    """A single tool an agent can use."""

    def __init__(self, name: str, description: str, handler: Callable,
                 category: str = "general", requires_api_key: bool = False):
        self.name = name
        self.description = description
        self.handler = handler
        self.category = category
        self.requires_api_key = requires_api_key
        self.usage_count = 0

    def execute(self, **kwargs):
        self.usage_count += 1
        return self.handler(**kwargs)


class ToolRegistry:
    """Registry of all tools available to agents."""

    def __init__(self):
        self.tools = {}
        self._register_builtin_tools()

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)

    def list_tools(self, category: str = None) -> list:
        if category:
            return [t for t in self.tools.values() if t.category == category]
        return list(self.tools.values())

    def _register_builtin_tools(self):
        """Register all built-in MCP and utility tools."""

        # ── CRYPTO TOOLS (via CoinGecko API) ──
        self.register(Tool(
            "crypto_price",
            "Get current price of BTC, ETH, SOL and other coins",
            self._crypto_price,
            category="crypto"
        ))
        self.register(Tool(
            "crypto_trending",
            "Get trending cryptocurrencies (most searched 24h)",
            self._crypto_trending,
            category="crypto"
        ))
        self.register(Tool(
            "crypto_fear_greed",
            "Get Fear & Greed Index",
            self._crypto_fear_greed,
            category="crypto"
        ))
        self.register(Tool(
            "crypto_market_overview",
            "Get global market cap, BTC dominance, active coins",
            self._crypto_market_overview,
            category="crypto"
        ))

        # ── SOCIAL TOOLS ──
        self.register(Tool(
            "generate_tweet",
            "Generate a tweet in builder-authority style",
            self._generate_tweet,
            category="social"
        ))
        self.register(Tool(
            "post_tweet",
            "Post a tweet via twikit",
            self._post_tweet,
            category="social"
        ))

        # ── WEB TOOLS ──
        self.register(Tool(
            "web_fetch",
            "Fetch and extract text from a URL",
            self._web_fetch,
            category="web"
        ))

        # ── UTILITY TOOLS ──
        self.register(Tool(
            "shell_command",
            "Execute a shell command safely",
            self._shell_command,
            category="utility"
        ))
        self.register(Tool(
            "read_file",
            "Read contents of a file",
            self._read_file,
            category="utility"
        ))
        self.register(Tool(
            "write_file",
            "Write contents to a file",
            self._write_file,
            category="utility"
        ))

    # ── Tool implementations ──

    @staticmethod
    def _crypto_price(coins: str = "bitcoin,ethereum,solana") -> dict:
        try:
            result = subprocess.run(
                ["python3", "-c", f"""
import urllib.request, json
url = "https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
req = urllib.request.Request(url, headers={{"Accept": "application/json", "User-Agent": "ZION/1.0"}})
resp = urllib.request.urlopen(req, timeout=10)
print(json.dumps(json.loads(resp.read())))
"""],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return json.loads(result.stdout.strip())
        except Exception as e:
            return {"error": str(e)}
        return {"error": "fetch failed"}

    @staticmethod
    def _crypto_trending() -> list:
        try:
            result = subprocess.run(
                ["python3", "-c", """
import urllib.request, json
url = "https://api.coingecko.com/api/v3/search/trending"
req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "ZION/1.0"})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())
coins = [{"name": c["item"]["name"], "symbol": c["item"]["symbol"]} for c in d.get("coins", [])[:7]]
print(json.dumps(coins))
"""],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return json.loads(result.stdout.strip())
        except Exception:
            pass
        return []

    @staticmethod
    def _crypto_fear_greed() -> dict:
        try:
            result = subprocess.run(
                ["python3", "-c", """
import urllib.request, json
url = "https://api.alternative.me/fng/?limit=1"
req = urllib.request.Request(url, headers={"User-Agent": "ZION/1.0"})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())
print(json.dumps(d["data"][0]))
"""],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return json.loads(result.stdout.strip())
        except Exception:
            pass
        return {}

    @staticmethod
    def _crypto_market_overview() -> dict:
        try:
            result = subprocess.run(
                ["python3", "-c", """
import urllib.request, json
url = "https://api.coingecko.com/api/v3/global"
req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "ZION/1.0"})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())["data"]
print(json.dumps({"total_market_cap_usd": d["total_market_cap"]["usd"], "btc_dominance": d["market_cap_percentage"]["btc"], "active_coins": d["active_cryptocurrencies"]}))
"""],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return json.loads(result.stdout.strip())
        except Exception:
            pass
        return {}

    @staticmethod
    def _generate_tweet(topic: str = "crypto", style: str = "data-driven") -> str:
        """Generate tweet using template system."""
        templates = {
            "crypto": [
                "The signal is in the divergence\n\nMarket moves. Builders ship\n\nOne of these compounds",
                "Every protocol needs an MCP server\n\nMost do not have one yet\n\nThe opportunity is obvious",
            ],
            "ai": [
                "AI agents will become the primary users of DeFi\n\nNot retail. Not institutions. Agents\n\nBuild the rails or become irrelevant",
                "The interface layer is collapsing into natural language\n\nEvery dashboard becomes a prompt",
            ],
            "builder": [
                "Ship first. Discuss later\n\nThe market rewards output, not opinions",
                "Another day of output. No roadmap presentation\n\nJust code that works",
            ],
        }
        pool = templates.get(topic, templates["crypto"])
        return random.choice(pool)

    @staticmethod
    def _post_tweet(text: str) -> dict:
        """Post via twikit/tweet_now.py."""
        try:
            script = os.path.expanduser("~/tweet_now.py")
            if os.path.exists(script):
                result = subprocess.run(
                    ["python3", script, text],
                    capture_output=True, text=True, timeout=60
                )
                return {"success": result.returncode == 0, "output": result.stdout[:200]}
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "error": "no posting script found"}

    @staticmethod
    def _web_fetch(url: str) -> str:
        try:
            result = subprocess.run(
                ["python3", "-c", f"""
import urllib.request
req = urllib.request.Request("{url}", headers={{"User-Agent": "ZION/1.0"}})
resp = urllib.request.urlopen(req, timeout=15)
print(resp.read().decode("utf-8", errors="ignore")[:5000])
"""],
                capture_output=True, text=True, timeout=20
            )
            return result.stdout[:5000] if result.returncode == 0 else ""
        except Exception:
            return ""

    @staticmethod
    def _shell_command(command: str, timeout: int = 30) -> dict:
        # Safety: block dangerous commands
        dangerous = ["rm -rf /", "mkfs", "dd if=", ":(){", "fork bomb"]
        for d in dangerous:
            if d in command:
                return {"error": "blocked: dangerous command"}
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return {
                "stdout": result.stdout[:2000],
                "stderr": result.stderr[:500],
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"error": "timeout"}

    @staticmethod
    def _read_file(path: str) -> str:
        try:
            return Path(path).read_text()[:10000]
        except Exception as e:
            return f"error: {e}"

    @staticmethod
    def _write_file(path: str, content: str) -> bool:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(content)
            return True
        except Exception:
            return False


# ─── ZION AGENT (Main class) ─────────────────────────────────────────
class ZionAgent:
    """
    Full autonomous agent with soul, memory, tools, and networking.
    Can create sub-agents that inherit its capabilities.
    """

    def __init__(self, name: str, role: str, voice: str = "builder-authority",
                 parent: "ZionAgent" = None, base_dir: Path = None):
        # Soul
        self.soul = AgentSoul(name, role, voice)

        # Memory
        self.base_dir = base_dir or Path.home() / name.lower().replace("/", "-")
        self.memory = AgentMemory(self.soul, self.base_dir)

        # Tools
        self.tools = ToolRegistry()

        # Network
        self.network = AgentNetwork()
        self.network.register_agent(self.soul)

        # Lineage
        self.parent = parent
        self.children = []

        # Skills (higher-level capabilities built on tools)
        self.skills = {}
        self._register_default_skills()

    def _register_default_skills(self):
        """Register skills that combine multiple tools."""
        self.skills["market_briefing"] = self._skill_market_briefing
        self.skills["post_enriched_tweet"] = self._skill_post_enriched_tweet
        self.skills["content_calendar"] = self._skill_content_calendar
        self.skills["security_scan"] = self._skill_security_scan

    # ── Skills (combine tools) ──

    def _skill_market_briefing(self) -> dict:
        """Generate a complete market briefing using multiple data sources."""
        prices = self.tools.get("crypto_price").execute()
        fng = self.tools.get("crypto_fear_greed").execute()
        trending = self.tools.get("crypto_trending").execute()
        overview = self.tools.get("crypto_market_overview").execute()

        briefing = {
            "prices": prices,
            "fear_greed": fng,
            "trending": trending,
            "market_overview": overview,
            "generated_at": datetime.now(BRT).isoformat(),
        }

        self.memory.observe(f"Market briefing generated: BTC={prices.get('bitcoin', {}).get('usd', '?')}")
        return briefing

    def _skill_post_enriched_tweet(self, template_type: str = "auto") -> dict:
        """Generate and post a data-enriched tweet."""
        # Get data
        prices = self.tools.get("crypto_price").execute()
        fng = self.tools.get("crypto_fear_greed").execute()

        # Generate tweet
        tweet_text = self.tools.get("generate_tweet").execute(
            topic="crypto" if template_type == "auto" else template_type
        )

        # Enrich with data
        if prices and not prices.get("error"):
            btc = prices.get("bitcoin", {}).get("usd", 0)
            if btc:
                tweet_text = tweet_text.replace("{btc_price}", f"{btc:,.0f}")

        if fng and not fng.get("error"):
            fg_val = fng.get("value", "?")
            fg_class = fng.get("value_classification", "?")
            tweet_text = tweet_text.replace("{fear_greed}", f"{fg_val} ({fg_class})")

        # Check duplicate
        if self.memory.is_duplicate(tweet_text):
            self.memory.observe("Duplicate tweet detected, skipping")
            return {"success": False, "reason": "duplicate"}

        # Post
        result = self.tools.get("post_tweet").execute(text=tweet_text)

        if result.get("success"):
            self.memory.record_action(tweet_text, template_type)
            self.network.increment_global_count()
            self.network.heartbeat(self.soul.name)

        return {"success": result.get("success"), "text": tweet_text}

    def _skill_content_calendar(self, days: int = 7) -> list:
        """Generate a content calendar for N days."""
        calendar = []
        schedule = [
            ("07:00", "metric_drop"),
            ("09:30", "builder_log"),
            ("12:00", "insider_alpha"),
            ("14:30", "binary_frame"),
            ("16:00", "builder_log"),
            ("18:30", "defi_alpha"),
            ("20:00", "sovereignty"),
            ("22:00", "two_word"),
        ]
        for day in range(days):
            date = (datetime.now(BRT) + timedelta(days=day)).strftime("%Y-%m-%d")
            weekday = (datetime.now(BRT) + timedelta(days=day)).strftime("%A")

            # Reduce on weekends
            day_schedule = schedule if weekday not in ["Saturday", "Sunday"] else schedule[:4]

            for time_slot, template_type in day_schedule:
                calendar.append({
                    "date": date,
                    "weekday": weekday,
                    "time_brt": time_slot,
                    "template_type": template_type,
                })
        return calendar

    def _skill_security_scan(self, target: str = "") -> dict:
        """Basic security reconnaissance."""
        results = {}
        if target:
            # DNS check
            dns = self.tools.get("shell_command").execute(
                command=f"dig +short {target} A 2>/dev/null | head -5"
            )
            results["dns"] = dns.get("stdout", "").strip()

            # Headers check
            headers = self.tools.get("shell_command").execute(
                command=f"curl -sI https://{target} 2>/dev/null | head -20"
            )
            results["headers"] = headers.get("stdout", "").strip()

        return results

    # ── Core Agent Methods ──

    def use_tool(self, tool_name: str, **kwargs):
        """Use a registered tool."""
        tool = self.tools.get(tool_name)
        if not tool:
            return {"error": f"tool '{tool_name}' not found"}
        result = tool.execute(**kwargs)
        self.memory.observe(f"Used tool: {tool_name}")
        return result

    def use_skill(self, skill_name: str, **kwargs):
        """Use a registered skill."""
        skill = self.skills.get(skill_name)
        if not skill:
            return {"error": f"skill '{skill_name}' not found"}
        result = skill(**kwargs)
        self.memory.observe(f"Used skill: {skill_name}")
        return result

    def create_child_agent(self, name: str, role: str, voice: str = "builder-authority") -> "ZionAgent":
        """Create a sub-agent that inherits tools and network access."""
        child = ZionAgent(
            name=name,
            role=role,
            voice=voice,
            parent=self,
            base_dir=self.base_dir / "children" / name.lower().replace("/", "-"),
        )

        self.children.append(child)

        # Notify network
        self.network.send_message(
            from_agent=self.soul.name,
            to_agent=name,
            message=f"Welcome. Created by {self.soul.name}. Role: {role}",
            priority="high"
        )

        self.memory.observe(f"Created child agent: {name} (role: {role})")
        return child

    def send_message(self, to_agent: str, message: str, priority: str = "normal"):
        self.network.send_message(self.soul.name, to_agent, message, priority)

    def check_messages(self) -> list:
        return self.network.get_messages(self.soul.name)

    def report_status(self) -> dict:
        return {
            "agent": self.soul.name,
            "role": self.soul.role,
            "voice": self.soul.voice,
            "total_actions": self.memory.long_term.get("total_actions", 0),
            "today_count": self.memory.today_count(),
            "children": [c.soul.name for c in self.children],
            "tools": len(self.tools.tools),
            "skills": list(self.skills.keys()),
            "active_agents": len(self.network.get_active_agents()),
        }


# ─── QUICK TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("ZION Agent Framework — Test")
    print("=" * 60)

    # Create Israel/One as master agent
    israel = ZionAgent("Israel/One", role="x_poster")
    status = israel.report_status()
    print(f"\nAgent: {status['agent']}")
    print(f"Role: {status['role']}")
    print(f"Tools: {status['tools']}")
    print(f"Skills: {status['skills']}")
    print(f"Active agents: {status['active_agents']}")

    # Create child agents
    scout = israel.create_child_agent("Israel/Scout", role="market_watcher")
    writer = israel.create_child_agent("Israel/Writer", role="content_creator")

    print(f"\nChildren: {[c.soul.name for c in israel.children]}")

    # Test tool usage
    print("\n--- Testing crypto_price tool ---")
    prices = israel.use_tool("crypto_price", coins="bitcoin")
    print(f"BTC: ${prices.get('bitcoin', {}).get('usd', '?')}")

    # Test skill
    print("\n--- Testing content_calendar skill ---")
    cal = israel.use_skill("content_calendar", days=1)
    for entry in cal[:3]:
        print(f"  {entry['time_brt']} — {entry['template_type']}")

    # Test messaging
    israel.send_message("Israel/Scout", "Check BTC dominance trend")
    msgs = scout.check_messages()
    print(f"\nScout received {len(msgs)} messages")

    # Report
    print(f"\nFinal status: {israel.report_status()}")
    print("\nZION Agent Framework: OK")
