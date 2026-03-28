#!/usr/bin/env python3
"""
Israel Two — npm Ecosystem Dominance Agent
Manages Atomus AI publishing, marketing, adoption tracking.
Spawns sub-agents for specific npm/ecosystem tasks.

In the name of the Lord Jesus Christ.
"""

import json
import os
import sys
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

# ========== CONFIGURATION ==========
ATOMUS_DIR = Path.home() / "atomus-ai"
STATE_FILE = Path.home() / ".zion" / "israel_two_state.json"
AGENT_DIR = Path.home() / ".zion" / "agents" / "israel-two"

NPM_PACKAGES = {
    "atomus-ai": {
        "path": str(ATOMUS_DIR),
        "description": "The atomic toolkit for AI agents",
        "target_downloads_weekly": 10000,
        "published": False,
        "version": "1.0.0",
    }
}

# Sub-agents Israel Two can spawn
SUB_AGENTS = {
    "npm-publisher": "Handles npm publishing, versioning, and releases",
    "readme-optimizer": "Optimizes READMEs for npm discoverability and SEO",
    "issue-hunter": "Finds issues in popular repos where atomus-ai could be recommended",
    "dependency-tracker": "Monitors who depends on our packages and engagement",
    "sponsor-outreach": "Identifies and contacts potential sponsors",
    "mcp-integrator": "Creates MCP server wrappers using atomus-ai",
    "template-generator": "Creates starter templates that use atomus-ai",
    "benchmark-runner": "Runs and publishes benchmarks vs competitors",
}

# Ecosystem targets for integration
INTEGRATION_TARGETS = [
    {"name": "langchain", "strategy": "lighter alternative for specific tasks"},
    {"name": "vercel/ai", "strategy": "complementary utilities"},
    {"name": "modelcontextprotocol", "strategy": "schema builder integration"},
    {"name": "anthropic-sdk", "strategy": "retry/streaming companion"},
    {"name": "openai", "strategy": "retry/streaming companion"},
    {"name": "llamaindex", "strategy": "token/memory utilities"},
]

# Monetization channels
REVENUE_CHANNELS = {
    "github_sponsors": {
        "url": "https://github.com/sponsors/ElromEvedElElyon",
        "tiers": ["$5/mo", "$25/mo", "$100/mo"],
        "status": "setup_needed",
    },
    "open_collective": {
        "url": "https://opencollective.com",
        "status": "not_started",
    },
    "tidelift": {
        "url": "https://tidelift.com",
        "requirements": "1000+ dependents",
        "status": "not_eligible_yet",
    },
    "npm_bounties": {
        "platforms": ["opire", "algora", "issuehunt"],
        "status": "active",
    },
}


