"""
Purchase model and data access operations
"""
from database.db import fetch_one, fetch_all, insert, delete


class Purchase:
    """Purchase data model and operations"""
    
    @staticmethod
    def create(medicine_id, quantity_added, supplier, user_id=1):
        """Create a new purchase entry"""
        query = """
            INSERT INTO purchases (medicine_id, quantity_added, supplier, user_id)
            VALUES (?, ?, ?, ?)
        """
        try:
            purchase_id = insert(query, (medicine_id, quantity_added, supplier, user_id))
            return purchase_id
        except Exception as e:
            raise Exception(f"Error creating purchase: {str(e)}")
    
    @staticmethod
    def get_by_id(purchase_id, user_id=1):
        """Get purchase by ID"""
        query = "SELECT * FROM purchases WHERE id = ? AND user_id = ?"
        return fetch_one(query, (purchase_id, user_id))
    
    @staticmethod
    def get_all(user_id=1):
        """Get all purchases for specific user"""
        query = "SELECT * FROM purchases WHERE user_id = ? ORDER BY date DESC"
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def get_today_purchases(user_id=1):
        """Get today's purchases for specific user"""
        query = """
            SELECT * FROM purchases 
            WHERE DATE(date) = DATE('now') AND user_id = ?
            ORDER BY date DESC
        """
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def get_daily_purchases(date, user_id=1):
        """Get purchases for a specific date for specific user"""
        query = """
            SELECT * FROM purchases 
            WHERE DATE(date) = ? AND user_id = ?
            ORDER BY date
        """
        return fetch_all(query, (date, user_id))
    
    @staticmethod
    def get_purchases_by_medicine(medicine_id, user_id=1):
        """Get all purchases for a medicine for specific user"""
        query = """
            SELECT * FROM purchases 
            WHERE medicine_id = ? AND user_id = ?
            ORDER BY date DESC
        """
        return fetch_all(query, (medicine_id, user_id))
    
    @staticmethod
    def get_purchases_by_supplier(supplier, user_id=1):
        """Get all purchases from a supplier for specific user"""
        query = """
            SELECT * FROM purchases 
            WHERE supplier = ? AND user_id = ?
            ORDER BY date DESC
        """
        return fetch_all(query, (supplier, user_id))
    
    @staticmethod
    def get_all_suppliers(user_id=1):
        """Get list of all unique suppliers for specific user"""
        query = """
            SELECT DISTINCT supplier FROM purchases
            WHERE user_id = ?
            ORDER BY supplier
        """
        results = fetch_all(query, (user_id,))
        return [row[0] for row in results]
    
    @staticmethod
    def get_purchase_summary(start_date, end_date, user_id=1):
        """Get purchase summary for date range for specific user"""
        query = """
            SELECT 
                SUM(quantity_added) as total_quantity,
                COUNT(*) as transaction_count
            FROM purchases 
            WHERE DATE(date) >= ? AND DATE(date) <= ? AND user_id = ?
        """
        result = fetch_one(query, (start_date, end_date, user_id))
        return {
            'total_quantity': result[0] or 0,
            'transaction_count': result[1] or 0
        }
    
    @staticmethod
    def delete_purchase(purchase_id, user_id=1):
        """Delete a purchase for specific user"""
        query = "DELETE FROM purchases WHERE id = ? AND user_id = ?"
        return delete(query, (purchase_id, user_id))
