"""
Billing service - Core business logic for sales transactions
"""
from models.medicine import Medicine
from models.sales import Sales
from utils.helpers import calculate_profit
from utils.validators import Validator
from datetime import datetime


class BillingService:
    """Handle billing operations"""
    
    def __init__(self, user_id=1):
        self.bill_items = []
        self.user_id = user_id
    
    def add_item_to_bill(self, medicine_id, quantity, unit_price):
        """Add item to bill"""
        # Validate medicine exists
        medicine = Medicine.get_by_id(medicine_id, self.user_id)
        if not medicine:
            return False, "Medicine not found"
        
        # Validate stock
        valid, msg = Validator.validate_stock_available(medicine['stock'], quantity)
        if not valid:
            return False, msg
        
        # Calculate amount and profit
        amount = quantity * unit_price
        profit = calculate_profit(unit_price, medicine['net_price'], quantity)
        
        # Add to bill
        self.bill_items.append({
            'medicine_id': medicine_id,
            'medicine_name': medicine['name'],
            'batch': medicine['batch'],
            'quantity': quantity,
            'unit_price': unit_price,
            'amount': amount,
            'profit': profit,
            'expiry_date': medicine['expiry_date']
        })
        
        return True, "Item added successfully"
    
    def remove_item_from_bill(self, index):
        """Remove item from bill"""
        if 0 <= index < len(self.bill_items):
            self.bill_items.pop(index)
            return True
        return False
    
    def get_bill_items(self):
        """Get all items in bill"""
        return self.bill_items
    
    def get_bill_total(self):
        """Get total bill amount"""
        return sum(item['amount'] for item in self.bill_items)
    
    def get_bill_profit(self):
        """Get total profit"""
        return sum(item['profit'] for item in self.bill_items)
    
    def clear_bill(self):
        """Clear all items from bill"""
        self.bill_items = []
    
    def finalize_sale(self):
        """
        Finalize the sale:
        1. Deduct stock from medicines
        2. Create sales records
        3. Return transaction details
        """
        if not self.bill_items:
            return False, "Bill is empty", None
        
        try:
            sale_records = []
            
            for item in self.bill_items:
                # Deduct stock
                Medicine.update_stock(item['medicine_id'], -item['quantity'])
                
                # Record sale with user_id
                sale_id = Sales.create(
                    medicine_id=item['medicine_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['amount'],
                    profit=item['profit'],
                    user_id=self.user_id
                )
                
                sale_records.append({
                    'sale_id': sale_id,
                    'medicine_id': item['medicine_id'],
                    'medicine_name': item['medicine_name'],
                    'quantity': item['quantity'],
                    'amount': item['amount'],
                    'profit': item['profit']
                })
            
            total = self.get_bill_total()
            total_profit = self.get_bill_profit()
            
            # Clear bill after successful sale
            self.clear_bill()
            
            return True, "Sale completed successfully", {
                'sale_records': sale_records,
                'total_amount': total,
                'total_profit': total_profit,
                'timestamp': datetime.now()
            }
        
        except Exception as e:
            return False, f"Error finalizing sale: {str(e)}", None
    
    def get_bill_summary(self):
        """Get bill summary"""
        return {
            'item_count': len(self.bill_items),
            'total_amount': self.get_bill_total(),
            'total_profit': self.get_bill_profit(),
            'items': self.bill_items
        }
