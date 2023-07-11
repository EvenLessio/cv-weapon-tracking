from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from settings_window import SettingsWindow
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi('UI/login_window.ui', self)

        self.register_button.clicked.connect(self.go_to_register_page)
        self.login_button.clicked.connect(self.open_settings_window)

        self.show()  # login window will be displayed

    def go_to_register_page(self):
        print("Go To Register Page")

    def open_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.displayInfo()
        self.close()
        print("Go To Settings Window")

