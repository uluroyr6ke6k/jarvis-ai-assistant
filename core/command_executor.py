import subprocess
import webbrowser
import os
import pyautogui
import psutil
from datetime import datetime

from core.logger import log_info, log_error


class CommandExecutor:
    """Executes structured commands and PC automation actions."""

    def __init__(self):
        self.quick_apps = {
            "youtube": "https://youtube.com",
            "chrome": "chrome",
            "files": "explorer.exe",
            "settings": "ms-settings:",
            "vscode": "code",
            "spotify": "spotify",
            "notion": "notion",
        }

    def execute(self, text: str) -> str:
        cmd = (text or "").lower().strip()
        if not cmd:
            return ""

        log_info(f"Executing command: {cmd}")

        if "open youtube" in cmd or "youtube" in cmd:
            return self.open_youtube()
        if "open chrome" in cmd or "chrome" in cmd:
            return self.open_chrome()
        if "open files" in cmd or "file explorer" in cmd:
            return self.open_files()
        if "open settings" in cmd or "settings" in cmd:
            return self.open_settings()
        if "screenshot" in cmd:
            return self.take_screenshot()
        if "what time" in cmd or "time is it" in cmd:
            return self.get_time()
        if "what's the weather" in cmd or "weather" in cmd:
            return self.get_weather()
        if "shutdown" in cmd:
            return self.shutdown_pc()
        if "restart" in cmd:
            return self.restart_pc()
        if "mute" in cmd:
            return self.mute_volume()
        if "volume up" in cmd:
            return self.volume_up()
        if "volume down" in cmd:
            return self.volume_down()

        return ""

    def open_youtube(self):
        try:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube."
        except Exception as e:
            log_error(f"Error opening youtube: {e}", e)
            return "I couldn't open YouTube."

    def open_chrome(self):
        try:
            subprocess.Popen("chrome")
            return "Opening Chrome."
        except Exception as e:
            log_error(f"Error opening Chrome: {e}", e)
            return "I couldn't open Chrome."

    def open_files(self):
        try:
            subprocess.Popen("explorer.exe")
            return "Opening File Explorer."
        except Exception as e:
            log_error(f"Error opening File Explorer: {e}", e)
            return "I couldn't open File Explorer."

    def open_settings(self):
        try:
            subprocess.Popen("ms-settings:")
            return "Opening Windows Settings."
        except Exception as e:
            log_error(f"Error opening settings: {e}", e)
            return "I couldn't open Settings."

    def take_screenshot(self):
        try:
            folder = "screenshots"
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            pyautogui.screenshot(filename)
            return f"Screenshot saved to {filename}."
        except Exception as e:
            log_error(f"Error taking screenshot: {e}", e)
            return "I couldn't take a screenshot."

    def get_time(self):
        return f"The current time is {datetime.now().strftime('%H:%M')}"

    def get_weather(self):
        return "I can provide weather information if you connect a weather API or a local data source."

    def shutdown_pc(self):
        try:
            os.system("shutdown /s /t 10")
            return "Shutdown initiated."
        except Exception as e:
            log_error(f"Error shutting down: {e}", e)
            return "I couldn't shutdown the computer."

    def restart_pc(self):
        try:
            os.system("shutdown /r /t 10")
            return "Restart initiated."
        except Exception as e:
            log_error(f"Error restarting PC: {e}", e)
            return "I couldn't restart the computer."

    def mute_volume(self):
        try:
            os.system("nircmd mutesysvolume 1")
            return "Volume muted."
        except Exception as e:
            log_error(f"Error muting volume: {e}", e)
            return "I couldn't mute the volume."

    def volume_up(self):
        try:
            os.system("nircmd changesysvolume 5000")
            return "Volume increased."
        except Exception as e:
            log_error(f"Error increasing volume: {e}", e)
            return "I couldn't increase the volume."

    def volume_down(self):
        try:
            os.system("nircmd changesysvolume -5000")
            return "Volume decreased."
        except Exception as e:
            log_error(f"Error decreasing volume: {e}", e)
            return "I couldn't decrease the volume."


executor_singleton = None


def get_executor():
    global executor_singleton
    if executor_singleton is None:
        executor_singleton = CommandExecutor()
    return executor_singleton
