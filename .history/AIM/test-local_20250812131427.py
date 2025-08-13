#!/usr/bin/env python3
"""
Simple Local Test for AIM Web Application
Test the web application locally before Azure deployment
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    print("🧪 AIM Web Application - Local Test")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('web_app.py').exists():
        print("❌ web_app.py not found. Please run this from the AIM directory.")
        return False
    
    print("✅ Files found")
    print("🚀 Starting Flask development server...")
    
    # Set environment variables for development
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = 'True'
    
    try:
        # Start the Flask app
        print("📍 Open your browser to: http://localhost:5000")
        print("📍 Press Ctrl+C to stop the server")
        print("-" * 40)
        
        # Run the Flask app directly
        subprocess.run([sys.executable, 'web_app.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Local testing completed!")
        print("\n🚀 Ready for Azure deployment!")
        print("Run: .\\deploy-to-azure.ps1")
    else:
        print("\n❌ Please fix issues before deployment.")
