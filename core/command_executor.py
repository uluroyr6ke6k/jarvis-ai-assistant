"""
J.A.R.V.I.S. Command Executor
Handles execution of recognized commands
"""

import subprocess
import webbrowser
import pyautogui
import os
import psutil
from config import AUTO_LAUNCH_APPS
from core.logger import log_info, log_error, log_debug
from core.ai_engine import get_ai_engine
from core.voice_engine import get_voice_engine

class CommandExecutor:
    """Executes commands and controls PC"""
    
    def __init__(self):
        """Initialize command executor"""
        self.ai_engine = get_ai_engine()
        self.voice_engine = get_voice_engine()
        self.commands = self._register_commands()
        log_info("Command Executor initialized")
    
    def _register_commands(self):
        """Register available commands"""
        return {
            "open": self.open_app,
            "close": self.close_app,
            "weather": self.get_weather,
            "time": self.get_time,
            "date": self.get_date,
            "screenshot": self.take_screenshot,
            "volume": self.control_volume,
            "brightness": self.control_brightness,
            "shutdown": self.shutdown_pc,
            "restart": self.restart_pc,
            "sleep": self.sleep_pc,
            "youtube": self.open_youtube,
            "chrome": self.open_chrome,
            "files": self.open_files,
            "settings": self.open_settings,
        }
    
    def execute(self, command: str) -> str:
        """
        Execute a command
        
        Args:
            command: Command string to execute
        
        Returns:
            str: Command result/response
        """
        try:
            log_debug(f"Executing command: {command}")
            
            # Parse command
            command_lower = command.lower().strip()
            
            # Check for exact command matches
            for cmd_key, cmd_func in self.commands.items():
                if cmd_key in command_lower:
                    log_info(f"Found command: {cmd_key}")
                    result = cmd_func(command)
                    return result
            
            # If no exact match, use AI to interpret
            log_debug("No exact match, using AI interpretation")
            response = self.ai_engine.process_command(command)
            return response
            
        except Exception as e:
            log_error(f"Error executing command: {e}", e)
            return "I encountered an error executing that command."
    
    def open_app(self, command: str) -> str:
        """Open an application"""
        try:
            for app_name, app_path in AUTO_LAUNCH_APPS.items():
                if app_name.lower() in command.lower():
                    subprocess.Popen(app_path)
                    response = f"Opening {app_name}"
                    log_info(response)
                    return response
            return "Application not found in quick launch."
        except Exception as e:
            log_error(f"Error opening app: {e}", e)
            return "I couldn't open that application."
    
    def close_app(self, command: str) -> str:
        """Close an application"""
        try:
            # Extract app name from command
            app_name = command.replace("close", "").strip()
            
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    response = f"Closing {app_name}"
                    log_info(response)
                    return response
            
            return f"Couldn't find {app_name} to close."
        except Exception as e:
            log_error(f"Error closing app: {e}", e)
            return "I couldn't close that application."
    
    def take_screenshot(self, command: str = "") -> str:
        """Take a screenshot"""
        try:
            timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join("screenshots", filename)
            os.makedirs("screenshots", exist_ok=True)
            
            pyautogui.screenshot(filepath)
            response = f"Screenshot saved: {filename}"
            log_info(response)
            return response
        except Exception as e:
            log_error(f"Error taking screenshot: {e}", e)
            return "I couldn't take a screenshot."
    
    def control_volume(self, command: str) -> str:
        """Control system volume"""
        try:
            if "up" in command.lower():
                os.system("nircmd changesysvolume 5000")
                return "Volume increased"
            elif "down" in command.lower():
                os.system("nircmd changesysvolume -5000")
                return "Volume decreased"
            elif "mute" in command.lower():
                os.system("nircmd mutesysvolume 1")
                return "Muted"
            return "Volume control not recognized."
        except Exception as e:
            log_error(f"Error controlling volume: {e}", e)
            return "I couldn't control the volume."
    
    def control_brightness(self, command: str) -> str:
        """Control screen brightness"""
        try:
            if "up" in command.lower():
                os.system("nircmd setbrightness 100")
                return "Brightness increased"
            elif "down" in command.lower():
                os.system("nircmd setbrightness 50")
                return "Brightness decreased"
            return "Brightness control not recognized."
        except Exception as e:
            log_error(f"Error controlling brightness: {e}", e)
            return "I couldn't control the brightness."
    
    def shutdown_pc(self, command: str = "") -> str:
        """Shutdown PC"""
        try:
            self.voice_engine.speak("Shutting down in 30 seconds. Cancel by pressing Escape.")
            os.system("shutdown /s /t 30")
            return "Shutdown initiated"
        except Exception as e:
            log_error(f"Error shutting down: {e}", e)
            return "I couldn't shutdown the PC."
    
    def restart_pc(self, command: str = "") -> str:
        """Restart PC"""
        try:
            self.voice_engine.speak("Restarting in 30 seconds. Cancel by pressing Escape.")
            os.system("shutdown /r /t 30")
            return "Restart initiated"
        except Exception as e:
            log_error(f"Error restarting: {e}", e)
            return "I couldn't restart the PC."
    
    def sleep_pc(self, command: str = "") -> str:
        """Put PC to sleep"""
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "PC going to sleep"
        except Exception as e:
            log_error(f"Error sleeping: {e}", e)
            return "I couldn't put the PC to sleep."
    
    def get_weather(self, command: str) -> str:
        """Get weather information"""
        try:
            response = self.ai_engine.process_command(f"What's the weather? {command}")
            return response
        except Exception as e:
            log_error(f"Error getting weather: {e}", e)
            return "I couldn't get the weather information."
    
    def get_time(self, command: str = "") -> str:
        """Get current time"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M")
        return f"Current time is {time_str}"
    
    def get_date(self, command: str = "") -> str:
        """Get current date"""
        from datetime import datetime
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"
    
    def open_youtube(self, command: str) -> str:
        """Open YouTube"""
        try:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube"
        except Exception as e:
            log_error(f"Error opening YouTube: {e}", e)
            return "I couldn't open YouTube."
    
    def open_chrome(self, command: str) -> str:
        """Open Chrome"""
        try:
            subprocess.Popen("chrome")
            return "Opening Chrome"
        except Exception as e:
            log_error(f"Error opening Chrome: {e}", e)
            return "I couldn't open Chrome."
    
    def open_files(self, command: str) -> str:
        """Open File Explorer"""
        try:
            subprocess.Popen("explorer.exe")
            return "Opening File Explorer"
        except Exception as e:
            log_error(f"Error opening files: {e}", e)
            return "I couldn't open File Explorer."
    
    def open_settings(self, command: str) -> str:
        """Open Windows Settings"""
        try:
            subprocess.Popen("ms-settings:")
            return "Opening Windows Settings"
        except Exception as e:
            log_error(f"Error opening settings: {e}", e)
            return "I couldn't open Settings."

# Global executor instance
executor = None

def get_executor():
    """Get or create command executor instance"""
    global executor
    if executor is None:
        executor = CommandExecutor()
    return executor
