from __future__ import annotations

from typing import Any, Dict, List

from core.automation_engine import AutomationEngine
from core.session_memory import SessionMemory


class WorkflowOrchestrator:
    """Coordinates multi-step tasks while maintaining awareness of previous actions."""

    def __init__(self):
        self.memory = SessionMemory()
        self.memory.load()
        self.automation = AutomationEngine()

    def execute(self, task: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        payload = payload or {}
        task_name = (task or "").strip()
        self.memory.log("workflow_execution", {"task": task_name, "payload": payload})

        results: List[Dict[str, Any]] = []
        steps = self._normalize_steps(task_name, payload)

        for step in steps:
            result = self._run_step(step)
            results.append({"step": step, "result": result})

        context = {"recent_actions": self.memory.get_recent(5), "steps": results}
        final_result = {
            "task": task_name,
            "status": "ok",
            "context": context,
            "payload": payload,
            "results": results,
        }

        self.memory.log("workflow_result", {"task": task_name, "result": final_result})
        return final_result

    def _normalize_steps(self, task: str, payload: Dict[str, Any]) -> List[str]:
        if payload.get("steps"):
            return [str(step) for step in payload["steps"]]

        if "|" in task:
            return [part.strip() for part in task.split("|") if part.strip()]

        if ";" in task:
            return [part.strip() for part in task.split(";") if part.strip()]

        return [task] if task else []

    def _run_step(self, step: str) -> Dict[str, Any]:
        normalized_step = (step or "").strip()
        if not normalized_step:
            return {"status": "empty", "type": "empty", "result": "No step to execute."}

        if normalized_step.lower() in {"status", "health", "system_status", "check_status"}:
            return self.automation.execute_task(normalized_step)

        if normalized_step.lower().startswith("remember ") or normalized_step.lower().startswith("remember_fact:"):
            return self.automation.execute_task(normalized_step)

        if normalized_step.lower().startswith("note ") or normalized_step.lower().startswith("note:"):
            return self.automation.execute_task(normalized_step)

        if normalized_step.lower() in {"open_youtube", "youtube", "open_chrome", "chrome", "open_files", "explorer", "file_explorer", "open_settings", "settings", "screenshot", "take_screenshot", "time", "what_time", "what time"}:
            return self.automation.execute_task(normalized_step)

        if normalized_step.lower() in {"help", "commands"}:
            return self.automation.execute_task(normalized_step)

        return {
            "status": "unsupported",
            "type": "unsupported",
            "result": f"Step '{normalized_step}' is not supported yet.",
        }

    def enqueue_batch(self, tasks: List[str]) -> List[Dict[str, Any]]:
        return [self.execute(task) for task in tasks]
