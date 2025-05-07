from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests
import matplotlib.pyplot as plt
import mplcursors

class StockChartPopup(QWidget):
    def __init__(self, symbol, token):
        super().__init__()
        self.symbol = symbol
        self.token = token
        self.setWindowTitle(f"{symbol} Stock Chart")
        self.resize(800, 620)

        layout = QVBoxLayout()

        self.label = QLabel(f"Showing chart for {symbol}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.selected_range = "1D"

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create horizontal button layout
        button_layout = QHBoxLayout()
        self.buttons = {}
        for label in ["1D", "1W", "1M", "3M", "1Y", "5Y"]:
            btn = QPushButton(label)
            btn.setStyleSheet("color: white; background-color: #222;")
            btn.clicked.connect(lambda _, l=label: self.on_range_selected(l))
            button_layout.addWidget(btn)
            self.buttons[label] = btn
        button_layout.setContentsMargins(0, 0, 0, 5)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_if_live)
        self.timer.start(20000)  # 20 seconds

        self.dot_timer = QTimer(self)
        self.dot_timer.timeout.connect(self.toggle_dot_visibility)
        self.dot_visible = True
        self.last_point_artist = None

        self.update_chart()

    def on_range_selected(self, label):
        self.selected_range = label
        self.update_chart()

    def update_chart(self):
        range_map = {
            "1D": "1 Day",
            "1W": "7 Days",
            "1M": "1 Month",
            "3M": "3 Months",
            "1Y": "1 Year",
            "5Y": "5 Years"
        }
        option = range_map.get(self.selected_range, "7 Days")
        headers = {"Authorization": f"Bearer {self.token}"}

        if option == "1 Day":
            url = f"http://127.0.0.1:9000/fetch/stocks/today/{self.symbol}"
        else:
            range_param_map = {
                "7 Days": "7d",
                "1 Month": "1m",
                "3 Months": "3m",
                "1 Year": "1y",
                "5 Years": "5y"
            }
            range_param = range_param_map.get(option, "7d")
            url = f"http://127.0.0.1:9000//fetch/stocks/history/{self.symbol}?range={range_param}"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                x_vals = [entry.get("timestamp") or entry.get("date") for entry in data]
                y_vals = [entry["price"] for entry in data]

                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.set_facecolor("#000000")
                self.figure.set_facecolor("#000000")

                x_vals, y_vals = zip(*sorted(zip(x_vals, y_vals)))

                line, = ax.plot(x_vals, y_vals, color="#00FF00", linewidth=2)
                cursor = mplcursors.cursor(line, hover=True)
                cursor.connect("add", lambda sel: (
                    sel.annotation.set_text(f"{y_vals[int(sel.index)]} at {x_vals[int(sel.index)]}"),
                    sel.annotation.get_bbox_patch().set(fc="white", alpha=0.95)
                ))

                ax.set_title(f"{self.symbol} - {option}", color="white")
                ax.set_xlabel("Time", color="white")
                ax.set_ylabel("Price", color="white")
                ax.tick_params(colors="white")
                ax.set_xticklabels([])
                # ax.legend()  # Removed legend
                self.canvas.draw()

                # Plot blinking dot at the end
                if self.selected_range == "1D" and x_vals and y_vals:
                    if self.last_point_artist:
                        try:
                            self.last_point_artist.remove()
                        except Exception:
                            pass
                    self.last_dot_x = x_vals[-1]
                    self.last_dot_y = y_vals[-1]
                    self.last_point_artist = ax.plot(self.last_dot_x, self.last_dot_y, 'o', color="#00FF00", markersize=8)[0]
                    self.dot_visible = True
                    self.dot_timer.start(500)
                else:
                    if self.last_point_artist:
                        try:
                            self.last_point_artist.remove()
                        except Exception:
                            pass
                        self.last_point_artist = None
                    self.dot_timer.stop()

                self.timer.start(30000) if option == "1 Day" else self.timer.stop()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception occurred: {e}")

    def refresh_if_live(self):
        if self.selected_range == "1D":
            self.update_chart()

    def toggle_dot_visibility(self):
        if self.last_point_artist:
            self.last_point_artist.set_visible(self.dot_visible)
            self.canvas.draw_idle()
            self.dot_visible = not self.dot_visible
