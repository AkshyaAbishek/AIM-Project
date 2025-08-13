#!/usr/bin/env python3
"""
Test script to verify AIM configuration after reorganization
"""

import os
import sys
from pathlib import Path

def test_configuration():
    """Test that all paths and configurations are working correctly"""
    print("🧪 Testing AIM Configuration")
    print("=" * 50)
    
    # Test project root
    project_root = Path(__file__).parent
    print(f"📁 Project root: {project_root}")
    
    # Test directory structure
    directories = [
        'runtime/uploads',
        'runtime/exports', 
        'runtime/logs',
        'database',
        'src',
        'static',
        'templates'
    ]
    
    print("\n📂 Directory structure:")
    for directory in directories:
        dir_path = project_root / directory
        status = "✓" if dir_path.exists() else "❌"
        print(f"  {status} {directory}")
    
    # Test database
    db_path = project_root / 'database' / 'aim_data.db'
    print(f"\n💾 Database:")
    print(f"  Path: {db_path}")
    print(f"  Exists: {'✓' if db_path.exists() else '❌'}")
    
    # Test web_app import
    print(f"\n🌐 Web Application:")
    try:
        sys.path.insert(0, str(project_root))
        import web_app
        print(f"  Import: ✓")
        print(f"  Upload folder: {web_app.app.config.get('UPLOAD_FOLDER')}")
        print(f"  Export folder: {web_app.app.config.get('EXPORT_FOLDER')}")
        print(f"  Database path: {web_app.app.config.get('DATABASE_PATH')}")
    except Exception as e:
        print(f"  Import: ❌ {e}")
    
    print(f"\n🎯 Configuration test complete!")

if __name__ == '__main__':
    test_configuration()
