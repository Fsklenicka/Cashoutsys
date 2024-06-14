import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)
import requests

server_url = 'http://127.0.0.1:5000'


class EarningsLogger(QMainWindow):
    def __init__(self):
        super().__init__()

        self.theme = 'light'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Earnings Logger")

        self.tabs = QTabWidget()
        self.manage_tab = QWidget()
        self.view_tab = QWidget()

        self.tabs.addTab(self.manage_tab, "Manage Earnings")
        self.tabs.addTab(self.view_tab, "View Earnings")

        self.setCentralWidget(self.tabs)

        # Manage Tab Layout
        self.manage_layout = QVBoxLayout()
        self.manage_form_layout = QHBoxLayout()
        self.manage_buttons_layout = QHBoxLayout()

        self.user_label = QLabel("User ID:")
        self.user_entry = QLineEdit()

        self.amount_label = QLabel("Amount:")
        self.amount_entry = QLineEdit()

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)

        self.modify_earnings_button = QPushButton("Modify Earnings")
        self.modify_earnings_button.clicked.connect(self.modify_earnings)

        self.cashout_button = QPushButton("Cashout")
        self.cashout_button.clicked.connect(self.cashout)

        self.theme_button = QPushButton("Toggle Theme")
        self.theme_button.clicked.connect(self.toggle_theme)

        self.manage_form_layout.addWidget(self.user_label)
        self.manage_form_layout.addWidget(self.user_entry)
        self.manage_form_layout.addWidget(self.amount_label)
        self.manage_form_layout.addWidget(self.amount_entry)

        self.manage_buttons_layout.addWidget(self.add_user_button)
        self.manage_buttons_layout.addWidget(self.modify_earnings_button)
        self.manage_buttons_layout.addWidget(self.cashout_button)
        self.manage_buttons_layout.addWidget(self.theme_button)

        self.manage_layout.addLayout(self.manage_form_layout)
        self.manage_layout.addLayout(self.manage_buttons_layout)
        self.manage_tab.setLayout(self.manage_layout)

        # View Tab Layout
        self.view_layout = QVBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_earnings)

        self.earnings_list = QListWidget()

        self.view_layout.addWidget(self.refresh_button)
        self.view_layout.addWidget(self.earnings_list)
        self.view_tab.setLayout(self.view_layout)

        self.apply_theme()

    def apply_theme(self):
        if self.theme == 'light':
            self.setStyleSheet("background-color: white; color: black;")
            self.user_label.setStyleSheet("color: black;")
            self.amount_label.setStyleSheet("color: black;")
        else:
            self.setStyleSheet("background-color: black; color: white;")
            self.user_label.setStyleSheet("color: white;")
            self.amount_label.setStyleSheet("color: white;")

    def toggle_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.apply_theme()

    def add_user(self):
        user_id = self.user_entry.text().strip()
        if not user_id:
            QMessageBox.critical(self, "Error", "User ID cannot be empty")
            return

        try:
            response = requests.post(f'{server_url}/add_user', json={'user_id': user_id})
            response.raise_for_status()
            QMessageBox.information(self, "Response", response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to add user: {e}")

    def modify_earnings(self):
        user_id = self.user_entry.text().strip()
        if not user_id:
            QMessageBox.critical(self, "Error", "User ID cannot be empty")
            return

        try:
            amount = float(self.amount_entry.text().strip())
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid amount")
            return

        try:
            response = requests.post(f'{server_url}/modify_earnings', json={'user_id': user_id, 'amount': amount})
            response.raise_for_status()
            QMessageBox.information(self, "Response", response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to modify earnings: {e}")

    def cashout(self):
        user_id = self.user_entry.text().strip()
        if not user_id:
            QMessageBox.critical(self, "Error", "User ID cannot be empty")
            return

        try:
            response = requests.post(f'{server_url}/cashout', json={'user_id': user_id})
            response.raise_for_status()
            QMessageBox.information(self, "Response", response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to cashout: {e}")

    def refresh_earnings(self):
        try:
            response = requests.get(f'{server_url}/get_earnings')
            response.raise_for_status()
            earnings_data = response.json()
            self.earnings_list.clear()
            for user_id, data in earnings_data.items():
                self.earnings_list.addItem(f"User ID: {user_id} - Earnings: ${data['earnings']}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh earnings: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EarningsLogger()
    ex.show()
    sys.exit(app.exec_())
