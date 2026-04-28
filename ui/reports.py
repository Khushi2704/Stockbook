"""
Reports window - View sales, profit, and business reports
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QLabel, QComboBox, QDateEdit, QMessageBox,
                             QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor
from services.report_service import ReportService
from utils.helpers import format_currency
from ui.styles import (
    get_page_title_style, get_section_title_style, get_field_label_style,
    get_report_summary_style, get_stat_card_style,
    get_primary_button_style, get_secondary_button_style,
    get_accent_button_style, get_warning_button_style,
    PRIMARY, WHITE, TEXT_DARK
)
from datetime import datetime, timedelta
import traceback


class ReportsWindow(QMainWindow):
    """Reports window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stockbook - Reports")
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
        title = QLabel("Sales & Business Reports")
        title.setStyleSheet(get_page_title_style())
        layout.addWidget(title)
        layout.addSpacing(18)
        
        # ── Filter Bar ────────────────────────────────────────────
        filter_frame = QFrame()
        filter_frame.setStyleSheet(get_stat_card_style())
        filter_shadow = QGraphicsDropShadowEffect()
        filter_shadow.setBlurRadius(16)
        filter_shadow.setOffset(0, 2)
        filter_shadow.setColor(QColor(31, 61, 44, 18))
        filter_frame.setGraphicsEffect(filter_shadow)
        
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(16, 14, 16, 14)
        filter_layout.setSpacing(12)
        
        selector_label = QLabel("Report Type:")
        selector_label.setStyleSheet(get_field_label_style())
        filter_layout.addWidget(selector_label)
        
        self.report_combo = QComboBox()
        self.report_combo.setFixedHeight(36)
        self.report_combo.addItem("Today's Sales", "today")
        self.report_combo.addItem("Last 7 Days", "week")
        self.report_combo.addItem("Last 30 Days", "month")
        self.report_combo.addItem("Monthly Report", "monthly")
        self.report_combo.addItem("Top Selling Medicines", "top_medicines")
        self.report_combo.addItem("Profit Analysis", "profit")
        self.report_combo.addItem("Business Summary", "summary")
        self.report_combo.addItem("Custom Range", "custom")
        self.report_combo.currentIndexChanged.connect(self.load_report)
        filter_layout.addWidget(self.report_combo)
        
        # Date pickers (for custom range)
        self.start_date_label = QLabel("From:")
        self.start_date_label.setStyleSheet(get_field_label_style())
        self.start_date_picker = QDateEdit()
        self.start_date_picker.setDate(QDate.currentDate().addDays(-30))
        self.start_date_picker.setFixedHeight(36)
        self.start_date_label.hide()
        self.start_date_picker.hide()
        
        self.end_date_label = QLabel("To:")
        self.end_date_label.setStyleSheet(get_field_label_style())
        self.end_date_picker = QDateEdit()
        self.end_date_picker.setDate(QDate.currentDate())
        self.end_date_picker.setFixedHeight(36)
        self.end_date_label.hide()
        self.end_date_picker.hide()
        
        filter_layout.addWidget(self.start_date_label)
        filter_layout.addWidget(self.start_date_picker)
        filter_layout.addWidget(self.end_date_label)
        filter_layout.addWidget(self.end_date_picker)
        
        load_btn = QPushButton("Load Report")
        load_btn.setFixedHeight(36)
        load_btn.setStyleSheet(get_accent_button_style())
        load_btn.setCursor(Qt.PointingHandCursor)
        load_btn.clicked.connect(self.load_report)
        filter_layout.addWidget(load_btn)
        
        filter_layout.addStretch()
        
        layout.addWidget(filter_frame)
        layout.addSpacing(16)
        
        # ── Summary Section ───────────────────────────────────────
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet(get_report_summary_style())
        layout.addWidget(self.summary_label)
        layout.addSpacing(12)
        
        # ── Data Table ────────────────────────────────────────────
        self.report_table = QTableWidget()
        self.report_table.setAlternatingRowColors(True)
        self.report_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.report_table.horizontalHeader().setStretchLastSection(True)
        self.report_table.verticalHeader().setVisible(False)
        layout.addWidget(self.report_table)
        
        # ── Action buttons ────────────────────────────────────────
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        export_btn = QPushButton("Export to CSV")
        export_btn.setFixedHeight(40)
        export_btn.setStyleSheet(get_warning_button_style())
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(export_btn)
        
        print_btn = QPushButton("Print")
        print_btn.setFixedHeight(40)
        print_btn.setStyleSheet(get_accent_button_style())
        print_btn.setCursor(Qt.PointingHandCursor)
        print_btn.clicked.connect(self.print_report)
        button_layout.addWidget(print_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet(get_secondary_button_style())
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addSpacing(10)
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
        
        # Load initial report
        self.load_report()
    
    # ─── ALL ORIGINAL LOGIC BELOW (untouched) ─────────────────────

    def load_report(self):
        """Load selected report"""
        try:
            report_type = self.report_combo.currentData()
            
            if report_type == "today":
                self.load_today_report()
            elif report_type == "week":
                self.load_week_report()
            elif report_type == "month":
                self.load_month_report()
            elif report_type == "monthly":
                self.load_monthly_report()
            elif report_type == "top_medicines":
                self.load_top_medicines_report()
            elif report_type == "profit":
                self.load_profit_report()
            elif report_type == "summary":
                self.load_summary_report()
            elif report_type == "custom":
                self.start_date_label.show()
                self.start_date_picker.show()
                self.end_date_label.show()
                self.end_date_picker.show()
                self.load_custom_range_report()
            else:
                self.start_date_label.hide()
                self.start_date_picker.hide()
                self.end_date_label.hide()
                self.end_date_picker.hide()
        
        except Exception as e:
            print(f"Error loading report: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load report: {str(e)}")
    
    def load_today_report(self):
        """Load today's sales report"""
        report = ReportService.get_today_sales(self.user_id)
        
        self.summary_label.setText(
            f"Today's Sales: {format_currency(report['total_amount'])} | "
            f"Profit: {format_currency(report['total_profit'])} | "
            f"Transactions: {report['transaction_count']}"
        )
        
        from database.db import fetch_all
        sales = fetch_all("""
            SELECT s.id, m.name as medicine_name, s.quantity,
                   s.unit_price, s.total_price, s.profit, s.date
            FROM sales s
            LEFT JOIN medicines m ON s.medicine_id = m.id
            WHERE DATE(s.date, 'localtime') = DATE('now', 'localtime')
            AND s.user_id = ?
            ORDER BY s.date DESC
        """, (self.user_id,))
        
        self.report_table.setColumnCount(7)
        self.report_table.setHorizontalHeaderLabels(["Date", "Time", "Medicine", "Qty", "Unit Price", "Total", "Profit"])
        self.report_table.setRowCount(0)
        
        total_qty = 0
        total_price = 0.0
        total_profit = 0.0
        
        for i, row in enumerate(sales):
            self.report_table.insertRow(i)
            raw_date = str(row['date']) if row['date'] else ''
            date_part = raw_date[:10] if raw_date else ''
            time_part = raw_date[11:16] if len(raw_date) > 10 else ''
            self.report_table.setItem(i, 0, QTableWidgetItem(date_part))
            self.report_table.setItem(i, 1, QTableWidgetItem(time_part))
            self.report_table.setItem(i, 2, QTableWidgetItem(str(row['medicine_name'] or 'Unknown')))
            self.report_table.setItem(i, 3, QTableWidgetItem(str(row['quantity'])))
            self.report_table.setItem(i, 4, QTableWidgetItem(format_currency(row['unit_price'])))
            self.report_table.setItem(i, 5, QTableWidgetItem(format_currency(row['total_price'])))
            self.report_table.setItem(i, 6, QTableWidgetItem(format_currency(row['profit'])))
            total_qty   += row['quantity']
            total_price += row['total_price']
            total_profit += row['profit']
        
        # Totals row
        if sales:
            t = self.report_table.rowCount()
            self.report_table.insertRow(t)
            bold_item = QTableWidgetItem("TOTAL")
            bold_item.setFont(QFont('Segoe UI', 10, QFont.Bold))
            self.report_table.setItem(t, 0, bold_item)
            self.report_table.setItem(t, 1, QTableWidgetItem(""))
            self.report_table.setItem(t, 2, QTableWidgetItem(""))
            self.report_table.setItem(t, 3, QTableWidgetItem(str(total_qty)))
            self.report_table.setItem(t, 4, QTableWidgetItem(""))
            self.report_table.setItem(t, 5, QTableWidgetItem(format_currency(total_price)))
            self.report_table.setItem(t, 6, QTableWidgetItem(format_currency(total_profit)))
            for col in range(7):
                item = self.report_table.item(t, col)
                if item:
                    item.setFont(QFont('Segoe UI', 10, QFont.Bold))
                    item.setBackground(QColor('#E8F5F0'))
    
    def load_week_report(self):
        """Load last 7 days report"""
        report = ReportService.get_last_7_days_report(self.user_id)
        
        self.summary_label.setText(
            f"Last 7 Days Sales: {format_currency(report['total_amount'])} | "
            f"Profit: {format_currency(sum(s['profit'] for s in report['sales']))} | "
            f"Transactions: {report['transactions']}"
        )
        
        self.report_table.setColumnCount(2)
        self.report_table.setHorizontalHeaderLabels(["Date", "Amount"])
        self.report_table.setRowCount(0)
        
        # Group by date
        from datetime import datetime
        by_date = {}
        for sale in report['sales']:
            date_str = sale['date'][:10]
            if date_str not in by_date:
                by_date[date_str] = 0
            by_date[date_str] += sale['total_price']
        
        row = 0
        for date, amount in sorted(by_date.items(), reverse=True):
            self.report_table.insertRow(row)
            self.report_table.setItem(row, 0, QTableWidgetItem(date))
            self.report_table.setItem(row, 1, QTableWidgetItem(format_currency(amount)))
            row += 1
    
    def load_month_report(self):
        """Load last 30 days report"""
        report = ReportService.get_last_30_days_report(self.user_id)
        
        total_profit = sum(s['profit'] for s in report['sales'])
        
        self.summary_label.setText(
            f"Last 30 Days Sales: {format_currency(report['total_amount'])} | "
            f"Profit: {format_currency(total_profit)} | "
            f"Transactions: {report['transactions']}"
        )
        
        self.report_table.setColumnCount(2)
        self.report_table.setHorizontalHeaderLabels(["Date", "Amount"])
        self.report_table.setRowCount(0)
        
        # Group by date
        by_date = {}
        for sale in report['sales']:
            date_str = sale['date'][:10]
            if date_str not in by_date:
                by_date[date_str] = 0
            by_date[date_str] += sale['total_price']
        
        row = 0
        for date, amount in sorted(by_date.items(), reverse=True):
            self.report_table.insertRow(row)
            self.report_table.setItem(row, 0, QTableWidgetItem(date))
            self.report_table.setItem(row, 1, QTableWidgetItem(format_currency(amount)))
            row += 1
    
    def load_monthly_report(self):
        """Load monthly report"""
        now = datetime.now()
        report = ReportService.get_monthly_sales(now.year, now.month, self.user_id)
        
        self.summary_label.setText(
            f"This Month Sales: {format_currency(report['total_amount'])} | "
            f"Profit: {format_currency(report['total_profit'])} | "
            f"Transactions: {report['transactions']}"
        )
        
        # Fetch sales with medicine names for better display
        from database.db import fetch_all as db_fetch_all
        sales = db_fetch_all("""
            SELECT s.id, m.name as medicine_name, s.quantity,
                   s.unit_price, s.total_price, s.profit, s.date
            FROM sales s
            LEFT JOIN medicines m ON s.medicine_id = m.id
            WHERE STRFTIME('%Y-%m', s.date) = ? AND s.user_id = ?
            ORDER BY s.date DESC
        """, (f"{now.year:04d}-{now.month:02d}", self.user_id))
        
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels(["Medicine", "Quantity", "Price", "Profit", "Date"])
        self.report_table.setRowCount(len(sales))
        
        for row, sale in enumerate(sales):
            self.report_table.setItem(row, 0, QTableWidgetItem(str(sale['medicine_name'] or 'Unknown')))
            self.report_table.setItem(row, 1, QTableWidgetItem(str(sale['quantity'])))
            self.report_table.setItem(row, 2, QTableWidgetItem(format_currency(sale['total_price'])))
            self.report_table.setItem(row, 3, QTableWidgetItem(format_currency(sale['profit'])))
            self.report_table.setItem(row, 4, QTableWidgetItem(str(sale['date'])[:10]))
    
    def load_top_medicines_report(self):
        """Load top selling medicines"""
        medicines = ReportService.get_top_medicines(10, self.user_id)
        
        self.summary_label.setText("Top 10 Selling Medicines by Quantity")
        
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels(["Medicine", "Batch", "Qty Sold", "Revenue", "Profit"])
        self.report_table.setRowCount(len(medicines))
        
        for row, med in enumerate(medicines):
            self.report_table.setItem(row, 0, QTableWidgetItem(med['name']))
            self.report_table.setItem(row, 1, QTableWidgetItem(med['batch']))
            self.report_table.setItem(row, 2, QTableWidgetItem(str(med['total_quantity'])))
            self.report_table.setItem(row, 3, QTableWidgetItem(format_currency(med['total_revenue'])))
            self.report_table.setItem(row, 4, QTableWidgetItem(format_currency(med['total_profit'])))
    
    def load_profit_report(self):
        """Load profit analysis"""
        report = ReportService.get_profit_analysis(user_id=self.user_id)
        
        self.summary_label.setText(
            f"Profit Analysis - {report['period']}\n"
            f"Total Profit: {format_currency(report['total_profit'])} | "
            f"Sales: {format_currency(report['total_sales'])} | "
            f"Margin: {report['profit_margin']:.1f}%"
        )
        
        self.report_table.setColumnCount(3)
        self.report_table.setHorizontalHeaderLabels(["Medicine", "Revenue", "Profit"])
        self.report_table.setRowCount(len(report['top_profitable_medicines']))
        
        for row, med in enumerate(report['top_profitable_medicines']):
            self.report_table.setItem(row, 0, QTableWidgetItem(med['name']))
            self.report_table.setItem(row, 1, QTableWidgetItem(format_currency(med['total_revenue'])))
            self.report_table.setItem(row, 2, QTableWidgetItem(format_currency(med['total_profit'])))
    
    def load_summary_report(self):
        """Load business summary"""
        summary = ReportService.get_business_summary(self.user_id)
        
        self.summary_label.setText(
            f"Today: {format_currency(summary['today']['total_amount'])} | "
            f"This Month: {format_currency(summary['this_month']['total_amount'])} | "
            f"This Week: {format_currency(summary['this_week']['total_amount'])}"
        )
        
        self.report_table.setColumnCount(3)
        self.report_table.setHorizontalHeaderLabels(["Top Medicine", "Quantity", "Revenue"])
        self.report_table.setRowCount(len(summary['top_medicines']))
        
        for row, med in enumerate(summary['top_medicines']):
            self.report_table.setItem(row, 0, QTableWidgetItem(med['name']))
            self.report_table.setItem(row, 1, QTableWidgetItem(str(med['total_quantity'])))
            self.report_table.setItem(row, 2, QTableWidgetItem(format_currency(med['total_revenue'])))
    
    def load_custom_range_report(self):
        """Load custom date range report"""
        start = self.start_date_picker.date().toString("yyyy-MM-dd")
        end = self.end_date_picker.date().toString("yyyy-MM-dd")
        
        report = ReportService.get_sales_range_report(start, end, self.user_id)
        
        self.summary_label.setText(
            f"Sales from {start} to {end}: {format_currency(report['total_amount'])} | "
            f"Profit: {format_currency(sum(s['profit'] for s in report['sales']))} | "
            f"Transactions: {report['transactions']}"
        )
        
        self.report_table.setColumnCount(2)
        self.report_table.setHorizontalHeaderLabels(["Date", "Amount"])
        self.report_table.setRowCount(0)
        
        by_date = {}
        for sale in report['sales']:
            date_str = sale['date'][:10]
            if date_str not in by_date:
                by_date[date_str] = 0
            by_date[date_str] += sale['total_price']
        
        row = 0
        for date, amount in sorted(by_date.items(), reverse=True):
            self.report_table.insertRow(row)
            self.report_table.setItem(row, 0, QTableWidgetItem(date))
            self.report_table.setItem(row, 1, QTableWidgetItem(format_currency(amount)))
            row += 1
    
    def export_report(self):
        """Export current report table to CSV"""
        import csv
        from PyQt5.QtWidgets import QFileDialog
        from datetime import datetime
        
        rows = self.report_table.rowCount()
        cols = self.report_table.columnCount()
        
        if rows == 0:
            QMessageBox.warning(self, "Export", "No data to export. Load a report first.")
            return
        
        # Default filename with timestamp
        default_name = f"stockbook_report_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report as CSV", default_name,
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # Header row
                headers = []
                for col in range(cols):
                    headers.append(self.report_table.horizontalHeaderItem(col).text())
                writer.writerow(headers)
                
                # Data rows
                for row in range(rows):
                    row_data = []
                    for col in range(cols):
                        item = self.report_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "Export Successful",
                                    f"Report saved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not save file:\n{str(e)}")
    
    def print_report(self):
        """Print current report table"""
        from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
        from PyQt5.QtGui import QTextDocument
        from datetime import datetime
        
        rows = self.report_table.rowCount()
        cols = self.report_table.columnCount()
        
        if rows == 0:
            QMessageBox.warning(self, "Print", "No data to print. Load a report first.")
            return
        
        # Build HTML table for printing
        html = f"""
        <html><body>
        <h2 style='text-align:center; font-family:Arial;'>Stockbook Medical Store</h2>
        <h3 style='text-align:center; font-family:Arial;'>Sales Report — {datetime.now().strftime('%d-%m-%Y %H:%M')}</h3>
        <p style='font-family:Arial;'>{self.summary_label.text()}</p>
        <table border='1' cellspacing='0' cellpadding='6' width='100%' 
               style='font-family:Arial; font-size:12px; border-collapse:collapse;'>
        <thead><tr style='background:#1F3D2C; color:white;'>
        """
        for col in range(cols):
            html += f"<th>{self.report_table.horizontalHeaderItem(col).text()}</th>"
        html += "</tr></thead><tbody>"
        
        for row in range(rows):
            bg = "#f5f5f5" if row % 2 == 0 else "white"
            html += f"<tr style='background:{bg};'>"
            for col in range(cols):
                item = self.report_table.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"
        
        html += "</tbody></table></body></html>"
        
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            doc = QTextDocument()
            doc.setHtml(html)
            doc.print_(printer)
