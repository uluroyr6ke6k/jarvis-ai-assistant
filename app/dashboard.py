from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont


class JarvisDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S.")
        self.setObjectName("mainWindow")
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
            .vlr {
                border: 1px solid #0ae0ff;
                border-radius: 10px;
            }
        ''')

        self.build_ui()
        self.start_clock()

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

        nav_items = [
            "Home", "Voice", "Control", "Files", "Applications",
            "Internet", "Settings"
        ]
        for item in nav_items:
            btn = QPushButton(item)
            btn.setProperty("class", "nav-btn")
            if item == "Home":
                btn.setProperty("class", "nav-btn active")
            panel_layout.addWidget(btn)

        panel_layout.addStretch()
        return panel

    def create_center_panel(self):
        panel = QWidget()
        panel.setProperty("class", "panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)

        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("PERSONAL AI ASSISTANT")
        title.setStyleSheet("color: #7fe4ff; font-size: 18px; letter-spacing: 3px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar_layout.addWidget(title)
        top_bar_layout.addStretch()

        time_label = QLabel("18:42")
        time_label.setObjectName("timeLabel")
        time_label.setStyleSheet("font-size: 21px; color: #7fe4ff; letter-spacing: 1px;")
        top_bar_layout.addWidget(time_label)

        layout.addWidget(top_bar)

        middle_grid = QGridLayout()
        middle_grid.setSpacing(12)

        weather = self.create_weather_card()
        system_status = self.create_system_status_card()
        voice_block = self.create_voice_block()

        middle_grid.addWidget(weather, 0, 0)
        middle_grid.addWidget(system_status, 0, 1)
        middle_grid.addWidget(voice_block, 0, 2)

        central = self.create_hologram_core()
        middle_grid.addWidget(central, 1, 0, 1, 3)

        layout.addLayout(middle_grid)

        bottom = QHBoxLayout()
        bottom.setSpacing(16)
        bottom.addWidget(self.create_live_news())
        bottom.addWidget(self.create_voice_prompt())

        layout.addLayout(bottom)
        return panel

    def create_right_panel(self):
        panel = QWidget()
        panel.setProperty("class", "panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)

        schedule = self.create_schedule_card()
        activity = self.create_recent_activity()
        commands = self.create_commands_panel()
        shortcuts = self.create_shortcuts_panel()

        layout.addWidget(schedule)
        layout.addWidget(activity)
        layout.addWidget(commands)
        layout.addWidget(shortcuts)
        return panel

    def create_weather_card(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)

        title = QLabel("WEATHER")
        title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;")
        layout.addWidget(title)

        temp = QLabel("27°")
        temp.setProperty("class", "big-number")
        layout.addWidget(temp)

        city = QLabel("Mostly Sunny")
        city.setStyleSheet("font-size: 16px; color: #cbeaff;")
        layout.addWidget(city)

        detail = QLabel("Lagos, Nigeria\nH: 32° | L: 24°")
        detail.setStyleSheet("color: #bfefff; font-size: 12px; line-height: 1.7;")
        layout.addWidget(detail)
        return widget

    def create_system_status_card(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        title = QLabel("SYSTEM STATUS")
        title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;")
        layout.addWidget(title)

        bars = [
            ("Disk Usage", "42%"),
            ("CPU", "58%"),
            ("Memory", "18%"),
        ]
        for label, percent in bars:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            l = QLabel(label)
            l.setStyleSheet("font-size: 12px; color: #dfefff;")
            v = QLabel(percent)
            v.setStyleSheet("font-size: 12px; color: #82ecff;")
            row_layout.addWidget(l)
            row_layout.addStretch()
            row_layout.addWidget(v)
            layout.addWidget(row)
        return widget

    def create_voice_block(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)

        title = QLabel("VOICE RECOGNITION")
        title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;")
        layout.addWidget(title)

        sound = QLabel("◉◉◉◉◉◉")
        sound.setStyleSheet("color: #8be9ff; font-size: 24px; letter-spacing: 3px;")
        sound.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sound)

        status = QLabel("LISTENING...")
        status.setStyleSheet("color: #8be9ff; font-size: 14px; letter-spacing: 2px;")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status)
        return widget

    def create_hologram_core(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        core = QLabel("J.A.R.V.I.S.\nONLINE")
        core.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        layout.addWidget(core)
        return widget

    def create_live_news(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)

        title = QLabel("LIVE NEWS")
        title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;")
        layout.addWidget(title)

        items = [
            "Global markets show steady growth...",
            "New AI breakthrough boosts productivity...",
            "Health experts recommend daily movement...",
        ]
        for item in items:
            label = QLabel("• " + item)
            label.setStyleSheet("color: #dfefff; font-size: 12px;")
            layout.addWidget(label)
        return widget

    def create_voice_prompt(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)

        mic = QLabel("🎙")
        mic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mic.setStyleSheet("font-size: 32px; color: #94f0ff;")
        layout.addWidget(mic)

        prompt = QLabel("How can I help you today?")
        prompt.setStyleSheet("color: #dff7ff; font-size: 18px; letter-spacing: 1px;")
        prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(prompt)
        return widget

    def create_schedule_card(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("TODAY'S SCHEDULE")
        title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;")
        layout.addWidget(title)

        entries = [
            ("08:00", "Morning Routine"),
            ("10:00", "Work on E-book"),
            ("13:00", "Lunch Break"),
            ("16:00", "YouTube Content"),
        ]
        for time_text, label_text in entries:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)

            key = QLabel(time_text)
            key.setStyleSheet("font-size: 12px; color: #bdecff;")
            value = QLabel(label_text)
            value.setStyleSheet("font-size: 12px; color: #dfefff;")
            row_layout.addWidget(key)
            row_layout.addWidget(value)
            row_layout.addStretch()
            layout.addWidget(row)
        return widget

    def create_recent_activity(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("RECENT ACTIVITY")
        title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;")
        layout.addWidget(title)

        rows = [
            ("Opened: YouTube", "2 mins ago"),
            ("Edited: The Welles Blueprint.pdf", "12 mins ago"),
            ("Visited: ChatGPT", "28 mins ago"),
        ]
        for activity, when in rows:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            a = QLabel(activity)
            a.setStyleSheet("font-size: 11px; color: #dfefff;")
            w = QLabel(when)
            w.setStyleSheet("font-size: 10px; color: #8fe3ff;")
            row_layout.addWidget(a)
            row_layout.addStretch()
            row_layout.addWidget(w)
            layout.addWidget(row)
        return widget

    def create_commands_panel(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("VOICE COMMANDS")
        title.setStyleSheet("color: #79dfff; letter-spacing: 2px; font-size: 14px;")
        layout.addWidget(title)

        commands = [
            '"Open YouTube"',
            '"Show my files"',
            '"Turn on dark mode"',
            '"What\'s the weather?"',
            '"Take a screenshot"',
        ]
        for cmd in commands:
            label = QLabel(cmd)
            label.setStyleSheet("font-size: 12px; color: #dfefff;")
            layout.addWidget(label)
        return widget

    def create_shortcuts_panel(self):
        widget = QWidget()
        widget.setProperty("class", "status-box")
        layout = QGridLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        items = [
            ("Open Browser", "💻"),
            ("Open Files", "📁"),
            ("Control Music", "🎵"),
            ("Take Screenshot", "📷"),
            ("Shutdown", "⏻"),
            ("Restart", "↻"),
        ]
        for idx, (text, icon) in enumerate(items):
            btn = QPushButton(f"{icon}\n{text}")
            btn.setStyleSheet('''
                QPushButton {
                    background: rgba(13, 38, 55, 0.8);
                    border: 2px solid #00d0ff;
                    border-radius: 10px;
                    color: #dfefff;
                    min-height: 70px;
                    font-size: 10px;
                }
            ''')
            layout.addWidget(btn, idx // 3, idx % 3)
        return widget

    def start_clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

    def update_clock(self):
        from datetime import datetime
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%a, %b %d, %Y")
        label = self.findChild(QLabel, "timeLabel")
        if label is not None:
            label.setText(time_str)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = JarvisDashboard()
    window.resize(1600, 900)
    window.show()
    sys.exit(app.exec())