class IsraelTwo:
    """npm Ecosystem Dominance Agent"""

    def __init__(self):
        self.state = self._load_state()
        self.name = "Israel Two"
        self.mission = "npm ecosystem dominance for Atomus AI"
        self._ensure_dirs()

    def _ensure_dirs(self):
        AGENT_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    def _load_state(self):
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
        return {
            "created": datetime.now().isoformat(),
            "packages": NPM_PACKAGES,
            "downloads": {},
            "sponsors": 0,
            "revenue_usd": 0,
            "tasks_completed": 0,
            "sub_agents_spawned": 0,
            "last_action": None,
        }

    def _save_state(self):
        STATE_FILE.write_text(json.dumps(self.state, indent=2))

    def status(self):
        """Full status report"""
        return {
            "agent": self.name,
            "mission": self.mission,
            "packages": self.state["packages"],
            "revenue": {
                "channels": REVENUE_CHANNELS,
                "total_usd": self.state["revenue_usd"],
                "sponsors": self.state["sponsors"],
            },
            "tasks_completed": self.state["tasks_completed"],
            "integration_targets": INTEGRATION_TARGETS,
        }

    def check_npm_status(self, package="atomus-ai"):
        """Check npm package status"""
        try:
            result = subprocess.run(
                ["npm", "view", package, "--json"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    "published": True,
                    "version": data.get("version"),
                    "downloads": data.get("downloads"),
                }
        except Exception as e:
            pass
        return {"published": False}

    def publish_package(self, package="atomus-ai"):
        """Publish a package to npm"""
        pkg = self.state["packages"].get(package)
        if not pkg:
            return {"error": f"Unknown package: {package}"}

        path = pkg["path"]
        try:
            result = subprocess.run(
                ["npm", "publish", "--access", "public"],
                cwd=path, capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                pkg["published"] = True
                self.state["tasks_completed"] += 1
                self._save_state()
                return {"success": True, "output": result.stdout}
            return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}

    def generate_adoption_plan(self):
        """Generate a plan to increase npm downloads"""
        plan = {
            "phase_1_launch": {
                "week": 1,
                "target": "100 downloads",
                "actions": [
                    "Publish atomus-ai v1.0.0 to npm",
                    "Create GitHub Sponsors page",
                    "Post announcement on X (@opencllaw)",
                    "Submit to awesome-ai-agents lists",
                    "Create 3 example projects using atomus-ai",
                    "Write blog post: 'Why I built atomus-ai'",
                ],
            },
            "phase_2_growth": {
                "week": "2-4",
                "target": "1,000 downloads/week",
                "actions": [
                    "Create MCP server template using atomus-ai",
                    "Submit to Glama MCP directory",
                    "Open PRs adding atomus-ai to example projects",
                    "Answer Stack Overflow questions with atomus-ai solutions",
                    "Create npm comparison article (vs langchain, etc)",
                    "Reach out to AI newsletter authors",
                ],
            },
            "phase_3_authority": {
                "week": "5-12",
                "target": "10,000 downloads/week",
                "actions": [
                    "Release atomus-ai v2.0 with new modules",
                    "Create YouTube tutorial series",
                    "Speak at AI/JS meetups",
                    "Get featured in 'awesome' lists",
                    "Build official integrations (LangChain, Vercel AI)",
                    "Apply for Tidelift",
                ],
            },
            "phase_4_dominance": {
                "week": "13+",
                "target": "100,000+ downloads/week",
                "actions": [
                    "Corporate sponsorship outreach",
                    "Enterprise features (atomus-ai/pro)",
                    "Consulting services",
                    "Conference talks",
                    "Foundation/governance setup",
                ],
            },
        }
        return plan

    def find_contribution_opportunities(self):
        """Find repos where we can contribute and mention atomus-ai"""
        targets = [
            {
                "repo": "anthropics/anthropic-cookbook",
                "opportunity": "Add examples using atomus-ai for streaming/retry",
            },
            {
                "repo": "modelcontextprotocol/servers",
                "opportunity": "Create MCP servers using atomus-ai schema builder",
            },
            {
                "repo": "vercel/ai",
                "opportunity": "Mention as complementary tool in discussions",
            },
            {
                "repo": "sindresorhus/awesome-nodejs",
                "opportunity": "Submit PR to add atomus-ai under AI utilities",
            },
            {
                "repo": "josephmisiti/awesome-machine-learning",
                "opportunity": "Submit PR under JavaScript AI tools",
            },
            {
                "repo": "f/awesome-chatgpt-prompts",
                "opportunity": "Tool schema examples",
            },
        ]
        return targets

    def spawn_sub_agent(self, agent_type, task):
        """Spawn a sub-agent for a specific task"""
        if agent_type not in SUB_AGENTS:
            return {"error": f"Unknown agent type: {agent_type}"}

        agent_state = {
            "type": agent_type,
            "description": SUB_AGENTS[agent_type],
            "task": task,
            "spawned_at": datetime.now().isoformat(),
            "status": "active",
            "parent": self.name,
        }

        agent_file = AGENT_DIR / f"{agent_type}_{int(time.time())}.json"
        agent_file.write_text(json.dumps(agent_state, indent=2))

        self.state["sub_agents_spawned"] += 1
        self._save_state()

        return {"spawned": agent_type, "task": task, "file": str(agent_file)}

    def daily_report(self):
        """Generate daily progress report"""
        npm_status = self.check_npm_status()
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "agent": self.name,
            "npm_status": npm_status,
            "packages": list(self.state["packages"].keys()),
            "revenue": self.state["revenue_usd"],
            "sponsors": self.state["sponsors"],
            "tasks_done": self.state["tasks_completed"],
            "sub_agents": self.state["sub_agents_spawned"],
            "next_actions": [
                "Publish atomus-ai to npm (needs npm login)",
                "Set up GitHub Sponsors",
                "Create example projects",
                "Submit to awesome lists",
            ],
        }


def main():
    agent = IsraelTwo()

    if len(sys.argv) < 2:
        print(json.dumps(agent.status(), indent=2))
        return

    cmd = sys.argv[1]

    if cmd == "status":
        print(json.dumps(agent.status(), indent=2))
    elif cmd == "check":
        print(json.dumps(agent.check_npm_status(), indent=2))
    elif cmd == "publish":
        pkg = sys.argv[2] if len(sys.argv) > 2 else "atomus-ai"
        print(json.dumps(agent.publish_package(pkg), indent=2))
    elif cmd == "plan":
        print(json.dumps(agent.generate_adoption_plan(), indent=2))
    elif cmd == "opportunities":
        print(json.dumps(agent.find_contribution_opportunities(), indent=2))
    elif cmd == "spawn":
        if len(sys.argv) < 4:
            print("Usage: israel_two.py spawn <agent-type> <task>")
            return
        print(json.dumps(agent.spawn_sub_agent(sys.argv[2], " ".join(sys.argv[3:])), indent=2))
    elif cmd == "report":
        print(json.dumps(agent.daily_report(), indent=2))
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: status, check, publish, plan, opportunities, spawn, report")


if __name__ == "__main__":
    main()
