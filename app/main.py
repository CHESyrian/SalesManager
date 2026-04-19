import sys
from PyQt6.QtWidgets import QApplication
from ui.modules.auth.login_view import LoginWindow

def main():
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())