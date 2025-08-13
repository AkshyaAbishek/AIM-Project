#!/usr/bin/env python3
"""
Script to restore the AIM database with original schema and sample data
"""

import sqlite3
import json
import hashlib
from datetime import datetime

def restore_database():
    """Restore the database with correct schema and sample data"""
    try:
        with sqlite3.connect('aim_data.db') as conn:
            cursor = conn.cursor()
            
            # Drop existing table
            cursor.execute("DROP TABLE IF EXISTS user_data")
            
            # Create table with original schema
            cursor.execute("""
                CREATE TABLE user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    product_type TEXT NOT NULL,
                    data_hash TEXT UNIQUE NOT NULL,
                    json_data TEXT NOT NULL,
                    validation_status TEXT DEFAULT 'pending',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    quality_score REAL DEFAULT 0,
                    session_id TEXT,
                    calculator_path TEXT,
                    raw_data TEXT,
                    processed_data TEXT,
                    field_mappings TEXT,
                    status TEXT,
                    file_source TEXT,
                    processing_notes TEXT,
                    notes TEXT,
                    source_record_id TEXT
                )
            """)
            
            # Sample life insurance policies
            policies = [
                {
                    "name": "Sample Life Policy 1",
                    "product_type": "life",
                    "data": {
                        "policy_number": "LP001",
                        "insured_name": "John Smith",
                        "face_amount": 250000,
                        "premium": 1200,
                        "issue_date": "2024-01-15"
                    }
                },
                {
                    "name": "Premium Life Policy",
                    "product_type": "life",
                    "data": {
                        "policy_number": "LP002",
                        "insured_name": "Sarah Johnson",
                        "face_amount": 500000,
                        "premium": 2400,
                        "issue_date": "2024-02-01"
                    }
                }
            ]
            
            # Sample annuity contracts
            annuities = [
                {
                    "name": "Retirement Annuity 1",
                    "product_type": "annuity",
                    "data": {
                        "contract_number": "AN001",
                        "owner_name": "Robert Wilson",
                        "premium": 100000,
                        "interest_rate": 0.035,
                        "issue_date": "2024-01-20"
                    }
                },
                {
                    "name": "Investment Annuity",
                    "product_type": "annuity",
                    "data": {
                        "contract_number": "AN002",
                        "owner_name": "Mary Brown",
                        "premium": 150000,
                        "interest_rate": 0.04,
                        "issue_date": "2024-02-15"
                    }
                }
            ]
            
            # Add more sample records
            additional_records = []
            for i in range(1, 10):  # This will add 9 more records
                record = {
                    "name": f"Test Record {i}",
                    "product_type": "life" if i % 2 == 0 else "annuity",
                    "data": {
                        "number": f"TEST{i:03d}",
                        "amount": 100000 + (i * 10000),
                        "date": "2024-03-01"
                    }
                }
                additional_records.append(record)
            
            # Combine all records
            all_records = policies + annuities + additional_records
            
            # Insert all records
            for record in all_records:
                json_str = json.dumps(record['data'], sort_keys=True)
                data_hash = hashlib.md5(json_str.encode()).hexdigest()
                
                cursor.execute("""
                    INSERT INTO user_data 
                    (name, product_type, data_hash, json_data, validation_status, 
                     created_date, quality_score, session_id, calculator_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    record['name'],
                    record['product_type'],
                    data_hash,
                    json_str,
                    'validated',
                    datetime.now().isoformat(),
                    95.0,
                    datetime.now().strftime('%Y%m%d_%H%M%S'),
                    f"/calculators/{record['product_type']}/standard.json"
                ))
            
            conn.commit()
            
            # Verify the records
            cursor.execute("SELECT COUNT(*) FROM user_data")
            count = cursor.fetchone()[0]
            print(f"\nRestored {count} records to the database")
            
            # Show sample of restored records
            cursor.execute("""
                SELECT id, name, product_type, validation_status 
                FROM user_data 
                ORDER BY id
            """)
            print("\nSample of restored records:")
            for row in cursor.fetchall():
                print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}, Status: {row[3]}")
                
    except Exception as e:
        print(f"Error restoring database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Restoring AIM database with original schema and sample data...")
    restore_database()
    print("\nDatabase restoration completed!")
