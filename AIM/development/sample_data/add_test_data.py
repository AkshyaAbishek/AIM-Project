#!/usr/bin/env python3
"""Add sample data for testing the compare page"""

import sqlite3
import json
from datetime import datetime

def add_sample_data():
    try:
        conn = sqlite3.connect('aim_data.db')
        cursor = conn.cursor()
        
        # Sample life insurance data
        sample_life_data = {
            "policy_number": "LIFE001234",
            "applicant_first_name": "John",
            "applicant_last_name": "Doe",
            "birth_date": "1980-01-01",
            "effective_date": "2025-01-01",
            "face_amount": 100000,
            "premium": 1200,
            "gender": "M",
            "product_code": "TERM20"
        }
        
        # Sample annuity data
        sample_annuity_data = {
            "contract_number": "ANN001234",
            "owner_first_name": "Jane",
            "owner_last_name": "Smith",
            "birth_date": "1970-01-01",
            "effective_date": "2025-01-01",
            "initial_deposit": 50000,
            "product_code": "FIXED5",
            "interest_rate": 3.5
        }
        
        # Insert sample records
        cursor.execute("""
            INSERT INTO user_data 
            (name, product_type, json_data, calculator_path, created_date, validation_status, quality_score, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Sample Life Insurance Policy",
            "life_insurance",
            json.dumps(sample_life_data),
            "/calculators/life_insurance/standard.json",
            datetime.now().isoformat(),
            "processed",
            85.5,
            "test_session_1"
        ))
        
        cursor.execute("""
            INSERT INTO user_data 
            (name, product_type, json_data, calculator_path, created_date, validation_status, quality_score, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Sample Annuity Contract",
            "annuity",
            json.dumps(sample_annuity_data),
            "/calculators/annuity/fixed.json",
            datetime.now().isoformat(),
            "processed",
            92.0,
            "test_session_2"
        ))
        
        # Add a partial data record for testing missing values
        partial_life_data = {
            "policy_number": "LIFE005678",
            "applicant_first_name": "Bob",
            "applicant_last_name": "Johnson",
            "birth_date": "1985-05-15",
            "face_amount": 250000,
            "gender": "M"
            # Missing effective_date, premium, product_code
        }
        
        cursor.execute("""
            INSERT INTO user_data 
            (name, product_type, json_data, calculator_path, created_date, validation_status, quality_score, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Partial Life Insurance Data",
            "life_insurance",
            json.dumps(partial_life_data),
            "/calculators/life_insurance/term.json",
            datetime.now().isoformat(),
            "processed",
            65.0,
            "test_session_3"
        ))
        
        conn.commit()
        conn.close()
        
        print("Sample data added successfully!")
        print("Added 3 test records:")
        print("1. Sample Life Insurance Policy (complete data)")
        print("2. Sample Annuity Contract (complete data)")
        print("3. Partial Life Insurance Data (missing some fields)")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")

if __name__ == "__main__":
    add_sample_data()
