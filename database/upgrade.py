"""
Database upgrade script for multi-tenancy support
"""
from database.db import execute_query, fetch_all

def upgrade_to_multitenancy():
    """Upgrade existing database to support multi-tenant architecture"""
    print("Upgrading database for multi-tenancy...")
    
    try:
        # Check if user_id already exists in medicines, if not add it
        medicines = fetch_all("PRAGMA table_info(medicines)")
        medicine_columns = [col[1] for col in medicines]
        
        if 'user_id' not in medicine_columns:
            print("Adding user_id to medicines table...")
            execute_query("ALTER TABLE medicines ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
        
        # Check sales table
        sales = fetch_all("PRAGMA table_info(sales)")
        sales_columns = [col[1] for col in sales]
        
        if 'user_id' not in sales_columns:
            print("Adding user_id to sales table...")
            execute_query("ALTER TABLE sales ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
        
        # Check purchases table
        purchases = fetch_all("PRAGMA table_info(purchases)")
        purchase_columns = [col[1] for col in purchases]
        
        if 'user_id' not in purchase_columns:
            print("Adding user_id to purchases table...")
            execute_query("ALTER TABLE purchases ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
        
        # Create indexes if not exist
        execute_query("CREATE INDEX IF NOT EXISTS idx_medicines_user ON medicines(user_id)")
        execute_query("CREATE INDEX IF NOT EXISTS idx_sales_user ON sales(user_id)")
        execute_query("CREATE INDEX IF NOT EXISTS idx_purchases_user ON purchases(user_id)")
        
        print("Database upgrade complete!")
        return True
    except Exception as e:
        print(f"Error during upgrade: {e}")
        return False

if __name__ == "__main__":
    upgrade_to_multitenancy()
