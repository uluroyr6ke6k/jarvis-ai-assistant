from __future__ import annotations

from typing import Any, Dict, List

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QTextEdit, QLineEdit
from PyQt6.QtCore import QTimer, Qt

from core.model_provider import ModelProvider
from core.system_monitor import SystemMonitor


class JarvisDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S.")
        self.setObjectName("mainWindow")
        self.model_provider = ModelProvider()
        self.status_label = None
        self.assistant_label = None
        self.listening_label = None
        self.cpu_label = None
        self.memory_label = None
        self.disk_label = None
        self.last_command_label = None
        self.task_log = None
        self.command_input = None
        self.command_button = None
        self.command_callback = None
        self.setStyleSheet('''
            QWidget {
                background: #050d1d;
                color: #dfefff;
            }
            QLabel {
                color: #dfefff;
            }
            #mainWindow {
                border: 2px solid #00d0ff;
                border-radius: 18px;
            }
            .panel {
                background: rgba(9, 27, 45, 0.92);
                border: 2px solid #00d0ff;
                border-radius: 16px;
                padding: 10px;
            }
            .nav-btn {
                background: rgba(8, 26, 44, 0.8);
                border: 2px solid #00d0ff;
                border-radius: 12px;
                color: #dfefff;
                padding: 10px;
                min-height: 42px;
            }
            .nav-btn.active {
                background: linear-gradient(180deg, #0b7bcf 0%, #0d5ca8 100%);
                border: 2px solid #75dcff;
            }
            .title {
                color: #5be2ff;
                font-size: 32px;
                font-weight: 700;
                letter-spacing: 6px;
            }
            .tagline {
                color: #6ef5ff;
                font-size: 16px;
                letter-spacing: 2px;
            }
            .tiny {
                color: #9fe8ff;
                font-size: 11px;
            }
            .big-number {
                color: #8de7ff;
                font-size: 36px;
                font-weight: 700;
            }
            .primary-text {
                color: #9fe8ff;
                font-size: 16px;
            }
            .status-box {
                background: rgba(11, 30, 45, 0.95);
                border: 2px solid #00d0ff;
                border-radius: 12px;
                padding: 10px;
            }
            QTextEdit, QLineEdit {
                background: rgba(4, 17, 29, 0.9);
                border: 2px solid #00d0ff;
                border-radius: 10px;
                color: #dfefff;
                padding: 8px;
            }
            QPushButton {
                background: rgba(13, 38, 55, 0.8);
                border: 2px solid #00d0ff;
                border-radius: 10px;
                color: #dfefff;
            }
        ''')
        self.build_ui()
        self.start_clock()
        self.refresh_status()

    def bind_command_handler(self, callback):
        self.command_callback = callback
        if self.command_button is not None:
            self.command_button.clicked.connect(self.submit_command)

    def submit_command(self):
        if self.command_callback is None or self.command_input is None:
            return
        text = self.command_input.text().strip()
        if not text:
            return
        self.set_last_command(text)
        response = str(self.command_callback(text))
        self.set_status_message(response)
        self.set_assistant_response(response[:28])
        self.command_input.clear()

    def build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        sidebar = self.create_sidebar()
        center = self.create_center_panel()
        right = self.create_right_panel()

        root.addWidget(sidebar, 1)
        root.addWidget(center, 5)
        root.addWidget(right, 2)

    def create_sidebar(self):
        panel = QWidget()
        panel.setProperty("class", "panel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(12, 12, 12, 12)

        brand = QLabel("J.A.R.V.I.S.")
        brand.setProperty("class", "title")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(brand)

        nav_items = ["Home", "Voice", "Control", "Files", "Applications", "Internet", "Settings"]
        for item in nav_items:
            btn = QPushButton(item)
            btn.setProperty("class", "nav-btn")
            if item == "Home":
                btn.setProperty("class", "nav-btn active")
            panel_layout.addWidget(btn)

        panel_layout.addStretch()
        return panel

    def create_center_panel(self):
        panel = QWidget(); panel.setProperty("class", "panel")
        layout = QVBoxLayout(panel); layout.setContentsMargins(12, 12, 12, 12); layout.setSpacing(14)

        top_bar = QWidget(); top_bar_layout = QHBoxLayout(top_bar); top_bar_layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("PERSONAL AI ASSISTANT"); title.setStyleSheet("color: #7fe4ff; font-size: 18px; letter-spacing: 3px;"); title.setAlignment(Qt.AlignmentFlag.AlignCenter); top_bar_layout.addWidget(title); top_bar_layout.addStretch()
        time_label = QLabel("18:42"); time_label.setObjectName("timeLabel"); time_label.setStyleSheet("font-size: 21px; color: #7fe4ff; letter-spacing: 1px;"); top_bar_layout.addWidget(time_label)
        layout.addWidget(top_bar)

        middle_grid = QGridLayout(); middle_grid.setSpacing(12)
        weather = self.create_weather_card(); system_status = self.create_system_status_card(); voice_block = self.create_voice_block()
        middle_grid.addWidget(weather, 0, 0); middle_grid.addWidget(system_status, 0, 1); middle_grid.addWidget(voice_block, 0, 2)
        central = self.create_hologram_core(); middle_grid.addWidget(central, 1, 0, 1, 3)
        layout.addLayout(middle_grid)

        bottom = QHBoxLayout(); bottom.setSpacing(16); bottom.addWidget(self.create_live_news()); bottom.addWidget(self.create_voice_prompt())
        layout.addLayout(bottom)
        return panel

    def create_right_panel(self):
        panel = QWidget(); panel.setProperty("class", "panel")
        layout = QVBoxLayout(panel); layout.setContentsMargins(12, 12, 12, 12); layout.setSpacing(14)
        layout.addWidget(self.create_schedule_card()); layout.addWidget(self.create_recent_activity()); layout.addWidget(self.create_commands_panel()); layout.addWidget(self.create_shortcuts_panel())
        return panel

    def create_weather_card(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(12, 12, 12, 12)
        title = QLabel("WEATHER"); title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;"); layout.addWidget(title)
        temp = QLabel("27°"); temp.setProperty("class", "big-number"); layout.addWidget(temp)
        city = QLabel("Mostly Sunny"); city.setStyleSheet("font-size: 16px; color: #cbeaff;"); layout.addWidget(city)
        detail = QLabel("Lagos, Nigeria\nH: 32° | L: 24°"); detail.setStyleSheet("color: #bfefff; font-size: 12px; line-height: 1.7;"); layout.addWidget(detail)
        return widget

    def create_system_status_card(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        title = QLabel("SYSTEM STATUS"); title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;"); layout.addWidget(title)
        bars = [("Disk Usage", "0%"), ("CPU", "0%"), ("Memory", "0%")]
        for label, percent in bars:
            row = QWidget(); row_layout = QHBoxLayout(row); row_layout.setContentsMargins(0, 0, 0, 0)
            l = QLabel(label); l.setStyleSheet("font-size: 12px; color: #dfefff;")
            if label == "Disk Usage": v = QLabel(percent); self.disk_label = v
            elif label == "CPU": v = QLabel(percent); self.cpu_label = v
            else: v = QLabel(percent); self.memory_label = v
            v.setStyleSheet("font-size: 12px; color: #82ecff;")
            row_layout.addWidget(l); row_layout.addStretch(); row_layout.addWidget(v); layout.addWidget(row)
        return widget

    def create_voice_block(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(12, 12, 12, 12)
        title = QLabel("VOICE RECOGNITION"); title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;"); layout.addWidget(title)
        sound = QLabel("◉◉◉◉◉◉"); sound.setStyleSheet("color: #8be9ff; font-size: 24px; letter-spacing: 3px;"); sound.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(sound)
        status = QLabel("LISTENING..."); status.setObjectName("voiceStatus"); self.listening_label = status
        status.setStyleSheet("color: #8be9ff; font-size: 14px; letter-spacing: 2px;"); status.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(status)
        return widget

    def create_hologram_core(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(20, 20, 20, 20)
        core = QLabel("J.A.R.V.I.S.\nONLINE"); core.setAlignment(Qt.AlignmentFlag.AlignCenter)
        core.setStyleSheet('''
            color: #c7f7ff;
            font-size: 34px;
            font-weight: 700;
            letter-spacing: 8px;
            background: radial-gradient(circle, rgba(0, 205, 255, 0.2), rgba(0, 0, 0, 0));
            border: 3px solid #00d0ff;
            border-radius: 50%;
            min-height: 340px;
            min-width: 340px;
        ''')
        self.assistant_label = core; layout.addWidget(core)
        return widget

    def create_live_news(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(12, 12, 12, 12)
        title = QLabel("LIVE NEWS"); title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;"); layout.addWidget(title)
        for item in ["Global markets show steady growth...", "New AI breakthrough boosts productivity...", "Health experts recommend daily movement..."]:
            label = QLabel("• " + item); label.setStyleSheet("color: #dfefff; font-size: 12px;"); layout.addWidget(label)
        return widget

    def create_voice_prompt(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(16, 16, 16, 16)
        mic = QLabel("🎙"); mic.setAlignment(Qt.AlignmentFlag.AlignCenter); mic.setStyleSheet("font-size: 32px; color: #94f0ff;"); layout.addWidget(mic)
        prompt = QLabel("How can I help you today?"); prompt.setObjectName("promptText"); self.status_label = prompt
        prompt.setStyleSheet("color: #dff7ff; font-size: 18px; letter-spacing: 1px;"); prompt.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(prompt)

        self.last_command_label = QLabel("Last command: none"); self.last_command_label.setStyleSheet("color: #8fe3ff; font-size: 11px;"); layout.addWidget(self.last_command_label)

        self.command_input = QLineEdit(); self.command_input.setPlaceholderText("Type a command or ask J.A.R.V.I.S..."); self.command_input.setFixedHeight(40); layout.addWidget(self.command_input)
        self.command_button = QPushButton("Execute"); self.command_button.setFixedHeight(38); layout.addWidget(self.command_button)

        self.task_log = QTextEdit(); self.task_log.setPlaceholderText("Assistant activity..."); self.task_log.setReadOnly(True); self.task_log.setFixedHeight(80); layout.addWidget(self.task_log)
        return widget

    def create_schedule_card(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(10, 10, 10, 10)
        title = QLabel("TODAY'S SCHEDULE"); title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;"); layout.addWidget(title)
        for time_text, label_text in [("08:00", "Morning Routine"), ("10:00", "Work on E-book"), ("13:00", "Lunch Break"), ("16:00", "YouTube Content")]:
            row = QWidget(); row_layout = QHBoxLayout(row); row_layout.setContentsMargins(0, 0, 0, 0)
            key = QLabel(time_text); key.setStyleSheet("font-size: 12px; color: #bdecff;")
            value = QLabel(label_text); value.setStyleSheet("font-size: 12px; color: #dfefff;")
            row_layout.addWidget(key); row_layout.addWidget(value); row_layout.addStretch(); layout.addWidget(row)
        return widget

    def create_recent_activity(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(10, 10, 10, 10)
        title = QLabel("RECENT ACTIVITY"); title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;"); layout.addWidget(title)
        for activity, when in [("Opened: YouTube", "2 mins ago"), ("Edited: The Welles Blueprint.pdf", "12 mins ago"), ("Visited: ChatGPT", "28 mins ago")]:
            row = QWidget(); row_layout = QHBoxLayout(row); row_layout.setContentsMargins(0, 0, 0, 0)
            a = QLabel(activity); a.setStyleSheet("font-size: 11px; color: #dfefff;")
            w = QLabel(when); w.setStyleSheet("font-size: 10px; color: #8fe3ff;")
            row_layout.addWidget(a); row_layout.addStretch(); row_layout.addWidget(w); layout.addWidget(row)
        return widget

    def create_commands_panel(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget); layout.setContentsMargins(10, 10, 10, 10)
        title = QLabel("VOICE COMMANDS"); title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;"); layout.addWidget(title)
        for cmd in ['"Open YouTube"', '"Show my files"', '"Take a screenshot"', '"What\'s the weather?"', '"Remember my preference"']:
            label = QLabel(cmd); label.setStyleSheet("font-size: 12px; color: #dfefff;"); layout.addWidget(label)
        return widget

    def create_shortcuts_panel(self):
        widget = QWidget(); widget.setProperty("class", "status-box")
        layout = QGridLayout(widget); layout.setContentsMargins(10, 10, 10, 10); layout.setSpacing(10)
        items = [("Open Browser", "💻"), ("Open Files", "📁"), ("Control Music", "���"), ("Take Screenshot", "📷"), ("Shutdown", "⏻"), ("Restart", "↻")]
        for idx, (text, icon) in enumerate(items):
            btn = QPushButton(f"{icon}\n{text}"); btn.setStyleSheet('''
                QPushButton {
                    background: rgba(13, 38, 55, 0.8);
                    border: 2px solid #00d0ff;
                    border-radius: 10px;
                    color: #dfefff;
                    min-height: 70px;
                    font-size: 10px;
                }
            '''); layout.addWidget(btn, idx // 3, idx % 3)
        return widget

    def refresh_status(self):
        metrics = SystemMonitor.get_status()
        if self.cpu_label is not None: self.cpu_label.setText(f"{metrics['cpu']:.0f}%")
        if self.memory_label is not None: self.memory_label.setText(f"{metrics['memory']:.0f}%")
        if self.disk_label is not None: self.disk_label.setText(f"{metrics['disk']:.0f}%")

        local_ai_ready = self.model_provider.is_available()
        if self.listening_label is not None:
            self.listening_label.setText("READY" if local_ai_ready else "OFFLINE")
        if self.assistant_label is not None:
            self.assistant_label.setText("J.A.R.V.I.S.\nREADY" if local_ai_ready else "J.A.R.V.I.S.\nOFFLINE")
        if self.status_label is not None:
            self.status_label.setText("Local AI: ready" if local_ai_ready else "Local AI: offline")

    def set_status_message(self, text: str):
        if self.status_label is not None: self.status_label.setText(text)
        if self.task_log is not None:
            existing = self.task_log.toPlainText().strip()
            if existing:
                self.task_log.setPlainText(existing + "\n" + text)
            else:
                self.task_log.setPlainText(text)

    def set_assistant_response(self, text: str):
        if self.assistant_label is not None: self.assistant_label.setText(f"J.A.R.V.I.S.\n{text[:24]}")

    def set_listening_state(self, is_listening: bool):
        if self.listening_label is not None: self.listening_label.setText("LISTENING..." if is_listening else "STANDBY")

    def set_last_command(self, text: str):
        if self.last_command_label is not None: self.last_command_label.setText(f"Last command: {text}")

    def start_clock(self):
        self.timer = QTimer(self); self.timer.timeout.connect(self.update_clock); self.timer.start(1000)

    def update_clock(self):
        from datetime import datetime
        now = datetime.now(); time_str = now.strftime("%H:%M")
        label = self.findChild(QLabel, "timeLabel")
        if label is not None: label.setText(time_str)
        if now.second % 5 == 0: self.refresh_status()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = JarvisDashboard(); window.resize(1600, 900); window.show(); sys.exit(app.exec())
