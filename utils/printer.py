"""
Billing and invoice printer
"""
from datetime import datetime
from utils.helpers import format_currency


class BillPrinter:
    """Generate text-based bills for printing"""
    
    def __init__(self, shop_name="Stockbook Medical Store"):
        self.shop_name = shop_name
        self.width = 50
    
    def generate_bill(self, items, total_amount, payment_method="Cash"):
        """
        Generate a printable bill
        items: list of {medicine_name, batch, quantity, unit_price, amount}
        """
        bill = []
        
        # Header
        bill.append("=" * self.width)
        bill.append(self.center(self.shop_name))
        bill.append(self.center("MEDICAL STORE"))
        bill.append("=" * self.width)
        
        # Date and time
        now = datetime.now()
        bill.append(self.left(f"Date: {now.strftime('%d-%m-%Y')}"))
        bill.append(self.left(f"Time: {now.strftime('%H:%M:%S')}"))
        bill.append("-" * self.width)
        
        # Header for items
        bill.append(self.format_item_header())
        bill.append("-" * self.width)
        
        # Items
        for item in items:
            bill.append(self.format_item_row(item))
        
        # Footer
        bill.append("-" * self.width)
        bill.append(self.right(f"Total: {format_currency(total_amount)}"))
        bill.append(self.right(f"Payment: {payment_method}"))
        bill.append("=" * self.width)
        bill.append(self.center("Thank You! Visit Again"))
        bill.append("=" * self.width)
        
        return "\n".join(bill)
    
    def generate_detailed_bill(self, items, total_amount, profit, payment_method="Cash"):
        """Generate detailed bill with profit info"""
        bill = []
        
        # Header
        bill.append("=" * self.width)
        bill.append(self.center(self.shop_name))
        bill.append(self.center("DETAILED INVOICE"))
        bill.append("=" * self.width)
        
        # Date and time
        now = datetime.now()
        bill.append(self.left(f"Date: {now.strftime('%d-%m-%Y')}"))
        bill.append(self.left(f"Time: {now.strftime('%H:%M:%S')}"))
        bill.append(self.left(f"Invoice #: {now.strftime('%Y%m%d%H%M%S')}"))
        bill.append("-" * self.width)
        
        # Header for items
        bill.append(self.format_detailed_item_header())
        bill.append("-" * self.width)
        
        # Items
        for item in items:
            bill.append(self.format_detailed_item_row(item))
        
        # Summary
        bill.append("-" * self.width)
        bill.append(self.right(f"Total Sale: {format_currency(total_amount)}"))
        bill.append(self.right(f"Profit: {format_currency(profit)}"))
        bill.append(self.right(f"Payment: {payment_method}"))
        bill.append("=" * self.width)
        bill.append(self.center("Thank You! Visit Again"))
        bill.append("=" * self.width)
        
        return "\n".join(bill)
    
    def center(self, text):
        """Center text"""
        return text.center(self.width)
    
    def left(self, text):
        """Left align text"""
        return text.ljust(self.width)
    
    def right(self, text):
        """Right align text"""
        return text.rjust(self.width)
    
    def format_item_header(self):
        """Format item table header"""
        return f"{'Medicine':<20} {'Qty':>5} {'Price':>10} {'Amount':>10}"
    
    def format_item_row(self, item):
        """Format item row"""
        name = item.get('medicine_name', '')[:20].ljust(20)
        qty = str(item.get('quantity', 0)).rjust(5)
        price = format_currency(item.get('unit_price', 0)).rjust(10)
        amount = format_currency(item.get('amount', 0)).rjust(10)
        return f"{name} {qty} {price} {amount}"
    
    def format_detailed_item_header(self):
        """Format detailed item header"""
        return f"{'Med':<15} {'Batch':>10} {'Qty':>4} {'Rate':>8} {'Profit':>8}"
    
    def format_detailed_item_row(self, item):
        """Format detailed item row"""
        name = item.get('medicine_name', '')[:15].ljust(15)
        batch = str(item.get('batch', ''))[:10].rjust(10)
        qty = str(item.get('quantity', 0)).rjust(4)
        rate = format_currency(item.get('unit_price', 0)).rjust(8)
        profit = format_currency(item.get('profit', 0)).rjust(8)
        return f"{name} {batch} {qty} {rate} {profit}"
    
    def generate_daily_report(self, date, total_sales, total_profit, transactions):
        """Generate daily sales report"""
        report = []
        
        report.append("=" * self.width)
        report.append(self.center(self.shop_name))
        report.append(self.center("DAILY SALES REPORT"))
        report.append(self.center(f"Date: {date}"))
        report.append("=" * self.width)
        
        report.append(self.left(f"Total Sales: {format_currency(total_sales)}"))
        report.append(self.left(f"Total Profit: {format_currency(total_profit)}"))
        report.append(self.left(f"Transactions: {transactions}"))
        report.append(self.left(f"Avg per transaction: {format_currency(total_sales/transactions if transactions > 0 else 0)}"))
        
        report.append("=" * self.width)
        
        return "\n".join(report)
    
    @staticmethod
    def print_bill(bill_text):
        """Print bill to printer"""
        try:
            import subprocess
            # For Windows
            with open('temp_bill.txt', 'w') as f:
                f.write(bill_text)
            subprocess.Popen(['notepad', 'temp_bill.txt'])
            return True
        except Exception as e:
            print(f"Print failed: {e}")
            return False
