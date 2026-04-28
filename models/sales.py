"""
Sales model and data access operations
"""
from database.db import fetch_one, fetch_all, insert, update, delete
from datetime import datetime, timedelta


class Sales:
    """Sales data model and operations"""
    
    @staticmethod
    def create(medicine_id, quantity, unit_price, total_price, profit, user_id=1):
        """Create a new sale entry"""
        query = """
            INSERT INTO sales (medicine_id, quantity, unit_price, total_price, profit, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            sale_id = insert(query, (medicine_id, quantity, unit_price, total_price, profit, user_id))
            return sale_id
        except Exception as e:
            raise Exception(f"Error creating sale: {str(e)}")
    
    @staticmethod
    def get_by_id(sale_id, user_id=1):
        """Get sale by ID"""
        query = "SELECT * FROM sales WHERE id = ? AND user_id = ?"
        return fetch_one(query, (sale_id, user_id))
    
    @staticmethod
    def get_all(user_id=1):
        """Get all sales for specific user"""
        query = "SELECT * FROM sales WHERE user_id = ? ORDER BY date DESC"
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def get_today_sales(user_id=1):
        """Get today's sales for specific user"""
        query = """
            SELECT * FROM sales 
            WHERE DATE(date, 'localtime') = DATE('now', 'localtime')
            AND user_id = ?
            ORDER BY date DESC
        """
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def get_daily_sales(date, user_id=1):
        """Get sales for a specific date for specific user"""
        query = """
            SELECT * FROM sales 
            WHERE DATE(date) = ? AND user_id = ?
            ORDER BY date
        """
        return fetch_all(query, (date, user_id))
    
    @staticmethod
    def get_sales_range(start_date, end_date, user_id=1):
        """Get sales between date range for specific user"""
        query = """
            SELECT * FROM sales 
            WHERE DATE(date) >= ? AND DATE(date) <= ? AND user_id = ?
            ORDER BY date DESC
        """
        return fetch_all(query, (start_date, end_date, user_id))
    
    @staticmethod
    def get_sales_by_medicine(medicine_id, user_id=1):
        """Get all sales for a medicine for specific user"""
        query = """
            SELECT * FROM sales 
            WHERE medicine_id = ? AND user_id = ?
            ORDER BY date DESC
        """
        return fetch_all(query, (medicine_id, user_id))
    
    @staticmethod
    def get_today_total(user_id=1):
        """Get today's total sales for specific user"""
        query = """
            SELECT 
                SUM(total_price) as total_amount,
                SUM(profit) as total_profit,
                COUNT(*) as transaction_count
            FROM sales 
            WHERE DATE(date, 'localtime') = DATE('now', 'localtime')
            AND user_id = ?
        """
        result = fetch_one(query, (user_id,))
        return {
            'total_amount': result[0] or 0,
            'total_profit': result[1] or 0,
            'transaction_count': result[2] or 0
        }
    
    @staticmethod
    def get_monthly_total(year, month, user_id=1):
        """Get monthly total sales for specific user"""
        query = """
            SELECT 
                SUM(total_price) as total_amount,
                SUM(profit) as total_profit,
                COUNT(*) as transaction_count
            FROM sales 
            WHERE STRFTIME('%Y-%m', date) = ? AND user_id = ?
        """
        date_str = f"{year:04d}-{month:02d}"
        result = fetch_one(query, (date_str, user_id))
        return {
            'total_amount': result[0] or 0,
            'total_profit': result[1] or 0,
            'transaction_count': result[2] or 0
        }
    
    @staticmethod
    def get_top_medicines(limit=10, user_id=1):
        """Get top selling medicines for specific user"""
        query = """
            SELECT 
                m.id, m.name, m.batch,
                SUM(s.quantity) as total_quantity,
                SUM(s.total_price) as total_revenue,
                SUM(s.profit) as total_profit,
                COUNT(*) as transaction_count
            FROM sales s
            JOIN medicines m ON s.medicine_id = m.id
            WHERE s.user_id = ?
            GROUP BY s.medicine_id
            ORDER BY total_quantity DESC
            LIMIT ?
        """
        return fetch_all(query, (user_id, limit))
    
    @staticmethod
    def delete_sale(sale_id, user_id=1):
        """Delete a sale for specific user"""
        query = "DELETE FROM sales WHERE id = ? AND user_id = ?"
        return delete(query, (sale_id, user_id))
