from __future__ import annotations

import os
import subprocess
from typing import Any, Dict, List


class ModelProvider:
    """Abstraction for local LLM providers like Ollama."""

    def __init__(self, backend: str = "ollama"):
        self.backend = backend

    def is_available(self) -> bool:
        if self.backend != "ollama":
            return False
        return subprocess.run(["which", "ollama"], capture_output=True, text=True).returncode == 0

    def generate_text(self, prompt: str, model: str = "llama3") -> Dict[str, Any]:
        if not self.is_available():
            return {
                "status": "unavailable",
                "message": "Ollama is not installed or not available on PATH.",
                "text": "",
            }

        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "message": result.stderr.strip() or "Model generation failed.",
                "text": "",
            }

        return {
            "status": "ok",
            "message": "Generated successfully.",
            "text": result.stdout.strip(),
        }

    def list_models(self) -> List[str]:
        if not self.is_available():
            return []
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return []
        return [line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip()]
