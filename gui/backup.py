from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMenu, QFrame, QScrollArea, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import requests
from PyQt6.QtWidgets import QWidget

# Home page
class DashboardPage(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.initUI()

    def create_card(self, title, value_label_id, arrow=None, note_label_id=None):
        frame = QFrame()
        frame.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
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
        from PyQt6.QtWidgets import QGridLayout
        grid = QGridLayout()

        # Place all cards at precise positions in the grid
        # Top row
        grid.addWidget(self.create_top_gainers_card(), 0, 0)
        grid.addWidget(self.create_top_loser_card(), 0, 1)
        grid.addWidget(self.create_card("Market Insights", "market_insights_value"), 1, 0)
        # Bottom row
        grid.addWidget(self.create_active_stocks_card(), 0, 2)
        grid.addWidget(self.create_suggestions_card(), 1, 1)
        grid.addWidget(self.create_stock_alerts_card(), 1, 2)

        self.setLayout(grid)

    def create_top_gainers_card(self):
        self.top_gainers_card = QFrame()
        self.top_gainers_card.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
        layout = QVBoxLayout()

        title_label = QLabel("Top Gainers")
        title_label.setFont(QFont('Arial', 16))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        try:
            response = requests.get(
                "http://127.0.0.1:9000/win_loss/gainers",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                gainers = response.json()
                for stock in gainers:
                    stock_box = QFrame()
                    stock_box.setStyleSheet(
                        "background-color: #F2F2F2; border: 1px solid black; border-radius: 4px; margin: 2px; padding: 0.02px;"
                    )
                    stock_box.setMinimumHeight(35)
                    row_layout = QHBoxLayout()

                    symbol_label = QLabel(stock['symbol'])
                    name_label = QLabel(stock['name'])
                    price_label = QLabel(f"${stock['current_price']}")
                    percent_label = QLabel(f"{stock['percent_change']}%")

                    symbol_label.setFont(QFont('Arial', 12))
                    symbol_label.setFixedWidth(40)
                    symbol_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(symbol_label)

                    name_label.setFont(QFont('Arial', 12))
                    name_label.setFixedWidth(170)
                    name_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(name_label)

                    price_label.setFont(QFont('Arial', 12))
                    price_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(price_label)

                    percent_label.setFont(QFont('Arial', 12))
                    percent_label.setStyleSheet("border: none; background-color: none; color: #03C04A;")
                    
                    row_layout.addWidget(percent_label)

                    stock_box.setLayout(row_layout)
                    layout.addWidget(stock_box)
            else:
                print("Failed to load top gainers:", response.text)
        except Exception as e:
            print("Error loading top gainers:", str(e))

        self.top_gainers_card.setLayout(layout)
        return self.top_gainers_card

    def create_top_loser_card(self):
        self.top_losers_card = QFrame()
        self.top_losers_card.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
        layout = QVBoxLayout()

        title_label = QLabel("Top Losers")
        title_label.setFont(QFont('Arial', 16))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        try:
            response = requests.get(
                "http://127.0.0.1:9000/win_loss/losers",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                losers = response.json()
                for stock in losers:
                    stock_box = QFrame()
                    stock_box.setStyleSheet(
                        "background-color: #F2F2F2; border: 1px solid black; border-radius: 4px; margin: 2px; padding: 0.02px;"
                    )
                    stock_box.setMinimumHeight(35)
                    row_layout = QHBoxLayout()

                    symbol_label = QLabel(stock['symbol'])
                    name_label = QLabel(stock['name'])
                    price_label = QLabel(f"${stock['current_price']}")
                    percent_label = QLabel(f"{stock['percent_change']}%")

                    symbol_label.setFont(QFont('Arial', 12))
                    symbol_label.setFixedWidth(45)
                    symbol_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(symbol_label)

                    name_label.setFont(QFont('Arial', 12))
                    name_label.setFixedWidth(170)
                    name_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(name_label)

                    price_label.setFont(QFont('Arial', 12))
                    price_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(price_label)

                    percent_label.setFont(QFont('Arial', 12))
                    percent_label.setStyleSheet("border: none; background-color: none; color: #FF0000;")
                    row_layout.addWidget(percent_label)

                    stock_box.setLayout(row_layout)
                    layout.addWidget(stock_box)
            else:
                print("Failed to load top losers:", response.text)
        except Exception as e:
            print("Error loading top losers:", str(e))

        self.top_losers_card.setLayout(layout)
        return self.top_losers_card

    def create_stock_alerts_card(self):
        return self.create_card("Stock Alerts", "stock_alerts_value", note_label_id="stock_alerts_note")

    def create_suggestions_card(self):
        self.suggestions_card = QFrame()
        self.suggestions_card.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
        layout = QVBoxLayout()

        title_label = QLabel("Market Suggestions")
        title_label.setFont(QFont('Arial', 16))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        try:
            response = requests.get(
                "http://127.0.0.1:9000/suggest/suggestions",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                suggestions = response.json()
                for stock in suggestions:
                    stock_box = QFrame()
                    stock_box.setStyleSheet(
                        "background-color: #F2F2F2; border: 1px solid black; border-radius: 4px; margin: 2px; padding: 0.02px;"
                    )
                    stock_box.setMinimumHeight(35)
                    row_layout = QHBoxLayout()

                    symbol_label = QLabel(stock['symbol'])
                    name_label = QLabel(stock['name'])
                    price_label = QLabel(f"${stock['current_price']}")
                    suggestion_label = QLabel(stock['suggestion'])

                    symbol_label.setFont(QFont('Arial', 12))
                    symbol_label.setFixedWidth(45)
                    symbol_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(symbol_label)

                    name_label.setFont(QFont('Arial', 12))
                    name_label.setFixedWidth(170)
                    name_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(name_label)

                    price_label.setFont(QFont('Arial', 12))
                    price_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(price_label)

                    suggestion_label.setFont(QFont('Arial', 12))
                    if stock['suggestion'] == 'BUY':
                        suggestion_label.setStyleSheet("border: none; background-color: none; color: #03C04A;")
                    elif stock['suggestion'] == 'SELL':
                        suggestion_label.setStyleSheet("border: none; background-color: none; color: #FF0000;")
                    else:
                        suggestion_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(suggestion_label)

                    stock_box.setLayout(row_layout)
                    layout.addWidget(stock_box)
            else:
                print("Failed to load suggestions:", response.text)
        except Exception as e:
            print("Error loading suggestions:", str(e))

        self.suggestions_card.setLayout(layout)
        return self.suggestions_card

    def create_active_stocks_card(self):
        self.active_stocks_card = QFrame()
        self.active_stocks_card.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
        self.active_stocks_card.setFixedHeight(390)
        layout = QVBoxLayout()

        title_label = QLabel("Active Stocks")
        title_label.setFont(QFont('Arial', 16))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        try:
            response = requests.get(
                "http://127.0.0.1:9000/fetch/show_list",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                active_stocks = response.json()
                for stock in active_stocks:
                    stock_box = QFrame()
                    stock_box.setStyleSheet(
                        "background-color: #F2F2F2; border: 1px solid black; border-radius: 4px; margin: 2px; padding: 0.02px;"
                    )
                    stock_box.setMinimumHeight(35)
                    row_layout = QHBoxLayout()

                    symbol_label = QLabel(stock['symbol'])
                    name_label = QLabel(stock['name'])
                    price_label = QLabel(f"${stock['current_price']}")

                    symbol_label.setFont(QFont('Arial', 12))
                    symbol_label.setFixedWidth(45)
                    symbol_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(symbol_label)

                    name_label.setFont(QFont('Arial', 12))
                    name_label.setFixedWidth(170)
                    name_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(name_label)

                    price_label.setFont(QFont('Arial', 12))
                    price_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(price_label)

                    stock_box.setLayout(row_layout)
                    scroll_layout.addWidget(stock_box)
            else:
                print("Failed to load active stocks:", response.text)
        except Exception as e:
            print("Error loading active stocks:", str(e))

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        layout.addWidget(scroll_area)
        self.active_stocks_card.setLayout(layout)
        return self.active_stocks_card