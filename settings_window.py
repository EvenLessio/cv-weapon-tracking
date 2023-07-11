from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from detection_window import DetectionWindow
class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        loadUi('UI/settings_window.ui', self)

        self.detection_window = DetectionWindow()

        self.start_button.clicked.connect(self.go_to_detection)

    def displayInfo(self):
        self.show()
    def go_to_detection(self):
        if self.detection_window.isVisible():
            print('Detection Window already opened')
        else:
            self.detection_window.create_detection_instance()
            self.detection_window.start_detection()

    def closeEvent(self, event):
        if self.detection_window.isVisible():
            self.detection_dindow.detection.running = False
            self.detection_window.close()
            event.accept()
