import threading
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal

from core.ai_engine import get_ai_engine
from core.command_executor import get_executor
from core.voice_engine import get_voice_engine


class AssistantController(QObject):
    """Controller that bridges voice input, AI interpretation, and command execution."""

    response_ready = pyqtSignal(str)
    status_ready = pyqtSignal(str)
    listening_ready = pyqtSignal(bool)

    def __init__(self, dashboard=None, parent=None):
        super().__init__(parent)
        self.dashboard = dashboard
        self.ai_engine = get_ai_engine()
        self.executor = get_executor()
        self.voice_engine = get_voice_engine()
        self.running = False
        self._thread: Optional[threading.Thread] = None

        self.response_ready.connect(self._emit_response)
        self.status_ready.connect(self._emit_status)
        self.listening_ready.connect(self._emit_listening_state)

    def _emit_response(self, text: str):
        if self.dashboard is not None:
            self.dashboard.set_assistant_response(text)

    def _emit_status(self, text: str):
        if self.dashboard is not None:
            self.dashboard.set_status_message(text)

    def _emit_listening_state(self, is_listening: bool):
        if self.dashboard is not None:
            self.dashboard.set_listening_state(is_listening)

    def start(self):
        """Start the assistant background voice loop."""
        if self.running:
            return
        self.running = True
        self.status_ready.emit("System online")
        self.listening_ready.emit(True)
        self._thread = threading.Thread(target=self._voice_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the assistant voice loop."""
        self.running = False
        self.listening_ready.emit(False)
        self.status_ready.emit("System standby")

    def handle_text(self, text: str):
        """Handle a recognized text transcription."""
        if not text:
            return

        text = text.strip()
        self.status_ready.emit(f"Processing: {text}")
        self.response_ready.emit(f"You said: {text}")

        result = self.executor.execute(text)

        if not result:
            result = self.ai_engine.process_command(text)

        self.response_ready.emit(result)
        self.status_ready.emit("Ready")

    def _voice_loop(self):
        """Background loop that listens for speech and processes it."""
        while self.running:
            try:
                spoken = self.voice_engine.listen(timeout=8)
                if spoken:
                    self.handle_text(spoken)
            except Exception:
                continue

    def speak(self, text: str):
        """Speak a response to the user."""
        try:
            self.voice_engine.speak(text)
        except Exception:
            pass
