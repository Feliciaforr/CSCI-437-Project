from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QComboBox, QHBoxLayout, QPushButton,
    QStackedWidget, QFrame, QSizePolicy,  QLineEdit,QMenu,QLabel,QMessageBox, QTabWidget
   
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QTimer, QSize
import sys


# Home page
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def create_card(self, title, value_label_id, arrow=None, note_label_id=None):
        frame = QFrame()
        frame.setStyleSheet("background-color: #b0c4de; border-radius: 10px;")
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 10))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        value_label = QLabel("")
        value_label.setObjectName(value_label_id)
        value_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        if arrow:
            arrow_label = QLabel()
            arrow_label.setPixmap(QPixmap(arrow).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(arrow_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        if note_label_id:
            note_label = QLabel("")
            note_label.setObjectName(note_label_id)
            note_label.setFont(QFont('Arial', 8))
            note_label.setStyleSheet("color: black;")
            layout.addWidget(note_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        frame.setLayout(layout)
        return frame

    def update_card(self, label_id, new_text):
        label = self.findChild(QLabel, label_id)
        if label:
            label.setText(new_text)

    def initUI(self):
        main_layout = QVBoxLayout()

        # Navigation Bar- it should be always visible
        top_nav = QHBoxLayout()
        logo = QLabel("STOCKSIGHT")
        logo.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        top_nav.addWidget(logo)
        top_nav.addStretch()

        btn_style = """
            QPushButton {
                border: none;
                background: none;
                font-weight: bold;
                color: black;
            }
            QPushButton:hover {
                color: #007acc;
            }
        """

        home_btn = QPushButton("HOME")
        login_btn = QPushButton("LOGIN")
        support_btn = QPushButton("SUPPORT")
        for btn in (home_btn, login_btn, support_btn):
            btn.setStyleSheet(btn_style)
            

        menu_btn = QPushButton("MENU")
        menu_btn.setStyleSheet(btn_style)
        menu = QMenu()
        menu.addAction("Sign Out")
        menu.addAction("Buy")
        menu.addAction("Sell")
        menu.addAction("Active Companies")
        menu_btn.setMenu(menu)
        top_nav.addWidget(menu_btn)




        # Top Cards- titles of frame etc
        card_layout = QHBoxLayout()
        self.top_gainer_card = self.create_card("Top Gainer", "top_gainer_value", "up_arrow.png")
        self.top_loser_card = self.create_card("Top Loser", "top_loser_value", "down_arrow.png")
        self.stock_alerts_card = self.create_card("Stock Alerts", "stock_alerts_value", note_label_id="stock_alerts_note")

        card_layout.addWidget(self.top_gainer_card)
        card_layout.addWidget(self.top_loser_card)
        card_layout.addWidget(self.stock_alerts_card)

        main_layout.addLayout(card_layout)

        # Bottom frames
        bottom_layout = QHBoxLayout()

        self.market_insights_card = self.create_card("Market Insights", "market_insights_value")
        self.active_stocks_card = self.create_card("Active Stocks", "active_stocks_value", note_label_id="active_stocks_note")

        bottom_layout.addWidget(self.market_insights_card)
        bottom_layout.addWidget(self.active_stocks_card)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

# Designing Support Page
class SupportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        
        welcome_label = QLabel("Welcome to the Support Page")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(welcome_label)

        # Dropdown feature
        issue_label = QLabel("Please select your issue:")
        layout.addWidget(issue_label)

        self.issue_combo = QComboBox()
        self.issue_combo.addItems([
            "Unable to log in",
            "Dashboard not loading",
            "Data not updating",
            "Feature request",
            "Others"
        ])
        self.issue_combo.currentTextChanged.connect(self.toggle_textbox)
        layout.addWidget(self.issue_combo)

        # text box for user input
        self.issue_text = QTextEdit()
        self.issue_text.setPlaceholderText("Please describe your issue...")
        self.issue_text.hide()
        layout.addWidget(self.issue_text)

        # Submit button
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_issue)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

        
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
            }
            QLabel {
                font-size: 14px;
            }
            QComboBox, QTextEdit, QPushButton {
                font-size: 14px;
                padding: 6px;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
        """)

    def toggle_textbox(self, text):
        self.issue_text.setVisible(text == "Others")

    def submit_issue(self):
        from PyQt6.QtWidgets import QMessageBox
        issue = self.issue_combo.currentText()
        description = self.issue_text.toPlainText() if issue == "Others" else issue
        QMessageBox.information(self, "Issue Submitted", f"Your issue has been submitted:\n\n{description}")


# Design the login page here
class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login and Registration")
        self.setGeometry(300, 200, 500, 400)  # Increased frame size

        self.layout = QVBoxLayout()

        # Logo and Welcome
        logo_label = QLabel("📈")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 60px;")  # Emoji/logo
        self.layout.addWidget(logo_label)

        welcome_label = QLabel("Welcome to StockSight")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(welcome_label)

        # Tabs
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
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Customer", "Agent"])
        self.role_combo.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.role_combo)

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
        self.email_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.email_input)

        self.username_input_register = QLineEdit()
        self.username_input_register.setPlaceholderText("Username")
        self.username_input_register.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.username_input_register)

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact Number")
        self.contact_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.contact_input)

        self.register_password_input = QLineEdit()
        self.register_password_input.setPlaceholderText("Password")
        self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.register_password_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        self.register_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.register_button)

        self.register_tab.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()

        QMessageBox.information(self, "Login", f"Login attempted for {username} as {role}")

     

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        username = self.username_input_register.text()
        contact = self.contact_input.text()
        password = self.register_password_input.text()

        QMessageBox.information(self, "Register",
                                f"Registration attempted for {name}\nEmail: {email}\nContact: {contact}")




# Agent page here
class AgentPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Agent Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #34495e")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Example agent controls
        info_btn = QPushButton("View Customer Info")
        buy_btn = QPushButton("Buy Stocks for Customer")
        sell_btn = QPushButton("Sell Stocks for Customer")
        transactions_btn = QPushButton("View All Transactions")

        for btn in [info_btn, buy_btn, sell_btn, transactions_btn]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("font-size: 16px;")

        layout.addWidget(title)
        layout.addWidget(info_btn)
        layout.addWidget(buy_btn)
        layout.addWidget(sell_btn)
        layout.addWidget(transactions_btn)
        layout.addStretch()

        self.setLayout(layout)

# Customer page here
 
# --- Main Application Window ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Exchange Dashboard")
        self.setMinimumSize(1000, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # --- Stacked Widget for Pages ---
        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.login_page = LoginPage()
        self.support_page = SupportPage()

        self.stack.addWidget(self.dashboard_page)  # Home Page
        self.stack.addWidget(self.login_page)      # Login Page
        self.stack.addWidget(self.support_page)    # Support Page

        # --- Top Navigation Bar (Always Visible) ---
        top_nav = QHBoxLayout()
        logo = QLabel("STOCKSIGHT")
        logo.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        top_nav.addWidget(logo)
        top_nav.addStretch()

        btn_style = """
            QPushButton {
                border: none;
                background: none;
                font-weight: bold;
                color: black;
            }
            QPushButton:hover {
                color: #007acc;
            }
        """

        home_btn = QPushButton("HOME")
        login_btn = QPushButton("LOGIN")
        support_btn = QPushButton("SUPPORT")
        menu_btn = QPushButton("MENU")
        for btn in (home_btn, login_btn, support_btn):
            btn.setStyleSheet(btn_style)

        top_nav.addWidget(home_btn)
        top_nav.addWidget(support_btn)
        top_nav.addWidget(login_btn)
        top_nav.addWidget(menu_btn)
        menu_btn.setStyleSheet(btn_style)
        menu = QMenu()
        menu.addAction("Sign Out")
        menu.addAction("Buy")
        menu.addAction("Sell")
        menu.addAction("Active Companies")
        menu_btn.setMenu(menu)
        top_nav.addWidget(menu_btn)

        main_layout.addLayout(top_nav)
 



   

        # --- Connect Buttons to Switch Pages ---
        home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        login_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        support_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)


# --- Run the App ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
