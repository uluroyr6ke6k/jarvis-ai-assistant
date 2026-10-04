from __future__ import annotations

from app.response_formatter import ResponseFormatter
from core.context_manager import ContextManager
from core.learning_assistant import LearningAssistant
from core.model_provider import ModelProvider
from core.session_memory import SessionMemory
from core.workflow_orchestrator import WorkflowOrchestrator


class AIServiceLayer:
    """Coordinates the local AI backend with memory, profile context, workflow execution, and learning."""

    def __init__(self):
        self.provider = ModelProvider()
        self.session_memory = SessionMemory()
        self.session_memory.load()
        self.workflow = WorkflowOrchestrator()
        self.context_manager = ContextManager()
        self.learning = LearningAssistant()

    def generate_response(self, prompt: str) -> dict:
        enriched_prompt = self.context_manager.enrich_prompt(prompt)
        context = self.context_manager.build_context(prompt)
        self.session_memory.log("ai_request", {"prompt": prompt, "enriched_prompt": enriched_prompt})

        result = self.provider.generate_text(enriched_prompt)
        if result["status"] != "ok":
            self.session_memory.log("ai_failure", {"prompt": prompt, "result": result})
            evaluation = self.learning.evaluate_task(prompt, {"status": "fallback", "type": "ai_failure", "result": result})
            return {
                "status": "fallback",
                "message": "Local AI backend is not available. Falling back to workflow assistance.",
                "context": context,
                "learning": evaluation,
            }

        self.session_memory.log("ai_success", {"prompt": prompt, "result": result})
        self.context_manager.remember_response(prompt, result["text"])
        evaluation = self.learning.evaluate_task(prompt, {"status": "ok", "type": "ai_response", "result": result})
        return {
            "status": "ok",
            "message": result["text"],
            "context": context,
            "learning": evaluation,
        }

    def orchestrate(self, task: str, payload: dict | None = None) -> dict:
        workflow_result = self.workflow.execute(task, payload or {})
        evaluation = self.learning.evaluate_task(task, {"status": "ok", "type": "workflow", "result": workflow_result})
        return {
            "status": "ok",
            "workflow": workflow_result,
            "learning": evaluation,
        }

    def format_text(self, prompt: str) -> str:
        result = self.generate_response(prompt)
        if result["status"] == "ok":
            return result["message"]
        return ResponseFormatter.format_fallback(prompt)
