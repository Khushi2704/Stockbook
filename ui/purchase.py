"""
Inventory window - Search and view medicines
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QMessageBox, QSpinBox, QDoubleSpinBox,
                             QDialog, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QPen, QPainterPath
from services.inventory_service import InventoryService
from utils.helpers import format_currency, format_date
from ui.styles import (
    get_page_title_style, get_section_title_style, get_field_label_style,
    get_detail_panel_style, get_stat_card_style,
    get_primary_button_style, get_secondary_button_style,
    PRIMARY, WHITE, TEXT_DARK, TEXT_MUTED
)
import traceback


class PurchaseWindow(QMainWindow):
    """Inventory search and view window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stockbook - Inventory")
        self.setGeometry(50, 50, 1050, 720)
        self.user_id = parent.user_id if parent else 1
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(0)
        
        # ── Header ────────────────────────────────────────────────
        title = QLabel("Inventory")
        title.setStyleSheet(get_page_title_style())
        layout.addWidget(title)
        layout.addSpacing(18)
        
        # ── Search Bar ────────────────────────────────────────────
        search_frame = QFrame()
        search_frame.setStyleSheet(get_stat_card_style())
        search_shadow = QGraphicsDropShadowEffect()
        search_shadow.setBlurRadius(16)
        search_shadow.setOffset(0, 2)
        search_shadow.setColor(QColor(31, 61, 44, 18))
        search_frame.setGraphicsEffect(search_shadow)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(16, 12, 16, 12)
        search_layout.setSpacing(12)
        
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 16px; background: transparent;")
        search_layout.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by medicine name or batch...")
        self.search_input.setFixedHeight(38)
        self.search_input.textChanged.connect(self.search_medicines)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_frame)
        layout.addSpacing(16)
        
        # ── Medicines Table ───────────────────────────────────────
        table_header = QLabel("ALL MEDICINES IN INVENTORY")
        table_header.setStyleSheet(get_section_title_style())
        layout.addWidget(table_header)
        layout.addSpacing(8)
        
        self.medicines_table = QTableWidget()
        self.medicines_table.setColumnCount(7)
        self.medicines_table.setHorizontalHeaderLabels(["Name", "Batch", "Expiry", "Stock", "MRP", "Net Price", "Action"])
        self.medicines_table.setAlternatingRowColors(True)
        self.medicines_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.medicines_table.horizontalHeader().setStretchLastSection(True)
        self.medicines_table.verticalHeader().setVisible(False)
        self.medicines_table.setColumnWidth(6, 90)
        layout.addWidget(self.medicines_table)
        
        # ── Bottom bar ────────────────────────────────────────────
        bottom_layout = QHBoxLayout()
        self.count_label = QLabel("")
        self.count_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")
        bottom_layout.addWidget(self.count_label)
        bottom_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet(get_secondary_button_style())
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        bottom_layout.addWidget(close_btn)
        
        layout.addSpacing(10)
        layout.addLayout(bottom_layout)
        
        central_widget.setLayout(layout)
        
        # Load all medicines
        self.load_all_medicines()
    
    def search_medicines(self, search_term):
        """Filter medicines table by search term"""
        if len(search_term.strip()) < 1:
            self.load_all_medicines()
            return
        
        try:
            medicines = InventoryService.search_medicines(search_term, self.user_id)
            self._populate_table(medicines)
        except Exception as e:
            print(f"Error searching: {e}")
    
    def load_all_medicines(self):
        """Load all medicines in table"""
        try:
            medicines = InventoryService.get_all_medicines(self.user_id)
            self._populate_table(medicines)
        except Exception as e:
            print(f"Error loading medicines: {e}")
    
    def _populate_table(self, medicines):
        """Fill the table with medicine data"""
        self.medicines_table.setRowCount(0)
        
        for row, medicine in enumerate(medicines):
            self.medicines_table.insertRow(row)
            self.medicines_table.setItem(row, 0, QTableWidgetItem(medicine['name']))
            self.medicines_table.setItem(row, 1, QTableWidgetItem(medicine['batch']))
            self.medicines_table.setItem(row, 2, QTableWidgetItem(format_date(medicine['expiry_date'])))
            self.medicines_table.setItem(row, 3, QTableWidgetItem(str(medicine['stock'])))
            self.medicines_table.setItem(row, 4, QTableWidgetItem(format_currency(medicine['mrp'])))
            self.medicines_table.setItem(row, 5, QTableWidgetItem(format_currency(medicine['net_price'])))
            
            # Edit button container for centering
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setAlignment(Qt.AlignCenter)
            
            edit_btn = QPushButton("✎ Edit")
            edit_btn.setFixedSize(65, 28)
            edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #F8F9FA; color: #333333;
                    border: 1px solid #CED4DA; border-radius: 4px;
                    font-weight: 500; font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: #E2E6EA; border-color: #DAE0E5;
                }}
            """)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setToolTip("Edit medicine")
            edit_btn.clicked.connect(lambda checked, mid=medicine['id']: self.edit_medicine(mid))
            
            action_layout.addWidget(edit_btn)
            self.medicines_table.setCellWidget(row, 6, action_widget)
        
        self.count_label.setText(f"{len(medicines)} medicine(s) found")
    

    def edit_medicine(self, medicine_id):
        """Edit medicine details"""
        medicine = InventoryService.get_medicine_details(medicine_id, self.user_id)
        if not medicine:
            QMessageBox.warning(self, "Error", "Medicine not found")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Medicine")
        dialog.setGeometry(100, 100, 420, 350)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)
        
        # Fields
        mrp_label = QLabel("MRP:")
        mrp_label.setStyleSheet(get_field_label_style())
        mrp_input = QDoubleSpinBox()
        mrp_input.setFixedHeight(38)
        mrp_input.setMaximum(999999.0)
        mrp_input.setValue(medicine['mrp'])
        layout.addWidget(mrp_label)
        layout.addWidget(mrp_input)
        
        net_price_label = QLabel("Net Price:")
        net_price_label.setStyleSheet(get_field_label_style())
        net_price_input = QDoubleSpinBox()
        net_price_input.setFixedHeight(38)
        net_price_input.setMaximum(999999.0)
        net_price_input.setValue(medicine['net_price'])
        layout.addWidget(net_price_label)
        layout.addWidget(net_price_input)
        
        stock_label = QLabel("Stock:")
        stock_label.setStyleSheet(get_field_label_style())
        stock_input = QSpinBox()
        stock_input.setFixedHeight(38)
        stock_input.setMaximum(100000)
        stock_input.setValue(medicine['stock'])
        layout.addWidget(stock_label)
        layout.addWidget(stock_input)
        
        layout.addSpacing(15)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet(get_primary_button_style())
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(lambda: self.save_edited_medicine(
            medicine_id, mrp_input.value(), net_price_input.value(), stock_input.value(), dialog
        ))
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet(get_secondary_button_style())
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec_()
    
    def save_edited_medicine(self, medicine_id, mrp, net_price, stock, dialog):
        """Save edited medicine"""
        try:
            success, msg = InventoryService.update_medicine(
                medicine_id,
                mrp=mrp,
                net_price=net_price
            )
            
            if success:
                from models.medicine import Medicine
                current_stock = InventoryService.get_medicine_stock(medicine_id)
                stock_change = stock - current_stock
                
                if stock_change != 0:
                    Medicine.set_stock(medicine_id, stock)
                
                dialog.accept()
                self.load_all_medicines()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")
