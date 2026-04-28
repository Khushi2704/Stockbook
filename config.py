"""
Configuration and constants for Medical Store Management System
"""
import os
from pathlib import Path

# Application Settings
APP_NAME = "Stockbook"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Database
DB_PATH = os.path.join(str(Path.home()), ".stockbook", "database.db")
BACKUP_DIR = os.path.join(str(Path.home()), ".stockbook", "backups")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Business Logic Constants
LOW_STOCK_THRESHOLD = 10  # Alert when stock < 10 units
EXPIRY_ALERT_DAYS = 30    # Alert if expiry within 30 days
MAX_BILL_ITEMS = 100      # Max items per bill

# UI Constants
FONT_SIZE_NORMAL = 10
FONT_SIZE_LARGE = 14
FONT_SIZE_TITLE = 16

# Subscription
SUBSCRIPTION_PRICE = 10000  # ₹10,000/year
TRIAL_DAYS = 7

# Billing
BILL_HEADERS = ["Medicine", "Batch", "Qty", "Price", "Amount"]

# Performance
SEARCH_TIMEOUT = 2  # seconds
BILLING_TIMEOUT = 3  # seconds
