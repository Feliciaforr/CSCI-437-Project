from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QGroupBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
import requests


class AgentsCustomerPage(QWidget):
    def __init__(self, token):
        self.token = token
        self.user_name = "Customer"
        self.account_balance = 0.0
        super().__init__()
        self.setWindowTitle("Customer Dashboard")
        self.setMinimumSize(800, 600)

        self.prices = {}
        self.update_prices_timer = QTimer()
        self.update_prices_timer.timeout.connect(self.fetch_latest_prices)

        main_layout = QVBoxLayout()

        # Title
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #34495e")
        main_layout.addWidget(self.title_label)

        self.balance_label = QLabel()
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.balance_label.setStyleSheet("font-size: 16px; color: #2c3e50; padding-right: 10px;")
        self.balance_label.setText("Balance: $0.00")
        main_layout.addWidget(self.balance_label)

        from PyQt6.QtWidgets import QComboBox

        # Inside __init__ after setting up main_layout
        self.selected_customer_id = None
        self.customer_dropdown = QComboBox()
        self.customer_dropdown.currentIndexChanged.connect(self.handle_customer_selection)
        main_layout.addWidget(self.customer_dropdown)

        # Holdings Table
        self.holdings_table = QTableWidget(0, 5)
        self.holdings_table.setHorizontalHeaderLabels(["Company", "Quantity", "Avg Buy Price", "Current Price", "P/L"])
        main_layout.addWidget(self.holdings_table)

        self.fetch_customers_list()

        # Buy/Sell Layouts
        actions_layout = QHBoxLayout()
        actions_layout.addWidget(self.create_buy_widget())
        actions_layout.addWidget(self.create_sell_widget())
        main_layout.addLayout(actions_layout)

        self.fetch_latest_prices()
        self.update_prices_timer.start(2000)  # 2 seconds
        self.load_holdings_data()
        self.portfolio_timer = QTimer()
        self.portfolio_timer.timeout.connect(self.load_holdings_data)
        self.portfolio_timer.start(30000)  # 30 seconds

        self.setLayout(main_layout)

        # Removed this line so it doesn't fetch agent info at start
        # self.fetch_user_info()
        # self.update_header()  # Set default header initially

    def fetch_user_info(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get("http://127.0.0.1:9000/auth/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                self.user_name = user_data.get("name", "Customer").split()[-1].capitalize()
                self.account_balance = user_data.get("account_balance", 0.0)
                self.update_header()
            else:
                print("Failed to fetch user info:", response.status_code)
        except Exception as e:
            print("Error fetching user info:", e)

    def update_header(self):
        self.title_label.setText(f"{self.user_name}'s Dashboard")
        self.balance_label.setText(f"Balance: ${self.account_balance:.2f}")
        self.balance_label.setStyleSheet("font-size: 16px; color: white; padding-right: 10px;")

    def fetch_latest_prices(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get("http://127.0.0.1:9000/fetch/show_list", headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.prices = {entry["symbol"]: entry["current_price"] for entry in data}
            else:
                print("Failed to fetch latest prices:", response.status_code)
        except Exception as e:
            print("Error fetching latest prices:", e)

        current_buy_selection = self.buy_dropdown.currentText()
        current_sell_selection = self.sell_dropdown.currentText()

        self.buy_dropdown.blockSignals(True)
        self.sell_dropdown.blockSignals(True)

        self.buy_dropdown.clear()
        self.buy_dropdown.addItems(sorted(self.prices.keys()))
        self.sell_dropdown.clear()
        self.sell_dropdown.addItems(sorted(self.prices.keys()))

        self.buy_dropdown.setCurrentText(current_buy_selection)
        self.sell_dropdown.setCurrentText(current_sell_selection)

        self.buy_dropdown.blockSignals(False)
        self.sell_dropdown.blockSignals(False)

    def load_holdings_data(self):
        if not self.selected_customer_id:
            return
        try:
            print("Fetching holdings data...")
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"http://127.0.0.1:9000/agent/customer/{self.selected_customer_id}/portfolio"
            response = requests.get(url, headers=headers)
            print("Response status:", response.status_code)
            print("Response content:", response.text)
            if response.status_code == 200:
                holdings = response.json()
                print("Parsed holdings:", holdings)
                self.holdings_table.setRowCount(len(holdings))
                for row, h in enumerate(holdings):
                    pl_item = QTableWidgetItem(f"${h['profit_or_loss']:.2f}")
                    pl_item.setForeground(Qt.GlobalColor.green if h["profit_or_loss"] >= 0 else Qt.GlobalColor.red)

                    self.holdings_table.setItem(row, 0, QTableWidgetItem(h["stock"]))
                    self.holdings_table.setItem(row, 1, QTableWidgetItem(str(h["quantity"])))
                    self.holdings_table.setItem(row, 2, QTableWidgetItem(f"${h['average_price']:.2f}"))
                    self.holdings_table.setItem(row, 3, QTableWidgetItem(f"${h['current_price']:.2f}"))
                    self.holdings_table.setItem(row, 4, pl_item)
            else:
                print("Failed to fetch holdings:", response.status_code)
        except Exception as e:
            print("Error loading holdings:", e)

    def create_buy_widget(self):
        group = QGroupBox("Buy Stocks")
        layout = QVBoxLayout()

        self.buy_dropdown = QComboBox()
        self.buy_dropdown.addItems(sorted(self.prices.keys()))

        self.buy_quantity = QLineEdit()
        self.buy_quantity.setPlaceholderText("Enter quantity")
        self.buy_quantity.textChanged.connect(self.update_buy_total)

        self.buy_total = QLabel("Total: $0")

        buy_btn = QPushButton("Buy")
        buy_btn.clicked.connect(self.buy_stock)

        layout.addWidget(self.buy_dropdown)
        layout.addWidget(self.buy_quantity)
        layout.addWidget(self.buy_total)
        layout.addWidget(buy_btn)

        group.setLayout(layout)
        return group

    def create_sell_widget(self):
        group = QGroupBox("Sell Stocks")
        layout = QVBoxLayout()

        self.sell_dropdown = QComboBox()
        self.sell_dropdown.addItems(sorted(self.prices.keys()))

        self.sell_quantity = QLineEdit()
        self.sell_quantity.setPlaceholderText("Enter quantity")
        self.sell_quantity.textChanged.connect(self.update_sell_total)

        self.sell_total = QLabel("Total: $0")

        sell_btn = QPushButton("Sell")
        sell_btn.clicked.connect(self.sell_stock)

        layout.addWidget(self.sell_dropdown)
        layout.addWidget(self.sell_quantity)
        layout.addWidget(self.sell_total)
        layout.addWidget(sell_btn)

        group.setLayout(layout)
        return group

    def update_buy_total(self):
        try:
            qty = int(self.buy_quantity.text())
            if qty < 0:
                raise ValueError
            symbol = self.buy_dropdown.currentText()
            price_per_unit = self.prices.get(symbol, 100)
            self.buy_total.setText(f"Total: ${qty * price_per_unit:.2f}")
        except ValueError:
            self.buy_total.setText("Total: $0")

    def update_sell_total(self):
        try:
            qty = int(self.sell_quantity.text())
            if qty < 0:
                raise ValueError
            symbol = self.sell_dropdown.currentText()
            price_per_unit = self.prices.get(symbol, 100)
            self.sell_total.setText(f"Total: ${qty * price_per_unit:.2f}")
        except ValueError:
            self.sell_total.setText("Total: $0")

    def buy_stock(self):
        try:
            qty = int(self.buy_quantity.text())
            if qty <= 0:
                raise ValueError
            stock = self.buy_dropdown.currentText()
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            data = {"symbol": stock, "quantity": qty}
            url = f"http://127.0.0.1:9000/agent/customer/{self.selected_customer_id}/buy"
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                msg = (
                    f"{result['message']}\n"
                    f"Stock: {result['stock']}\n"
                    f"Quantity: {result['quantity']}\n"
                    f"Total Cost: ${result['total_cost']:.2f}\n"
                    f"Remaining Balance: ${result['remaining_balance']:.2f}"
                )
                QMessageBox.information(self, "Buy Success", msg)
                self.load_holdings_data()
                self.fetch_customer_balance()
            else:
                try:
                    error_msg = response.json().get("error", response.text)
                except Exception:
                    error_msg = response.text
                QMessageBox.warning(self, "Buy Failed", f"Error: {error_msg}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid whole number")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def sell_stock(self):
        try:
            qty = int(self.sell_quantity.text())
            if qty <= 0:
                raise ValueError
            stock = self.sell_dropdown.currentText()
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            data = {"symbol": stock, "quantity": qty}
            url = f"http://127.0.0.1:9000/agent/customer/{self.selected_customer_id}/sell"
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                msg = (
                    f"{result['message']}\n"
                    f"Stock: {result['stock']}\n"
                    f"Quantity: {result['quantity']}\n"
                    f"Total Earnings: ${result['total_earnings']:.2f}\n"
                    f"Updated Balance: ${result['updated_balance']:.2f}"
                )
                QMessageBox.information(self, "Sell Success", msg)
                self.load_holdings_data()
                self.fetch_customer_balance()
            else:
                error_msg = response.json().get("error", response.text)
                QMessageBox.warning(self, "Sell Failed", f"Error: {error_msg}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid whole number")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def fetch_customers_list(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get("http://127.0.0.1:9000/agent/customers", headers=headers)
            if response.status_code == 200:
                customers = response.json()
                self.customer_dropdown.clear()
                self.customer_map = {}
                for customer in customers:
                    full_name = f"{customer['first_name']} {customer['last_name']}"
                    self.customer_map[full_name] = customer["id"]
                    self.customer_dropdown.addItem(full_name)
            else:
                print("Failed to fetch customer list:", response.status_code)
        except Exception as e:
            print("Error fetching customers:", e)

    def handle_customer_selection(self, index):
        name = self.customer_dropdown.currentText()
        self.selected_customer_id = self.customer_map.get(name)
        print(f"Selected Customer ID: {self.selected_customer_id}")
        self.load_holdings_data()
        self.fetch_customer_balance()

    def fetch_customer_balance(self):
        if not self.selected_customer_id:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"http://127.0.0.1:9000/agent/customer/{self.selected_customer_id}/me"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                full_name = user_data.get("name", "Customer")
                self.user_name = full_name.split()[0].capitalize()
                self.account_balance = user_data.get("account_balance", 0.0)
                self.update_header()
            else:
                print("Failed to fetch customer info:", response.status_code)
        except Exception as e:
            print("Error fetching customer info:", e)
