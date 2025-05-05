from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests

class StockChartPopup(QWidget):
    def __init__(self, symbol, token):
        super().__init__()
        self.symbol = symbol
        self.token = token
        self.setWindowTitle(f"{symbol} Stock Chart")
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.label = QLabel(f"Showing chart for {symbol}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["1 Day", "7 Days", "1 Month", "3 Months", "1 Year", "5 Years"])
        self.combo.currentIndexChanged.connect(self.update_chart)
        layout.addWidget(self.combo)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_if_live)
        self.timer.start(20000)  # 20 seconds
        self.update_chart()

    def update_chart(self):
        option = self.combo.currentText()
        headers = {"Authorization": f"Bearer {self.token}"}

        if option == "1 Day":
            url = f"http://127.0.0.1:9000/fetch/stocks/today/{self.symbol}"
        else:
            range_map = {
                "7 Days": "7d",
                "1 Month": "1m",
                "3 Months": "3m",
                "1 Year": "1y",
                "5 Years": "5y"
            }
            range_param = range_map.get(option, "7d")
            url = f"http://127.0.0.1:9000//fetch/stocks/history/{self.symbol}?range={range_param}"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                x_vals = [entry.get("timestamp") or entry.get("date") for entry in data]
                y_vals = [entry["price"] for entry in data]

                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot(x_vals, y_vals, label="Close Price")
                ax.set_title(f"{self.symbol} - {option}")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price")
                ax.legend()
                self.canvas.draw()
                self.timer.start(20000) if option == "1 Day" else self.timer.stop()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception occurred: {e}")

    def refresh_if_live(self):
        if self.combo.currentText() == "1 Day":
            self.update_chart()
