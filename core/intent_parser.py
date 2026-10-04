from __future__ import annotations

import re
from typing import Dict, Any


class IntentParser:
    """Heuristic parser for Jarvis voice and text commands."""

    @staticmethod
    def parse(command: str) -> Dict[str, Any]:
        text = (command or "").strip()
        if not text:
            return {"type": "empty", "topic": "", "raw": text}

        normalized = text.lower()

        if any(keyword in normalized for keyword in ["status", "health", "check system", "system status"]):
            return {"type": "system_status", "topic": "system", "raw": text}

        if any(keyword in normalized for keyword in ["help", "what can you do", "commands"]):
            return {"type": "help", "topic": "assistant", "raw": text}

        if any(keyword in normalized for keyword in ["blender", "3d scene", "3d asset", "render scene"]):
            return {"type": "blender_generation", "topic": IntentParser._extract_topic(text), "raw": text}

        if any(keyword in normalized for keyword in ["image", "thumbnail", "cover art", "poster", "hero image"]):
            return {"type": "image_generation", "topic": IntentParser._extract_topic(text), "raw": text}

        if any(keyword in normalized for keyword in ["youtube", "video idea", "content pack", "content brief", "video project", "video script"]):
            return {"type": "content_generation", "topic": IntentParser._extract_topic(text), "raw": text}

        if any(keyword in normalized for keyword in ["create", "generate", "make", "build"]):
            if "image" in normalized:
                return {"type": "image_generation", "topic": IntentParser._extract_topic(text), "raw": text}
            if "blender" in normalized or "3d" in normalized:
                return {"type": "blender_generation", "topic": IntentParser._extract_topic(text), "raw": text}
            if "youtube" in normalized or "video" in normalized or "content" in normalized:
                return {"type": "content_generation", "topic": IntentParser._extract_topic(text), "raw": text}

        return {"type": "fallback", "topic": "", "raw": text}

    @staticmethod
    def _extract_topic(command: str) -> str:
        cleaned = command.strip()
        for keyword in [
            "create ", "generate ", "make ", "build ",
            "a ", "an ", "the ",
            "youtube ", "video ", "content ", "image ", "thumbnail ", "cover ",
            "blender ", "3d ", "scene ", "asset ", "idea ",
        ]:
            if cleaned.lower().startswith(keyword):
                cleaned = cleaned[len(keyword):]
                break

        cleaned = re.sub(r"\b(status|health|check|system|assistant|jarvis|help)\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip(" .,-_:/")
        if not cleaned:
            return "AI automation workflow"
        return cleaned
