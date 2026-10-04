from __future__ import annotations

import os
import json
from datetime import datetime
from typing import Any, Dict, List


class SessionMemory:
    """Stores recent assistant actions and interactions for context-aware reuse."""

    def __init__(self, storage_dir: str = "memory"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.history: List[Dict[str, Any]] = []

    def log(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "payload": payload,
        }
        self.history.append(entry)
        self._save()
        return entry

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.history[-limit:]

    def _save(self):
        path = os.path.join(self.storage_dir, "session_memory.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.history, handle, indent=2)

    def load(self):
        path = os.path.join(self.storage_dir, "session_memory.json")
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as handle:
            self.history = json.load(handle)
        return self.history
