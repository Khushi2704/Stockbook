"""
User Management and Subscription window
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QTableWidget, 
                             QTableWidgetItem, QDialog, QLineEdit, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from models.user import User
from utils.helpers import hash_password
from ui.styles import (
    get_page_title_style, get_section_title_style, get_status_label_style,
    get_field_label_style, get_primary_button_style, get_secondary_button_style,
    get_danger_button_style, get_accent_button_style,
    PRIMARY, PRIMARY_LIGHT, WHITE, TEXT_DARK, BG_WINDOW
)
import traceback


class UserManagementWindow(QMainWindow):
    """User Management and Subscription Control window"""
    
    def __init__(self, parent=None, user_id=None):
        super().__init__(parent)
        
        # Security check - only admin can access
        if user_id != 1:
            QMessageBox.critical(None, "Access Denied", "Only the admin user can access User Management!")
            return
        
        self.user_id = user_id
        self.setWindowTitle("Stockbook - User Management & Subscriptions")
        self.setGeometry(50, 50, 1000, 620)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(0)
        
        # Header
        title = QLabel("User Management")
        title.setStyleSheet(get_page_title_style())
        layout.addWidget(title)
        layout.addSpacing(18)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        add_user_btn = QPushButton("Add New User")
        add_user_btn.setFixedHeight(42)
        add_user_btn.setStyleSheet(get_primary_button_style())
        add_user_btn.setCursor(Qt.PointingHandCursor)
        add_user_btn.clicked.connect(self.add_new_user)
        button_layout.addWidget(add_user_btn)
        
        activate_btn = QPushButton("Activate Selected")
        activate_btn.setFixedHeight(42)
        activate_btn.setStyleSheet(get_accent_button_style())
        activate_btn.setCursor(Qt.PointingHandCursor)
        activate_btn.clicked.connect(self.activate_user)
        button_layout.addWidget(activate_btn)
        
        deactivate_btn = QPushButton("Deactivate Selected")
        deactivate_btn.setFixedHeight(42)
        deactivate_btn.setStyleSheet(get_danger_button_style())
        deactivate_btn.setCursor(Qt.PointingHandCursor)
        deactivate_btn.clicked.connect(self.deactivate_user)
        button_layout.addWidget(deactivate_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addSpacing(18)
        
        # Users table
        users_label = QLabel("REGISTERED USERS")
        users_label.setStyleSheet(get_section_title_style())
        layout.addWidget(users_label)
        layout.addSpacing(8)
        
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Username", "Status", "Created", "Action"])
        self.users_table.setColumnWidth(0, 50)
        self.users_table.setColumnWidth(1, 180)
        self.users_table.setColumnWidth(2, 120)
        self.users_table.setColumnWidth(3, 160)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.verticalHeader().setVisible(False)
        layout.addWidget(self.users_table)
        
        # Info label
        self.info_label = QLabel("Status: Ready")
        self.info_label.setStyleSheet(get_status_label_style())
        layout.addSpacing(8)
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        
        central_widget.setLayout(layout)
    
    # ─── ALL ORIGINAL LOGIC BELOW (untouched) ─────────────────────

    def load_users(self):
        """Load all users"""
        try:
            users = User.get_all_with_status()
            self.users_table.setRowCount(0)
            
            for user in users:
                row = self.users_table.rowCount()
                self.users_table.insertRow(row)
                
                # ID
                self.users_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
                
                # Username
                self.users_table.setItem(row, 1, QTableWidgetItem(user['username']))
                
                # Status
                status = user['status']
                status_item = QTableWidgetItem(status)
                if status == 'Active':
                    status_item.setBackground(QColor(144, 238, 144))  # Light green
                else:
                    status_item.setBackground(QColor(255, 192, 192))  # Light red
                self.users_table.setItem(row, 2, status_item)
                
                # Created date
                self.users_table.setItem(row, 3, QTableWidgetItem(str(user['created_at'])[:10]))
                
                # Action buttons
                action_text = "Active" if user['is_active'] else "Inactive"
                self.users_table.setItem(row, 4, QTableWidgetItem(action_text))
            
            self.info_label.setText(f"Status: {len(users)} user(s) registered")
        except Exception as e:
            self.info_label.setText(f"Error loading users: {str(e)}")
            traceback.print_exc()
    
    def add_new_user(self):
        """Add a new user"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New User")
        dialog.setGeometry(100, 100, 420, 340)
        dialog.setStyleSheet(f"QDialog {{ background-color: {BG_WINDOW}; }}")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)
        
        # Username
        u_label = QLabel("Username")
        u_label.setStyleSheet(get_field_label_style())
        layout.addWidget(u_label)
        username_input = QLineEdit()
        username_input.setFixedHeight(38)
        layout.addWidget(username_input)
        
        layout.addSpacing(4)
        
        # Password
        p_label = QLabel("Password")
        p_label.setStyleSheet(get_field_label_style())
        layout.addWidget(p_label)
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setFixedHeight(38)
        layout.addWidget(password_input)
        
        layout.addSpacing(4)
        
        # Confirm Password
        c_label = QLabel("Confirm Password")
        c_label.setStyleSheet(get_field_label_style())
        layout.addWidget(c_label)
        confirm_input = QLineEdit()
        confirm_input.setEchoMode(QLineEdit.Password)
        confirm_input.setFixedHeight(38)
        layout.addWidget(confirm_input)
        
        layout.addSpacing(16)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        create_btn = QPushButton("Create User")
        create_btn.setFixedHeight(42)
        create_btn.setStyleSheet(get_primary_button_style())
        create_btn.setCursor(Qt.PointingHandCursor)
        def create_user():
            username = username_input.text().strip()
            password = password_input.text()
            confirm = confirm_input.text()
            
            if not username or not password or not confirm:
                QMessageBox.warning(dialog, "Error", "Please fill all fields")
                return
            
            if password != confirm:
                QMessageBox.warning(dialog, "Error", "Passwords do not match")
                return
            
            if len(password) < 6:
                QMessageBox.warning(dialog, "Error", "Password must be at least 6 characters")
                return
            
            try:
                if User.exists(username):
                    QMessageBox.warning(dialog, "Error", "Username already exists")
                    return
                
                user_id = User.create(username, password)
                dialog.accept()
                self.load_users()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Failed to create user: {str(e)}")
        
        create_btn.clicked.connect(create_user)
        button_layout.addWidget(create_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(42)
        cancel_btn.setStyleSheet(get_secondary_button_style())
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def activate_user(self):
        """Activate selected user"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a user to activate")
            return
        
        user_id = int(self.users_table.item(current_row, 0).text())
        username = self.users_table.item(current_row, 1).text()
        
        try:
            if User.activate_user(user_id):
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", "Failed to activate user")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            traceback.print_exc()
    
    def deactivate_user(self):
        """Deactivate selected user"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a user to deactivate")
            return
        
        user_id = int(self.users_table.item(current_row, 0).text())
        username = self.users_table.item(current_row, 1).text()
        
        # Prevent deactivating admin user (ID 1)
        if user_id == 1:
            QMessageBox.warning(self, "Error", "Cannot deactivate the admin user")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Deactivation",
            f"Deactivate user '{username}'? They won't be able to login.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            if User.deactivate_user(user_id):
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", "Failed to deactivate user")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            traceback.print_exc()
