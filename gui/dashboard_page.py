# dashboard_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMenu, QFrame
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

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

        # Top Cards
        card_layout = QHBoxLayout()
        self.top_gainer_card = self.create_card("Top Gainer", "top_gainer_value", "up_arrow.png")
        self.top_loser_card = self.create_card("Top Loser", "top_loser_value", "down_arrow.png")
        self.stock_alerts_card = self.create_card("Stock Alerts", "stock_alerts_value", note_label_id="stock_alerts_note")

        card_layout.addWidget(self.top_gainer_card)
        card_layout.addWidget(self.top_loser_card)
        card_layout.addWidget(self.stock_alerts_card)

        main_layout.addLayout(card_layout)

        # Bottom Cards
        bottom_layout = QHBoxLayout()
        self.market_insights_card = self.create_card("Market Insights", "market_insights_value")
        self.active_stocks_card = self.create_card("Active Stocks", "active_stocks_value", note_label_id="active_stocks_note")

        bottom_layout.addWidget(self.market_insights_card)
        bottom_layout.addWidget(self.active_stocks_card)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

