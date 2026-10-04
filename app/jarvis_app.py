from __future__ import annotations

from core.ai_service_layer import AIServiceLayer


class JarvisApp:
    """Main application shell that wires the assistant, model service, and workflow engine together."""

    def __init__(self):
        self.ai_service = AIServiceLayer()

    def process_user_input(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            return "I didn’t receive a command."

        result = self.ai_service.generate_response(prompt)
        if result["status"] == "ok":
            return result["message"]

        return "The local AI backend is unavailable. My workflow layer is still ready to help."

    def run_workflow(self, task: str, payload: dict | None = None):
        return self.ai_service.orchestrate(task, payload)
