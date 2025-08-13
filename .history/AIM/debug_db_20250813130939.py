#!/usr/bin/env python3
"""
Quick debug script to check what's in the database
"""
import sqlite3
import os
import json

# Get database path
db_path = os.path.join(os.path.dirname(__file__), 'aim_data.db')
print(f"Checking database: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    print(f"Database size: {os.path.getsize(db_path)} bytes")
    
    # Connect and check data
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\nTables found: {[t[0] for t in tables]}")
        
        # Check user_data table
        try:
            cursor.execute("SELECT COUNT(*) FROM user_data")
            count = cursor.fetchone()[0]
            print(f"\nTotal records in user_data: {count}")
            
            if count > 0:
                # Get sample records
                cursor.execute("""
                    SELECT id, name, product_type, created_date, validation_status, 
                           quality_score, file_source, session_id
                    FROM user_data ORDER BY created_date DESC LIMIT 5
                """)
                
                records = cursor.fetchall()
                print(f"\nSample records:")
                for i, record in enumerate(records, 1):
                    print(f"  {i}. ID={record['id']}, Name='{record['name']}', "
                          f"Product='{record['product_type']}', Session='{record['session_id']}', "
                          f"Status='{record['validation_status']}'")
            
        except Exception as e:
            print(f"Error checking user_data: {e}")
else:
    print("Database file does not exist!")
