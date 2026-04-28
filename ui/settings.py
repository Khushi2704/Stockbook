"""
Settings and Configuration window
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QLineEdit, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from models.user import User
from utils.helpers import verify_password
from ui.styles import (
    get_page_title_style, get_field_label_style,
    get_primary_button_style, get_secondary_button_style, BG_WINDOW
)
import traceback


class SettingsWindow(QMainWindow):
    """Settings and Configuration window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stockbook - Settings")
        self.setGeometry(50, 50, 500, 440)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(0)
        
        # Header
        title = QLabel("Settings")
        title.setStyleSheet(get_page_title_style())
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Change Password Section
        password_group = QGroupBox("Change Password")
        password_layout = QVBoxLayout()
        password_layout.setContentsMargins(16, 20, 16, 16)
        password_layout.setSpacing(8)
        
        # Current password
        cur_label = QLabel("Current Password")
        cur_label.setStyleSheet(get_field_label_style())
        password_layout.addWidget(cur_label)
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setFixedHeight(38)
        password_layout.addWidget(self.current_password_input)
        
        password_layout.addSpacing(6)
        
        # New password
        new_label = QLabel("New Password")
        new_label.setStyleSheet(get_field_label_style())
        password_layout.addWidget(new_label)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setFixedHeight(38)
        password_layout.addWidget(self.new_password_input)
        
        password_layout.addSpacing(6)
        
        # Confirm password
        conf_label = QLabel("Confirm Password")
        conf_label.setStyleSheet(get_field_label_style())
        password_layout.addWidget(conf_label)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setFixedHeight(38)
        password_layout.addWidget(self.confirm_password_input)
        
        password_group.setLayout(password_layout)
        layout.addWidget(password_group)
        
        layout.addSpacing(20)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        change_pwd_btn = QPushButton("Change Password")
        change_pwd_btn.setFixedHeight(42)
        change_pwd_btn.setStyleSheet(get_primary_button_style())
        change_pwd_btn.setCursor(Qt.PointingHandCursor)
        change_pwd_btn.clicked.connect(self.change_password)
        button_layout.addWidget(change_pwd_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(42)
        close_btn.setStyleSheet(get_secondary_button_style())
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        central_widget.setLayout(layout)
    
    # ─── ORIGINAL LOGIC (untouched) ──────────────────────────────

    def change_password(self):
        """Change user password"""
        current_pwd = self.current_password_input.text()
        new_pwd = self.new_password_input.text()
        confirm_pwd = self.confirm_password_input.text()
        
        # Validation
        if not all([current_pwd, new_pwd, confirm_pwd]):
            QMessageBox.warning(self, "Validation", "Please fill all password fields")
            return
        
        if new_pwd != confirm_pwd:
            QMessageBox.warning(self, "Validation", "New passwords do not match")
            return
        
        if len(new_pwd) < 6:
            QMessageBox.warning(self, "Validation", "Password must be at least 6 characters")
            return
        
        try:
            # Change password using the correct method
            result = User.change_password(1, current_pwd, new_pwd)
            
            if not result:
                QMessageBox.warning(self, "Error", "Current password is incorrect")
                return
            
            # Clear fields
            self.current_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to change password:\n{str(e)}")
            traceback.print_exc()
