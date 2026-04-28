"""
Setup Guide for Stockbook Medical Store Application
"""

SETUP_GUIDE = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                    STOCKBOOK SETUP & QUICK START GUIDE                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

📋 TABLE OF CONTENTS
==================
1. Installation
2. First Login
3. Adding Medicines
4. Processing Sales
5. Viewing Reports
6. Backup & Restore
7. Troubleshooting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ INSTALLATION
================

Option A: From Python Source
─────────────────────────────
1. Ensure Python 3.7+ is installed
2. Open Command Prompt in the Stockbook folder
3. Run: pip install -r requirements.txt
4. Run: python main.py

Option B: Using Executable
──────────────────────────
1. Download Stockbook.exe
2. Double-click to run
3. No installation required

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ FIRST LOGIN
===============

Default Credentials (CHANGE THESE!):
────────────────────────────────────
Username: admin
Password: admin123

Steps:
1. Enter username: admin
2. Enter password: admin123
3. Click Login
4. You'll see the Dashboard

⚠️ IMPORTANT: Change password after first login!
Go to Settings → Change Password

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣ ADDING MEDICINES
====================

Steps:
1. Click "➕ Add Medicine" button on Dashboard
2. Fill in the details:
   - Medicine Name: e.g., "Aspirin 500mg"
   - Batch Number: e.g., "ASP001234"
   - Expiry Date: Format YYYY-MM-DD (e.g., 2026-12-31)
   - MRP: Maximum Retail Price (e.g., 50.00)
   - Net Price: Your cost price (e.g., 30.00)
   - Initial Stock: Number of units (e.g., 100)
3. Click "Add Medicine"
4. You'll see confirmation message

💡 Tips:
- MRP must be greater than Net Price
- Expiry date must be in future
- Use consistent batch numbering
- Add sufficient stock initially

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4️⃣ PROCESSING SALES (BILLING)
================================

Steps:
1. Click "💳 Billing" button on Dashboard
2. In the Search box, type medicine name or batch number
3. Select from dropdown
4. Enter quantity needed
5. Price is auto-filled from MRP
6. Click "Add to Bill"
7. Repeat for more items
8. Click "Finalize Sale" to complete

Bill Display:
──────────
- Shows all items added
- Total amount calculated
- Profit shown separately
- Remove items if needed

Finalizing Sale:
───────────────
1. Review bill items and total
2. Click "Finalize Sale"
3. Choose payment method
4. Click "Print Bill"
5. Stock is automatically updated

💡 Tips:
- Search is case-insensitive
- Can adjust quantities before sale
- Remove items by clicking "Remove"
- Bills print to text format

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5️⃣ VIEWING REPORTS
====================

Report Types:
────────────
- Today's Sales
- Last 7 Days
- Last 30 Days
- Monthly Report
- Top Selling Medicines
- Profit Analysis
- Business Summary
- Custom Date Range

Steps:
1. Click "📊 Reports" button
2. Select report type from dropdown
3. Click "Load Report"
4. Data displays in table
5. Click "Export to CSV" to download
6. Click "Print" to print report

Summary Information:
───────────────────
- Total Sales Amount
- Profit Earned
- Number of Transactions
- Top-selling medicines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6️⃣ BACKUP & RESTORE
====================

Automatic Backup:
─────────────────
- System creates daily backups
- Stored in: C:\\Users\\[Your Name]\\.stockbook\\backups\\

Manual Backup:
──────────────
1. Click "🔄 Backup/Restore" on Dashboard
2. Click "Create Backup"
3. Confirm location
4. Done!

Restore from Backup:
───────────────────
1. Click "🔄 Backup/Restore"
2. Click "Restore"
3. Select backup file
4. Confirm restore
5. Application restarts with restored data

⚠️ WARNING: Restore will overwrite current data!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7️⃣ TROUBLESHOOTING
===================

Problem: "Database Error" on startup
───────────────────────────────────
Solution:
1. Navigate to: C:\\Users\\[Your Name]\\.stockbook\\
2. Delete the "database.db" file
3. Restart application (database recreates)

Problem: Slow search or billing
────────────────────────────────
Solution:
1. Close other applications
2. Restart Stockbook
3. Check internet connection (if cloud features used)

Problem: Can't find medicine in search
──────────────────────────────────────
Solution:
1. Check medicine name spelling
2. Search by batch number
3. Click "📦 Inventory" to see all medicines
4. Add medicine if not found

Problem: Stock not updating correctly
──────────────────────────────────────
Solution:
1. Check if sale was "Finalized"
2. Review sales history in reports
3. Manually adjust stock in Inventory

Problem: Lost data
──────────────────
Solution:
1. Check backup folder: C:\\Users\\[Your Name]\\.stockbook\\backups\\
2. Use "🔄 Backup/Restore" to restore

Need help?
──────────
- Check README.md for technical details
- Contact support with error message
- Include database.log file if available

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 KEY METRICS TO TRACK
=======================

Daily:
- Total Sales Amount
- Total Profit
- Number of Transactions
- Top-selling medicine

Monthly:
- Total Revenue
- Total Profit
- Profit Margin %
- Average transaction value

Inventory:
- Low stock items
- Expiring medicines
- Stock value

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 SUCCESS CHECKLIST
====================

□ Application installed and running
□ Can login with admin credentials
□ Added at least 5 medicines
□ Processed at least one sale
□ Generated bill receipt
□ Viewed sales report
□ Created backup
□ Changed admin password
□ Trained staff on basic operations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Version: 1.0.0
Last Updated: 2026-04-25
Status: Production Ready

╔═══════════════════════════════════════════════════════════════════════════╗
║                   Thank you for using Stockbook!                          ║
║              Making pharmacy management simple and efficient              ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(SETUP_GUIDE)
    
    # Save to file
    with open("SETUP_GUIDE.txt", "w", encoding="utf-8") as f:
        f.write(SETUP_GUIDE)
    
    print("\n\n✓ Setup guide saved to SETUP_GUIDE.txt")
