"""Capture updated login screenshot"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from database.db import init_database
from database.upgrade import upgrade_to_multitenancy
from ui.styles import get_global_stylesheet
from ui.login import LoginDialog

app = QApplication(sys.argv)
app.setStyleSheet(get_global_stylesheet())
init_database()
upgrade_to_multitenancy()

dialog = LoginDialog()
dialog.show()

def take_screenshot():
    ss = dialog.grab()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "login_screenshot_v2.png")
    ss.save(path)
    print(f"Saved: {path}")
    dialog.close()
    app.quit()

QTimer.singleShot(1500, take_screenshot)
sys.exit(app.exec_())
