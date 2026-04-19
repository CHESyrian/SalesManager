from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)

from core.services.auth_service import AuthService
from infrastructure.database.connection import SessionLocal


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sales Manager Login")
        self.setFixedSize(350, 220)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def login(self):
        db = SessionLocal()

        user = AuthService.authenticate(
            db,
            self.username.text(),
            self.password.text()
        )

        db.close()

        if not user:
            QMessageBox.warning(self, "Error", "Invalid credentials")
            return

        from ui.main_window import MainWindow

        self.main = MainWindow(user)
        self.main.show()
        self.close()