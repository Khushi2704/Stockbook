"""
Stockbook UI Styles & Theme
Pharmacy Fresh Green Palette with Dark/Light Mode Support

This file contains all styling constants and stylesheets.
No application logic is defined here.
"""
import os
import json

# ─── Theme State ─────────────────────────────────────────────────
_current_theme = "light"  # "light" or "dark"

def _get_theme_config_path():
    """Get path to theme config file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "profile_config.json")

def load_theme_preference():
    """Load saved theme from profile_config.json."""
    global _current_theme
    try:
        path = _get_theme_config_path()
        if os.path.exists(path):
            with open(path, 'r') as f:
                cfg = json.load(f)
                _current_theme = cfg.get('theme', 'light')
    except Exception:
        _current_theme = "light"
    return _current_theme

def save_theme_preference(theme):
    """Save theme to profile_config.json."""
    global _current_theme
    _current_theme = theme
    try:
        path = _get_theme_config_path()
        cfg = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                cfg = json.load(f)
        cfg['theme'] = theme
        with open(path, 'w') as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

def is_dark_mode():
    """Check if dark mode is active."""
    return _current_theme == "dark"

def get_current_theme():
    """Get current theme name."""
    return _current_theme

# ─── Light Theme Palette ─────────────────────────────────────────
LIGHT = {
    'PRIMARY': "#2CB67D",
    'PRIMARY_DARK': "#2AAE8A",
    'PRIMARY_HOVER': "#24A074",
    'PRIMARY_LIGHT': "#E8F5E9",
    'BG_MAIN': "#F2FFFB",
    'BG_WINDOW': "#F5F8F6",
    'TEXT_DARK': "#1F3D2C",
    'TEXT_SECONDARY': "#124D41",
    'TEXT_MUTED': "#5A8A7A",
    'CARD_BG': "rgba(255, 255, 255, 0.88)",
    'CARD_BG_SOLID': "#FFFFFF",
    'CARD_BORDER': "rgba(44, 182, 125, 0.18)",
    'CARD_BORDER_SOLID': "#D5EDE3",
    'INPUT_BG': "#FAFFFE",
    'INPUT_BORDER': "#C8E0D6",
    'WHITE': "#FFFFFF",
    'DIVIDER': "#E0EDE7",
    'TABLE_HEADER_BG': "#E8F5E9",
    'TABLE_ALT_ROW': "#F8FCFA",
    'SHADOW': "rgba(31, 61, 44, 0.10)",
    'LOGIN_OVERLAY_BG': "rgba(242, 255, 251, 0.45)",
}

# ─── Dark Theme Palette ──────────────────────────────────────────
DARK = {
    'PRIMARY': "#3DD68E",
    'PRIMARY_DARK': "#2CB67D",
    'PRIMARY_HOVER': "#4AE09A",
    'PRIMARY_LIGHT': "#1A3328",
    'BG_MAIN': "#0F1A14",
    'BG_WINDOW': "#121E17",
    'TEXT_DARK': "#E8F5EE",
    'TEXT_SECONDARY': "#B0D4C4",
    'TEXT_MUTED': "#6A9A8A",
    'CARD_BG': "rgba(20, 35, 27, 0.92)",
    'CARD_BG_SOLID': "#182A21",
    'CARD_BORDER': "rgba(61, 214, 142, 0.20)",
    'CARD_BORDER_SOLID': "#243D30",
    'INPUT_BG': "#14231B",
    'INPUT_BORDER': "#2A4D3A",
    'WHITE': "#182A21",
    'DIVIDER': "#243D30",
    'TABLE_HEADER_BG': "#1A3328",
    'TABLE_ALT_ROW': "#14231B",
    'SHADOW': "rgba(0, 0, 0, 0.25)",
    'LOGIN_OVERLAY_BG': "rgba(15, 26, 20, 0.65)",
}

def _t():
    """Get current theme palette."""
    return DARK if is_dark_mode() else LIGHT

# ─── Dynamic Color Accessors ─────────────────────────────────────
# These are properties that return values based on current theme
def _get(key):
    return _t()[key]

# For backwards compatibility, we define module-level constants
# These are used at IMPORT time, so we need to keep them.
# However, all style functions use _t() for dynamic theming.
PRIMARY = "#2CB67D"
PRIMARY_DARK = "#2AAE8A"
PRIMARY_HOVER = "#24A074"
PRIMARY_LIGHT = "#E8F5E9"
BG_MAIN = "#F2FFFB"
BG_WINDOW = "#F5F8F6"
TEXT_DARK = "#1F3D2C"
TEXT_SECONDARY = "#124D41"
TEXT_MUTED = "#5A8A7A"
CARD_BG = "rgba(255, 255, 255, 0.88)"
CARD_BG_SOLID = "#FFFFFF"
CARD_BORDER = "rgba(44, 182, 125, 0.18)"
CARD_BORDER_SOLID = "#D5EDE3"
INPUT_BG = "#FAFFFE"
INPUT_BORDER = "#C8E0D6"
INPUT_FOCUS_BORDER = PRIMARY
SHADOW = "rgba(31, 61, 44, 0.10)"
ALERT_RED = "#E74C3C"
ALERT_RED_BG = "#FFF0EE"
ALERT_ORANGE = "#F39C12"
ALERT_ORANGE_BG = "#FFF8EC"
WHITE = "#FFFFFF"
DIVIDER = "#E0EDE7"
TABLE_HEADER_BG = "#E8F5E9"
TABLE_ALT_ROW = "#F8FCFA"
BLUE_ACCENT = "#3498DB"
ORANGE_ACCENT = "#F39C12"

# ─── Asset Paths ─────────────────────────────────────────────────
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
LOGIN_BG_PATH = os.path.join(ASSETS_DIR, "login_bg.png")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

# Load theme on import
load_theme_preference()

# ═══════════════════════════════════════════════════════════════════
#  GLOBAL APPLICATION STYLESHEET
# ═══════════════════════════════════════════════════════════════════

def get_global_stylesheet():
    """Return a global stylesheet applied to the entire QApplication."""
    t = _t()
    return f"""
        /* ── Base ─────────────────────────────────────── */
        QMainWindow, QDialog {{
            background-color: {t['BG_WINDOW']};
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
            color: {t['TEXT_DARK']};
        }}

        QWidget {{
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
        }}

        /* ── Labels ───────────────────────────────────── */
        QLabel {{
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
            background: transparent;
        }}

        /* ── Input Fields ─────────────────────────────── */
        QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{
            background-color: {t['INPUT_BG']};
            border: 1.5px solid {t['INPUT_BORDER']};
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
            selection-background-color: {t['PRIMARY']};
            selection-color: {'#FFFFFF' if not is_dark_mode() else '#0F1A14'};
        }}
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
            border: 2px solid {t['PRIMARY']};
            background-color: {t['WHITE']};
        }}

        /* ── ComboBox ─────────────────────────────────── */
        QComboBox {{
            background-color: {t['INPUT_BG']};
            border: 1.5px solid {t['INPUT_BORDER']};
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
        }}
        QComboBox:focus {{
            border: 2px solid {t['PRIMARY']};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {t['WHITE']};
            border: 1px solid {t['CARD_BORDER_SOLID']};
            border-radius: 4px;
            selection-background-color: {t['PRIMARY_LIGHT']};
            selection-color: {t['TEXT_DARK']};
            padding: 4px;
        }}

        /* ── Buttons ──────────────────────────────────── */
        QPushButton {{
            background-color: {t['WHITE']};
            color: {t['TEXT_DARK']};
            border: 1.5px solid {t['INPUT_BORDER']};
            border-radius: 8px;
            padding: 8px 18px;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {t['PRIMARY_LIGHT']};
            border-color: {t['PRIMARY']};
            color: {t['TEXT_DARK']};
        }}
        QPushButton:pressed {{
            background-color: {t['PRIMARY']};
            color: {'#FFFFFF' if not is_dark_mode() else '#0F1A14'};
        }}

        /* ── Tables ───────────────────────────────────── */
        QTableWidget {{
            background-color: {t['WHITE']};
            border: 1px solid {t['CARD_BORDER_SOLID']};
            border-radius: 8px;
            gridline-color: {t['DIVIDER']};
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            selection-background-color: {t['PRIMARY_LIGHT']};
            selection-color: {t['TEXT_DARK']};
            alternate-background-color: {t['TABLE_ALT_ROW']};
        }}
        QTableWidget::item {{
            padding: 6px 10px;
            border: none;
            color: {t['TEXT_DARK']};
        }}
        QTableWidget::item:selected {{
            background-color: {t['PRIMARY_LIGHT']};
            color: {t['TEXT_DARK']};
        }}
        QHeaderView::section {{
            background-color: {t['TABLE_HEADER_BG']};
            color: {t['TEXT_SECONDARY']};
            font-weight: 700;
            font-size: 12px;
            padding: 8px 10px;
            border: none;
            border-bottom: 2px solid {t['PRIMARY']};
            border-right: 1px solid {t['DIVIDER']};
        }}
        QHeaderView::section:last {{
            border-right: none;
        }}

        /* ── Group Box ────────────────────────────────── */
        QGroupBox {{
            background-color: {t['WHITE']};
            border: 1.5px solid {t['CARD_BORDER_SOLID']};
            border-radius: 10px;
            margin-top: 16px;
            padding: 20px 16px 16px 16px;
            font-size: 13px;
            font-weight: 600;
            color: {t['TEXT_DARK']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 16px;
            padding: 0 8px;
            background-color: {t['WHITE']};
            color: {t['PRIMARY']};
            font-weight: 700;
        }}

        /* ── ScrollBar ────────────────────────────────── */
        QScrollBar:vertical {{
            background: {t['BG_WINDOW']};
            width: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {t['INPUT_BORDER']};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {t['PRIMARY']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}

        /* ── MessageBox ───────────────────────────────── */
        QMessageBox {{
            background-color: {t['WHITE']};
        }}
        QMessageBox QLabel {{
            color: {t['TEXT_DARK']};
            font-size: 13px;
        }}
        QMessageBox QPushButton {{
            min-width: 80px;
        }}
    """


# ═══════════════════════════════════════════════════════════════════
#  LOGIN PAGE STYLES
# ═══════════════════════════════════════════════════════════════════

def get_login_dialog_style():
    """Return the full stylesheet for the Login dialog."""
    bg_path = LOGIN_BG_PATH.replace("\\", "/")
    return f"""
        QDialog#LoginDialog {{
            background-image: url("{bg_path}");
            background-repeat: no-repeat;
            background-position: center;
        }}
    """


def get_login_overlay_style():
    """Semi-transparent overlay that sits behind the card."""
    t = _t()
    return f"""
        QWidget#LoginOverlay {{
            background-color: {t['LOGIN_OVERLAY_BG']};
        }}
    """


def get_login_card_style():
    """Glassmorphic card container."""
    t = _t()
    return f"""
        QFrame#LoginCard {{
            background-color: {t['CARD_BG']};
            border: 1px solid {t['CARD_BORDER']};
            border-radius: 20px;
        }}
    """


def get_login_title_style():
    """App title label style."""
    t = _t()
    return f"""
        QLabel#LoginTitle {{
            color: {t['TEXT_DARK']};
            font-size: 26px;
            font-weight: 700;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            background: transparent;
        }}
    """


def get_login_subtitle_style():
    """Subtitle / tagline style."""
    t = _t()
    return f"""
        QLabel#LoginSubtitle {{
            color: {t['TEXT_SECONDARY']};
            font-size: 13px;
            font-weight: 400;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            background: transparent;
        }}
    """


def get_input_label_style():
    """Label above input fields."""
    t = _t()
    return f"""
        QLabel.InputLabel {{
            color: {t['TEXT_SECONDARY']};
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
            padding-left: 2px;
        }}
    """


def get_input_field_style():
    """Styled QLineEdit for login inputs."""
    t = _t()
    return f"""
        QLineEdit.LoginInput {{
            background-color: {t['INPUT_BG']};
            border: 1.5px solid {t['CARD_BORDER']};
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
            selection-background-color: {t['PRIMARY']};
            selection-color: {'#FFFFFF' if not is_dark_mode() else '#0F1A14'};
        }}
        QLineEdit.LoginInput:focus {{
            border: 2px solid {t['PRIMARY']};
            background-color: {t['WHITE']};
        }}
        QLineEdit.LoginInput::placeholder {{
            color: {t['TEXT_MUTED']};
        }}
    """


def get_login_button_style():
    """Primary login button style."""
    t = _t()
    return f"""
        QPushButton#LoginButton {{
            background-color: {t['PRIMARY']};
            color: {'#FFFFFF' if not is_dark_mode() else '#0F1A14'};
            border: none;
            border-radius: 10px;
            padding: 12px 0px;
            font-size: 15px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 0.5px;
        }}
        QPushButton#LoginButton:hover {{
            background-color: {t['PRIMARY_HOVER']};
        }}
        QPushButton#LoginButton:pressed {{
            background-color: {t['PRIMARY_DARK']};
        }}
    """


def get_exit_button_style():
    """Secondary exit button style."""
    t = _t()
    return f"""
        QPushButton#ExitButton {{
            background-color: transparent;
            color: {t['TEXT_MUTED']};
            border: 1.5px solid {t['CARD_BORDER']};
            border-radius: 10px;
            padding: 12px 0px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton#ExitButton:hover {{
            background-color: {t['PRIMARY_LIGHT']};
            color: {t['TEXT_DARK']};
            border-color: {t['PRIMARY']};
        }}
    """


def get_show_password_btn_style():
    """Toggle show/hide password button."""
    t = _t()
    return f"""
        QPushButton#ShowPasswordBtn {{
            background: transparent;
            border: none;
            color: {t['PRIMARY']};
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            padding: 0 8px;
        }}
        QPushButton#ShowPasswordBtn:hover {{
            color: {t['PRIMARY_HOVER']};
            text-decoration: underline;
        }}
    """


def get_footer_label_style():
    """Footer / version label."""
    t = _t()
    return f"""
        QLabel#FooterLabel {{
            color: {t['TEXT_MUTED']};
            font-size: 11px;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
        }}
    """


def get_icon_label_style():
    """Icon / logo label."""
    return f"""
        QLabel#IconLabel {{
            background: transparent;
        }}
    """


# ═══════════════════════════════════════════════════════════════════
#  REUSABLE COMPONENT STYLES (for inside-app screens)
# ═══════════════════════════════════════════════════════════════════

def get_primary_button_style():
    """Primary action button (e.g., Add to Bill, Finalize Sale)."""
    t = _t()
    return f"""
        QPushButton {{
            background-color: {t['PRIMARY']};
            color: {'#FFFFFF' if not is_dark_mode() else '#0F1A14'};
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {t['PRIMARY_HOVER']};
        }}
        QPushButton:pressed {{
            background-color: #1E8C60;
        }}
    """


def get_secondary_button_style():
    """Secondary action button (e.g., Clear, Close)."""
    t = _t()
    return f"""
        QPushButton {{
            background-color: {t['WHITE']};
            color: {t['TEXT_SECONDARY']};
            border: 1.5px solid {t['INPUT_BORDER']};
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {t['PRIMARY_LIGHT']};
            border-color: {t['PRIMARY']};
            color: {t['TEXT_DARK']};
        }}
    """


def get_danger_button_style():
    """Danger/warning button (e.g., Delete)."""
    t = _t()
    return f"""
        QPushButton {{
            background-color: {t['WHITE']};
            color: {ALERT_RED};
            border: 1.5px solid {ALERT_RED};
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {ALERT_RED};
            color: #FFFFFF;
        }}
    """


def get_accent_button_style():
    """Accent button (e.g., Print, Export)."""
    return f"""
        QPushButton {{
            background-color: {BLUE_ACCENT};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: #2980B9;
        }}
    """


def get_warning_button_style():
    """Warning/orange button (e.g., Finalize Sale)."""
    return f"""
        QPushButton {{
            background-color: {ORANGE_ACCENT};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: #E67E22;
        }}
    """


def get_stat_card_style(bg_color=None):
    """Stat card for dashboard metrics."""
    t = _t()
    bg = bg_color or t['WHITE']
    return f"""
        QFrame {{
            background-color: {bg};
            border: 1px solid {t['CARD_BORDER_SOLID']};
            border-radius: 12px;
            padding: 0px;
        }}
    """


def get_page_title_style():
    """Page-level title style (used at the top of every screen)."""
    t = _t()
    return f"""
        QLabel {{
            color: {t['TEXT_DARK']};
            font-size: 20px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            padding: 0px;
        }}
    """


def get_section_title_style():
    """Section title within a page."""
    t = _t()
    return f"""
        QLabel {{
            color: {t['TEXT_SECONDARY']};
            font-size: 13px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
    """


def get_field_label_style():
    """Label for form fields."""
    t = _t()
    return f"""
        QLabel {{
            color: {t['TEXT_SECONDARY']};
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
    """


def get_detail_panel_style():
    """Medicine detail panel in billing/purchase."""
    t = _t()
    return f"""
        QLabel {{
            background-color: {t['BG_MAIN']};
            border: 1px solid {t['CARD_BORDER_SOLID']};
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
            line-height: 1.6;
        }}
    """


def get_bill_summary_style():
    """Bill total summary bar."""
    t = _t()
    return f"""
        QLabel {{
            background-color: {t['PRIMARY_LIGHT']};
            border: 1.5px solid {t['PRIMARY']};
            border-radius: 10px;
            padding: 14px 18px;
            font-size: 16px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
        }}
    """


def get_report_summary_style():
    """Report summary bar."""
    t = _t()
    return f"""
        QLabel {{
            background-color: {t['PRIMARY_LIGHT']};
            border: 1px solid {t['CARD_BORDER_SOLID']};
            border-radius: 10px;
            padding: 14px 18px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            color: {t['TEXT_DARK']};
        }}
    """


def get_status_label_style():
    """Status / info label at the bottom of windows."""
    t = _t()
    return f"""
        QLabel {{
            color: {t['TEXT_MUTED']};
            font-size: 11px;
            font-family: 'Segoe UI', sans-serif;
        }}
    """


def get_nav_button_style():
    """Dashboard navigation button (large action card)."""
    t = _t()
    return f"""
        QPushButton {{
            background-color: {t['WHITE']};
            color: {t['TEXT_DARK']};
            border: 1.5px solid {t['CARD_BORDER_SOLID']};
            border-radius: 12px;
            padding: 16px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {t['PRIMARY_LIGHT']};
            border-color: {t['PRIMARY']};
        }}
        QPushButton:pressed {{
            background-color: {t['PRIMARY']};
            color: {'#FFFFFF' if not is_dark_mode() else '#0F1A14'};
        }}
    """


def get_alert_table_item_style(alert_type):
    """Return color for alert table items based on type."""
    if alert_type == "expired":
        return ALERT_RED
    elif alert_type == "expiring":
        return ALERT_ORANGE
    elif alert_type == "low_stock":
        return ALERT_ORANGE
    t = _t()
    return t['TEXT_DARK']


def get_theme_toggle_style():
    """Style for the dark/light mode toggle button."""
    t = _t()
    return f"""
        QPushButton#ThemeToggle {{
            background-color: {t['PRIMARY_LIGHT']};
            border: 1.5px solid {t['CARD_BORDER_SOLID']};
            border-radius: 16px;
            padding: 4px 12px;
            font-size: 16px;
            min-width: 32px;
            min-height: 32px;
        }}
        QPushButton#ThemeToggle:hover {{
            background-color: {t['PRIMARY']};
            border-color: {t['PRIMARY']};
        }}
    """
