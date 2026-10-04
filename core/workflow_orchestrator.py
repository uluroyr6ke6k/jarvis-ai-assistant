from __future__ import annotations

from typing import Any, Dict, List

from core.session_memory import SessionMemory


class WorkflowOrchestrator:
    """Coordinates multi-step tasks while maintaining awareness of previous actions."""

    def __init__(self):
        self.memory = SessionMemory()
        self.memory.load()

    def execute(self, task: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        payload = payload or {}
        self.memory.log("workflow_execution", {"task": task, "payload": payload})

        recent = self.memory.get_recent(5)
        context = {"recent_actions": recent}
        result = {
            "task": task,
            "status": "ok",
            "context": context,
            "payload": payload,
        }

        self.memory.log("workflow_result", {"task": task, "result": result})
        return result

    def enqueue_batch(self, tasks: List[str]) -> List[Dict[str, Any]]:
        return [self.execute(task) for task in tasks]
