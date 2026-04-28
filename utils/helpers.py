"""
Helper utilities and functions
"""
import hashlib
import hmac
import os
from datetime import datetime
import shutil
from config import BACKUP_DIR, DB_PATH
import json


def hash_password(password, salt=None):
    """Hash password with salt"""
    if salt is None:
        salt = os.urandom(32)
    else:
        salt = salt.encode() if isinstance(salt, str) else salt
    
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return (salt + pwd_hash).hex()


def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        hashed_bytes = bytes.fromhex(hashed)
        salt = hashed_bytes[:32]
        stored_hash = hashed_bytes[32:]
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hmac.compare_digest(pwd_hash, stored_hash)
    except:
        return False


def format_currency(amount):
    """Format amount as currency (₹)"""
    return f"₹{amount:.2f}"


def format_date(date_obj):
    """Format date object as string in DD-MM-YYYY format"""
    if isinstance(date_obj, str):
        # If already a string, try to convert from YYYY-MM-DD to DD-MM-YYYY
        try:
            from datetime import datetime
            parsed = datetime.strptime(date_obj, "%Y-%m-%d")
            return parsed.strftime("%d-%m-%Y")
        except:
            return date_obj
    return date_obj.strftime("%d-%m-%Y") if date_obj else ""


def parse_date(date_str):
    """Parse date string to datetime"""
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").date()
    except:
        return None


def calculate_profit(mrp, net_price, quantity):
    """Calculate profit for a transaction"""
    return (mrp - net_price) * quantity


def backup_database():
    """Create backup of database"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"stockbook_backup_{timestamp}.db")
        shutil.copy2(DB_PATH, backup_file)
        return backup_file
    except Exception as e:
        raise Exception(f"Backup failed: {str(e)}")


def restore_database(backup_file):
    """Restore database from backup"""
    try:
        if not os.path.exists(backup_file):
            raise Exception("Backup file not found")
        
        # Close any open connections
        from database.db import close_connection
        close_connection()
        
        shutil.copy2(backup_file, DB_PATH)
        
        # Reinitialize connection
        from database.db import init_database
        init_database()
        
        return True
    except Exception as e:
        raise Exception(f"Restore failed: {str(e)}")


def get_backup_list():
    """Get list of all backups"""
    try:
        backups = []
        for file in os.listdir(BACKUP_DIR):
            if file.startswith("stockbook_backup_") and file.endswith(".db"):
                filepath = os.path.join(BACKUP_DIR, file)
                size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                backups.append({
                    'filename': file,
                    'path': filepath,
                    'size': size,
                    'date': datetime.fromtimestamp(mtime)
                })
        return sorted(backups, key=lambda x: x['date'], reverse=True)
    except Exception as e:
        print(f"Error getting backup list: {e}")
        return []


def delete_backup(backup_file):
    """Delete a backup file"""
    try:
        if os.path.exists(backup_file):
            os.remove(backup_file)
            return True
    except Exception as e:
        raise Exception(f"Failed to delete backup: {str(e)}")


def get_database_size():
    """Get database file size in MB"""
    try:
        size = os.path.getsize(DB_PATH)
        return size / (1024 * 1024)
    except:
        return 0


def calculate_days_until_expiry(expiry_date):
    """Calculate days until expiry"""
    try:
        from datetime import datetime as dt
        if isinstance(expiry_date, str):
            exp = datetime.strptime(expiry_date, "%Y-%m-%d").date()
        else:
            exp = expiry_date
        
        days = (exp - dt.now().date()).days
        return days
    except:
        return -1


def is_expired(expiry_date):
    """Check if medicine is expired"""
    return calculate_days_until_expiry(expiry_date) < 0
