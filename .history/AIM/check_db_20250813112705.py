#!/usr/bin/env python3
"""Quick script to check database contents"""

import sqlite3
import json

def check_database():
    try:
        conn = sqlite3.connect('aim_data.db')
        cursor = conn.cursor()
        
        # Get table schema
        cursor.execute("PRAGMA table_info(user_data)")
        columns = cursor.fetchall()
        print("Database columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get all records
        cursor.execute("SELECT id, name, product_type, validation_status FROM user_data")
        records = cursor.fetchall()
        
        print(f"\nTotal records: {len(records)}")
        
        if records:
            print("\nRecords:")
            for record in records[:10]:  # Show first 10 records
                print(f"  ID: {record[0]}, Name: {record[1]}, Product: {record[2]}, Status: {record[3]}")
        else:
            print("No records found")
            
        # Check if there are any processed records
        cursor.execute("""
            SELECT id, name, product_type, validation_status
            FROM user_data 
            WHERE validation_status IN ('processed', 'saved') OR validation_status = 'processed'
        """)
        processed_records = cursor.fetchall()
        print(f"\nProcessed records: {len(processed_records)}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_database()
