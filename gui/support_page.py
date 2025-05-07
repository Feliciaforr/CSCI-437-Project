# support_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Support Page
class SupportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        welcome_label = QLabel("Welcome to the Support Page")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(welcome_label)

        issue_label = QLabel("Please select your issue:")
        layout.addWidget(issue_label)

        self.issue_combo = QComboBox()
        self.issue_combo.addItems([
            "Unable to log in",
            "Dashboard not loading",
            "Data not updating",
            "Feature request",
            "Others"
        ])
        self.issue_combo.currentTextChanged.connect(self.toggle_textbox)
        layout.addWidget(self.issue_combo)

        self.issue_text = QTextEdit()
        self.issue_text.setPlaceholderText("Please describe your issue...")
        self.issue_text.hide()
        layout.addWidget(self.issue_text)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_issue)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
            }
            QLabel {
                font-size: 14px;
            }
            QComboBox, QTextEdit, QPushButton {
                font-size: 14px;
                padding: 6px;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
        """)

    def toggle_textbox(self, text):
        self.issue_text.setVisible(text == "Others")

    def submit_issue(self):
        issue = self.issue_combo.currentText()
        description = self.issue_text.toPlainText() if issue == "Others" else issue
        QMessageBox.information(self, "Issue Submitted", f"Your issue has been submitted:\n\n{description}")

# ------ End of support_page.py ------

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SupportPage()
    window.setWindowTitle("Support Page")
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())