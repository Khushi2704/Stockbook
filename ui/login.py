"""
Login screen
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QWidget, QGraphicsDropShadowEffect, QSizePolicy,
                             QSpacerItem)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QFont, QIcon, QPen, QPainterPath
from models.user import User
from ui.styles import (
    get_login_dialog_style, get_login_card_style, get_login_title_style,
    get_login_subtitle_style, get_input_label_style, get_input_field_style,
    get_login_button_style, get_exit_button_style, get_show_password_btn_style,
    get_footer_label_style, get_icon_label_style, get_login_overlay_style,
    LOGIN_BG_PATH, LOGO_PATH, PRIMARY, TEXT_DARK, TEXT_MUTED
)
import traceback
import os


class LoginDialog(QDialog):
    """Login dialog window"""
    
    login_successful = pyqtSignal(int)  # Emit user_id on successful login
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stockbook - Login")
        self.setModal(True)
        self.setObjectName("LoginDialog")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)
        self._password_visible = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI with glassmorphic pharmacy theme"""
        # ── Background ────────────────────────────────────────────
        self.setStyleSheet(get_login_dialog_style())

        # Main layout fills the dialog
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Semi-transparent overlay widget
        overlay = QWidget(self)
        overlay.setObjectName("LoginOverlay")
        overlay.setStyleSheet(get_login_overlay_style())
        overlay_layout = QVBoxLayout(overlay)
        overlay_layout.setAlignment(Qt.AlignCenter)

        # ── Glassmorphic Card ─────────────────────────────────────
        card = QFrame()
        card.setObjectName("LoginCard")
        card.setStyleSheet(get_login_card_style())
        card.setFixedSize(420, 520)

        # Card shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(31, 61, 44, 45))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 30)
        card_layout.setSpacing(0)

        # ── Logo / Icon ───────────────────────────────────────────
        icon_label = QLabel()
        icon_label.setObjectName("IconLabel")
        icon_label.setStyleSheet(get_icon_label_style())
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Load and set the new custom logo
        icon_pixmap = QPixmap(LOGO_PATH)
        if not icon_pixmap.isNull():
            # Scale to appropriate size for the login card
            icon_pixmap = icon_pixmap.scaled(108, 108, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            
        card_layout.addWidget(icon_label)

        card_layout.addSpacing(12)

        # ── Title ─────────────────────────────────────────────────
        title = QLabel("Stockbook")
        title.setObjectName("LoginTitle")
        title.setStyleSheet(get_login_title_style())
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(4)

        # ── Subtitle ──────────────────────────────────────────────
        subtitle = QLabel("Sign in to manage your pharmacy")
        subtitle.setObjectName("LoginSubtitle")
        subtitle.setStyleSheet(get_login_subtitle_style())
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(28)

        # ── Username Field ────────────────────────────────────────
        username_label = QLabel("Username")
        username_label.setProperty("class", "InputLabel")
        username_label.setStyleSheet(get_input_label_style())
        card_layout.addWidget(username_label)

        card_layout.addSpacing(6)

        self.username_input = QLineEdit()
        self.username_input.setProperty("class", "LoginInput")
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(44)
        self.username_input.setStyleSheet(get_input_field_style())
        card_layout.addWidget(self.username_input)

        card_layout.addSpacing(18)

        # ── Password Field ────────────────────────────────────────
        password_label = QLabel("Password")
        password_label.setProperty("class", "InputLabel")
        password_label.setStyleSheet(get_input_label_style())
        card_layout.addWidget(password_label)

        card_layout.addSpacing(6)

        # Password field with embedded eye icon
        self.password_input = QLineEdit()
        self.password_input.setProperty("class", "LoginInput")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(44)
        self.password_input.setStyleSheet(get_input_field_style())

        # Create eye toggle action inside the field
        self._eye_open_icon = QIcon(self._create_eye_icon(open_eye=True))
        self._eye_closed_icon = QIcon(self._create_eye_icon(open_eye=False))
        self._toggle_action = self.password_input.addAction(
            self._eye_closed_icon, QLineEdit.TrailingPosition
        )
        self._toggle_action.triggered.connect(self._toggle_password_visibility)

        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(28)

        # ── Login Button ──────────────────────────────────────────
        login_btn = QPushButton("Login")
        login_btn.setObjectName("LoginButton")
        login_btn.setStyleSheet(get_login_button_style())
        login_btn.setFixedHeight(48)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)

        card_layout.addSpacing(12)

        # ── Exit Button ───────────────────────────────────────────
        exit_btn = QPushButton("Exit")
        exit_btn.setObjectName("ExitButton")
        exit_btn.setStyleSheet(get_exit_button_style())
        exit_btn.setFixedHeight(42)
        exit_btn.setCursor(Qt.PointingHandCursor)
        exit_btn.clicked.connect(self.close)
        card_layout.addWidget(exit_btn)

        card_layout.addStretch()

        # ── Footer ────────────────────────────────────────────────
        footer = QLabel("Stockbook Medical Store Management v1.0")
        footer.setObjectName("FooterLabel")
        footer.setStyleSheet(get_footer_label_style())
        footer.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(footer)

        # Add card to overlay
        overlay_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addWidget(overlay)

        # ── Focus & Shortcuts ─────────────────────────────────────
        self.username_input.setFocus()
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(lambda: self.password_input.setFocus())

    def _create_pharmacy_icon(self, size):
        """Draw a simple pharmacy cross icon programmatically."""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Circle background
        painter.setBrush(QBrush(QColor(PRIMARY)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        # White cross
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        cross_w = size * 0.22
        cross_h = size * 0.55
        cx = size / 2
        cy = size / 2
        # Vertical bar
        painter.drawRoundedRect(
            int(cx - cross_w / 2), int(cy - cross_h / 2),
            int(cross_w), int(cross_h), 3, 3
        )
        # Horizontal bar
        painter.drawRoundedRect(
            int(cx - cross_h / 2), int(cy - cross_w / 2),
            int(cross_h), int(cross_w), 3, 3
        )

        painter.end()
        return pixmap

    def _create_eye_icon(self, open_eye=True):
        """Draw an eye icon programmatically."""
        size = 22
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(TEXT_MUTED))
        pen.setWidthF(1.6)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        # Eye shape
        path = QPainterPath()
        path.moveTo(2, size / 2)
        path.cubicTo(6, 5, size - 6, 5, size - 2, size / 2)
        path.cubicTo(size - 6, size - 5, 6, size - 5, 2, size / 2)
        painter.drawPath(path)

        # Pupil
        painter.setBrush(QColor(TEXT_MUTED))
        painter.drawEllipse(int(size / 2 - 3), int(size / 2 - 3), 6, 6)

        # Slash line for closed eye
        if not open_eye:
            pen.setWidthF(2.0)
            painter.setPen(pen)
            painter.drawLine(4, 4, size - 4, size - 4)

        painter.end()
        return pixmap

    def _toggle_password_visibility(self):
        """Toggle password field between visible and hidden."""
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self._toggle_action.setIcon(self._eye_open_icon)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self._toggle_action.setIcon(self._eye_closed_icon)

    # ─── ORIGINAL LOGIC (untouched) ──────────────────────────────

    def handle_login(self):
        """Handle login button click"""
        try:
            username = self.username_input.text().strip()
            password = self.password_input.text()
            
            if not username:
                QMessageBox.warning(self, "Error", "Please enter username")
                return
            
            if not password:
                QMessageBox.warning(self, "Error", "Please enter password")
                return
            
            # Authenticate user
            user, message = User.authenticate(username, password)
            
            if user:
                self.login_successful.emit(user['id'])
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
                self.password_input.clear()
                self.username_input.setFocus()
        
        except Exception as e:
            print(f"Login error: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

    def paintEvent(self, event):
        """Custom paint to draw the background image scaled to fill."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        bg_pixmap = QPixmap(LOGIN_BG_PATH)
        if not bg_pixmap.isNull():
            # Scale to fill the entire dialog while keeping aspect ratio
            scaled = bg_pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            # Center the image
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        
        super().paintEvent(event)
