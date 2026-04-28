"""
Input validators
"""
import re
from datetime import datetime


class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_medicine_name(name):
        """Validate medicine name"""
        if not name or len(name.strip()) == 0:
            return False, "Medicine name is required"
        if len(name) > 100:
            return False, "Medicine name too long (max 100 chars)"
        return True, ""
    
    @staticmethod
    def validate_batch(batch):
        """Validate batch number"""
        if not batch or len(batch.strip()) == 0:
            return False, "Batch number is required"
        if len(batch) > 50:
            return False, "Batch number too long (max 50 chars)"
        return True, ""
    
    @staticmethod
    def validate_date(date_str):
        """Validate date format (DD-MM-YYYY or YYYY-MM-DD)"""
        # Try DD-MM-YYYY first (preferred user input)
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True, ""
        except:
            pass
        # Fallback to YYYY-MM-DD
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, ""
        except:
            return False, "Invalid date format (use DD-MM-YYYY)"
    
    @staticmethod
    def validate_expiry_date(expiry_date_str):
        """Validate expiry date"""
        valid, msg = Validator.validate_date(expiry_date_str)
        if not valid:
            return False, msg
        
        # Parse either format
        try:
            exp_date = datetime.strptime(expiry_date_str, "%d-%m-%Y").date()
        except:
            exp_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        
        today = datetime.now().date()
        
        if exp_date <= today:
            return False, "Expiry date must be in future"
        
        return True, ""
    
    @staticmethod
    def validate_price(price_str):
        """Validate price"""
        try:
            price = float(price_str)
            if price < 0:
                return False, "Price cannot be negative"
            if price > 999999:
                return False, "Price too high"
            return True, ""
        except:
            return False, "Invalid price format"
    
    @staticmethod
    def validate_quantity(qty_str):
        """Validate quantity"""
        try:
            qty = int(qty_str)
            if qty <= 0:
                return False, "Quantity must be greater than 0"
            if qty > 10000:
                return False, "Quantity too high"
            return True, ""
        except:
            return False, "Invalid quantity (must be number)"
    
    @staticmethod
    def validate_username(username):
        """Validate username"""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 50:
            return False, "Username too long (max 50 chars)"
        if not re.match("^[a-zA-Z0-9_.-]+$", username):
            return False, "Username contains invalid characters"
        return True, ""
    
    @staticmethod
    def validate_password(password):
        """Validate password"""
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters"
        if len(password) > 100:
            return False, "Password too long"
        return True, ""
    
    @staticmethod
    def validate_supplier(supplier):
        """Validate supplier name"""
        if not supplier or len(supplier.strip()) == 0:
            return False, "Supplier name is required"
        if len(supplier) > 100:
            return False, "Supplier name too long"
        return True, ""
    
    @staticmethod
    def validate_stock_available(stock, requested_qty):
        """Validate stock availability"""
        if requested_qty > stock:
            return False, f"Insufficient stock. Available: {stock}"
        return True, ""
    
    @staticmethod
    def validate_medicine_data(name, batch, expiry_date, mrp, net_price):
        """Validate complete medicine data"""
        errors = []
        
        valid, msg = Validator.validate_medicine_name(name)
        if not valid:
            errors.append(msg)
        
        valid, msg = Validator.validate_batch(batch)
        if not valid:
            errors.append(msg)
        
        valid, msg = Validator.validate_expiry_date(expiry_date)
        if not valid:
            errors.append(msg)
        
        valid, msg = Validator.validate_price(mrp)
        if not valid:
            errors.append(f"MRP: {msg}")
        
        valid, msg = Validator.validate_price(net_price)
        if not valid:
            errors.append(f"Net Price: {msg}")
        
        # Check MRP > Net Price
        try:
            if float(mrp) <= float(net_price):
                errors.append("MRP must be greater than Net Price")
        except:
            pass
        
        return len(errors) == 0, errors
