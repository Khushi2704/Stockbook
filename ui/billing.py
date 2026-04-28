"""
Billing window - Core billing interface for sales
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QLabel, QMessageBox, QSpinBox, QDoubleSpinBox, 
                             QComboBox, QDialog, QFrame, QSizePolicy,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from services.billing_service import BillingService
from services.inventory_service import InventoryService
from utils.helpers import format_currency, format_date
from utils.printer import BillPrinter
from ui.styles import (
    PRIMARY, PRIMARY_LIGHT, TEXT_DARK, TEXT_SECONDARY, TEXT_MUTED, WHITE,
    BG_WINDOW, CARD_BORDER_SOLID, INPUT_BORDER, DIVIDER,
    get_page_title_style, get_section_title_style, get_field_label_style,
    get_detail_panel_style, get_bill_summary_style,
    get_primary_button_style, get_secondary_button_style,
    get_accent_button_style, get_warning_button_style,
    get_stat_card_style
)
from datetime import datetime
import traceback


class BillingWindow(QMainWindow):
    """Billing window for sales transactions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stockbook - Billing")
        self.setGeometry(50, 50, 1100, 750)
        self.user_id = parent.user_id if parent else 1
        self.billing_service = BillingService(self.user_id)
        self.bill_printer = BillPrinter()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(20)
        
        # ══════════════════════════════════════════════════════════
        #  LEFT PANEL — Search & Add Items
        # ══════════════════════════════════════════════════════════
        left_frame = QFrame()
        left_frame.setStyleSheet(get_stat_card_style())
        left_shadow = QGraphicsDropShadowEffect()
        left_shadow.setBlurRadius(16)
        left_shadow.setOffset(0, 2)
        left_shadow.setColor(QColor(31, 61, 44, 18))
        left_frame.setGraphicsEffect(left_shadow)
        
        left_panel = QVBoxLayout(left_frame)
        left_panel.setContentsMargins(20, 20, 20, 20)
        left_panel.setSpacing(10)
        
        # Section title
        search_title = QLabel("ADD ITEM TO BILL")
        search_title.setStyleSheet(get_section_title_style())
        left_panel.addWidget(search_title)
        left_panel.addSpacing(6)
        
        # Search
        search_label = QLabel("Search Medicine")
        search_label.setStyleSheet(get_field_label_style())
        left_panel.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type medicine name or batch...")
        self.search_input.setFixedHeight(38)
        self.search_input.textChanged.connect(self.search_medicines)
        left_panel.addWidget(self.search_input)
        
        # Search results dropdown
        self.medicine_combo = QComboBox()
        self.medicine_combo.setFixedHeight(38)
        self.medicine_combo.currentIndexChanged.connect(self.on_medicine_selected)
        left_panel.addWidget(self.medicine_combo)
        
        # Medicine details
        self.medicine_details_label = QLabel()
        self.medicine_details_label.setStyleSheet(get_detail_panel_style())
        self.medicine_details_label.setMinimumHeight(80)
        left_panel.addWidget(self.medicine_details_label)
        
        left_panel.addSpacing(6)
        
        # Quantity & Price row
        qty_price_layout = QHBoxLayout()
        qty_price_layout.setSpacing(12)
        
        qty_col = QVBoxLayout()
        qty_label = QLabel("Quantity")
        qty_label.setStyleSheet(get_field_label_style())
        qty_col.addWidget(qty_label)
        self.qty_spinbox = QSpinBox()
        self.qty_spinbox.setMinimum(1)
        self.qty_spinbox.setMaximum(10000)
        self.qty_spinbox.setValue(1)
        self.qty_spinbox.setFixedHeight(38)
        qty_col.addWidget(self.qty_spinbox)
        qty_price_layout.addLayout(qty_col)
        
        price_col = QVBoxLayout()
        price_label = QLabel("Unit Price (MRP)")
        price_label.setStyleSheet(get_field_label_style())
        price_col.addWidget(price_label)
        self.price_spinbox = QDoubleSpinBox()
        self.price_spinbox.setMinimum(0.0)
        self.price_spinbox.setMaximum(999999.0)
        self.price_spinbox.setDecimals(2)
        self.price_spinbox.setFixedHeight(38)
        price_col.addWidget(self.price_spinbox)
        qty_price_layout.addLayout(price_col)
        
        left_panel.addLayout(qty_price_layout)
        
        left_panel.addSpacing(10)
        
        # Add to bill button
        add_btn = QPushButton("Add to Bill")
        add_btn.setFixedHeight(44)
        add_btn.setStyleSheet(get_primary_button_style())
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_to_bill)
        left_panel.addWidget(add_btn)
        
        left_panel.addStretch()
        
        # ══════════════════════════════════════════════════════════
        #  RIGHT PANEL — Bill Display
        # ══════════════════════════════════════════════════════════
        right_frame = QFrame()
        right_frame.setStyleSheet(get_stat_card_style())
        right_shadow = QGraphicsDropShadowEffect()
        right_shadow.setBlurRadius(16)
        right_shadow.setOffset(0, 2)
        right_shadow.setColor(QColor(31, 61, 44, 18))
        right_frame.setGraphicsEffect(right_shadow)
        
        right_panel = QVBoxLayout(right_frame)
        right_panel.setContentsMargins(20, 20, 20, 20)
        right_panel.setSpacing(10)
        
        bill_title = QLabel("BILL ITEMS")
        bill_title.setStyleSheet(get_section_title_style())
        right_panel.addWidget(bill_title)
        right_panel.addSpacing(4)
        
        # Bill table
        self.bill_table = QTableWidget()
        self.bill_table.setColumnCount(6)
        self.bill_table.setHorizontalHeaderLabels(["Medicine", "Batch", "Qty", "Price", "Amount", ""])
        self.bill_table.setAlternatingRowColors(True)
        self.bill_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bill_table.horizontalHeader().setStretchLastSection(True)
        self.bill_table.verticalHeader().setVisible(False)
        self.bill_table.setColumnWidth(5, 50)
        right_panel.addWidget(self.bill_table)
        
        # Bill summary
        self.bill_summary_label = QLabel()
        self.bill_summary_label.setStyleSheet(get_bill_summary_style())
        self.bill_summary_label.setText("Total Amount: ₹0.00  |  Profit: ₹0.00")
        right_panel.addWidget(self.bill_summary_label)
        
        # Payment mode toggle
        payment_layout = QHBoxLayout()
        payment_layout.setSpacing(0)
        
        payment_label = QLabel("Payment:")
        payment_label.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {TEXT_DARK};")
        payment_layout.addWidget(payment_label)
        payment_layout.addSpacing(8)
        
        self.cash_btn = QPushButton("Cash")
        self.cash_btn.setFixedHeight(38)
        self.cash_btn.setCheckable(True)
        self.cash_btn.setChecked(True)
        self.cash_btn.setCursor(Qt.PointingHandCursor)
        self.cash_btn.clicked.connect(lambda: self._set_payment_mode('Cash'))
        payment_layout.addWidget(self.cash_btn)
        
        self.online_btn = QPushButton("Online")
        self.online_btn.setFixedHeight(38)
        self.online_btn.setCheckable(True)
        self.online_btn.setCursor(Qt.PointingHandCursor)
        self.online_btn.clicked.connect(lambda: self._set_payment_mode('Online'))
        payment_layout.addWidget(self.online_btn)
        
        payment_layout.addStretch()
        right_panel.addLayout(payment_layout)
        
        self.payment_mode = 'Cash'
        self._update_payment_buttons()
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        clear_btn = QPushButton("Clear Bill")
        clear_btn.setFixedHeight(42)
        clear_btn.setStyleSheet(get_secondary_button_style())
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_bill)
        button_layout.addWidget(clear_btn)
        
        print_btn = QPushButton("Print Bill")
        print_btn.setFixedHeight(42)
        print_btn.setStyleSheet(get_accent_button_style())
        print_btn.setCursor(Qt.PointingHandCursor)
        print_btn.clicked.connect(self.print_bill)
        button_layout.addWidget(print_btn)
        
        finalize_btn = QPushButton("Finalize Sale")
        finalize_btn.setFixedHeight(42)
        finalize_btn.setStyleSheet(get_warning_button_style())
        finalize_btn.setCursor(Qt.PointingHandCursor)
        finalize_btn.clicked.connect(self.finalize_sale)
        button_layout.addWidget(finalize_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(42)
        close_btn.setStyleSheet(get_secondary_button_style())
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        right_panel.addLayout(button_layout)
        
        # Combine panels
        main_layout.addWidget(left_frame, 1)
        main_layout.addWidget(right_frame, 2)
        
        central_widget.setLayout(main_layout)
        
        # Set focus on search
        self.search_input.setFocus()
    
    # ─── ALL ORIGINAL LOGIC BELOW (untouched) ─────────────────────

    def search_medicines(self, search_term):
        """Search medicines"""
        self.medicine_combo.clear()
        
        if len(search_term.strip()) < 1:
            self.medicine_details_label.setText("")
            return
        
        try:
            medicines = InventoryService.search_medicines(search_term, self.user_id)
            
            for medicine in medicines:
                display_text = f"{medicine['name']} (Batch: {medicine['batch']}, Exp: {format_date(medicine['expiry_date'])})"
                self.medicine_combo.addItem(display_text, medicine['id'])
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed: {str(e)}")
    
    def on_medicine_selected(self):
        """Handle medicine selection"""
        try:
            if self.medicine_combo.currentIndex() == -1:
                self.medicine_details_label.setText("")
                return
            
            medicine_id = self.medicine_combo.currentData()
            medicine = InventoryService.get_medicine_details(medicine_id, self.user_id)
            
            if medicine:
                profit_per_unit = medicine['mrp'] - medicine['net_price']
                details_text = (
                    f"Name: {medicine['name']}\n"
                    f"Batch: {medicine['batch']}\n"
                    f"Expiry: {format_date(medicine['expiry_date'])}\n"
                    f"MRP: {format_currency(medicine['mrp'])}\n"
                    f"Net Price: {format_currency(medicine['net_price'])}\n"
                    f"Profit/Unit: {format_currency(profit_per_unit)}\n"
                    f"Stock: {medicine['stock']} units"
                )
                self.medicine_details_label.setText(details_text)
                
                # Auto-fill price
                self.price_spinbox.setValue(medicine['mrp'])
                self.qty_spinbox.setValue(1)
        
        except Exception as e:
            print(f"Error selecting medicine: {e}")
    
    def add_to_bill(self):
        """Add item to bill"""
        try:
            if self.medicine_combo.currentIndex() == -1:
                QMessageBox.warning(self, "Error", "Please select a medicine first")
                return
            
            medicine_id = self.medicine_combo.currentData()
            quantity = self.qty_spinbox.value()
            unit_price = self.price_spinbox.value()
            
            success, msg = self.billing_service.add_item_to_bill(medicine_id, quantity, unit_price)
            
            if not success:
                QMessageBox.warning(self, "Error", msg)
                return
            
            self.update_bill_display()
            
            # Reset inputs
            self.medicine_combo.setCurrentIndex(-1)
            self.search_input.clear()
            self.search_input.setFocus()
        
        except Exception as e:
            print(f"Error adding to bill: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to add item: {str(e)}")
    
    def update_bill_display(self):
        """Update bill display table"""
        items = self.billing_service.get_bill_items()
        self.bill_table.setRowCount(0)
        
        for index, item in enumerate(items):
            self.bill_table.insertRow(index)
            self.bill_table.setItem(index, 0, QTableWidgetItem(item['medicine_name']))
            self.bill_table.setItem(index, 1, QTableWidgetItem(item['batch']))
            self.bill_table.setItem(index, 2, QTableWidgetItem(str(item['quantity'])))
            self.bill_table.setItem(index, 3, QTableWidgetItem(format_currency(item['unit_price'])))
            self.bill_table.setItem(index, 4, QTableWidgetItem(format_currency(item['amount'])))
            
            remove_btn = QPushButton("✕")
            remove_btn.setFixedSize(32, 28)
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FDEDEC; color: #E74C3C;
                    border: 1px solid #F5C6CB; border-radius: 6px;
                    font-weight: 700; font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #E74C3C; color: #FFFFFF;
                }
            """)
            remove_btn.setCursor(Qt.PointingHandCursor)
            remove_btn.setToolTip("Remove item")
            remove_btn.clicked.connect(lambda checked, i=index: self.remove_from_bill(i))
            self.bill_table.setCellWidget(index, 5, remove_btn)
        
        # Update summary
        total = self.billing_service.get_bill_total()
        profit = self.billing_service.get_bill_profit()
        self.bill_summary_label.setText(
            f"Total Amount: {format_currency(total)}  |  Profit: {format_currency(profit)}"
        )
    
    def remove_from_bill(self, index):
        """Remove item from bill"""
        self.billing_service.remove_item_from_bill(index)
        self.update_bill_display()
    
    def clear_bill(self):
        """Clear entire bill"""
        reply = QMessageBox.question(self, "Clear Bill", "Clear all items from bill?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.billing_service.clear_bill()
            self.update_bill_display()
    
    def _set_payment_mode(self, mode):
        """Set payment mode"""
        self.payment_mode = mode
        self._update_payment_buttons()
    
    def _update_payment_buttons(self):
        """Update payment button styles based on selected mode"""
        active_style = f"""
            QPushButton {{
                background-color: {PRIMARY}; color: #FFFFFF;
                border: none; border-radius: 8px;
                padding: 6px 16px; font-size: 13px; font-weight: 700;
            }}
        """
        inactive_style = f"""
            QPushButton {{
                background-color: {WHITE}; color: {TEXT_DARK};
                border: 1.5px solid {CARD_BORDER_SOLID};
                border-radius: 8px; padding: 6px 16px;
                font-size: 13px; font-weight: 600;
            }}
            QPushButton:hover {{
                border-color: {PRIMARY};
            }}
        """
        if self.payment_mode == 'Cash':
            self.cash_btn.setStyleSheet(active_style)
            self.cash_btn.setChecked(True)
            self.online_btn.setStyleSheet(inactive_style)
            self.online_btn.setChecked(False)
        else:
            self.online_btn.setStyleSheet(active_style)
            self.online_btn.setChecked(True)
            self.cash_btn.setStyleSheet(inactive_style)
            self.cash_btn.setChecked(False)
    
    def _create_invoice_dialog(self, items, total, profit=None, title="Bill Preview"):
        """Create a professional GST invoice-style dialog"""
        from datetime import datetime
        import json, os
        
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setGeometry(80, 60, 700, 580)
        dialog.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(0)
        
        # Load full shop profile from config
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profile_config.json")
        pharmacy_name = "My Pharmacy"
        phone = address = gst_no = ""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    cfg = json.load(f)
                    pharmacy_name = cfg.get('pharmacy_name', pharmacy_name)
                    phone         = cfg.get('phone', '')
                    address       = cfg.get('address', '')
                    gst_no        = cfg.get('gst_no', '')
        except Exception:
            pass
        
        # Header
        header = QLabel(pharmacy_name.upper())
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: 700; color: #1F3D2C; letter-spacing: 2px;")
        layout.addWidget(header)
        
        subtitle = QLabel("MEDICAL STORE  |  GST INVOICE")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 11px; color: #555; margin-bottom: 2px;")
        layout.addWidget(subtitle)
        
        # Address line
        if address:
            addr_lbl = QLabel(address)
            addr_lbl.setAlignment(Qt.AlignCenter)
            addr_lbl.setStyleSheet("font-size: 10px; color: #555;")
            layout.addWidget(addr_lbl)
        
        contact_parts = []
        if phone:  contact_parts.append(f"Ph: {phone}")
        if gst_no: contact_parts.append(f"GST: {gst_no}")
        if contact_parts:
            contact_lbl = QLabel("  |  ".join(contact_parts))
            contact_lbl.setAlignment(Qt.AlignCenter)
            contact_lbl.setStyleSheet("font-size: 10px; color: #555; margin-bottom: 2px;")
            layout.addWidget(contact_lbl)
        
        div1 = QFrame()
        div1.setFrameShape(QFrame.HLine)
        div1.setStyleSheet("color: #1F3D2C; margin: 6px 0;")
        layout.addWidget(div1)
        
        # Invoice info row
        info_layout = QHBoxLayout()
        now = datetime.now()
        inv_no = f"INV-{now.strftime('%Y%m%d%H%M%S')}"
        
        left_info = QLabel(f"Invoice No: {inv_no}")
        left_info.setStyleSheet("font-size: 11px; color: #333; font-weight: 600;")
        info_layout.addWidget(left_info)
        info_layout.addStretch()
        right_info = QLabel(f"Date: {now.strftime('%d-%m-%Y')}    Time: {now.strftime('%H:%M:%S')}")
        right_info.setStyleSheet("font-size: 11px; color: #333; font-weight: 600;")
        info_layout.addWidget(right_info)
        layout.addLayout(info_layout)
        layout.addSpacing(8)
        
        # Items Table
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["S.No", "Item Name", "Batch", "Expiry", "Qty", "Rate", "Amount"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setColumnWidth(0, 40)
        table.setColumnWidth(1, 180)
        table.setColumnWidth(2, 90)
        table.setColumnWidth(3, 80)
        table.setColumnWidth(4, 45)
        table.setColumnWidth(5, 80)
        table.horizontalHeader().setStretchLastSection(True)
        table.setStyleSheet("""
            QTableWidget { border: 1px solid #1F3D2C; gridline-color: #ccc; font-size: 11px; }
            QHeaderView::section { background-color: #1F3D2C; color: white; font-weight: 700; font-size: 11px; padding: 6px 4px; border: none; }
            QTableWidget::item { padding: 4px 6px; }
        """)
        
        table.setRowCount(len(items))
        for i, item in enumerate(items):
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            table.setItem(i, 1, QTableWidgetItem(item['medicine_name']))
            table.setItem(i, 2, QTableWidgetItem(item['batch']))
            table.setItem(i, 3, QTableWidgetItem(format_date(item.get('expiry_date', ''))))
            table.setItem(i, 4, QTableWidgetItem(str(item['quantity'])))
            table.setItem(i, 5, QTableWidgetItem(format_currency(item['unit_price'])))
            table.setItem(i, 6, QTableWidgetItem(format_currency(item['amount'])))
            for col in [0, 4, 5, 6]:
                table.item(i, col).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        layout.addWidget(table)
        layout.addSpacing(8)
        
        div2 = QFrame()
        div2.setFrameShape(QFrame.HLine)
        div2.setStyleSheet("color: #1F3D2C;")
        layout.addWidget(div2)
        layout.addSpacing(4)
        
        # Totals
        totals_layout = QHBoxLayout()
        totals_layout.addStretch()
        totals_text = f"Total Amount:  {format_currency(total)}"
        total_label = QLabel(totals_text)
        total_label.setStyleSheet("font-size: 14px; font-weight: 700; color: #1F3D2C;")
        totals_layout.addWidget(total_label)
        layout.addLayout(totals_layout)
        layout.addSpacing(4)
        
        pay_layout = QHBoxLayout()
        pay_layout.addStretch()
        pay_label = QLabel(f"Payment: {self.payment_mode}")
        pay_label.setStyleSheet("font-size: 11px; color: #555; font-weight: 600;")
        pay_layout.addWidget(pay_label)
        layout.addLayout(pay_layout)
        layout.addSpacing(8)
        
        div3 = QFrame()
        div3.setFrameShape(QFrame.HLine)
        div3.setStyleSheet("color: #1F3D2C;")
        layout.addWidget(div3)
        
        footer = QLabel("Thank You! Visit Again")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 12px; font-weight: 600; color: #1F3D2C; margin-top: 6px;")
        layout.addWidget(footer)
        layout.addSpacing(12)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(38)
        close_btn.setStyleSheet(get_secondary_button_style())
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        return dialog

    def print_bill(self):
        """Print the bill"""
        try:
            items = self.billing_service.get_bill_items()
            if not items:
                QMessageBox.warning(self, "Error", "Bill is empty")
                return
            total = self.billing_service.get_bill_total()
            profit = self.billing_service.get_bill_profit()
            dialog = self._create_invoice_dialog(items, total, title="Bill Preview")
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate bill: {str(e)}")
    
    def finalize_sale(self):
        """Finalize and complete the sale"""
        try:
            items = self.billing_service.get_bill_items()
            if not items:
                QMessageBox.warning(self, "Error", "Bill is empty")
                return
            saved_items = list(items)
            success, msg, transaction = self.billing_service.finalize_sale()
            if not success:
                QMessageBox.critical(self, "Error", msg)
                return
            total = transaction['total_amount']
            profit = transaction['total_profit']
            dialog = self._create_invoice_dialog(saved_items, total, title="Sale Receipt")
            dialog.exec_()
            self.update_bill_display()
            self.search_input.clear()
            self.search_input.setFocus()
            if hasattr(self.parent(), 'refresh_alerts'):
                self.parent().refresh_alerts()
        except Exception as e:
            print(f"Error finalizing sale: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to finalize sale: {str(e)}")

