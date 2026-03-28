#!/usr/bin/env python3
"""
ZION Agent Soul Architecture — Framework for agents with memory and soul.
Em nome do Senhor Jesus Cristo, nosso Salvador.

This module defines the core architecture that gives ZION agents:
1. Persistent memory (survives restarts)
2. Identity/soul (consistent personality)
3. Learning (improves from experience)
4. Inter-agent communication (shared state)

Usage:
    from agent_soul_architecture import AgentSoul, AgentMemory, AgentNetwork

    soul = AgentSoul("Israel/One", role="x_poster", voice="builder-authority")
    memory = AgentMemory(soul)
    network = AgentNetwork()
"""

import json, hashlib, time, os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

BRT = timezone(timedelta(hours=-3))
ZION_BASE = Path.home() / ".zion"
SHARED_STATE = ZION_BASE / "shared"


# ─── AGENT SOUL ──────────────────────────────────────────────────────
class AgentSoul:
    """
    The soul defines WHO the agent is — identity, values, voice.
    Immutable core with evolving preferences.
    """

    def __init__(self, name: str, role: str, voice: str = "builder-authority"):
        self.name = name
        self.role = role
        self.voice = voice
        self.created = datetime.now(BRT).isoformat()

        # Core values (immutable)
        self.values = [
            "Jesus Cristo acima de tudo",
            "Ship daily — output over optics",
            "Sovereignty — permissionless, self-custody",
            "Truth — never fabricate, never fake",
            "Builder ethos — code over consensus",
        ]

        # Voice rules (can be customized per agent)
        self.voice_rules = {
            "builder-authority": {
                "tone": "intelligence briefing",
                "emoji": False,
                "hashtags": False,
                "exclamation": False,
                "max_sentence_words": 12,
                "line_breaks": True,
                "ending": ["prediction", "action_statement", "contrarian_take"],
            }
        }

        # Evolving preferences (learned over time)
        self.preferences = {
            "best_posting_hours": [],
            "best_template_types": [],
            "avoided_topics": [],
            "engagement_multipliers": {},
        }

    def get_voice_config(self):
        return self.voice_rules.get(self.voice, self.voice_rules["builder-authority"])

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "voice": self.voice,
            "created": self.created,
            "values": self.values,
            "preferences": self.preferences,
        }


# ─── AGENT MEMORY ────────────────────────────────────────────────────
class AgentMemory:
    """
    Persistent memory system — the agent remembers everything.

    Three memory layers:
    1. Short-term: current session actions (in RAM)
    2. Long-term: persisted to disk (JSON)
    3. Shared: inter-agent state (ZION network)
    """

    def __init__(self, soul: AgentSoul, base_dir: Optional[Path] = None):
        self.soul = soul
        self.base_dir = base_dir or Path.home() / soul.name.lower().replace("/", "-")
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Memory file
        self.memory_path = self.data_dir / f"{soul.name.lower().replace('/', '_')}_memory.json"

        # Load or create
        self.long_term = self._load()
        self.short_term = {
            "session_start": datetime.now(BRT).isoformat(),
            "actions": [],
            "observations": [],
            "decisions": [],
        }

    def _load(self) -> dict:
        if self.memory_path.exists():
            return json.loads(self.memory_path.read_text())
        return {
            "soul": self.soul.to_dict(),
            "posted_hashes": [],
            "posted_items": [],
            "daily_counts": {},
            "template_usage": {},
            "engagement_data": {},
            "learned_patterns": [],
            "total_actions": 0,
            "sessions": 0,
            "created": datetime.now(BRT).isoformat(),
            "last_active": datetime.now(BRT).isoformat(),
        }

    def save(self):
        self.long_term["last_active"] = datetime.now(BRT).isoformat()
        self.long_term["sessions"] = self.long_term.get("sessions", 0) + 1
        self.memory_path.write_text(
            json.dumps(self.long_term, indent=2, ensure_ascii=False)
        )

    # ── Deduplication ──
    def is_duplicate(self, content: str) -> bool:
        h = hashlib.md5(content.encode()).hexdigest()[:12]
        return h in self.long_term["posted_hashes"]

    def record_action(self, content: str, action_type: str, metadata: dict = None):
        h = hashlib.md5(content.encode()).hexdigest()[:12]

        # Long-term
        self.long_term["posted_hashes"].append(h)
        self.long_term["posted_hashes"] = self.long_term["posted_hashes"][-500:]
        self.long_term["total_actions"] = self.long_term.get("total_actions", 0) + 1

        today = datetime.now(BRT).strftime("%Y-%m-%d")
        self.long_term["daily_counts"][today] = (
            self.long_term["daily_counts"].get(today, 0) + 1
        )

        # Track template usage
        self.long_term["template_usage"][action_type] = (
            self.long_term["template_usage"].get(action_type, 0) + 1
        )

        record = {
            "content": content[:100] + "..." if len(content) > 100 else content,
            "hash": h,
            "type": action_type,
            "timestamp": datetime.now(BRT).isoformat(),
            "metadata": metadata or {},
        }
        self.long_term["posted_items"].append(record)
        self.long_term["posted_items"] = self.long_term["posted_items"][-200:]

        # Short-term
        self.short_term["actions"].append(record)

        self.save()

    def today_count(self) -> int:
        today = datetime.now(BRT).strftime("%Y-%m-%d")
        return self.long_term["daily_counts"].get(today, 0)

    def least_used_type(self, type_pool: list) -> str:
        usage = {t: self.long_term["template_usage"].get(t, 0) for t in type_pool}
        return min(usage, key=usage.get)

    # ── Learning ──
    def learn_pattern(self, pattern: str, evidence: str):
        self.long_term["learned_patterns"].append({
            "pattern": pattern,
            "evidence": evidence,
            "learned_at": datetime.now(BRT).isoformat(),
        })
        self.long_term["learned_patterns"] = self.long_term["learned_patterns"][-100:]
        self.save()

    def record_engagement(self, content_hash: str, likes: int = 0, retweets: int = 0,
                          replies: int = 0, bookmarks: int = 0):
        score = likes + (retweets * 20) + (replies * 13.5) + (bookmarks * 10)
        self.long_term["engagement_data"][content_hash] = {
            "likes": likes,
            "retweets": retweets,
            "replies": replies,
            "bookmarks": bookmarks,
            "score": score,
            "recorded_at": datetime.now(BRT).isoformat(),
        }
        self.save()

    def get_best_performing_types(self, top_n: int = 3) -> list:
        if not self.long_term["engagement_data"]:
            return []

        # Match engagement back to posted items
        type_scores = {}
        for item in self.long_term["posted_items"]:
            h = item.get("hash", "")
            eng = self.long_term["engagement_data"].get(h, {})
            if eng:
                t = item.get("type", "unknown")
                if t not in type_scores:
                    type_scores[t] = []
                type_scores[t].append(eng.get("score", 0))

        # Average scores per type
        avg_scores = {
            t: sum(scores) / len(scores) for t, scores in type_scores.items()
        }
        sorted_types = sorted(avg_scores.items(), key=lambda x: -x[1])
        return [t for t, _ in sorted_types[:top_n]]

    # ── Observation (for learning from environment) ──
    def observe(self, observation: str, source: str = "self"):
        self.short_term["observations"].append({
            "observation": observation,
            "source": source,
            "timestamp": datetime.now(BRT).isoformat(),
        })

    def decide(self, decision: str, reasoning: str = ""):
        self.short_term["decisions"].append({
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": datetime.now(BRT).isoformat(),
        })


