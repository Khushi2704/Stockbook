"""
Report service - Generate sales and business reports
"""
from models.sales import Sales
from models.purchase import Purchase
from models.medicine import Medicine
from datetime import datetime, timedelta
from utils.helpers import format_currency


class ReportService:
    """Generate various business reports"""
    
    @staticmethod
    def get_today_sales(user_id=1):
        """Get today's sales summary for specific user"""
        return Sales.get_today_total(user_id)
    
    @staticmethod
    def get_daily_sales(date, user_id=1):
        """Get sales for specific date and user"""
        sales = Sales.get_daily_sales(date, user_id)
        total_amount = sum(s['total_price'] for s in sales)
        total_profit = sum(s['profit'] for s in sales)
        
        return {
            'date': date,
            'transactions': len(sales),
            'total_amount': total_amount,
            'total_profit': total_profit,
            'sales': sales
        }
    
    @staticmethod
    def get_monthly_sales(year, month, user_id=1):
        """Get sales for specific month and user"""
        summary = Sales.get_monthly_total(year, month, user_id)
        sales = Sales.get_sales_range(
            f"{year:04d}-{month:02d}-01",
            f"{year:04d}-{month:02d}-31",
            user_id
        )
        
        return {
            'year': year,
            'month': month,
            'transactions': summary['transaction_count'],
            'total_amount': summary['total_amount'],
            'total_profit': summary['total_profit'],
            'sales': sales
        }
    
    @staticmethod
    def get_sales_range_report(start_date, end_date, user_id=1):
        """Get sales for date range for specific user"""
        sales = Sales.get_sales_range(start_date, end_date, user_id)
        total_amount = sum(s['total_price'] for s in sales)
        total_profit = sum(s['profit'] for s in sales)
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'transactions': len(sales),
            'total_amount': total_amount,
            'total_profit': total_profit,
            'avg_per_transaction': total_amount / len(sales) if sales else 0,
            'sales': sales
        }
    
    @staticmethod
    def get_top_medicines(limit=10, user_id=1):
        """Get top selling medicines for specific user"""
        return Sales.get_top_medicines(limit, user_id)
    
    @staticmethod
    def get_medicine_sales_report(medicine_id, user_id=1):
        """Get sales report for specific medicine for specific user"""
        medicine = Medicine.get_by_id(medicine_id, user_id)
        sales = Sales.get_sales_by_medicine(medicine_id, user_id)
        
        total_quantity = sum(s['quantity'] for s in sales)
        total_amount = sum(s['total_price'] for s in sales)
        total_profit = sum(s['profit'] for s in sales)
        
        return {
            'medicine': medicine,
            'total_quantity_sold': total_quantity,
            'total_amount': total_amount,
            'total_profit': total_profit,
            'transactions': len(sales),
            'sales': sales
        }
    
    @staticmethod
    def get_profit_analysis(year=None, month=None, user_id=1):
        """Get profit analysis for specific user"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        summary = Sales.get_monthly_total(year, month, user_id)
        top_medicines = Sales.get_top_medicines(5, user_id)
        
        return {
            'period': f"{month:02d}/{year:04d}",
            'total_profit': summary['total_profit'],
            'total_sales': summary['total_amount'],
            'profit_margin': (summary['total_profit'] / summary['total_amount'] * 100) if summary['total_amount'] > 0 else 0,
            'avg_profit_per_transaction': summary['total_profit'] / summary['transaction_count'] if summary['transaction_count'] > 0 else 0,
            'transactions': summary['transaction_count'],
            'top_profitable_medicines': top_medicines
        }
    
    @staticmethod
    def get_last_7_days_report(user_id=1):
        """Get sales for last 7 days for specific user"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        return ReportService.get_sales_range_report(
            str(start_date), str(end_date), user_id
        )
    
    @staticmethod
    def get_last_30_days_report(user_id=1):
        """Get sales for last 30 days for specific user"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        return ReportService.get_sales_range_report(
            str(start_date), str(end_date), user_id
        )
    
    @staticmethod
    def get_business_summary(user_id=1):
        """Get overall business summary for specific user"""
        # Today's stats
        today_sales = Sales.get_today_total(user_id)
        
        # This month's stats
        now = datetime.now()
        month_sales = Sales.get_monthly_total(now.year, now.month, user_id)
        
        # Top medicines
        top_medicines = Sales.get_top_medicines(5, user_id)
        
        # Last 7 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        week_sales = Sales.get_sales_range(str(start_date), str(end_date), user_id)
        week_amount = sum(s['total_price'] for s in week_sales)
        week_profit = sum(s['profit'] for s in week_sales)
        
        return {
            'today': today_sales,
            'this_month': month_sales,
            'this_week': {
                'total_amount': week_amount,
                'total_profit': week_profit,
                'transactions': len(week_sales)
            },
            'top_medicines': top_medicines
        }
    
    @staticmethod
    def format_report_for_print(report_data):
        """Format report for printing"""
        output = []
        output.append("=" * 60)
        output.append("SALES REPORT".center(60))
        output.append("=" * 60)
        
        for key, value in report_data.items():
            if key != 'sales' and key != 'top_medicines':
                if isinstance(value, float):
                    output.append(f"{key}: {format_currency(value)}")
                else:
                    output.append(f"{key}: {value}")
        
        return "\n".join(output)
