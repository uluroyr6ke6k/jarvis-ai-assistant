from __future__ import annotations

from typing import Any, Dict

from core.command_executor import CommandExecutor
from core.context_manager import ContextManager
from core.memory_store import MemoryStore
from core.system_monitor import SystemMonitor


class AutomationEngine:
    """Handles concrete assistant actions like opening apps, checking system health, and storing facts."""

    def __init__(self):
        self.command_executor = CommandExecutor()
        self.context_manager = ContextManager()
        self.memory_store = MemoryStore()

    def execute_task(self, task: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        task_name = (task or "").strip().lower()
        payload = payload or {}

        if not task_name:
            return {"status": "empty", "type": "empty", "result": "No task provided."}

        if task_name in {"status", "health", "system_status", "check_status"}:
            return {
                "status": "ok",
                "type": "system_status",
                "result": SystemMonitor.get_status(),
            }

        if task_name in {"open_youtube", "youtube"}:
            return {"status": "ok", "type": "open_app", "result": self.command_executor.open_youtube()}

        if task_name in {"open_chrome", "chrome"}:
            return {"status": "ok", "type": "open_app", "result": self.command_executor.open_chrome()}

        if task_name in {"open_files", "explorer", "file_explorer"}:
            return {"status": "ok", "type": "open_app", "result": self.command_executor.open_files()}

        if task_name in {"open_settings", "settings"}:
            return {"status": "ok", "type": "open_app", "result": self.command_executor.open_settings()}

        if task_name in {"screenshot", "take_screenshot"}:
            return {"status": "ok", "type": "system_action", "result": self.command_executor.take_screenshot()}

        if task_name in {"time", "what_time", "what time"}:
            return {"status": "ok", "type": "system_action", "result": self.command_executor.get_time()}

        if task_name.startswith("remember "):
            fact = task_name.replace("remember ", "", 1).strip()
            if not fact:
                return {"status": "ok", "type": "memory", "result": "No fact provided to remember."}
            self.memory_store.add_fact(fact)
            return {"status": "ok", "type": "memory", "result": f"Saved fact: {fact}"}

        if task_name.startswith("note "):
            note = task_name.replace("note ", "", 1).strip()
            if not note:
                return {"status": "ok", "type": "memory", "result": "No note provided."}
            self.memory_store.add_note(note)
            return {"status": "ok", "type": "memory", "result": f"Saved note: {note}"}

        if task_name.startswith("remember_fact:"):
            fact = task_name.split(":", 1)[1].strip()
            if not fact:
                return {"status": "ok", "type": "memory", "result": "No fact provided to remember."}
            self.memory_store.add_fact(fact)
            return {"status": "ok", "type": "memory", "result": f"Saved fact: {fact}"}

        if task_name.startswith("note:"):
            note = task_name.split(":", 1)[1].strip()
            if not note:
                return {"status": "ok", "type": "memory", "result": "No note provided."}
            self.memory_store.add_note(note)
            return {"status": "ok", "type": "memory", "result": f"Saved note: {note}"}

        if task_name in {"help", "commands"}:
            return {
                "status": "ok",
                "type": "help",
                "result": [
                    "status",
                    "open_youtube",
                    "open_chrome",
                    "open_files",
                    "open_settings",
                    "screenshot",
                    "time",
                    "remember <fact>",
                    "note <text>",
                ],
            }

        return {
            "status": "unsupported",
            "type": "unsupported",
            "result": f"Task '{task}' is not supported yet by the automation engine.",
        }
