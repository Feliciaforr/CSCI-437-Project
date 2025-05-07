# app.py (for frontend GUI)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication, QStackedWidget
from gui.login_page import LoginPage
from gui.dashboard_page import DashboardPage
from gui.main_window import MainWindow

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.login_page = LoginPage(self)
        self.addWidget(self.login_page)
        self.setCurrentWidget(self.login_page)

    def show_dashboard(self, token):
        self.dashboard = DashboardPage(token)
        self.addWidget(self.dashboard)
        self.setCurrentWidget(self.dashboard)
        
    def show_main_window(self, token, role):
        self.main_window = MainWindow(token, role)
        self.addWidget(self.main_window)
        self.setCurrentWidget(self.main_window)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #000000;
            color: #E6EDF3;
        }
        QScrollArea, QFrame, QLabel {
            background-color: #000000;
            color: #E6EDF3;
        }
        QPushButton {
            background-color: #21262D;
            color: #E6EDF3;
            border: 1px solid #30363D;
            border-radius: 6px;
            padding: 4px 8px;
        }
        QPushButton:hover {
            background-color: #30363D;
        }
    """)
    main_app = MainApp()
    main_app.setWindowTitle("StockSight")
    main_app.resize(1200, 800)
    main_app.show()
    sys.exit(app.exec())