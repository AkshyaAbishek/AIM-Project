#!/usr/bin/env python3
"""
Restore sample data to the AIM database
"""

import sqlite3
import json
import hashlib
from datetime import datetime

def restore_sample_data():
    """Restore sample data for testing"""
    try:
        # Sample life insurance data
        life_data = {
            "policy_number": "LIFE123456",
            "applicant_first_name": "John",
            "applicant_last_name": "Doe",
            "birth_date": "1985-03-15",
            "effective_date": "2024-01-01",
            "face_amount": 250000,
            "premium_frequency": "monthly",
            "risk_class": "standard_plus",
            "state_issued": "NY",
            "agent_code": "AGT001",
            "premium_mode": "annual",
            "policy_type": "term_life"
        }
        
        # Sample annuity data
        annuity_data = {
            "contract_number": "ANN789012",
            "owner_first_name": "Jane",
            "owner_last_name": "Smith", 
            "birth_date": "1970-08-12",
            "effective_date": "2024-06-01",
            "initial_premium": 75000,
            "guaranteed_rate": 0.035,
            "surrender_period": 7,
            "state_issued": "FL",
            "agent_code": "AGT002",
            "annuity_type": "fixed_deferred"
        }
        
        # Another life insurance record
        life_data2 = {
            "policy_number": "LIFE789012",
            "applicant_first_name": "Michael",
            "applicant_last_name": "Johnson",
            "birth_date": "1978-11-22",
            "effective_date": "2024-03-15",
            "face_amount": 500000,
            "premium_frequency": "quarterly",
            "risk_class": "standard",
            "state_issued": "CA",
            "agent_code": "AGT003",
            "premium_mode": "quarterly",
            "policy_type": "whole_life"
        }
        
        records = [
            ("Sample Life Insurance Policy", "life", life_data, "validated"),
            ("Sample Annuity Contract", "annuity", annuity_data, "processed"),
            ("Premium Life Policy", "life", life_data2, "validated")
        ]
        
        with sqlite3.connect('aim_data.db') as conn:
            cursor = conn.cursor()
            
            for name, product_type, data, status in records:
                json_str = json.dumps(data, sort_keys=True)
                data_hash = hashlib.md5(json_str.encode()).hexdigest()
                
                # Check if record already exists
                cursor.execute("SELECT id FROM user_data WHERE data_hash = ?", (data_hash,))
                if cursor.fetchone():
                    print(f"Record '{name}' already exists, skipping...")
                    continue
                
                cursor.execute("""
                    INSERT INTO user_data 
                    (name, product_type, data_hash, json_data, validation_status, 
                     created_date, quality_score, session_id, file_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, product_type, data_hash, json_str, status,
                    datetime.now().isoformat(), 95.0, 
                    datetime.now().strftime('%Y%m%d_%H%M%S'), "restored_sample"
                ))
                
                print(f"Added record: {name}")
            
            conn.commit()
            
            # Check final count
            cursor.execute("SELECT COUNT(*) FROM user_data")
            count = cursor.fetchone()[0]
            print(f"\nTotal records in database: {count}")
            
            # Show sample records
            cursor.execute("SELECT id, name, validation_status, product_type FROM user_data ORDER BY id")
            records = cursor.fetchall()
            print("\nAll records:")
            for record in records:
                print(f"  ID: {record[0]}, Name: {record[1]}, Status: {record[2]}, Type: {record[3]}")
                
    except Exception as e:
        print(f"Error restoring data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Restoring sample data to AIM database...")
    restore_sample_data()
    print("Data restoration completed!")
