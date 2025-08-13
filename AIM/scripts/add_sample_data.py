#!/usr/bin/env python3
"""
Add sample data to test the View Data functionality
"""

import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta
import hashlib

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Sample data
sample_records = [
    {
        "name": "John Doe Life Policy",
        "product_type": "life",
        "json_data": {
            "policy_number": "LI-2025-001",
            "insured_name": "John Doe",
            "birth_date": "1985-03-15",
            "gender": "M",
            "coverage_amount": 250000,
            "premium_amount": 1500,
            "effective_date": "2025-01-01",
            "product_code": "TERM_20"
        },
        "quality_score": 95.5,
        "file_source": "Excel Import"
    },
    {
        "name": "Jane Smith Annuity",
        "product_type": "annuity", 
        "json_data": {
            "contract_number": "ANN-2025-001",
            "annuitant_name": "Jane Smith",
            "birth_date": "1970-07-22",
            "gender": "F",
            "initial_premium": 100000,
            "annuity_type": "Fixed",
            "interest_rate": 3.5,
            "start_date": "2025-01-01"
        },
        "quality_score": 88.2,
        "file_source": "JSON Upload"
    },
    {
        "name": "Robert Johnson Policy",
        "product_type": "life",
        "json_data": {
            "policy_number": "LI-2025-002", 
            "insured_name": "Robert Johnson",
            "birth_date": "1992-11-08",
            "gender": "M",
            "coverage_amount": 500000,
            "premium_amount": 2800,
            "effective_date": "2025-02-01",
            "product_code": "WHOLE_LIFE"
        },
        "quality_score": 72.3,
        "file_source": "Manual Entry"
    },
    {
        "name": "Emily Davis Annuity Plan",
        "product_type": "annuity",
        "json_data": {
            "contract_number": "ANN-2025-002",
            "annuitant_name": "Emily Davis", 
            "birth_date": "1965-12-03",
            "gender": "F",
            "initial_premium": 75000,
            "annuity_type": "Variable",
            "start_date": "2025-03-01"
        },
        "quality_score": 91.7,
        "file_source": "CSV Import"
    }
]

def add_sample_data():
    """Add sample data to the database"""
    db_path = "aim_data.db"
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        print("Adding sample data...")
        
        for i, record in enumerate(sample_records):
            # Create data hash
            data_str = json.dumps(record["json_data"], sort_keys=True)
            data_hash = hashlib.md5(data_str.encode()).hexdigest()
            
            # Calculate created date (spread over last few days)
            created_date = (datetime.now() - timedelta(days=i)).isoformat()
            
            cursor.execute("""
                INSERT OR IGNORE INTO user_data 
                (name, product_type, data_hash, json_data, created_date, 
                 validation_status, quality_score, file_source, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record["name"],
                record["product_type"], 
                data_hash,
                json.dumps(record["json_data"]),
                created_date,
                'processed',
                record["quality_score"],
                record["file_source"],
                'sample_session'
            ))
            
            print(f"✅ Added: {record['name']}")
        
        conn.commit()
        print(f"\n🎉 Successfully added {len(sample_records)} sample records!")

if __name__ == "__main__":
    add_sample_data()
