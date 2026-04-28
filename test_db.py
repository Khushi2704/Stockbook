import traceback
try:
    from database.db import init_database
    from database.upgrade import upgrade_to_multitenancy
    init_database()
    upgrade_to_multitenancy()
    print("Success")
except Exception as e:
    traceback.print_exc()
