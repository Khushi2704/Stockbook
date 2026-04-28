"""
Inventory service - Manage medicines and stock
"""
from models.medicine import Medicine
from models.purchase import Purchase
from utils.validators import Validator
from config import LOW_STOCK_THRESHOLD, EXPIRY_ALERT_DAYS


class InventoryService:
    """Manage inventory operations"""
    
    @staticmethod
    def add_medicine(name, batch, expiry_date, mrp, net_price, stock=0, user_id=1):
        """Add new medicine to inventory"""
        # Validate input
        valid, errors = Validator.validate_medicine_data(name, batch, expiry_date, mrp, net_price)
        if not valid:
            return False, errors
        
        try:
            medicine_id = Medicine.create(name, batch, expiry_date, mrp, net_price, stock, user_id)
            return True, medicine_id
        except Exception as e:
            return False, [str(e)]
    
    @staticmethod
    def update_medicine(medicine_id, **kwargs):
        """Update medicine details"""
        try:
            rows = Medicine.update(medicine_id, **kwargs)
            if rows == 0:
                return False, "Medicine not found"
            return True, "Updated successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def add_stock(medicine_id, quantity, supplier, user_id=1):
        """Add stock to medicine"""
        # Validate quantity
        valid, msg = Validator.validate_quantity(str(quantity))
        if not valid:
            return False, msg
        
        try:
            # Update medicine stock
            Medicine.update_stock(medicine_id, quantity)
            
            # Record purchase
            Purchase.create(medicine_id, quantity, supplier, user_id)
            
            return True, f"Added {quantity} units successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_all_medicines(user_id=1):
        """Get all medicines for specific user"""
        return Medicine.get_all(user_id)
    
    @staticmethod
    def search_medicines(search_term, user_id=1):
        """Search medicines for specific user"""
        if not search_term or len(search_term.strip()) == 0:
            return []
        return Medicine.search(search_term, user_id)
    
    @staticmethod
    def get_low_stock_medicines(user_id=1, threshold=None):
        """Get medicines with low stock for specific user"""
        if threshold is None:
            threshold = LOW_STOCK_THRESHOLD
        return Medicine.get_low_stock(user_id, threshold)
    
    @staticmethod
    def get_expiring_medicines(user_id=1, days=None):
        """Get medicines expiring soon for specific user"""
        if days is None:
            days = EXPIRY_ALERT_DAYS
        return Medicine.get_expiring_soon(user_id, days)
    
    @staticmethod
    def get_expired_medicines(user_id=1):
        """Get expired medicines for specific user"""
        return Medicine.get_expired(user_id)
    
    @staticmethod
    def get_medicine_details(medicine_id, user_id=1):
        """Get medicine details for specific user"""
        return Medicine.get_by_id(medicine_id, user_id)
    
    @staticmethod
    def get_medicine_stock(medicine_id):
        """Get medicine stock level"""
        medicine = Medicine.get_by_id(medicine_id)
        if medicine:
            return medicine['stock']
        return 0
    
    @staticmethod
    def check_alerts(user_id=1):
        """Check and return all alerts for specific user"""
        alerts = {
            'low_stock': InventoryService.get_low_stock_medicines(user_id),
            'expiring': InventoryService.get_expiring_medicines(user_id),
            'expired': InventoryService.get_expired_medicines(user_id)
        }
        return alerts
    
    @staticmethod
    def get_alert_count(user_id=1):
        """Get count of all alerts for specific user"""
        alerts = InventoryService.check_alerts(user_id)
        return {
            'low_stock_count': len(alerts['low_stock']),
            'expiring_count': len(alerts['expiring']),
            'expired_count': len(alerts['expired']),
            'total_alerts': len(alerts['low_stock']) + len(alerts['expiring']) + len(alerts['expired'])
        }
    
    @staticmethod
    def delete_medicine(medicine_id):
        """Delete medicine"""
        try:
            Medicine.delete(medicine_id)
            return True, "Medicine deleted successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_inventory_summary():
        """Get inventory summary statistics"""
        medicines = Medicine.get_all()
        
        total_medicines = len(medicines)
        total_stock = sum(m['stock'] for m in medicines)
        total_value = sum(m['stock'] * m['mrp'] for m in medicines)
        
        alerts = InventoryService.check_alerts()
        
        return {
            'total_medicines': total_medicines,
            'total_stock_units': total_stock,
            'total_value': total_value,
            'low_stock_count': len(alerts['low_stock']),
            'expiring_count': len(alerts['expiring']),
            'expired_count': len(alerts['expired'])
        }
