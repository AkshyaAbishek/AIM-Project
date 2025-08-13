#!/usr/bin/env python3
"""
Quick script to check database content and add test data if needed
"""

import sqlite3
import json
import hashlib
from datetime import datetime

def check_database():
    """Check what's in the database"""
    try:
        with sqlite3.connect('aim_data.db') as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            # Check table structure
            cursor.execute("PRAGMA table_info(user_data)")
            columns = cursor.fetchall()
            print("Database columns:")
            for col in columns:
                print(f"  {col['name']} ({col['type']})")
            
            # Check existing records
            cursor.execute("SELECT COUNT(*) as count FROM user_data")
            count = cursor.fetchone()['count']
            print(f"\nTotal records: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, name, validation_status, product_type FROM user_data LIMIT 5")
                records = cursor.fetchall()
                print("\nSample records:")
                for record in records:
                    print(f"  ID: {record['id']}, Name: {record['name']}, Status: {record['validation_status']}, Type: {record['product_type']}")
            
            return count
    except Exception as e:
        print(f"Error checking database: {e}")
        return 0

def add_test_data():
    """Add some test data for testing process functionality"""
    try:
        # Sample test data
        test_data = {
            "policy_details": {
                "policy_number": "TEST001",
                "issue_date": "2024-01-01",
                "face_amount": 100000
            },
            "insured_info": {
                "age": 35,
                "gender": "M",
                "smoking_status": "N"
            }
        }
        
        json_data = json.dumps(test_data)
        data_hash = hashlib.md5(json_data.encode()).hexdigest()
        
        with sqlite3.connect('aim_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO user_data 
                (name, product_type, data_hash, json_data, validation_status) 
                VALUES (?, ?, ?, ?, ?)
            """, ("Test Life Insurance", "life", data_hash, json_data, "validated"))
            
            # Add annuity test data
            annuity_data = {
                "policy_details": {
                    "contract_number": "ANN001",
                    "issue_date": "2024-01-01",
                    "premium": 50000
                },
                "annuitant_info": {
                    "age": 45,
                    "gender": "F"
                }
            }
            
            annuity_json = json.dumps(annuity_data)
            annuity_hash = hashlib.md5(annuity_json.encode()).hexdigest()
            
            cursor.execute("""
                INSERT OR IGNORE INTO user_data 
                (name, product_type, data_hash, json_data, validation_status) 
                VALUES (?, ?, ?, ?, ?)
            """, ("Test Annuity", "annuity", annuity_hash, annuity_json, "validated"))
            
            conn.commit()
            print("Added test data successfully")
            
    except Exception as e:
        print(f"Error adding test data: {e}")

if __name__ == "__main__":
    print("Checking AIM database...")
    count = check_database()
    
    if count == 0:
        print("\nNo records found. Adding test data...")
        add_test_data()
        print("\nRechecking database after adding test data...")
        check_database()
    else:
        print(f"\nDatabase contains {count} records - ready for testing!")
