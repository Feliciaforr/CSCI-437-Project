

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QTextEdit, QComboBox, QMessageBox
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import requests

# Login and Registration Page
class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the main window
        self.setWindowTitle("Login and Registration")
        self.setGeometry(300, 200, 500, 400)

        self.layout = QVBoxLayout()

        # Add a logo at the top
        logo_label = QLabel()
        pixmap = QPixmap("/Users/amangill/Stock_trade_project/project/gui/Stocksight logo.png")
        pixmap = pixmap.scaledToHeight(80, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(logo_label)

        # Add a welcome message
        welcome_label = QLabel("Welcome to StockSight")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(welcome_label)

        # Create tabs for Login and Registration
        self.tabs = QTabWidget()
        self.login_tab = QWidget()
        self.register_tab = QWidget()
        self.testing_tab = QWidget()  

        self.tabs.addTab(self.login_tab, "Login")
        self.tabs.addTab(self.register_tab, "Register")
        self.tabs.addTab(self.testing_tab, "Testing")  

        self.layout.addWidget(self.tabs)

        # Initialize the forms for login and registration
        self.login_form()
        self.register_form()
        self.testing_form() # Placeholder for testing form
        

        self.setLayout(self.layout)

    # Create the login form
    def login_form(self):
        layout = QVBoxLayout()

        # Input for email
        self.username_input = QLineEdit()
        self.username_input.editingFinished.connect(self.validate_email_input)  # Validate email format
        self.username_input.setPlaceholderText("Email")
        self.username_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.username_input)

        # Input for password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password input
        self.password_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)  # Connect to the login function
        self.login_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.login_button)

        self.login_tab.setLayout(layout)

    # Create the registration form
    def register_form(self):
        layout = QVBoxLayout()

        # Input for full name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.name_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.name_input)

        # Input for email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.editingFinished.connect(self.validate_email_input_res)  # Validate email format
        self.email_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.email_input)

        # Input for username
        self.username_input_register = QLineEdit()
        self.username_input_register.setPlaceholderText("Username")
        self.username_input_register.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.username_input_register)
        
        # Input for password
        self.register_password_input = QLineEdit()
        self.register_password_input.setPlaceholderText("Password")
        self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password input
        self.register_password_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.register_password_input)

        # Input for contact number
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact Number")
        self.contact_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.contact_input)
        
        # Input for account balance
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Account Balance")
        self.account_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.account_input)
        
        # Dropdown for role selection
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Customer"])  # Currently only "Customer" is available
        self.role_combo.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.role_combo)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)  # Connect to the register function
        self.register_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.register_button)

        self.register_tab.setLayout(layout)

    # Handle login functionality
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText().lower()

        # Ensure both email and password are provided
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both email and password.")
            return

        try:
            # Send login request to the backend
            response = requests.post("http://127.0.0.1:9000/auth/login", json={
                "email": username,
                "password": password,
            })

            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                role =  data.get('user', {}).get('role')

                if token:
                    QMessageBox.information(self, "Login Successful", f"Welcome!")

                    # Store token and role in the parent widget
                    self.parent().setProperty('access_token', token)
                    self.parent().setProperty('role', role)
                    self.parent().setProperty('username', username)

                    # Switch to the main application view
                    self.parent().show_main_window(token, role)
                else:
                    QMessageBox.warning(self, "Error", "Login failed. No token received.")
            else:
                QMessageBox.warning(self, "Error", "Invalid email or password.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    # Handle registration functionality
    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        username = self.username_input_register.text()
        contact = self.contact_input.text()
        password = self.register_password_input.text()
        balance = self.account_input.text()
        role = self.role_combo.currentText().lower()

        # Ensure all fields are filled
        if not name or not email or not username or not contact or not password or not balance:
            QMessageBox.warning(self, "Error", "Please fill out all registration fields.")
            return

        try:
            # Send registration request to the backend
            response = requests.post("http://127.0.0.1:9000/auth/register", json={
                "name": name,
                "email": email,
                "username": username,
                "phone": contact,
                "password": password,
                "account_balance": balance,
                "role": role
            })

            if response.status_code == 201:
                QMessageBox.information(self, "Registration Successful", "You have been registered successfully.")
                self.tabs.setCurrentIndex(0)  # Switch to login tab
            else:
                error_message = response.json().get("detail", "Registration failed.")
                QMessageBox.warning(self, "Error", error_message)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        
    # Validate email format for login
    def validate_email_input(self):
        email = self.username_input.text()
        import re
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address")
            self.username_input.setFocus()
            
    # Validate email format for registration
    def validate_email_input_res(self):
        email = self.email_input.text()
        import re
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address")
            self.email_input.setFocus()
            
    # **TESTING TAB SETUP**
    def testing_form(self):
        layout = QVBoxLayout()

        # Testing button
        self.testing_button = QPushButton("Test")
        self.testing_button.clicked.connect(self.test_function)
        
        layout.addWidget(self.testing_button)

        # Assign layout to the testing tab
        self.testing_tab.setLayout(layout)
        
    def test_function(self):
        # Placeholder for testing functionality
    
        try:
            response = requests.post("http://127.0.0.1:9000/auth/login", json={
                "email": "agent001@example.com",
                "password": "strongpassword123",
            })

            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                role =  data.get('user', {}).get('role')

                if token:
                    # QMessageBox.information(self, "Login Successful", f"Welcome!")


                    self.parent().setProperty('access_token', token)
                    # self.parent().setProperty('role', role)
                    # self.parent().setProperty('username', username)

      
                    self.parent().show_main_window(token, role)
                else:
                    QMessageBox.warning(self, "Error", "Login failed. No token received.")
            else:
                QMessageBox.warning(self, "Error", "Invalid email or password.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

# ------ End of login_page.py ------