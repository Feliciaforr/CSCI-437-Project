# login_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QTextEdit, QComboBox, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import requests

# Login and Registration Page
class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login and Registration")
        self.setGeometry(300, 200, 500, 400)

        self.layout = QVBoxLayout()

        logo_label = QLabel("📈")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 60px;")
        self.layout.addWidget(logo_label)

        welcome_label = QLabel("Welcome to StockSight")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(welcome_label)

        self.tabs = QTabWidget()
        self.login_tab = QWidget()
        self.register_tab = QWidget()

        self.tabs.addTab(self.login_tab, "Login")
        self.tabs.addTab(self.register_tab, "Register")

        self.layout.addWidget(self.tabs)

        self.login_form()
        self.register_form()

        self.setLayout(self.layout)

    def login_form(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.editingFinished.connect(self.validate_email_input)
        self.username_input.setPlaceholderText("Emailsss")
        self.username_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.login_button)

        self.login_tab.setLayout(layout)

    def register_form(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.name_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.editingFinished.connect(self.validate_email_input)

        self.email_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.email_input)

        self.username_input_register = QLineEdit()
        self.username_input_register.setPlaceholderText("Username")
        self.username_input_register.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.username_input_register)
        
        self.register_password_input = QLineEdit()
        self.register_password_input.setPlaceholderText("Password")
        self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.register_password_input)

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact Number")
        self.contact_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.contact_input)
        
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Account Balance")
        self.account_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.account_input)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Customer"])
        self.role_combo.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.role_combo)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        self.register_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.register_button)
        


        self.register_tab.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText().lower()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both email and password.")
            return

        try:
            response = requests.post("http://127.0.0.1:9000/auth/login", json={
                "email": username,
                "password": password,
            })

            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')

                if token:
                    QMessageBox.information(self, "Login Successful", f"Welcome!")

                    self.parent().setProperty('access_token', token)
                    self.parent().setProperty('role', role)
                    self.parent().setProperty('username', username)

                    self.parent().parent().stack.setCurrentIndex(0)
                else:
                    QMessageBox.warning(self, "Error", "Login failed. No token received.")
            else:
                QMessageBox.warning(self, "Error", "Invalid email or password.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        username = self.username_input_register.text()
        contact = self.contact_input.text()
        password = self.register_password_input.text()

        QMessageBox.information(self, "Register",
                                f"Registration attempted for {name}\nEmail: {email}\nContact: {contact}")
        
        
    def validate_email_input(self):
        email = self.username_input.text()
        import re
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address")
            self.username_input.setFocus()

# ------ End of login_page.py ------