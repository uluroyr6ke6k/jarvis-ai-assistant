from __future__ import annotations

from app.dashboard import JarvisDashboard
from app.jarvis_app import JarvisApp


class RuntimeController:
    """Coordinates the app shell and dashboard into a single live runtime loop."""

    def __init__(self):
        self.app = JarvisApp()
        self.dashboard = JarvisDashboard()

    def boot(self):
        self.dashboard.set_status_message("System online")
        self.dashboard.set_assistant_response("Ready")
        self.dashboard.set_listening_state(False)
        return True

    def process(self, prompt: str):
        self.dashboard.set_assistant_response("Processing...")
        response = self.app.process_user_input(prompt)
        self.dashboard.set_assistant_response(response)
        self.dashboard.set_status_message("Command complete")
        return response

    def run_workflow(self, task: str, payload: dict | None = None):
        return self.app.run_workflow(task, payload)
