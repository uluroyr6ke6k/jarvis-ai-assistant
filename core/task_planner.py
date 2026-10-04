from __future__ import annotations

from typing import Any, Dict, List

from core.automation_engine import AutomationEngine
from core.context_manager import ContextManager
from core.session_memory import SessionMemory


class TaskPlanner:
    """Turns natural language requests into actionable executable task plans."""

    def __init__(self):
        self.memory = SessionMemory()
        self.memory.load()
        self.automation = AutomationEngine()
        self.context = ContextManager()

    def plan(self, request: str) -> Dict[str, Any]:
        text = (request or "").strip()
        if not text:
            return {"status": "empty", "tasks": []}

        enriched = self.context.enrich_prompt(text)
        tasks: List[str] = []

        lowered = text.lower()
        if any(keyword in lowered for keyword in ["status", "health", "system"]):
            tasks.append("status")

        if any(keyword in lowered for keyword in ["youtube", "open youtube"]):
            tasks.append("open_youtube")

        if any(keyword in lowered for keyword in ["chrome", "open chrome"]):
            tasks.append("open_chrome")

        if any(keyword in lowered for keyword in ["files", "explorer"]):
            tasks.append("open_files")

        if any(keyword in lowered for keyword in ["settings"]):
            tasks.append("open_settings")

        if any(keyword in lowered for keyword in ["screenshot", "screen capture"]):
            tasks.append("take_screenshot")

        if any(keyword in lowered for keyword in ["remember", "save fact", "note that"]):
            if "remember" in lowered:
                fact = text.split("remember", 1)[1].strip(" :-")
                tasks.append(f"remember_fact:{fact or 'new fact'}")
            elif "note that" in lowered:
                note = text.split("note that", 1)[1].strip(" :-")
                tasks.append(f"note:{note or 'new note'}")

        if not tasks:
            tasks.append("help")

        self.memory.log("task_plan_created", {"request": text, "enriched_prompt": enriched, "tasks": tasks})
        return {"status": "ok", "request": text, "tasks": tasks}

    def execute(self, request: str) -> Dict[str, Any]:
        plan = self.plan(request)
        if plan["status"] != "ok":
            return plan

        results = []
        for task in plan["tasks"]:
            result = self.automation.execute_task(task)
            results.append({"task": task, "result": result})

        outcome = {
            "status": "ok",
            "request": request,
            "tasks": plan["tasks"],
            "results": results,
        }
        self.memory.log("task_plan_executed", outcome)
        return outcome
