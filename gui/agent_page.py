# agent_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Agent Page
class AgentPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Agent Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #34495e")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AgentPage()
    window.setWindowTitle("Agent Dashboard")
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
