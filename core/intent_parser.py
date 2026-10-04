from __future__ import annotations

from typing import Any, Dict, List


class IntentParser:
    """Heuristic parser for chained commands and workflow-style instructions."""

    @staticmethod
    def parse(command: str) -> Dict[str, Any]:
        text = (command or "").strip()
        if not text:
            return {"type": "empty", "topic": "", "raw": text, "steps": []}

        normalized = text.lower()

        if "|" in text or ";" in text:
            steps = [part.strip() for part in re.split(r"[|;]", text) if part.strip()]
            return {
                "type": "workflow_chain",
                "topic": "automation",
                "raw": text,
                "steps": steps,
            }

        if any(keyword in normalized for keyword in ["status", "health", "system status", "check system"]):
            return {"type": "system_status", "topic": "system", "raw": text, "steps": ["status"]}

        if any(keyword in normalized for keyword in ["remember", "save fact", "store fact"]):
            fact = IntentParser._extract_after_keyword(text, ["remember", "save fact", "store fact"])
            return {"type": "remember_fact", "topic": fact or "memory", "raw": text, "steps": [f"remember_fact:{fact or 'new fact'}"]}

        if any(keyword in normalized for keyword in ["note", "save note", "write note"]):
            note = IntentParser._extract_after_keyword(text, ["note", "save note", "write note"])
            return {"type": "save_note", "topic": note or "note", "raw": text, "steps": [f"note:{note or 'new note'}"]}

        if any(keyword in normalized for keyword in ["youtube", "open youtube"]):
            return {"type": "open_app", "topic": "youtube", "raw": text, "steps": ["open_youtube"]}

        if any(keyword in normalized for keyword in ["chrome", "open chrome"]):
            return {"type": "open_app", "topic": "chrome", "raw": text, "steps": ["open_chrome"]}

        if any(keyword in normalized for keyword in ["files", "explorer", "file explorer"]):
            return {"type": "open_app", "topic": "files", "raw": text, "steps": ["open_files"]}

        if any(keyword in normalized for keyword in ["settings", "open settings"]):
            return {"type": "open_app", "topic": "settings", "raw": text, "steps": ["open_settings"]}

        if any(keyword in normalized for keyword in ["screenshot", "take screenshot"]):
            return {"type": "system_action", "topic": "screenshot", "raw": text, "steps": ["take_screenshot"]}

        if any(keyword in normalized for keyword in ["time", "what time"]):
            return {"type": "system_action", "topic": "time", "raw": text, "steps": ["time"]}

        if any(keyword in normalized for keyword in ["help", "what can you do", "commands"]):
            return {"type": "help", "topic": "assistant", "raw": text, "steps": ["help"]}

        return {"type": "fallback", "topic": "", "raw": text, "steps": [text]}

    @staticmethod
    def _extract_after_keyword(text: str, keywords: List[str]) -> str:
        lowered = text.lower()
        for keyword in keywords:
            idx = lowered.find(keyword)
            if idx >= 0:
                result = text[idx + len(keyword):].strip(" :-")
                return result
        return ""


import re
