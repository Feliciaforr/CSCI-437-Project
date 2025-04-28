# customer_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Customer Page
class CustomerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Customer Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #34495e")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        view_btn = QPushButton("View My Stocks")
        buy_btn = QPushButton("Buy Stocks")
        sell_btn = QPushButton("Sell Stocks")
        transactions_btn = QPushButton("View My Transactions")

        for btn in [view_btn, buy_btn, sell_btn, transactions_btn]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("font-size: 16px;")

        layout.addWidget(title)
        layout.addWidget(view_btn)
        layout.addWidget(buy_btn)
        layout.addWidget(sell_btn)
        layout.addWidget(transactions_btn)
        layout.addStretch()

        self.setLayout(layout)

