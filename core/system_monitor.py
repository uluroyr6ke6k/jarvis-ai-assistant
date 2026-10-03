import os
import shutil
import subprocess
from typing import Dict

import psutil


class SystemMonitor:
    """Collect basic system health information."""

    @staticmethod
    def get_cpu_usage() -> float:
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_usage() -> float:
        mem = psutil.virtual_memory()
        return mem.percent

    @staticmethod
    def get_disk_usage() -> float:
        disk = psutil.disk_usage('/')
        return (disk.used / disk.total) * 100

    @staticmethod
    def get_status() -> Dict[str, float]:
        return {
            "cpu": SystemMonitor.get_cpu_usage(),
            "memory": SystemMonitor.get_memory_usage(),
            "disk": SystemMonitor.get_disk_usage(),
        }

    @staticmethod
    def check_ollama() -> Dict[str, object]:
        installed = shutil.which("ollama") is not None
        reachable = False
        if installed:
            try:
                result = subprocess.run(
                    ["ollama", "list"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                reachable = result.returncode == 0
            except Exception:
                reachable = False

        return {
            "installed": installed,
            "reachable": reachable,
            "status": "ready" if installed and reachable else "missing_or_unreachable",
        }
