from __future__ import annotations

from typing import Dict, Any

from app.response_formatter import ResponseFormatter
from core.content_pipeline import ContentPipeline
from core.task_planner import TaskPlanner
from core.system_monitor import SystemMonitor


class AssistantController:
    """Routes user intents to the right functional modules and adaptive task planner."""

    def __init__(self, dashboard=None):
        self.dashboard = dashboard
        self.pipeline = ContentPipeline()
        self.task_planner = TaskPlanner()

    def handle_command(self, text: str) -> Dict[str, Any]:
        command = (text or "").strip().lower()
        if not command:
            return {"status": "empty", "type": "empty", "message": "No command received."}

        if command in {"help", "commands", "what can you do"}:
            return {
                "status": "ok",
                "type": "help",
                "message": "Commands: status, youtube, browser, files, settings, screenshot, remember fact, note, help.",
            }

        if "status" in command or "health" in command:
            system = SystemMonitor.get_status(); ollama = SystemMonitor.check_ollama()
            return {"status": "ok", "type": "system_status", "system": system, "ollama": ollama}

        if "remember" in command or "note" in command:
            plan = self.task_planner.plan(command)
            if plan["status"] == "ok":
                result = self.task_planner.execute(command)
                return {"status": "ok", "type": "task_plan", "plan": result, "message": "Memory updated."}

        if "youtube" in command or "content" in command or "video idea" in command:
            topic = self._extract_topic(command, default="AI automation workflow")
            bundle = self.pipeline.build_bundle(topic)
            return {"status": "ok", "type": "content_generation", "topic": topic, "bundle": bundle}

        if "browse" in command or "browser" in command or "chrome" in command or "open chrome" in command:
            plan = self.task_planner.plan(command)
            result = self.task_planner.execute(command)
            return {"status": "ok", "type": "task_plan", "plan": result, "message": "Browser action queued."}

        if "file" in command or "files" in command or "explorer" in command:
            plan = self.task_planner.plan(command)
            result = self.task_planner.execute(command)
            return {"status": "ok", "type": "task_plan", "plan": result, "message": "File action queued."}

        if "settings" in command:
            plan = self.task_planner.plan(command)
            result = self.task_planner.execute(command)
            return {"status": "ok", "type": "task_plan", "plan": result, "message": "Settings action queued."}

        if "screenshot" in command or "screen" in command:
            plan = self.task_planner.plan(command)
            result = self.task_planner.execute(command)
            return {"status": "ok", "type": "task_plan", "plan": result, "message": "Screenshot action queued."}

        if "image" in command:
            topic = self._extract_topic(command, default="futuristic dashboard")
            result = self.pipeline.image_generator.generate(topic)
            return {"status": "ok", "type": "image_generation", "topic": topic, "result": result}

        if "blender" in command or "3d" in command:
            topic = self._extract_topic(command, default="futuristic robot")
            result = self.pipeline.blender_generator.create_asset(topic)
            return {"status": "ok", "type": "blender_generation", "topic": topic, "result": result}

        plan = self.task_planner.plan(command)
        if plan.get("status") == "ok" and plan.get("tasks"):
            result = self.task_planner.execute(command)
            return {"status": "ok", "type": "task_plan", "plan": result, "message": "Task plan executed."}

        return {"status": "ok", "type": "fallback", "message": f"I can help with that: {text}"}

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
        if action_type == "task_plan":
            plan = result.get("plan", {})
            tasks = plan.get("tasks", []) if isinstance(plan, dict) else []
            if tasks:
                return f"Task plan executed: {' -> '.join(str(task) for task in tasks)}."
            return result.get("message", "Task plan processed.")
        if action_type == "help":
            return ResponseFormatter.format_help(result.get("message", ""))
        return ResponseFormatter.format_fallback(text)

    def start(self):
        if self.dashboard is not None:
            self.dashboard.set_assistant_response("Assistant online and ready")
        return True
