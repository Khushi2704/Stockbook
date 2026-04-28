"""
Backup and Restore management window
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QTableWidget, 
                             QTableWidgetItem, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.helpers import backup_database, restore_database, get_backup_list
from ui.styles import (
    get_page_title_style, get_section_title_style, get_status_label_style,
    get_primary_button_style, get_secondary_button_style,
    get_accent_button_style, get_danger_button_style
)
import traceback
import os


class BackupWindow(QMainWindow):
    """Backup and Restore management window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stockbook - Backup & Restore")
        self.setGeometry(50, 50, 720, 520)
        self.init_ui()
        self.load_backups()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(0)
        
        # Header
        title = QLabel("Backup & Restore")
        title.setStyleSheet(get_page_title_style())
        layout.addWidget(title)
        layout.addSpacing(18)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        backup_btn = QPushButton("Create New Backup")
        backup_btn.setFixedHeight(42)
        backup_btn.setStyleSheet(get_primary_button_style())
        backup_btn.setCursor(Qt.PointingHandCursor)
        backup_btn.clicked.connect(self.create_backup)
        button_layout.addWidget(backup_btn)
        
        restore_btn = QPushButton("Restore Selected")
        restore_btn.setFixedHeight(42)
        restore_btn.setStyleSheet(get_accent_button_style())
        restore_btn.setCursor(Qt.PointingHandCursor)
        restore_btn.clicked.connect(self.restore_backup)
        button_layout.addWidget(restore_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.setFixedHeight(42)
        delete_btn.setStyleSheet(get_danger_button_style())
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_backup)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        layout.addSpacing(18)
        
        # Backups table
        backups_label = QLabel("AVAILABLE BACKUPS")
        backups_label.setStyleSheet(get_section_title_style())
        layout.addWidget(backups_label)
        layout.addSpacing(8)
        
        self.backups_table = QTableWidget()
        self.backups_table.setColumnCount(3)
        self.backups_table.setHorizontalHeaderLabels(["Filename", "Size", "Created"])
        self.backups_table.setAlternatingRowColors(True)
        self.backups_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.backups_table.horizontalHeader().setStretchLastSection(True)
        self.backups_table.verticalHeader().setVisible(False)
        layout.addWidget(self.backups_table)
        
        # Info label
        self.info_label = QLabel("Status: Ready")
        self.info_label.setStyleSheet(get_status_label_style())
        layout.addSpacing(8)
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        
        central_widget.setLayout(layout)
    
    # ─── ALL ORIGINAL LOGIC BELOW (untouched) ─────────────────────

    def load_backups(self):
        """Load list of available backups"""
        try:
            backups = get_backup_list()
            self.backups_table.setRowCount(0)
            
            for backup in backups:
                row = self.backups_table.rowCount()
                self.backups_table.insertRow(row)
                
                # Filename
                filename = os.path.basename(backup['path'])
                self.backups_table.setItem(row, 0, QTableWidgetItem(filename))
                
                # Size
                size_mb = backup['size'] / (1024 * 1024)
                self.backups_table.setItem(row, 1, QTableWidgetItem(f"{size_mb:.2f} MB"))
                
                # Created date
                self.backups_table.setItem(row, 2, QTableWidgetItem(backup['created']))
            
            self.info_label.setText(f"Status: {len(backups)} backup(s) available")
        except Exception as e:
            self.info_label.setText(f"Error loading backups: {str(e)}")
    
    def create_backup(self):
        """Create a new backup"""
        try:
            backup_file = backup_database()
            self.load_backups()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create backup:\n{str(e)}")
            traceback.print_exc()
    
    def restore_backup(self):
        """Restore selected backup"""
        current_row = self.backups_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a backup to restore")
            return
        
        filename = self.backups_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(
            self, "Confirm Restore",
            f"This will replace your current database with the backup:\n{filename}\n\n"
            "Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            backups = get_backup_list()
            if current_row < len(backups):
                backup_path = backups[current_row]['path']
                restore_database(backup_path)
                self.load_backups()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to restore backup:\n{str(e)}")
            traceback.print_exc()
    
    def delete_backup(self):
        """Delete selected backup"""
        current_row = self.backups_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a backup to delete")
            return
        
        filename = self.backups_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete this backup?\n{filename}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            backups = get_backup_list()
            if current_row < len(backups):
                backup_path = backups[current_row]['path']
                os.remove(backup_path)
                self.load_backups()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete backup:\n{str(e)}")
            traceback.print_exc()
