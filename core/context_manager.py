from __future__ import annotations

from core.memory_store import MemoryStore
from core.user_profile import UserProfile


class ContextManager:
    """Combines persistent user memory and profile context into a single assistant context."""

    def __init__(self):
        self.profile = UserProfile()
        self.memory = MemoryStore()

    def build_context(self, prompt: str, recent_n: int = 5) -> dict:
        recent = self.memory.get_recent_interactions(recent_n)
        profile = self.profile.get_summary()
        facts = self.memory.get_facts()

        return {
            "user_profile": profile,
            "recent_interactions": recent,
            "known_facts": facts,
            "current_prompt": prompt,
        }

    def enrich_prompt(self, prompt: str, recent_n: int = 5) -> str:
        context = self.build_context(prompt, recent_n)
        profile = context["user_profile"]
        facts = context["known_facts"]
        recent = context["recent_interactions"]

        prompt_parts = [
            "You are a helpful personal AI assistant.",
            f"The user's name is {profile.get('name', 'User')}.",
            f"Preferences: {profile.get('preferences', {})}",
        ]

        if facts:
            prompt_parts.append("Known facts:")
            for fact in facts[-5:]:
                prompt_parts.append(f"- {fact.get('fact', '')}")

        if recent:
            prompt_parts.append("Recent interactions:")
            for item in recent[-3:]:
                prompt_parts.append(f"- User: {item.get('prompt', '')} | Assistant: {item.get('response', '')}")

        prompt_parts.append(f"Current request: {prompt}")
        return "\n".join(prompt_parts)

    def remember_response(self, prompt: str, response: str):
        self.memory.add_interaction(prompt, response)
        self.profile.remember_topic(prompt[:80])
