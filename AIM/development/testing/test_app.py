#!/usr/bin/env python3
print("Starting AIM Web Application Test...")

try:
    from flask import Flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import error: {e}")

try:
    import pandas as pd
    print("✓ Pandas imported successfully")
except ImportError as e:
    print(f"✗ Pandas import error: {e}")

try:
    import sqlite3
    print("✓ SQLite3 imported successfully")
except ImportError as e:
    print(f"✗ SQLite3 import error: {e}")

print("Test completed.")

# Try to create a simple Flask app
try:
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Hello from AIM!"
    
    print("✓ Flask app created successfully")
    print("Starting server on http://localhost:5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except Exception as e:
    print(f"✗ Error running Flask app: {e}")
    import traceback
    traceback.print_exc()
