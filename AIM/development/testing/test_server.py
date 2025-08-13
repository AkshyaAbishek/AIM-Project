#!/usr/bin/env python3
"""
Simple test to start Flask server and test routes
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from web_app import app, db_manager

if __name__ == '__main__':
    print("=== TESTING DATABASE BEFORE STARTING SERVER ===")
    
    # Test database directly
    try:
        test_data = db_manager.get_all_data()
        print(f"Database test: Found {len(test_data)} records")
        if test_data:
            print("Sample record:", dict(test_data[0]))
    except Exception as e:
        print(f"Database test failed: {e}")
    
    print("=== STARTING FLASK SERVER ===")
    print("Navigate to:")
    print("- http://localhost:5000/view-data (to see records)")
    print("- http://localhost:5000/compare (to test compare page)")  
    print("- http://localhost:5000/debug/database (to see debug info)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
