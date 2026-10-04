from __future__ import annotations

from typing import Dict, Any

from app.response_formatter import ResponseFormatter
from core.content_pipeline import ContentPipeline
from core.system_monitor import SystemMonitor


class AssistantController:
    """Routes user intents to the right functional modules."""

    def __init__(self, dashboard=None):
        self.dashboard = dashboard
        self.pipeline = ContentPipeline()

    def handle_command(self, text: str) -> Dict[str, Any]:
        command = (text or "").strip().lower()

        if not command:
            return {"status": "empty", "message": "No command received."}

        if "status" in command or "health" in command:
            system = SystemMonitor.get_status()
            ollama = SystemMonitor.check_ollama()
            return {
                "status": "ok",
                "type": "system_status",
                "system": system,
                "ollama": ollama,
            }

        if "youtube" in command or "content" in command or "video idea" in command:
            topic = self._extract_topic(command, default="AI automation workflow")
            bundle = self.pipeline.build_bundle(topic)
            return {
                "status": "ok",
                "type": "content_generation",
                "topic": topic,
                "bundle": bundle,
            }

        if "image" in command:
            topic = self._extract_topic(command, default="futuristic dashboard")
            result = self.pipeline.image_generator.generate(topic)
            return {
                "status": "ok",
                "type": "image_generation",
                "topic": topic,
                "result": result,
            }

        if "blender" in command or "3d" in command:
            topic = self._extract_topic(command, default="futuristic robot")
            result = self.pipeline.blender_generator.create_asset(topic)
            return {
                "status": "ok",
                "type": "blender_generation",
                "topic": topic,
                "result": result,
            }

        return {
            "status": "ok",
            "type": "fallback",
            "message": f"I can help with that: {text}",
        }

    def _extract_topic(self, command: str, default: str) -> str:
        cleaned = command.replace("create", "").replace("generate", "").replace("make", "")
        cleaned = cleaned.replace("youtube", "").replace("image", "").replace("blender", "").replace("3d", "")
        cleaned = cleaned.replace("video", "").replace("content", "")
        cleaned = " ".join(cleaned.split())
        return cleaned.strip() or default

    def process_text(self, text: str) -> str:
        result = self.handle_command(text)
        action_type = result.get("type", "fallback")

        if action_type == "system_status":
            return ResponseFormatter.format_system_status(result)
        if action_type == "content_generation":
            return ResponseFormatter.format_content_bundle(result)
        if action_type == "image_generation":
            return ResponseFormatter.format_image_result(result)
        if action_type == "blender_generation":
            return ResponseFormatter.format_blender_result(result)
        return ResponseFormatter.format_fallback(text)

    def start(self):
        if self.dashboard is not None:
            self.dashboard.set_assistant_response("Assistant online and ready")
        return True
