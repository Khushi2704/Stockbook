"""
Testing script - Verify core functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database.db import init_database
from models.user import User
from models.medicine import Medicine
from models.sales import Sales
from services.billing_service import BillingService
from services.inventory_service import InventoryService
from services.report_service import ReportService
from datetime import datetime, timedelta


def test_database():
    """Test database initialization"""
    print("\n" + "="*60)
    print("TEST: Database Initialization")
    print("="*60)
    try:
        init_database()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False


def test_user_authentication():
    """Test user authentication"""
    print("\n" + "="*60)
    print("TEST: User Authentication")
    print("="*60)
    try:
        # Test authentication
        user = User.authenticate("admin", "admin123")
        if user:
            print("✓ User authentication successful")
            print(f"  User ID: {user['id']}")
            print(f"  Username: {user['username']}")
            return True
        else:
            print("✗ Authentication failed")
            return False
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        return False


def test_medicine_operations():
    """Test medicine operations"""
    print("\n" + "="*60)
    print("TEST: Medicine Operations")
    print("="*60)
    try:
        # Add medicine
        medicine_id = Medicine.create(
            name="Test Medicine",
            batch="BATCH001",
            expiry_date="2026-12-31",
            mrp=100.0,
            net_price=60.0,
            stock=100
        )
        print(f"✓ Medicine created: ID={medicine_id}")
        
        # Get medicine
        medicine = Medicine.get_by_id(medicine_id)
        print(f"✓ Medicine retrieved: {medicine['name']}")
        
        # Update stock
        Medicine.update_stock(medicine_id, -10)
        updated = Medicine.get_by_id(medicine_id)
        print(f"✓ Stock updated: {updated['stock']} units")
        
        return True
    except Exception as e:
        print(f"✗ Medicine operations failed: {e}")
        return False


def test_billing():
    """Test billing operations"""
    print("\n" + "="*60)
    print("TEST: Billing Operations")
    print("="*60)
    try:
        # Create billing service
        billing = BillingService()
        
        # Add test medicine
        medicine_id = Medicine.create(
            name="Aspirin",
            batch="ASP001",
            expiry_date="2026-12-31",
            mrp=50.0,
            net_price=30.0,
            stock=200
        )
        
        # Add to bill
        success, msg = billing.add_item_to_bill(medicine_id, 2, 50.0)
        print(f"✓ Added item to bill: {msg}")
        
        # Check bill
        total = billing.get_bill_total()
        profit = billing.get_bill_profit()
        print(f"✓ Bill total: ₹{total}, Profit: ₹{profit}")
        
        # Finalize sale
        success, msg, transaction = billing.finalize_sale()
        if success:
            print(f"✓ Sale finalized: {msg}")
            print(f"  Transaction ID: {len(transaction['sale_records'])} items")
            return True
        else:
            print(f"✗ Finalize sale failed: {msg}")
            return False
    
    except Exception as e:
        print(f"✗ Billing test failed: {e}")
        return False


def test_inventory():
    """Test inventory operations"""
    print("\n" + "="*60)
    print("TEST: Inventory Operations")
    print("="*60)
    try:
        # Get all medicines
        medicines = InventoryService.get_all_medicines()
        print(f"✓ Retrieved medicines: {len(medicines)} items")
        
        # Get alerts
        alerts = InventoryService.check_alerts()
        print(f"✓ Low stock items: {len(alerts['low_stock'])}")
        print(f"✓ Expiring items: {len(alerts['expiring'])}")
        
        # Get summary
        summary = InventoryService.get_inventory_summary()
        print(f"✓ Total medicines: {summary['total_medicines']}")
        print(f"✓ Total stock: {summary['total_stock_units']} units")
        
        return True
    except Exception as e:
        print(f"✗ Inventory test failed: {e}")
        return False


def test_reports():
    """Test reporting"""
    print("\n" + "="*60)
    print("TEST: Reporting")
    print("="*60)
    try:
        # Get today's sales
        today = ReportService.get_today_sales()
        print(f"✓ Today's sales: ₹{today['total_amount']}")
        print(f"  Profit: ₹{today['total_profit']}")
        print(f"  Transactions: {today['transaction_count']}")
        
        # Get top medicines
        top = ReportService.get_top_medicines(5)
        print(f"✓ Top medicines retrieved: {len(top)} items")
        
        return True
    except Exception as e:
        print(f"✗ Report test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# STOCKBOOK APPLICATION TEST SUITE")
    print("#"*60)
    
    tests = [
        ("Database", test_database),
        ("User Authentication", test_user_authentication),
        ("Medicine Operations", test_medicine_operations),
        ("Billing", test_billing),
        ("Inventory", test_inventory),
        ("Reports", test_reports),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("="*60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Application is ready.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
