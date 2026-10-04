from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class MemoryStore:
    """Persistent memory for user interactions, long-term facts, and context."""

    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.memory_dir / "memory_store.json"
        self.data: Dict[str, Any] = {
            "facts": [],
            "interactions": [],
            "notes": [],
        }
        self.load()

    def load(self):
        if self.memory_file.exists():
            try:
                with self.memory_file.open("r", encoding="utf-8") as handle:
                    self.data = json.load(handle)
            except json.JSONDecodeError:
                self.data = {"facts": [], "interactions": [], "notes": []}

    def save(self):
        with self.memory_file.open("w", encoding="utf-8") as handle:
            json.dump(self.data, handle, indent=2)

    def add_fact(self, fact: str, metadata: Dict[str, Any] | None = None):
        entry = {"fact": fact, "metadata": metadata or {}}
        self.data["facts"].append(entry)
        self.save()

    def add_interaction(self, prompt: str, response: str):
        self.data["interactions"].append({"prompt": prompt, "response": response})
        self.save()

    def add_note(self, note: str):
        self.data["notes"].append({"note": note})
        self.save()

    def get_recent_interactions(self, limit: int = 5) -> List[Dict[str, str]]:
        return list(reversed(self.data.get("interactions", [])))[-limit:]

    def get_facts(self) -> List[Dict[str, Any]]:
        return self.data.get("facts", [])

    def get_summary(self) -> Dict[str, Any]:
        return {
            "facts": self.get_facts(),
            "recent_interactions": self.get_recent_interactions(),
            "notes": self.data.get("notes", []),
        }
