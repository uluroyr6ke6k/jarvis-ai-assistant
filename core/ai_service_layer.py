from __future__ import annotations

from app.response_formatter import ResponseFormatter
from core.model_provider import ModelProvider
from core.session_memory import SessionMemory
from core.workflow_orchestrator import WorkflowOrchestrator


class AIServiceLayer:
    """Coordinates the local AI backend with memory and workflow execution."""

    def __init__(self):
        self.provider = ModelProvider()
        self.memory = SessionMemory()
        self.memory.load()
        self.workflow = WorkflowOrchestrator()

    def generate_response(self, prompt: str) -> dict:
        context = self.memory.get_recent(5)
        self.memory.log("ai_request", {"prompt": prompt})

        result = self.provider.generate_text(prompt)
        if result["status"] != "ok":
            self.memory.log("ai_failure", {"prompt": prompt, "result": result})
            return {
                "status": "fallback",
                "message": "Local AI backend is not available. Falling back to workflow assistance.",
                "context": context,
            }

        self.memory.log("ai_success", {"prompt": prompt, "result": result})
        return {
            "status": "ok",
            "message": result["text"],
            "context": context,
        }

    def orchestrate(self, task: str, payload: dict | None = None) -> dict:
        workflow_result = self.workflow.execute(task, payload or {})
        return {
            "status": "ok",
            "workflow": workflow_result,
        }

    def format_text(self, prompt: str) -> str:
        result = self.generate_response(prompt)
        if result["status"] == "ok":
            return result["message"]
        return ResponseFormatter.format_fallback(prompt)
