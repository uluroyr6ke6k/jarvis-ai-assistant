from __future__ import annotations

from typing import Any, Dict


class ResponseFormatter:
    """Formats structured action results into readable assistant messages."""

    @staticmethod
    def format_system_status(data: Dict[str, Any]) -> str:
        system = data.get("system", {})
        ollama = data.get("ollama", {})
        cpu = system.get("cpu", 0)
        memory = system.get("memory", 0)
        disk = system.get("disk", 0)
        status = ollama.get("status", "offline")
        return (
            f"System status: CPU {cpu:.1f}%, RAM {memory:.1f}%, Disk {disk:.1f}%. "
            f"Local AI: {status}."
        )

    @staticmethod
    def format_content_bundle(data: Dict[str, Any]) -> str:
        topic = data.get("topic", "your topic")
        bundle = data.get("bundle", {})
        youtube = bundle.get("youtube_brief", {})
        title = youtube.get("title", "Untitled video")
        duration = youtube.get("estimated_duration_minutes", "N/A")
        return (
            f"Content bundle ready for '{topic}'. "
            f"Main title: {title}. Estimated duration: {duration} minutes. "
            "I created the YouTube brief, image prompts, video plan, and 3D scene setup."
        )

    @staticmethod
    def format_image_result(data: Dict[str, Any]) -> str:
        topic = data.get("topic", "image")
        result = data.get("result", {})
        output = result.get("output_path", "not generated")
        return f"Image prompt created for '{topic}'. Output target: {output}."

    @staticmethod
    def format_blender_result(data: Dict[str, Any]) -> str:
        topic = data.get("topic", "3D concept")
        result = data.get("result", {})
        name = result.get("scene_name", "unnamed")
        return f"Blender scene '{name}' prepared for '{topic}'."

    @staticmethod
    def format_fallback(text: str) -> str:
        return f"I heard: '{text}'. I can help with system status, content generation, image generation, or Blender generation."
