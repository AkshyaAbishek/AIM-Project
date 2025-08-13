#!/usr/bin/env python
import os
import sys

# Change to the correct directory
os.chdir(r'C:\Users\2013041\VibeCode\AIM')
print(f"Current directory: {os.getcwd()}")

# Import and run the web app
try:
    from web_app import app
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
except Exception as e:
    print(f"Error starting app: {e}")
    import traceback
    traceback.print_exc()
