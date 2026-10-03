from core.system_monitor import SystemMonitor


class StartupChecker:
    """Ensures the assistant can boot cleanly and checks local services."""

    def __init__(self):
        self.system_status = SystemMonitor.get_status()

    def check(self):
        ollama = SystemMonitor.check_ollama()
        return {
            "system": self.system_status,
            "ollama": ollama,
            "ready": ollama.get("status") == "ready",
        }
