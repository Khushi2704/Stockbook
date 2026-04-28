# Stockbook Medical Store Management System

A production-ready desktop application for managing medical store (pharmacy) operations. Designed for simplicity, speed, and reliability.

## Features

### Core Features
- **Fast Billing**: Complete sales transactions in 2-3 seconds
- **Inventory Management**: Track medicines with batch numbers and expiry dates
- **Stock Tracking**: Real-time stock level monitoring
- **Sales Reports**: Daily, weekly, monthly, and custom range reports
- **Profit Analysis**: Track profit margins and business performance
- **Alert System**: Automatic alerts for low stock and expiring medicines
- **Backup & Restore**: Automatic and manual data backup functionality
- **User Authentication**: Secure login system

### Key Screens
1. **Login**: Secure user authentication
2. **Dashboard**: Quick overview of sales, profit, and alerts
3. **Billing**: Fast and intuitive sales interface
4. **Inventory**: Manage medicines and stock
5. **Reports**: Comprehensive business analytics
6. **Settings**: System configuration

## Installation

### Requirements
- Python 3.7 or higher
- Windows 7 or higher

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Application
```bash
python main.py
```

### Step 3: First Login
- Username: `admin`
- Password: `admin123`

## Building Executable

To convert to standalone .exe file:

```bash
python build.py
```

This will create a single executable file in the `dist/` folder.

## Project Structure

```
medical_store_app/
├── main.py                  # Application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── build.py               # Build script for PyInstaller
│
├── database/
│   ├── db.py              # Database connection
│   └── migrations.py       # Database schema
│
├── models/
│   ├── medicine.py        # Medicine data model
│   ├── sales.py           # Sales transactions
│   ├── purchase.py        # Purchase records
│   └── user.py            # User authentication
│
├── services/
│   ├── billing_service.py     # Billing logic
│   ├── inventory_service.py   # Inventory management
│   └── report_service.py      # Reporting
│
├── ui/
│   ├── login.py           # Login screen
│   ├── dashboard.py       # Main dashboard
│   ├── billing.py         # Billing interface
│   ├── add_medicine.py    # Add medicine dialog
│   ├── purchase.py        # Stock management
│   └── reports.py         # Reports viewer
│
├── utils/
│   ├── helpers.py         # Utility functions
│   ├── validators.py      # Input validation
│   └── printer.py         # Bill generation
│
├── backups/               # Database backups
└── assets/               # Application resources
```

## Database Design

### medicines table
- id: Primary key
- name: Medicine name
- batch: Batch number
- expiry_date: Expiry date
- mrp: Maximum Retail Price
- net_price: Cost price
- stock: Current stock quantity

### sales table
- id: Primary key
- medicine_id: Foreign key to medicines
- quantity: Units sold
- unit_price: Selling price per unit
- total_price: Total transaction amount
- profit: Profit from transaction
- date: Transaction timestamp

### purchases table
- id: Primary key
- medicine_id: Foreign key to medicines
- quantity_added: Units added to stock
- supplier: Supplier name
- date: Purchase date

### users table
- id: Primary key
- username: Login username
- password: Hashed password
- created_at: Account creation date

## Business Logic

### Profit Calculation
```
Profit per unit = MRP - Net Price
Total profit = Profit per unit × Quantity
```

### Stock Management
- Deduct from stock when selling
- Add to stock when purchasing
- Alert when stock < 10 units (configurable)

### Billing Workflow
1. Search for medicine by name or batch
2. Select quantity and price
3. Add to bill
4. Review total and profit
5. Finalize sale
6. Generate and print invoice

## Configuration

Edit `config.py` to customize:
- `LOW_STOCK_THRESHOLD`: Minimum stock level before alert (default: 10)
- `EXPIRY_ALERT_DAYS`: Days before expiry to alert (default: 30)
- `WINDOW_WIDTH` / `WINDOW_HEIGHT`: Application window size
- `SUBSCRIPTION_PRICE`: Subscription fee in rupees
- `TRIAL_DAYS`: Free trial period in days

## Data Storage

Data is stored in SQLite database at:
- Windows: `C:\Users\[Username]\.stockbook\database.db`

Backups are stored at:
- Windows: `C:\Users\[Username]\.stockbook\backups\`

## Security

- Passwords are hashed using PBKDF2-SHA256 with salt
- Database access is thread-safe
- Data backup prevents data loss

## Performance

- Billing operations: < 3 seconds
- Search results: Instant
- Stock updates: Real-time
- Database: Indexed for fast queries

## User Credentials

### Default Login
- Username: `admin`
- Password: `admin123`

*Note: Change these credentials after first login in production*

## Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed
- Check if PyQt5 is installed: `pip install PyQt5`
- Check database file permissions

### Database errors
- Delete `.stockbook` folder from home directory to reset
- Restart application

### Search not working
- Ensure medicine names are entered correctly
- Check if medicines exist in inventory

## Support Features

### Backup & Restore
- Automatic daily backups
- Manual backup anytime
- One-click restore functionality

### Data Integrity
- Transaction logging
- Stock reconciliation
- Error prevention

### Reports
- Daily sales summary
- Monthly profit analysis
- Top-selling medicines
- Custom date ranges

## Future Enhancements

- Multi-location support
- GST calculations
- Stock transfer between locations
- Supplier management
- Digital receipts (SMS/Email)
- Cloud backup
- Mobile app integration

## Technical Stack

- **Frontend**: PyQt5 (GUI)
- **Database**: SQLite3
- **Language**: Python 3.7+
- **Packaging**: PyInstaller
- **OS**: Windows

## License

This software is provided as-is for authorized users only.

## Support

For support, contact your service provider.

---

**Version**: 1.0.0
**Release Date**: 2026-04-25
**Status**: Production Ready
