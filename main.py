"""
Main application entry point
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from database.db import init_database
from database.upgrade import upgrade_to_multitenancy
from ui.login import LoginDialog
from ui.dashboard import Dashboard
from ui.styles import get_global_stylesheet
import traceback

def global_exception_handler(exc_type, exc_value, exc_traceback):
    with open("crash.log", "w") as f:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = global_exception_handler


# Set to True to skip login during development, False for production
DEV_MODE = True


class StockbookApp:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(get_global_stylesheet())
        self.current_window = None
        self.user_id = None
        self.init_database()
        if DEV_MODE:
            self.user_id = 1
            self.show_dashboard()
        else:
            self.show_login()
    
    def init_database(self):
        """Initialize database"""
        try:
            init_database()
            upgrade_to_multitenancy()  # Upgrade for multi-tenancy support
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to initialize database: {str(e)}")
            sys.exit(1)
    
    def show_login(self):
        """Show login dialog"""
        login_dialog = LoginDialog()
        login_dialog.login_successful.connect(self.on_login_success)
        
        if login_dialog.exec_():
            pass
        else:
            sys.exit(0)
    
    def on_login_success(self, user_id):
        """Handle successful login"""
        self.user_id = user_id
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show main dashboard"""
        self.current_window = Dashboard(self.user_id)
        self.current_window.logged_out.connect(self.on_logout)
        self.current_window.show()
    
    def on_logout(self):
        """Handle logout"""
        # Prevent the application from quitting when the dashboard closes during logout
        self.app.setQuitOnLastWindowClosed(False)
        
        if self.current_window:
            self.current_window.close()
            
        self.show_login()
        
        # Re-enable quit on last window closed after we're back
        self.app.setQuitOnLastWindowClosed(True)
    
    def run(self):
        """Run the application"""
        return self.app.exec_()


def main():
    """Application entry point"""
    try:
        app = StockbookApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"Application error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
