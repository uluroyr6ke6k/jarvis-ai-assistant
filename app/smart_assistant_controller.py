from __future__ import annotations

from app.assistant_controller import AssistantController
from core.intent_parser import IntentParser


class SmartAssistantController(AssistantController):
    """Uses intent parsing to route text and voice requests more reliably."""

    def __init__(self, dashboard=None):
        super().__init__(dashboard=dashboard)

    def handle_command(self, text: str):
        parsed = IntentParser.parse(text)
        command_type = parsed.get("type", "fallback")
        topic = parsed.get("topic", "AI automation workflow")

        if command_type == "system_status":
            from core.system_monitor import SystemMonitor
            system = SystemMonitor.get_status()
            ollama = SystemMonitor.check_ollama()
            return {
                "status": "ok",
                "type": "system_status",
                "system": system,
                "ollama": ollama,
            }

        if command_type == "content_generation":
            bundle = self.pipeline.build_bundle(topic)
            return {
                "status": "ok",
                "type": "content_generation",
                "topic": topic,
                "bundle": bundle,
            }

        if command_type == "image_generation":
            result = self.pipeline.image_generator.generate(topic)
            return {
                "status": "ok",
                "type": "image_generation",
                "topic": topic,
                "result": result,
            }

        if command_type == "blender_generation":
            result = self.pipeline.blender_generator.create_asset(topic)
            return {
                "status": "ok",
                "type": "blender_generation",
                "topic": topic,
                "result": result,
            }

        if command_type == "help":
            return {
                "status": "ok",
                "type": "fallback",
                "message": "Available actions: system status, content generation, image generation, Blender generation.",
            }

        return {
            "status": "ok",
            "type": "fallback",
            "message": f"I can help with that: {text}",
        }

    def process_text(self, text: str) -> str:
        result = self.handle_command(text)
        from app.response_formatter import ResponseFormatter
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
