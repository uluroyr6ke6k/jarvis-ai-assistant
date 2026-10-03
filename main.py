from PyQt6.QtWidgets import QApplication
import sys

from app.dashboard import JarvisDashboard
from app.assistant_controller import AssistantController


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

    assistant = AssistantController(dashboard=window)
    assistant.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
