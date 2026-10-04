from __future__ import annotations

import json
import os
from typing import Any, Dict


class UserProfile:
    """Stores user preferences, habits, and personalized context for the assistant."""

    def __init__(self, profile_dir: str = "profiles"):
        self.profile_dir = profile_dir
        self.profile_path = os.path.join(profile_dir, "user_profile.json")
        self.profile: Dict[str, Any] = {
            "name": "User",
            "preferences": {
                "tone": "helpful",
                "language": "en",
                "dark_mode": True,
            },
            "habits": [],
            "recent_topics": [],
        }
        os.makedirs(profile_dir, exist_ok=True)
        self.load()

    def load(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r", encoding="utf-8") as handle:
                try:
                    loaded = json.load(handle)
                    self.profile.update(loaded)
                except json.JSONDecodeError:
                    pass

    def save(self):
        with open(self.profile_path, "w", encoding="utf-8") as handle:
            json.dump(self.profile, handle, indent=2)

    def update_preference(self, key: str, value: Any):
        self.profile["preferences"][key] = value
        self.save()

    def remember_habit(self, habit: str):
        if habit not in self.profile["habits"]:
            self.profile["habits"].append(habit)
        self.save()

    def remember_topic(self, topic: str):
        if topic not in self.profile["recent_topics"]:
            self.profile["recent_topics"].append(topic)
        self.save()

    def get_summary(self) -> Dict[str, Any]:
        return {
            "name": self.profile.get("name", "User"),
            "preferences": self.profile.get("preferences", {}),
            "habits": self.profile.get("habits", []),
            "recent_topics": self.profile.get("recent_topics", []),
        }
