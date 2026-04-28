"""
Medicine model and data access operations
"""
from database.db import execute_query, fetch_one, fetch_all, insert, update, delete
from datetime import datetime


class Medicine:
    """Medicine data model and operations"""
    
    @staticmethod
    def create(name, batch, expiry_date, mrp, net_price, stock=0, user_id=1):
        """Create a new medicine entry"""
        query = """
            INSERT INTO medicines (user_id, name, batch, expiry_date, mrp, net_price, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            medicine_id = insert(query, (user_id, name, batch, expiry_date, mrp, net_price, stock))
            return medicine_id
        except Exception as e:
            raise Exception(f"Error creating medicine: {str(e)}")
    
    @staticmethod
    def get_by_id(medicine_id, user_id=1):
        """Get medicine by ID for specific user"""
        query = "SELECT * FROM medicines WHERE id = ? AND user_id = ?"
        return fetch_one(query, (medicine_id, user_id))
    
    @staticmethod
    def get_by_name(name, user_id=1):
        """Get all medicines by name for specific user"""
        query = "SELECT * FROM medicines WHERE name LIKE ? AND user_id = ? ORDER BY expiry_date"
        return fetch_all(query, (f"%{name}%", user_id))
    
    @staticmethod
    def search(search_term, user_id=1):
        """Search medicines by name or batch for specific user"""
        query = """
            SELECT * FROM medicines 
            WHERE (name LIKE ? OR batch LIKE ?) AND user_id = ?
            ORDER BY expiry_date ASC
            LIMIT 50
        """
        return fetch_all(query, (f"%{search_term}%", f"%{search_term}%", user_id))
    
    @staticmethod
    def get_by_batch(batch, user_id=1):
        """Get medicine by batch for specific user"""
        query = "SELECT * FROM medicines WHERE batch = ? AND user_id = ? ORDER BY expiry_date"
        return fetch_all(query, (batch, user_id))
    
    @staticmethod
    def get_all(user_id=1):
        """Get all medicines for specific user"""
        query = "SELECT * FROM medicines WHERE user_id = ? ORDER BY name"
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def update_stock(medicine_id, quantity_change):
        """Update medicine stock"""
        query = "UPDATE medicines SET stock = stock + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        return update(query, (quantity_change, medicine_id))
    
    @staticmethod
    def set_stock(medicine_id, quantity):
        """Set medicine stock to specific value"""
        query = "UPDATE medicines SET stock = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        return update(query, (quantity, medicine_id))
    
    @staticmethod
    def get_low_stock(user_id=1, threshold=10):
        """Get medicines with low stock for specific user"""
        query = "SELECT * FROM medicines WHERE stock < ? AND user_id = ? AND expiry_date > DATE('now') ORDER BY stock"
        return fetch_all(query, (threshold, user_id))
    
    @staticmethod
    def get_expiring_soon(user_id=1, days=30):
        """Get medicines expiring within specified days for specific user"""
        query = """
            SELECT * FROM medicines 
            WHERE expiry_date <= DATE('now', '+' || ? || ' days')
            AND expiry_date > DATE('now')
            AND user_id = ?
            ORDER BY expiry_date
        """
        return fetch_all(query, (days, user_id))
    
    @staticmethod
    def get_expired(user_id=1):
        """Get expired medicines for specific user"""
        query = "SELECT * FROM medicines WHERE expiry_date < DATE('now') AND user_id = ?"
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def update(medicine_id, **kwargs):
        """Update medicine details"""
        allowed_fields = ['name', 'batch', 'expiry_date', 'mrp', 'net_price']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return 0
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE medicines SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        values = list(updates.values()) + [medicine_id]
        
        return update(query, values)
    
    @staticmethod
    def delete(medicine_id):
        """Delete medicine"""
        query = "DELETE FROM medicines WHERE id = ?"
        return delete(query, (medicine_id,))
