from PyQt5.QtWidgets import QApplication
import sys
from login_window import LoginWindow

app = QApplication(sys.argv) # determing OS
mainwindow = LoginWindow()

try: # close the application without any errors
    sys.exit(app.exec_())
except:
    print('Exiting')

