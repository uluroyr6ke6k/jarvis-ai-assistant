from __future__ import annotations

from app.runtime_controller import RuntimeController


class JarvisRuntime:
    """Application bootstrap for the full Jarvis runtime."""

    def __init__(self):
        self.controller = RuntimeController()

    def start(self):
        self.controller.boot()
        return self.controller

    def handle(self, prompt: str):
        return self.controller.process(prompt)