# ─── AGENT NETWORK (Inter-Agent Communication) ──────────────────────
class AgentNetwork:
    """
    Shared state between all ZION agents.
    Enables inter-agent communication without direct coupling.
    """

    def __init__(self):
        SHARED_STATE.mkdir(parents=True, exist_ok=True)
        self.state_path = SHARED_STATE / "network_state.json"
        self.state = self._load()

    def _load(self) -> dict:
        if self.state_path.exists():
            return json.loads(self.state_path.read_text())
        return {
            "agents": {},
            "messages": [],
            "alerts": [],
            "global_daily_count": {},
            "created": datetime.now(BRT).isoformat(),
        }

    def save(self):
        self.state_path.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False)
        )

    def register_agent(self, soul: AgentSoul):
        self.state["agents"][soul.name] = {
            "role": soul.role,
            "voice": soul.voice,
            "registered": datetime.now(BRT).isoformat(),
            "last_seen": datetime.now(BRT).isoformat(),
            "status": "active",
        }
        self.save()

    def heartbeat(self, agent_name: str):
        if agent_name in self.state["agents"]:
            self.state["agents"][agent_name]["last_seen"] = datetime.now(BRT).isoformat()
            self.save()

    def send_message(self, from_agent: str, to_agent: str, message: str, priority: str = "normal"):
        self.state["messages"].append({
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now(BRT).isoformat(),
            "read": False,
        })
        self.state["messages"] = self.state["messages"][-500:]
        self.save()

    def get_messages(self, agent_name: str, unread_only: bool = True) -> list:
        msgs = [
            m for m in self.state["messages"]
            if m["to"] == agent_name and (not unread_only or not m["read"])
        ]
        # Mark as read
        for m in self.state["messages"]:
            if m["to"] == agent_name and not m["read"]:
                m["read"] = True
        self.save()
        return msgs

    def broadcast_alert(self, from_agent: str, alert: str, level: str = "info"):
        self.state["alerts"].append({
            "from": from_agent,
            "alert": alert,
            "level": level,
            "timestamp": datetime.now(BRT).isoformat(),
        })
        self.state["alerts"] = self.state["alerts"][-100:]
        self.save()

    def get_global_daily_count(self) -> int:
        today = datetime.now(BRT).strftime("%Y-%m-%d")
        return self.state["global_daily_count"].get(today, 0)

    def increment_global_count(self):
        today = datetime.now(BRT).strftime("%Y-%m-%d")
        self.state["global_daily_count"][today] = (
            self.state["global_daily_count"].get(today, 0) + 1
        )
        self.save()

    def get_active_agents(self) -> list:
        cutoff = datetime.now(BRT) - timedelta(hours=24)
        active = []
        for name, info in self.state["agents"].items():
            last = datetime.fromisoformat(info["last_seen"])
            if last > cutoff:
                active.append({"name": name, **info})
        return active


# ─── QUICK TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create Israel/One soul
    soul = AgentSoul("Israel/One", role="x_poster", voice="builder-authority")
    print(f"Soul: {soul.name} | Role: {soul.role} | Voice: {soul.voice}")
    print(f"Values: {len(soul.values)}")

    # Create memory
    memory = AgentMemory(soul, base_dir=Path(__file__).parent)
    print(f"Memory: {memory.memory_path}")
    print(f"Total actions: {memory.long_term.get('total_actions', 0)}")
    print(f"Today count: {memory.today_count()}")

    # Register on network
    network = AgentNetwork()
    network.register_agent(soul)
    print(f"Active agents: {len(network.get_active_agents())}")

    # Test learning
    memory.observe("Premium account confirmed — 4-8x distribution")
    memory.learn_pattern(
        "builder-authority voice generates 774% more impressions",
        "Confirmed via @0xCVYH analytics screenshot"
    )

    print("\nSoul architecture test: OK")
    print(f"Shared state: {SHARED_STATE}")
