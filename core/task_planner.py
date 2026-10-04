from __future__ import annotations

from typing import Any, Dict, List

from core.automation_engine import AutomationEngine
from core.context_manager import ContextManager
from core.learning_assistant import LearningAssistant
from core.session_memory import SessionMemory


class TaskPlanner:
    """Turns natural language requests into actionable executable task plans and learns from outcomes."""

    def __init__(self):
        self.memory = SessionMemory()
        self.memory.load()
        self.automation = AutomationEngine()
        self.context = ContextManager()
        self.learning = LearningAssistant()

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

        ranked_tasks = self.learning.improve_plan(text, tasks)
        self.memory.log("task_plan_created", {"request": text, "enriched_prompt": enriched, "tasks": ranked_tasks})
        return {
            "status": "ok",
            "request": text,
            "tasks": ranked_tasks,
            "learning_summary": self.learning.generate_learning_summary(),
        }

    def execute(self, request: str) -> Dict[str, Any]:
        plan = self.plan(request)
        if plan["status"] != "ok":
            return plan

        results = []
        for task in plan["tasks"]:
            result = self.automation.execute_task(task)
            evaluation = self.learning.evaluate_task(task, result)
            results.append({"task": task, "result": result, "evaluation": evaluation})

        outcome = {
            "status": "ok",
            "request": request,
            "tasks": plan["tasks"],
            "results": results,
            "learning_summary": self.learning.generate_learning_summary(),
        }
        self.memory.log("task_plan_executed", outcome)
        return outcome
