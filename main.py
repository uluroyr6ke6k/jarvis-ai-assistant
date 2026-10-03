import sys

from PyQt6.QtWidgets import QApplication

from app.dashboard import JarvisDashboard
from app.assistant_controller import AssistantController
from app.startup import StartupChecker


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        * {
            font-family: "Segoe UI";
            color: #dfefff;
        }
        QWidget {
            background: #040b1b;
        }
    ''')

    window = JarvisDashboard()
    window.resize(1600, 900)
    window.show()

    checker = StartupChecker()
    status = checker.check()
    window.set_status_message(f"System status: CPU {status['system']['cpu']:.1f}% | RAM {status['system']['memory']:.1f}% | DISK {status['system']['disk']:.1f}%")
    if status["ollama"]["status"] == "ready":
        window.set_assistant_response("Local AI ready")
    else:
        window.set_assistant_response("Local AI offline")

    assistant = AssistantController(dashboard=window)
    assistant.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
