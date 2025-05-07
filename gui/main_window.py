
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QMenu
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from gui.dashboard_page import DashboardPage
from gui.login_page import LoginPage
from gui.support_page import SupportPage
from gui.customer_page import CustomerPage
from gui.agent_s_customer_page import AgentsCustomerPage


class MainWindow(QWidget):
    def __init__(self, token, role):
        super().__init__()
        self.token = token
        self.role = role
        
        print("role", self.role)
        self.initUI()
        

    def initUI(self):
        main_layout = QVBoxLayout()

        # Pages
        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage(self.token)

        self.stack.addWidget(self.dashboard_page)

        # Top Navigation Bar
        top_nav = QHBoxLayout()
        logo_layout = QHBoxLayout()
        logo_icon = QLabel()
        logo_icon.setPixmap(QPixmap("/Users/amangill/Stock_trade_project/project/gui/Stocksight logo.png").scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_text = QLabel("STOCKSIGHT")
        logo_text.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        logo_text.setStyleSheet("color: white;")

        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()

        top_nav.addLayout(logo_layout)

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

        if self.role == "agent":
            customers_btn = QPushButton("CUSTOMERS")
            customers_btn.setStyleSheet(btn_style)
            customers_btn.clicked.connect(self.open_customers_page)  
            top_nav.addWidget(customers_btn)

        home_btn = QPushButton("HOME")
        portfolio_btn = QPushButton("PORTFOLIO")
        menu_btn = QPushButton("MENU")
        
        for btn in (home_btn,):
            btn.setStyleSheet(btn_style)
        portfolio_btn.setStyleSheet(btn_style)
        
        menu_btn.setStyleSheet(btn_style)
        menu = QMenu()
        sign_out_action = menu.addAction("Sign Out")
        sign_out_action.triggered.connect(self.handle_sign_out)
        # menu.addAction("Active Companies")
        menu_btn.setMenu(menu)

        top_nav.addWidget(home_btn)
        top_nav.addWidget(portfolio_btn)
        top_nav.addWidget(menu_btn)

        main_layout.addLayout(top_nav)

        # Button functionality
        home_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.customer_page = CustomerPage(self.token)
        self.stack.addWidget(self.customer_page)
        self.agent_customer_page = AgentsCustomerPage(self.token)
        self.stack.addWidget(self.agent_customer_page)
        portfolio_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.customer_page))

        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def handle_sign_out(self):
        from PyQt6.QtWidgets import QApplication
        from gui.MainApp import MainApp
        self.close()
        for widget in QApplication.topLevelWidgets():
            widget.close()
        self.new_session = MainApp()
        self.new_session.resize(900, 700)
        self.new_session.show()

    def open_customers_page(self):
        self.stack.setCurrentWidget(self.agent_customer_page)
