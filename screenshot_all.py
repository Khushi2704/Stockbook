"""Capture screenshots of all main screens"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from database.db import init_database
from database.upgrade import upgrade_to_multitenancy
from ui.styles import get_global_stylesheet

app = QApplication(sys.argv)
app.setStyleSheet(get_global_stylesheet())

init_database()
upgrade_to_multitenancy()

screenshots_taken = []

def capture_dashboard():
    from ui.dashboard import Dashboard
    dashboard = Dashboard(1)
    dashboard.show()
    
    def grab_dashboard():
        ss = dashboard.grab()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "screenshot_dashboard.png")
        ss.save(path)
        print(f"Dashboard saved: {path}")
        screenshots_taken.append(path)
        dashboard.close()
        capture_billing()
    
    QTimer.singleShot(1500, grab_dashboard)

def capture_billing():
    from ui.dashboard import Dashboard
    parent = Dashboard(1)
    parent.show()
    
    from ui.billing import BillingWindow
    billing = BillingWindow(parent)
    billing.show()
    
    def grab_billing():
        ss = billing.grab()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "screenshot_billing.png")
        ss.save(path)
        print(f"Billing saved: {path}")
        screenshots_taken.append(path)
        billing.close()
        parent.close()
        print("All screenshots captured!")
        app.quit()
    
    QTimer.singleShot(1500, grab_billing)

capture_dashboard()
sys.exit(app.exec_())
