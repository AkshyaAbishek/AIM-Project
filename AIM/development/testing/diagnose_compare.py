#!/usr/bin/env python3
"""Quick diagnostic to check if compare page should show data"""

import sqlite3
import json

try:
    # Check database directly using the same query as the compare route
    conn = sqlite3.connect('aim_data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Use the exact same query as in web_app.py
    cursor.execute("""
        SELECT id, name, product_type, created_date, calculator_path, json_data
        FROM user_data 
        ORDER BY created_date DESC
        LIMIT 50
    """)
    
    processed_records = [dict(row) for row in cursor.fetchall()]
    
    print(f"Found {len(processed_records)} records for compare page")
    
    if processed_records:
        print("\nRecords that should appear in dropdown:")
        for record in processed_records:
            print(f"- ID: {record['id']}, Name: {record['name']}, Product: {record['product_type']}")
    else:
        print("No records found - this explains why dropdown is empty")
        
        # Check if table exists and has any data at all
        cursor.execute("SELECT COUNT(*) FROM user_data")
        total_count = cursor.fetchone()[0]
        print(f"Total records in user_data table: {total_count}")
        
        if total_count == 0:
            print("Database is empty - need to add sample data")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    print("This suggests database connection or table structure issue")
