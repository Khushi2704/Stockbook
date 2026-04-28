"""
Receipts window - View and download all confirmed sale receipts
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QMessageBox, QDialog, QFrame,
                             QGraphicsDropShadowEffect, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from utils.helpers import format_currency, format_date
from ui.styles import (
    get_page_title_style, get_section_title_style, get_field_label_style,
    get_stat_card_style, get_primary_button_style, get_secondary_button_style,
    get_accent_button_style, get_warning_button_style,
    PRIMARY, WHITE, TEXT_DARK, TEXT_MUTED, CARD_BORDER_SOLID
)
from database.db import fetch_all
from datetime import datetime
import traceback
import json
import os


class ReceiptsWindow(QMainWindow):
    """Window to view all confirmed sale receipts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stockbook - Receipts")
        self.setGeometry(50, 50, 1050, 720)
        self.user_id = parent.user_id if parent else 1
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(0)
        
        # Title
        title = QLabel("Sale Receipts")
        title.setStyleSheet(get_page_title_style())
        layout.addWidget(title)
        layout.addSpacing(18)
        
        # ── Receipts Table ────────────────────────────────────────
        table_label = QLabel("ALL CONFIRMED SALES")
        table_label.setStyleSheet(get_section_title_style())
        layout.addWidget(table_label)
        layout.addSpacing(8)
        
        self.receipts_table = QTableWidget()
        self.receipts_table.setColumnCount(8)
        self.receipts_table.setHorizontalHeaderLabels([
            "Date", "Time", "Medicine", "Qty", "Unit Price", "Total", "Profit", "Actions"
        ])
        self.receipts_table.setAlternatingRowColors(True)
        self.receipts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.receipts_table.verticalHeader().setVisible(False)
        self.receipts_table.setColumnWidth(0, 100)
        self.receipts_table.setColumnWidth(1, 60)
        self.receipts_table.setColumnWidth(2, 160)
        self.receipts_table.setColumnWidth(3, 45)
        self.receipts_table.setColumnWidth(4, 95)
        self.receipts_table.setColumnWidth(5, 95)
        self.receipts_table.setColumnWidth(6, 90)
        self.receipts_table.setColumnWidth(7, 200)
        self.receipts_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.receipts_table)
        
        # ── Bottom Bar ────────────────────────────────────────────
        bottom_layout = QHBoxLayout()
        
        self.count_label = QLabel("")
        self.count_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")
        bottom_layout.addWidget(self.count_label)
        
        bottom_layout.addStretch()
        
        download_all_btn = QPushButton("Download All as CSV")
        download_all_btn.setFixedHeight(40)
        download_all_btn.setStyleSheet(get_warning_button_style())
        download_all_btn.setCursor(Qt.PointingHandCursor)
        download_all_btn.clicked.connect(self.download_all_csv)
        bottom_layout.addWidget(download_all_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet(get_secondary_button_style())
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        bottom_layout.addWidget(close_btn)
        
        layout.addSpacing(10)
        layout.addLayout(bottom_layout)
        
        central_widget.setLayout(layout)
        
        # Load receipts
        self.load_receipts()
    
    def load_receipts(self):
        """Load all confirmed sale receipts"""
        try:
            sales = fetch_all("""
                SELECT s.id, m.name as medicine_name, s.quantity,
                       s.unit_price, s.total_price, s.profit, s.date
                FROM sales s
                LEFT JOIN medicines m ON s.medicine_id = m.id
                WHERE s.user_id = ?
                ORDER BY s.date DESC
            """, (self.user_id,))
            
            self.receipts_table.setRowCount(0)
            
            for i, row in enumerate(sales):
                self.receipts_table.insertRow(i)
                raw_date = str(row['date']) if row['date'] else ''
                date_part = raw_date[:10] if raw_date else ''
                time_part = raw_date[11:16] if len(raw_date) > 10 else ''
                
                self.receipts_table.setItem(i, 0, QTableWidgetItem(date_part))
                self.receipts_table.setItem(i, 1, QTableWidgetItem(time_part))
                self.receipts_table.setItem(i, 2, QTableWidgetItem(str(row['medicine_name'] or 'Unknown')))
                self.receipts_table.setItem(i, 3, QTableWidgetItem(str(row['quantity'])))
                self.receipts_table.setItem(i, 4, QTableWidgetItem(format_currency(row['unit_price'])))
                self.receipts_table.setItem(i, 5, QTableWidgetItem(format_currency(row['total_price'])))
                self.receipts_table.setItem(i, 6, QTableWidgetItem(format_currency(row['profit'])))
                
                # Action buttons container
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(6, 4, 6, 4)
                action_layout.setSpacing(8)
                
                view_btn = QPushButton("📄 View")
                view_btn.setFixedHeight(28)
                view_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {PRIMARY}; color: #FFFFFF;
                        border: none; border-radius: 6px;
                        font-weight: 600; font-size: 11px;
                        padding: 2px 12px;
                    }}
                    QPushButton:hover {{ background-color: #24A074; }}
                """)
                view_btn.setCursor(Qt.PointingHandCursor)
                sale_id = row['id']
                view_btn.clicked.connect(lambda checked, sid=sale_id: self.view_receipt(sid))
                action_layout.addWidget(view_btn)
                
                download_btn = QPushButton("⬇ Download")
                download_btn.setFixedHeight(28)
                download_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498DB; color: #FFFFFF;
                        border: none; border-radius: 6px;
                        font-weight: 600; font-size: 11px;
                        padding: 2px 12px;
                    }
                    QPushButton:hover { background-color: #2980B9; }
                """)
                download_btn.setCursor(Qt.PointingHandCursor)
                download_btn.clicked.connect(lambda checked, sid=sale_id: self.download_receipt(sid))
                action_layout.addWidget(download_btn)
                
                self.receipts_table.setCellWidget(i, 7, action_widget)
                self.receipts_table.setRowHeight(i, 40)
            
            self.count_label.setText(f"{len(sales)} sale(s) found")
        
        except Exception as e:
            print(f"Error loading receipts: {e}")
            traceback.print_exc()
    
    def _get_sale_data(self, sale_id):
        """Get full sale data for a receipt"""
        sale = fetch_all("""
            SELECT s.id, m.name as medicine_name, m.batch, m.expiry_date,
                   s.quantity, s.unit_price, s.total_price, s.profit, s.date
            FROM sales s
            LEFT JOIN medicines m ON s.medicine_id = m.id
            WHERE s.id = ? AND s.user_id = ?
        """, (sale_id, self.user_id))
        return sale
    
    def _load_profile(self):
        """Load shop profile config"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profile_config.json")
        pharmacy_name = "My Pharmacy"
        phone = address = gst_no = ""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    cfg = json.load(f)
                    pharmacy_name = cfg.get('pharmacy_name', pharmacy_name)
                    phone = cfg.get('phone', '')
                    address = cfg.get('address', '')
                    gst_no = cfg.get('gst_no', '')
        except Exception:
            pass
        return pharmacy_name, phone, address, gst_no
    
    def view_receipt(self, sale_id):
        """View a single sale receipt"""
        sale_rows = self._get_sale_data(sale_id)
        if not sale_rows:
            QMessageBox.warning(self, "Error", "Receipt not found")
            return
        
        pharmacy_name, phone, address, gst_no = self._load_profile()
        row = sale_rows[0]
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Sale Receipt")
        dialog.setGeometry(80, 60, 700, 520)
        dialog.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(0)
        
        # Header
        header = QLabel(pharmacy_name.upper())
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: 700; color: #1F3D2C; letter-spacing: 2px;")
        layout.addWidget(header)
        
        subtitle = QLabel("MEDICAL STORE  |  GST INVOICE")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 11px; color: #555; margin-bottom: 2px;")
        layout.addWidget(subtitle)
        
        if address:
            addr_lbl = QLabel(address)
            addr_lbl.setAlignment(Qt.AlignCenter)
            addr_lbl.setStyleSheet("font-size: 10px; color: #555;")
            layout.addWidget(addr_lbl)
        
        contact_parts = []
        if phone: contact_parts.append(f"Ph: {phone}")
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
        
        # Invoice info
        raw_date = str(row['date']) if row['date'] else ''
        date_part = raw_date[:10] if raw_date else ''
        time_part = raw_date[11:19] if len(raw_date) > 10 else ''
        
        info_layout = QHBoxLayout()
        inv_no = f"INV-{sale_id}"
        left_info = QLabel(f"Invoice No: {inv_no}")
        left_info.setStyleSheet("font-size: 11px; color: #333; font-weight: 600;")
        info_layout.addWidget(left_info)
        info_layout.addStretch()
        right_info = QLabel(f"Date: {date_part}    Time: {time_part}")
        right_info.setStyleSheet("font-size: 11px; color: #333; font-weight: 600;")
        info_layout.addWidget(right_info)
        layout.addLayout(info_layout)
        layout.addSpacing(8)
        
        # Table
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
        
        total_amount = 0
        table.setRowCount(len(sale_rows))
        for i, s in enumerate(sale_rows):
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            table.setItem(i, 1, QTableWidgetItem(str(s['medicine_name'] or 'Unknown')))
            table.setItem(i, 2, QTableWidgetItem(str(s['batch'] or '')))
            table.setItem(i, 3, QTableWidgetItem(format_date(s['expiry_date']) if s['expiry_date'] else ''))
            table.setItem(i, 4, QTableWidgetItem(str(s['quantity'])))
            table.setItem(i, 5, QTableWidgetItem(format_currency(s['unit_price'])))
            table.setItem(i, 6, QTableWidgetItem(format_currency(s['total_price'])))
            for col in [0, 4, 5, 6]:
                table.item(i, col).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            total_amount += s['total_price']
        
        layout.addWidget(table)
        layout.addSpacing(8)
        
        div2 = QFrame()
        div2.setFrameShape(QFrame.HLine)
        div2.setStyleSheet("color: #1F3D2C;")
        layout.addWidget(div2)
        layout.addSpacing(4)
        
        # Total
        totals_layout = QHBoxLayout()
        totals_layout.addStretch()
        total_label = QLabel(f"Total Amount:  {format_currency(total_amount)}")
        total_label.setStyleSheet("font-size: 14px; font-weight: 700; color: #1F3D2C;")
        totals_layout.addWidget(total_label)
        layout.addLayout(totals_layout)
        layout.addSpacing(4)
        
        pay_layout = QHBoxLayout()
        pay_layout.addStretch()
        pay_label = QLabel("Payment: Cash")
        pay_label.setStyleSheet("font-size: 11px; color: #555;")
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
        
        dialog.exec_()
    
    def download_receipt(self, sale_id):
        """Download a single receipt as text file"""
        sale_rows = self._get_sale_data(sale_id)
        if not sale_rows:
            QMessageBox.warning(self, "Error", "Receipt not found")
            return
        
        pharmacy_name, phone, address, gst_no = self._load_profile()
        row = sale_rows[0]
        raw_date = str(row['date']) if row['date'] else ''
        date_part = raw_date[:10] if raw_date else ''
        time_part = raw_date[11:19] if len(raw_date) > 10 else ''
        
        # Build receipt text
        lines = []
        lines.append("=" * 50)
        lines.append(f"{pharmacy_name.upper():^50}")
        lines.append(f"{'MEDICAL STORE  |  GST INVOICE':^50}")
        if address:
            lines.append(f"{address:^50}")
        contact_parts = []
        if phone: contact_parts.append(f"Ph: {phone}")
        if gst_no: contact_parts.append(f"GST: {gst_no}")
        if contact_parts:
            lines.append(f"{'  |  '.join(contact_parts):^50}")
        lines.append("=" * 50)
        lines.append(f"Invoice: INV-{sale_id}    Date: {date_part}  Time: {time_part}")
        lines.append("-" * 50)
        lines.append(f"{'S.No':<5} {'Item':<18} {'Qty':<5} {'Rate':<10} {'Amount':<10}")
        lines.append("-" * 50)
        
        total = 0
        for i, s in enumerate(sale_rows):
            name = str(s['medicine_name'] or 'Unknown')[:18]
            lines.append(f"{i+1:<5} {name:<18} {s['quantity']:<5} {format_currency(s['unit_price']):<10} {format_currency(s['total_price']):<10}")
            total += s['total_price']
        
        lines.append("-" * 50)
        lines.append(f"{'TOTAL':>28} {format_currency(total):>20}")
        lines.append(f"{'Payment: Cash':>48}")
        lines.append("=" * 50)
        lines.append(f"{'Thank You! Visit Again':^50}")
        lines.append("=" * 50)
        
        receipt_text = "\n".join(lines)
        
        # Save dialog
        default_name = f"Receipt_INV-{sale_id}_{date_part}.txt"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Receipt", default_name,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(receipt_text)
            QMessageBox.information(self, "Saved", f"Receipt saved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def download_all_csv(self):
        """Download all receipts as CSV"""
        import csv
        
        rows = self.receipts_table.rowCount()
        if rows == 0:
            QMessageBox.warning(self, "No Data", "No receipts to download.")
            return
        
        default_name = f"all_receipts_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save All Receipts as CSV", default_name,
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # Header
                cols = self.receipts_table.columnCount() - 1  # exclude Actions column
                headers = []
                for col in range(cols):
                    headers.append(self.receipts_table.horizontalHeaderItem(col).text())
                writer.writerow(headers)
                
                # Data
                for row in range(rows):
                    row_data = []
                    for col in range(cols):
                        item = self.receipts_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "Saved", f"All receipts saved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
