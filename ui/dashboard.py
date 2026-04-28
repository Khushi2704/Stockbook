"""
Dashboard screen - Main application interface
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QTableWidget, 
                             QTableWidgetItem, QGridLayout, QFrame,
                             QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
                             QMenu, QAction, QDialog, QLineEdit, QFileDialog,
                             QToolButton, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint, QSize
from PyQt5.QtGui import (QFont, QIcon, QColor, QPixmap, QPainter, QPen,
                          QPainterPath, QBrush)
from services.inventory_service import InventoryService
from services.report_service import ReportService
from utils.helpers import format_currency, format_date
from ui.styles import (
    PRIMARY, PRIMARY_LIGHT, TEXT_DARK, TEXT_SECONDARY, TEXT_MUTED,
    WHITE, BG_WINDOW, CARD_BORDER_SOLID, ALERT_RED, ALERT_ORANGE,
    DIVIDER, get_stat_card_style, get_page_title_style,
    get_section_title_style, get_nav_button_style, get_primary_button_style,
    get_secondary_button_style, get_alert_table_item_style
)
from datetime import datetime
import traceback
import json
import os


class Dashboard(QMainWindow):
    """Main dashboard window"""
    
    logged_out = pyqtSignal()
    
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Stockbook Medical Store - Dashboard")
        self.setGeometry(0, 0, 1200, 800)
        self.init_ui()
        self.load_dashboard_data()
        
        # Set up auto-refresh timer for alerts
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_alerts)
        self.refresh_timer.start(3000)  # Refresh every 3 seconds
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(0)
        
        # ── Header Bar ────────────────────────────────────────────
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Stockbook Dashboard")
        title.setStyleSheet(get_page_title_style())
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Pharmacy name label
        self._load_profile_config()
        self.pharmacy_name_label = QLabel(self._profile_config.get('pharmacy_name', 'My Pharmacy'))
        self.pharmacy_name_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px; font-weight: 600; margin-right: 10px;")
        header_layout.addWidget(self.pharmacy_name_label)
        
        # Profile avatar button
        self.profile_btn = QToolButton()
        self.profile_btn.setFixedSize(40, 40)
        self.profile_btn.setCursor(Qt.PointingHandCursor)
        self.profile_btn.setPopupMode(QToolButton.InstantPopup)
        self._set_profile_avatar()
        self.profile_btn.setStyleSheet(f"""
            QToolButton {{
                border: 2px solid {CARD_BORDER_SOLID};
                border-radius: 20px;
                background-color: {WHITE};
                padding: 0px;
            }}
            QToolButton:hover {{
                border-color: {PRIMARY};
            }}
            QToolButton::menu-indicator {{
                image: none;
                width: 0px;
            }}
        """)
        
        # Profile dropdown menu
        profile_menu = QMenu(self)
        profile_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {WHITE};
                border: 1px solid {CARD_BORDER_SOLID};
                border-radius: 8px;
                padding: 6px 0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }}
            QMenu::item {{
                padding: 10px 24px;
                color: {TEXT_DARK};
            }}
            QMenu::item:selected {{
                background-color: {PRIMARY_LIGHT};
                color: {TEXT_DARK};
            }}
            QMenu::separator {{
                height: 1px;
                background: {DIVIDER};
                margin: 4px 12px;
            }}
        """)
        
        profile_action = profile_menu.addAction("Shop Profile")
        profile_action.triggered.connect(self._edit_shop_profile)
        
        password_action = profile_menu.addAction("Change Password")
        password_action.triggered.connect(self.open_settings)
        
        profile_menu.addSeparator()
        
        logout_action = profile_menu.addAction("Logout")
        logout_action.triggered.connect(self.handle_logout)
        
        self.profile_btn.setMenu(profile_menu)
        header_layout.addWidget(self.profile_btn)
        
        layout.addLayout(header_layout)
        layout.addSpacing(20)
        
        # ── Quick Stats Row ───────────────────────────────────────
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        # Today's Sales Card
        self.today_sales_card, self.today_sales_icon, self.today_sales_value, self.today_sales_sub = self._create_stat_card(
            "₹", "Today's Sales", "₹0.00", "0 transactions"
        )
        stats_layout.addWidget(self.today_sales_card)
        
        # Today's Profit Card
        self.today_profit_card, self.today_profit_icon, self.today_profit_value, self.today_profit_sub = self._create_stat_card(
            "₹", "Today's Profit", "₹0.00", ""
        )
        stats_layout.addWidget(self.today_profit_card)
        
        # Alerts Card
        self.alerts_card, self.alerts_icon, self.alerts_value, self.alerts_sub = self._create_stat_card(
            "!", "Alerts", "0", "Low Stock: 0 | Expiring: 0"
        )
        stats_layout.addWidget(self.alerts_card)
        
        layout.addLayout(stats_layout)
        layout.addSpacing(24)
        
        # ── Quick Actions Section ─────────────────────────────────
        actions_label = QLabel("QUICK ACTIONS")
        actions_label.setStyleSheet(get_section_title_style())
        layout.addWidget(actions_label)
        layout.addSpacing(10)
        
        main_buttons_layout = QGridLayout()
        main_buttons_layout.setSpacing(12)
        
        buttons = [
            ("Billing", self.open_billing, 0, 0),
            ("Inventory", self.open_inventory, 0, 1),
            ("Add Medicine", self.open_add_medicine, 0, 2),
            ("Reports", self.open_reports, 1, 0),
            ("Receipts", self.open_receipts, 1, 1),
            ("Backup / Restore", self.open_backup, 1, 2),
        ]
        
        # Only show User Management for admin (user_id = 1)
        if self.user_id == 1:
            buttons.append(("User Management", self.open_user_management, 2, 0))
        
        for label, callback, row, col in buttons:
            btn = QPushButton(label)
            btn.setFixedHeight(56)
            btn.setStyleSheet(get_nav_button_style())
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(callback)
            main_buttons_layout.addWidget(btn, row, col)
        
        layout.addLayout(main_buttons_layout)
        layout.addSpacing(24)
        
        # ── Alerts Table Section ──────────────────────────────────
        alerts_header_layout = QHBoxLayout()
        
        alerts_title = QLabel("ACTIVE ALERTS")
        alerts_title.setStyleSheet(get_section_title_style())
        alerts_header_layout.addWidget(alerts_title)
        
        alerts_header_layout.addStretch()
        
        self.alert_filter_combo = QComboBox()
        self.alert_filter_combo.setFixedHeight(30)
        self.alert_filter_combo.setFixedWidth(160)
        self.alert_filter_combo.addItem("All", "all")
        self.alert_filter_combo.addItem("Low Stock", "low_stock")
        self.alert_filter_combo.addItem("Expiring Soon", "expiring")
        self.alert_filter_combo.addItem("Expired", "expired")
        self.alert_filter_combo.currentIndexChanged.connect(self._on_alert_filter_changed)
        alerts_header_layout.addWidget(self.alert_filter_combo)
        
        layout.addLayout(alerts_header_layout)
        layout.addSpacing(8)
        
        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(5)
        self.alerts_table.setHorizontalHeaderLabels(["Type", "Medicine", "Batch", "Stock", "Expiry Date"])
        self.alerts_table.setAlternatingRowColors(True)
        self.alerts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.alerts_table.horizontalHeader().setStretchLastSection(True)
        self.alerts_table.horizontalHeader().setSectionsMovable(False)
        self.alerts_table.verticalHeader().setVisible(False)
        layout.addWidget(self.alerts_table)
        
        central_widget.setLayout(layout)
    
    def _create_stat_card(self, icon_text, title_text, value_text, sub_text):
        """Create a beautiful stat card widget."""
        card = QFrame()
        card.setStyleSheet(get_stat_card_style())
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setFixedHeight(100)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(31, 61, 44, 22))
        card.setGraphicsEffect(shadow)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(18, 14, 18, 14)
        card_layout.setSpacing(14)
        
        # Icon
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"""
            font-size: 28px;
            background: {PRIMARY_LIGHT};
            border-radius: 10px;
            padding: 6px;
        """)
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # Text column
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title_text)
        title_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px; font-weight: 600;")
        text_layout.addWidget(title_label)
        
        value_label = QLabel(value_text)
        value_label.setStyleSheet(f"color: {TEXT_DARK}; font-size: 22px; font-weight: 700;")
        text_layout.addWidget(value_label)
        
        sub_label = QLabel(sub_text)
        sub_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
        text_layout.addWidget(sub_label)
        
        card_layout.addLayout(text_layout)
        card_layout.addStretch()
        
        return card, icon_label, value_label, sub_label
    
    def load_dashboard_data(self):
        """Load and display dashboard data"""
        try:
            # Load today's sales
            today_sales = ReportService.get_today_sales(self.user_id)
            self.today_sales_value.setText(format_currency(today_sales['total_amount']))
            self.today_sales_sub.setText(f"{today_sales['transaction_count']} transactions")
            
            # Load today's profit
            self.today_profit_value.setText(format_currency(today_sales['total_profit']))
            
            # Load alerts
            alerts = InventoryService.check_alerts(self.user_id)
            alert_counts = InventoryService.get_alert_count(self.user_id)
            total_alerts = alert_counts['low_stock_count'] + alert_counts['expiring_count'] + alert_counts['expired_count']
            self.alerts_value.setText(str(total_alerts))
            self.alerts_sub.setText(
                f"Low Stock: {alert_counts['low_stock_count']} | "
                f"Expiring: {alert_counts['expiring_count']} | "
                f"Expired: {alert_counts['expired_count']}"
            )
            
            # Load alerts table
            self._current_alerts = alerts
            self.display_alerts(alerts)
        
        except Exception as e:
            print(f"Error loading dashboard: {e}")
            traceback.print_exc()
    
    def refresh_alerts(self):
        """Refresh only the alerts section"""
        try:
            alerts = InventoryService.check_alerts(self.user_id)
            alert_counts = InventoryService.get_alert_count(self.user_id)
            
            # Update alerts card
            total_alerts = alert_counts['low_stock_count'] + alert_counts['expiring_count'] + alert_counts['expired_count']
            self.alerts_value.setText(str(total_alerts))
            self.alerts_sub.setText(
                f"Low Stock: {alert_counts['low_stock_count']} | "
                f"Expiring: {alert_counts['expiring_count']} | "
                f"Expired: {alert_counts['expired_count']}"
            )
            
            # Update alerts table
            self._current_alerts = alerts
            self.display_alerts(alerts)
        except Exception as e:
            pass  # Silently fail to avoid disrupting user workflow
    
    def display_alerts(self, alerts):
        """Display alerts in table, respecting the current filter"""
        # Apply filter from dropdown
        filter_type = self.alert_filter_combo.currentData() if hasattr(self, 'alert_filter_combo') else 'all'
        
        self.alerts_table.setRowCount(0)
        row_num = 0
        
        # Low stock alerts
        if filter_type in ('all', 'low_stock'):
            for medicine in alerts['low_stock']:
                self.alerts_table.insertRow(row_num)
                type_item = QTableWidgetItem("LOW STOCK")
                type_item.setForeground(QColor(ALERT_ORANGE))
                self.alerts_table.setItem(row_num, 0, type_item)
                self.alerts_table.setItem(row_num, 1, QTableWidgetItem(medicine['name']))
                self.alerts_table.setItem(row_num, 2, QTableWidgetItem(medicine['batch']))
                self.alerts_table.setItem(row_num, 3, QTableWidgetItem(str(medicine['stock'])))
                self.alerts_table.setItem(row_num, 4, QTableWidgetItem(format_date(medicine['expiry_date']) if medicine['expiry_date'] else ''))
                row_num += 1
        
        # Expiring alerts
        if filter_type in ('all', 'expiring'):
            for medicine in alerts['expiring']:
                self.alerts_table.insertRow(row_num)
                type_item = QTableWidgetItem("EXPIRING SOON")
                type_item.setForeground(QColor(ALERT_ORANGE))
                self.alerts_table.setItem(row_num, 0, type_item)
                self.alerts_table.setItem(row_num, 1, QTableWidgetItem(medicine['name']))
                self.alerts_table.setItem(row_num, 2, QTableWidgetItem(medicine['batch']))
                self.alerts_table.setItem(row_num, 3, QTableWidgetItem(str(medicine['stock'])))
                self.alerts_table.setItem(row_num, 4, QTableWidgetItem(format_date(medicine['expiry_date'])))
                row_num += 1
        
        # Expired alerts
        if filter_type in ('all', 'expired'):
            for medicine in alerts['expired']:
                self.alerts_table.insertRow(row_num)
                type_item = QTableWidgetItem("EXPIRED")
                type_item.setForeground(QColor(ALERT_RED))
                self.alerts_table.setItem(row_num, 0, type_item)
                self.alerts_table.setItem(row_num, 1, QTableWidgetItem(medicine['name']))
                self.alerts_table.setItem(row_num, 2, QTableWidgetItem(medicine['batch']))
                self.alerts_table.setItem(row_num, 3, QTableWidgetItem(str(medicine['stock'])))
                self.alerts_table.setItem(row_num, 4, QTableWidgetItem(format_date(medicine['expiry_date'])))
                row_num += 1
    
    def _on_alert_filter_changed(self):
        """Handle alert filter dropdown change"""
        if hasattr(self, '_current_alerts'):
            self.display_alerts(self._current_alerts)
    
    def open_billing(self):
        """Open billing window"""
        from ui.billing import BillingWindow
        self.billing_window = BillingWindow(self)
        self.billing_window.show()
    
    def open_inventory(self):
        """Open inventory window"""
        from ui.purchase import PurchaseWindow
        self.inventory_window = PurchaseWindow(self)
        self.inventory_window.show()
    
    def open_add_medicine(self):
        """Open add medicine dialog"""
        from ui.add_medicine import AddMedicineDialog
        dialog = AddMedicineDialog(self)
        if dialog.exec_():
            self.load_dashboard_data()
    
    def open_reports(self):
        """Open reports window"""
        from ui.reports import ReportsWindow
        self.reports_window = ReportsWindow(self)
        self.reports_window.show()
    
    def open_receipts(self):
        """Open receipts window"""
        from ui.receipts import ReceiptsWindow
        self.receipts_window = ReceiptsWindow(self)
        self.receipts_window.show()
    
    def open_backup(self):
        """Open backup/restore window"""
        from ui.backup import BackupWindow
        self.backup_window = BackupWindow(self)
        self.backup_window.show()
    
    def open_settings(self):
        """Open settings window"""
        from ui.settings import SettingsWindow
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
    
    def open_user_management(self):
        """Open user management window"""
        from ui.user_management import UserManagementWindow
        self.user_management_window = UserManagementWindow(self, user_id=self.user_id)
        self.user_management_window.show()
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logged_out.emit()
            self.close()
    
    # ─── PROFILE MANAGEMENT ──────────────────────────────────────
    
    def _get_config_path(self):
        """Get profile config file path."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "profile_config.json")
    
    def _load_profile_config(self):
        """Load profile config from JSON file."""
        config_path = self._get_config_path()
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    self._profile_config = json.load(f)
            except Exception:
                self._profile_config = {}
        else:
            self._profile_config = {'pharmacy_name': 'My Pharmacy', 'profile_picture': ''}
    
    def _save_profile_config(self):
        """Save profile config to JSON file."""
        config_path = self._get_config_path()
        try:
            with open(config_path, 'w') as f:
                json.dump(self._profile_config, f, indent=2)
        except Exception as e:
            print(f"Error saving profile config: {e}")
    
    def _create_default_avatar(self):
        """Draw a default person avatar icon."""
        size = 36
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Circle background
        painter.setBrush(QBrush(QColor(PRIMARY_LIGHT)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)
        
        # Person silhouette
        pen = QPen(QColor(PRIMARY))
        pen.setWidthF(1.8)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(PRIMARY)))
        
        # Head
        head_r = 5
        painter.drawEllipse(int(size/2 - head_r), 7, head_r*2, head_r*2)
        
        # Body
        body_path = QPainterPath()
        body_path.moveTo(size/2 - 9, size - 5)
        body_path.cubicTo(size/2 - 9, 20, size/2 + 9, 20, size/2 + 9, size - 5)
        painter.drawPath(body_path)
        
        painter.end()
        return pixmap
    
    def _set_profile_avatar(self):
        """Set the profile button icon."""
        pic_path = self._profile_config.get('profile_picture', '')
        if pic_path and os.path.exists(pic_path):
            # Load custom picture and make it circular
            source = QPixmap(pic_path)
            size = 36
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, size, size, source)
            painter.end()
            self.profile_btn.setIcon(QIcon(pixmap))
        else:
            self.profile_btn.setIcon(QIcon(self._create_default_avatar()))
        self.profile_btn.setIconSize(QSize(36, 36))
    
    def _edit_shop_profile(self):
        """Open comprehensive shop profile dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Shop Profile")
        dialog.setFixedSize(480, 380)
        dialog.setStyleSheet(f"QDialog {{ background-color: {BG_WINDOW}; }}")
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(12)
        
        title = QLabel("Shop Profile")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {TEXT_DARK};")
        layout.addWidget(title)
        
        sub = QLabel("These details will appear on every printed bill.")
        sub.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; margin-bottom: 8px;")
        layout.addWidget(sub)
        
        def make_field(label_text, key, placeholder=""):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY};")
            layout.addWidget(lbl)
            inp = QLineEdit()
            inp.setFixedHeight(38)
            inp.setPlaceholderText(placeholder)
            inp.setText(self._profile_config.get(key, ''))
            layout.addWidget(inp)
            return inp
        
        name_inp    = make_field("Shop / Pharmacy Name",  'pharmacy_name',  "e.g., Sanket Medical Store")
        phone_inp   = make_field("Phone Number (10 digits)",  'phone',     "e.g., 9876543210")
        from PyQt5.QtGui import QRegExpValidator
        from PyQt5.QtCore import QRegExp
        phone_inp.setValidator(QRegExpValidator(QRegExp(r'\d{0,10}'), dialog))
        phone_inp.setMaxLength(10)
        address_inp = make_field("Shop Address",           'address',        "e.g., 123 Main Road, City - 400001")
        gst_inp     = make_field("GSTIN (15 characters)",  'gst_no',         "e.g., 27AABCU9603R1ZV")
        gst_inp.setMaxLength(15)
        
        layout.addSpacing(8)
        
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        
        save_btn = QPushButton("Save Profile")
        save_btn.setFixedHeight(42)
        save_btn.setStyleSheet(get_primary_button_style())
        save_btn.setCursor(Qt.PointingHandCursor)
        
        def save():
            import re
            phone = phone_inp.text().strip()
            gst   = gst_inp.text().strip().upper()
            
            # Phone: must be exactly 10 digits
            if phone and not re.match(r'^\d{10}$', phone):
                QMessageBox.warning(dialog, "Invalid Phone", "Phone number must be exactly 10 digits.\ne.g., 9876543210")
                return
            
            # GST: 15 char alphanumeric GSTIN format
            if gst and not re.match(r'^\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]$', gst):
                QMessageBox.warning(dialog, "Invalid GSTIN", "GSTIN must be 15 characters in format:\n  22AAAAA0000A1Z5\n  (2-digit state code + 10-char PAN + 1 entity + Z + 1 check digit)")
                return
            
            self._profile_config['pharmacy_name'] = name_inp.text().strip() or 'My Pharmacy'
            self._profile_config['phone']         = phone
            self._profile_config['address']       = address_inp.text().strip()
            self._profile_config['gst_no']        = gst
            self._save_profile_config()
            self.pharmacy_name_label.setText(self._profile_config['pharmacy_name'])
            dialog.accept()
        
        save_btn.clicked.connect(save)
        btn_row.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(42)
        cancel_btn.setStyleSheet(get_secondary_button_style())
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(dialog.reject)
        btn_row.addWidget(cancel_btn)
        
        layout.addLayout(btn_row)
        dialog.exec_()

