from gui.customer_page import CustomerPage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMenu, QFrame, QScrollArea, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer
import requests
from PyQt6.QtWidgets import QWidget
from datetime import datetime
from gui.stock_chart_popup import StockChartPopup


class DashboardPage(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.active_stocks_scroll_layout = None
        self.top_gainers_scroll_layout = None
        self.top_losers_scroll_layout = None
        self.stock_alerts_scroll_layout = None
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


        # Top row
        grid.addWidget(self.create_top_gainers_card(), 0, 0)
        grid.addWidget(self.create_top_loser_card(), 0, 1)
        grid.addWidget(self.create_card(" ", "market_insights_value"), 1, 0)
        # Bottom row
        grid.addWidget(self.create_active_stocks_card(), 0, 2)
        grid.addWidget(self.create_suggestions_card(), 1, 1)
        grid.addWidget(self.create_stock_alerts_card(), 1, 2)

        self.setLayout(grid)

        # Set the text after layout has been applied
        self.update_card(
            "market_insights_value",
            "<div style='color:black;'>"
            "<div style='font-size:17px; font-weight:bold; text-align:center; padding-bottom:5px;'>Developed by GSC Pvt</div>"
            "<div style='font-size:14px; text-align:center;'>"
            "Developers:<br>"
            "Amrinder Singh<br>"
            "Felicia Forester<br>"
            "Savian Brown<br>"
            "Saniah Weston<br>"
            "Jeivan Riely"
            "</div></div>"
        )

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_active_stocks)
        self.timer.timeout.connect(self.update_top_gainers)
        self.timer.timeout.connect(self.update_top_losers)
        self.timer.timeout.connect(self.update_stock_alerts)
        self.timer.start(5000)

    def create_top_gainers_card(self):
        self.top_gainers_card = QFrame()
        self.top_gainers_card.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
        self.top_gainers_card.setFixedHeight(390)
        layout = QVBoxLayout()

        title_label = QLabel("Top Gainers")
        title_label.setFont(QFont('Arial', 16))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        self.top_gainers_scroll_layout = scroll_layout

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        self.top_gainers_card.setLayout(layout)
        # Populate the card initially
        self.update_top_gainers()
        return self.top_gainers_card

    def create_top_loser_card(self):
        self.top_losers_card = QFrame()
        self.top_losers_card.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
        self.top_losers_card.setFixedHeight(390)
        layout = QVBoxLayout()

        title_label = QLabel("Top Losers")
        title_label.setFont(QFont('Arial', 16))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        self.top_losers_scroll_layout = scroll_layout

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        self.top_losers_card.setLayout(layout)
        # Populate the card initially
        self.update_top_losers()
        return self.top_losers_card

    def create_stock_alerts_card(self):
        self.stock_alerts_card = QFrame()
        self.stock_alerts_card.setStyleSheet("background-color: #f3903a; border-radius: 5px;")
        self.stock_alerts_card.setFixedHeight(390)
        layout = QVBoxLayout()

        title_label = QLabel("Stock Alerts")
        title_label.setFont(QFont('Arial', 16))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        self.stock_alerts_scroll_layout = scroll_layout

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        self.stock_alerts_card.setLayout(layout)
        self.stock_alerts_card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.update_stock_alerts()
        return self.stock_alerts_card

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
                    suggestion_label.setFixedWidth(40)

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
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        self.active_stocks_scroll_layout = scroll_layout

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.active_stocks_card.setLayout(layout)
        # Populate the stocks initially
        self.update_active_stocks()
        return self.active_stocks_card

    def update_active_stocks(self):
        self.update_scrollable_card(
            self.active_stocks_scroll_layout,
            "http://127.0.0.1:9000/fetch/show_list",
            ["symbol", "name", "current_price"]
        )
        print("Active Stocks updated")
    def update_scrollable_card(self, layout, endpoint_url, fields, highlight_field=None, highlight_color=None):
        # Clear previous widgets
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        else:
            return
        try:
            response = requests.get(
                endpoint_url,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                stocks = response.json()
                for stock in stocks:
                    stock_box = QFrame()
                    stock_box.setStyleSheet(
                        "background-color: #F2F2F2; border: 1px solid black; border-radius: 4px; margin: 2px; padding: 0.02px;"
                    )
                    stock_box.setMinimumHeight(55)
                    stock_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    row_layout = QHBoxLayout()
                    for idx, field in enumerate(fields):
                        label = QLabel(str(stock.get(field, "")))
                        label.setFont(QFont('Arial', 12))
                        if field == "symbol":
                            label.setFixedWidth(45)
                        elif field == "name":
                            label.setFixedWidth(170)
                        label.setStyleSheet("border: none; background-color: none; color: #000000;")
                        row_layout.addWidget(label)
                    if highlight_field:
                        highlight_value = stock.get(highlight_field, "")
                        highlight_label = QLabel(f"{highlight_value}%")
                        highlight_label.setFont(QFont('Arial', 12))
                        color = highlight_color if highlight_color else "#000000"
                        highlight_label.setStyleSheet(f"border: none; background-color: none; color: {color};")
                        row_layout.addWidget(highlight_label)
                    stock_box.setLayout(row_layout)
                   
                    if "symbol" in stock:
                        symbol = stock["symbol"]
                        def make_click_handler(sym=symbol):
                            return lambda event: self.open_chart_popup(sym)
                        stock_box.mousePressEvent = make_click_handler()
                    layout.addWidget(stock_box)
            else:
                print(f"Failed to load data from {endpoint_url}:", response.text)
        except Exception as e:
            print(f"Error loading data from {endpoint_url}:", str(e))

    def update_top_gainers(self):
        self.update_scrollable_card(
            self.top_gainers_scroll_layout,
            "http://127.0.0.1:9000/win_loss/gainers",
            ["symbol", "name", "current_price"],
            "percent_change",
            "#03C04A"
        )
        print("Top Gainers updated")

    def update_top_losers(self):
        self.update_scrollable_card(
            self.top_losers_scroll_layout,
            "http://127.0.0.1:9000/win_loss/losers",
            ["symbol", "name", "current_price"],
            "percent_change",
            "#FF0000"
        )
        print("Top Losers updated")

    def update_stock_alerts(self):
        if self.stock_alerts_scroll_layout is None:
            return
        while self.stock_alerts_scroll_layout.count():
            item = self.stock_alerts_scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        try:
            response = requests.get(
                "http://127.0.0.1:9000/alert/notification",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                alerts = response.json()
                for alert in alerts:
                    symbol = alert.get('stock_symbol', '')
                    direction = alert.get('direction', '').lower()
                    change_percentage = alert.get('change_percentage', 0)
                    triggered_at_raw = alert.get('triggered_at', '')
                    try:
                        dt = datetime.fromisoformat(triggered_at_raw)
                        triggered_at = dt.strftime("%m/%d; %H:%M")
                    except Exception:
                        triggered_at = triggered_at_raw

                    alert_box = QFrame()
                    alert_box.setStyleSheet(
                        "background-color: #F2F2F2; border: 1px solid black; border-radius: 4px; margin: 2px; padding: 0.02px;"
                    )
                    alert_box.setMinimumHeight(55)
                    alert_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    row_layout = QHBoxLayout()

                    symbol_label = QLabel(symbol)
                    symbol_label.setFont(QFont('Arial', 12))
                    symbol_label.setFixedWidth(45)
                    symbol_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(symbol_label)

                    direction_label = QLabel(direction.capitalize())
                    direction_label.setFont(QFont('Arial', 12))
                    direction_label.setFixedWidth(60)
                    direction_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(direction_label)

                    change_label = QLabel(f"{change_percentage}%")
                    change_label.setFont(QFont('Arial', 12))
                    color = "#03C04A" if direction == "up" else "#FF0000" if direction == "down" else "#000000"
                    change_label.setStyleSheet(f"border: none; background-color: none; color: {color};")
                    change_label.setFixedWidth(60)
                    row_layout.addWidget(change_label)

                    triggered_label = QLabel(triggered_at)
                    triggered_label.setFont(QFont('Arial', 12))
                    triggered_label.setStyleSheet("border: none; background-color: none; color: #000000;")
                    row_layout.addWidget(triggered_label)

                    alert_box.setLayout(row_layout)
                    self.stock_alerts_scroll_layout.addWidget(alert_box)
            else:
                print("Failed to load stock alerts:", response.text)
        except Exception as e:
            print("Error loading stock alerts:", str(e))
        print("Stock Alerts updated")
    def open_chart_popup(self, symbol):
        self.chart_popup = StockChartPopup(symbol, self.token)
        self.chart_popup.show()
    def open_customer_page(self):
        self.customer_page = CustomerPage()
        self.customer_page.show()