#!/usr/bin/env python3
"""Add test data and check if it appears in compare page"""

import sqlite3
import json
from datetime import datetime

def add_and_process_test_data():
    try:
        conn = sqlite3.connect('aim_data.db')
        cursor = conn.cursor()
        
        # Add test data with 'validated' status (like upload page does)
        test_data = {
            "policy_number": "COMPARE001",
            "applicant_first_name": "Alice",
            "applicant_last_name": "Compare",
            "birth_date": "1990-01-01",
            "effective_date": "2025-01-01",
            "face_amount": 200000,
            "premium": 2400,
            "gender": "F",
            "product_code": "WHOLE"
        }
        
        cursor.execute("""
            INSERT INTO user_data 
            (name, product_type, json_data, calculator_path, created_date, validation_status, quality_score, session_id, file_source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Compare Test Policy",
            "life_insurance",
            json.dumps(test_data),
            "/calculators/life_insurance/standard.json",
            datetime.now().isoformat(),
            "validated",
            90.0,
            "test_compare_session",
            "manual_test"
        ))
        
        record_id = cursor.lastrowid
        print(f"Added test record with ID: {record_id}")
        
        # Now update it to 'processed' status (like process_data route does)
        cursor.execute("""
            UPDATE user_data 
            SET validation_status = 'processed'
            WHERE id = ?
        """, (record_id,))
        
        conn.commit()
        
        # Check what records exist and their statuses
        cursor.execute("""
            SELECT id, name, product_type, validation_status, created_date
            FROM user_data 
            ORDER BY created_date DESC
        """)
        
        records = cursor.fetchall()
        print(f"\nAll records in database:")
        for record in records:
            print(f"  ID: {record[0]}, Name: {record[1]}, Product: {record[2]}, Status: {record[3]}")
        
        # Check what the compare page query would return
        cursor.execute("""
            SELECT id, name, product_type, created_date, calculator_path, json_data
            FROM user_data 
            ORDER BY created_date DESC
            LIMIT 50
        """)
        
        compare_records = cursor.fetchall()
        print(f"\nRecords that should appear in compare dropdown: {len(compare_records)}")
        for record in compare_records:
            print(f"  ID: {record[0]}, Name: {record[1]}, Product: {record[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_and_process_test_data()
