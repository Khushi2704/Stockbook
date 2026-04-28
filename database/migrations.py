"""
Database migrations and schema
"""
from database.db import execute_query, fetch_one


def create_tables():
    """Create all required tables"""
    
    # Users table
    execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add is_active column if it doesn't exist (for existing databases)
    try:
        execute_query("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")
    except:
        pass  # Column already exists
    
    # Medicines table
    execute_query("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            name TEXT NOT NULL,
            batch TEXT NOT NULL,
            expiry_date DATE NOT NULL,
            mrp REAL NOT NULL,
            net_price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, name, batch, expiry_date),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Add user_id column if it doesn't exist
    try:
        execute_query("ALTER TABLE medicines ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
    except:
        pass
    
    # Sales table
    execute_query("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            medicine_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            profit REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medicine_id) REFERENCES medicines(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Add user_id column if it doesn't exist
    try:
        execute_query("ALTER TABLE sales ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
    except:
        pass
    
    # Purchases table
    execute_query("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            medicine_id INTEGER NOT NULL,
            quantity_added INTEGER NOT NULL,
            supplier TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medicine_id) REFERENCES medicines(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Add user_id column if it doesn't exist
    try:
        execute_query("ALTER TABLE purchases ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
    except:
        pass
    
    # Create indexes for performance
    execute_query("CREATE INDEX IF NOT EXISTS idx_medicines_user ON medicines(user_id)")
    execute_query("CREATE INDEX IF NOT EXISTS idx_medicines_user_name ON medicines(user_id, name)")
    execute_query("CREATE INDEX IF NOT EXISTS idx_medicines_expiry ON medicines(user_id, expiry_date)")
    execute_query("CREATE INDEX IF NOT EXISTS idx_sales_user ON sales(user_id)")
    execute_query("CREATE INDEX IF NOT EXISTS idx_sales_user_date ON sales(user_id, date)")
    execute_query("CREATE INDEX IF NOT EXISTS idx_purchases_user ON purchases(user_id)")
    execute_query("CREATE INDEX IF NOT EXISTS idx_purchases_user_date ON purchases(user_id, date)")
    
    # Create default user if not exists
    user_exists = fetch_one("SELECT id FROM users WHERE username = ?", ("admin",))
    if not user_exists:
        from utils.helpers import hash_password
        hashed_pwd = hash_password("Kritagya")
        execute_query(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hashed_pwd)
        )
    else:
        # Update admin password to new one
        from utils.helpers import hash_password
        hashed_pwd = hash_password("Kritagya")
        execute_query(
            "UPDATE users SET password = ? WHERE username = ? AND id = 1",
            (hashed_pwd, "admin")
        )
    
    print("Database initialized successfully")
