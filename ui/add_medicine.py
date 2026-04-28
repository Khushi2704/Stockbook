"""
Add medicine dialog
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton,
                             QDateEdit, QMessageBox, QFrame, QCompleter,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
from services.inventory_service import InventoryService
from utils.validators import Validator
from ui.styles import (
    get_page_title_style, get_section_title_style, get_field_label_style,
    get_primary_button_style, get_secondary_button_style, BG_WINDOW
)
import traceback


class AddMedicineDialog(QDialog):
    """Dialog to add new medicine"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Medicine")
        self.setModal(True)
        self.setGeometry(100, 100, 480, 520)
        self.setStyleSheet(f"QDialog {{ background-color: {BG_WINDOW}; }}")
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Add New Medicine")
        title.setStyleSheet(get_page_title_style())
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        # Medicine Name with autocomplete suggestions
        name_label = QLabel("Medicine Name")
        name_label.setStyleSheet(get_field_label_style())
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Aspirin, Paracetamol")
        self.name_input.setFixedHeight(38)
        layout.addWidget(self.name_input)
        
        # Add autocomplete from existing medicines
        self._setup_name_completer()
        
        # Batch Number
        batch_label = QLabel("Batch Number")
        batch_label.setStyleSheet(get_field_label_style())
        layout.addWidget(batch_label)
        self.batch_input = QLineEdit()
        self.batch_input.setPlaceholderText("e.g., AB123456")
        self.batch_input.setFixedHeight(38)
        layout.addWidget(self.batch_input)
        
        # Expiry Date
        expiry_label = QLabel("Expiry Date (DD-MM-YYYY)")
        expiry_label.setStyleSheet(get_field_label_style())
        layout.addWidget(expiry_label)
        self.expiry_input = QLineEdit()
        self.expiry_input.setInputMask("99-99-9999")
        self.expiry_input.setFixedHeight(38)
        layout.addWidget(self.expiry_input)
        
        # MRP & Net Price side by side
        price_row = QHBoxLayout()
        price_row.setSpacing(12)
        
        mrp_col = QVBoxLayout()
        mrp_label = QLabel("MRP (₹)")
        mrp_label.setStyleSheet(get_field_label_style())
        mrp_col.addWidget(mrp_label)
        self.mrp_input = QDoubleSpinBox()
        self.mrp_input.setMinimum(0.0)
        self.mrp_input.setMaximum(999999.0)
        self.mrp_input.setDecimals(2)
        self.mrp_input.setFixedHeight(38)
        mrp_col.addWidget(self.mrp_input)
        price_row.addLayout(mrp_col)
        
        net_col = QVBoxLayout()
        net_price_label = QLabel("Net Price (₹)")
        net_price_label.setStyleSheet(get_field_label_style())
        net_col.addWidget(net_price_label)
        self.net_price_input = QDoubleSpinBox()
        self.net_price_input.setMinimum(0.0)
        self.net_price_input.setMaximum(999999.0)
        self.net_price_input.setDecimals(2)
        self.net_price_input.setFixedHeight(38)
        net_col.addWidget(self.net_price_input)
        price_row.addLayout(net_col)
        
        layout.addLayout(price_row)
        
        # Stock
        stock_label = QLabel("Initial Stock (units)")
        stock_label.setStyleSheet(get_field_label_style())
        layout.addWidget(stock_label)
        self.stock_input = QSpinBox()
        self.stock_input.setMinimum(0)
        self.stock_input.setMaximum(100000)
        self.stock_input.setValue(0)
        self.stock_input.setFixedHeight(38)
        layout.addWidget(self.stock_input)
        
        layout.addSpacing(18)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        save_btn = QPushButton("Add Medicine")
        save_btn.setFixedHeight(42)
        save_btn.setStyleSheet(get_primary_button_style())
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_medicine)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(42)
        cancel_btn.setStyleSheet(get_secondary_button_style())
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set focus
        self.name_input.setFocus()
    
    # ─── ORIGINAL LOGIC (untouched) ──────────────────────────────

    def save_medicine(self):
        """Save medicine"""
        try:
            name = self.name_input.text().strip()
            batch = self.batch_input.text().strip()
            expiry_date = self.expiry_input.text().strip()
            mrp = self.mrp_input.value()
            net_price = self.net_price_input.value()
            stock = self.stock_input.value()
            
            # Validate
            valid, errors = Validator.validate_medicine_data(name, batch, expiry_date, str(mrp), str(net_price))
            
            if not valid:
                QMessageBox.warning(self, "Validation Error", "\n".join(errors))
                return
            
            # Convert DD-MM-YYYY to YYYY-MM-DD for database storage
            try:
                from datetime import datetime
                parsed = datetime.strptime(expiry_date, "%d-%m-%Y")
                expiry_date = parsed.strftime("%Y-%m-%d")
            except ValueError:
                pass  # Already in YYYY-MM-DD or will be caught by service
            
            # Add medicine
            success, result = InventoryService.add_medicine(name, batch, expiry_date, mrp, net_price, stock)
            
            if not success:
                QMessageBox.warning(self, "Error", "\n".join(result))
                return
            
            self.accept()
        
        except Exception as e:
            print(f"Error saving medicine: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to add medicine: {str(e)}")
    
    def _setup_name_completer(self):
        """Set up autocomplete for the medicine name field."""
        try:
            from models.medicine import Medicine
            medicines = Medicine.get_all()
            # Get unique names
            names = sorted(set(str(m['name']) for m in medicines if m['name']))
            completer = QCompleter(names, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            completer.setMaxVisibleItems(8)
            completer.popup().setStyleSheet("""
                QListView {
                    font-size: 12px;
                    padding: 4px;
                    border: 1px solid #1F3D2C;
                    background: white;
                }
                QListView::item:hover {
                    background: #E8F5F0;
                }
            """)
            self.name_input.setCompleter(completer)
        except Exception:
            pass
