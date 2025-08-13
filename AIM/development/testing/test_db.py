import sqlite3
import os

# Test database connection
db_path = "aim_data.db"
print(f"Testing database: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

try:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        # Check user_data table schema
        cursor.execute("PRAGMA table_info(user_data)")
        columns = cursor.fetchall()
        print(f"user_data columns: {columns}")
        
        # Try the basic query that's failing
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        print(f"Total records: {count}")
        
except Exception as e:
    print(f"Database error: {e}")
    import traceback
    traceback.print_exc()
