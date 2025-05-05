# main_window.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QMenu
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from gui.dashboard_page import DashboardPage
from gui.login_page import LoginPage
from gui.support_page import SupportPage

# --- Main Application Window ---
class MainWindow(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        # self.setWindowTitle("Stock Exchange Dashboard")
        # self.setMinimumSize(100, 100)
        self.initUI()
        

    def initUI(self):
        main_layout = QVBoxLayout()

        # Pages
        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage(self.token)
        self.support_page = SupportPage()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.support_page)

        # Top Navigation Bar
        top_nav = QHBoxLayout()
        logo = QLabel("STOCKSIGHT")
        logo.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        top_nav.addWidget(logo)
        top_nav.addStretch()

        btn_style = """
            QPushButton {
                border: none;
                background: none;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                color: #F26E22;
            }
        """

        home_btn = QPushButton("HOME")
        support_btn = QPushButton("SUPPORT")
        menu_btn = QPushButton("MENU")
        
        for btn in (home_btn, support_btn):
            btn.setStyleSheet(btn_style)
        
        menu_btn.setStyleSheet(btn_style)
        menu = QMenu()
        menu.addAction("Sign Out")
        menu.addAction("Buy")
        menu.addAction("Sell")
        menu.addAction("Active Companies")
        menu_btn.setMenu(menu)

        top_nav.addWidget(home_btn)
        top_nav.addWidget(support_btn)
        top_nav.addWidget(menu_btn)

        main_layout.addLayout(top_nav)

        # Button functionality
        home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        support_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)
