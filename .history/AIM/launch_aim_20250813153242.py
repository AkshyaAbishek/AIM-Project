#!/usr/bin/env python3
"""
AIM Application Launcher
Updated for new organized project structure
"""

import os
import sys
import subprocess
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

def setup_python_path():
    """Add necessary paths to Python path for imports"""
    # Add src directory to path
    src_path = PROJECT_ROOT / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    # Add common directory to path
    common_path = PROJECT_ROOT / 'common'
    if str(common_path) not in sys.path:
        sys.path.insert(0, str(common_path))
    
    # Add core directory to path
    core_path = PROJECT_ROOT / 'core'
    if str(core_path) not in sys.path:
        sys.path.insert(0, str(core_path))

def ensure_directories():
    """Ensure all necessary runtime directories exist"""
    directories = [
        PROJECT_ROOT / 'runtime' / 'uploads',
        PROJECT_ROOT / 'runtime' / 'exports', 
        PROJECT_ROOT / 'runtime' / 'logs',
        PROJECT_ROOT / 'runtime' / 'temp_uploads',
        PROJECT_ROOT / 'runtime' / 'saved_mappings',
        PROJECT_ROOT / 'database'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Ensured directory: {directory}")

def check_database():
    """Check if database exists and copy if needed"""
    db_path = PROJECT_ROOT / 'database' / 'aim_data.db'
    
    # If database doesn't exist in new location, try to copy from old location
    if not db_path.exists():
        old_db_path = PROJECT_ROOT / 'aim_data.db'
        if old_db_path.exists():
            import shutil
            shutil.copy2(old_db_path, db_path)
            print(f"✓ Copied database to new location: {db_path}")
        else:
            print(f"ℹ Database will be created at: {db_path}")
    else:
        print(f"✓ Database found at: {db_path}")

def main():
    """Main launcher function"""
    print("🚀 AIM Application Launcher")
    print("=" * 50)
    
    # Setup environment
    setup_python_path()
    ensure_directories()
    check_database()
    
    # Change to web app directory
    web_app_dir = PROJECT_ROOT / 'core' / 'web'
    os.chdir(web_app_dir)
    
    print(f"📂 Working directory: {web_app_dir}")
    print("🌐 Starting AIM Web Application...")
    print("=" * 50)
    
    # Set environment variables for the new structure
    os.environ['AIM_PROJECT_ROOT'] = str(PROJECT_ROOT)
    os.environ['AIM_DATABASE_PATH'] = str(PROJECT_ROOT / 'database' / 'aim_data.db')
    os.environ['AIM_UPLOAD_PATH'] = str(PROJECT_ROOT / 'runtime' / 'uploads')
    os.environ['AIM_EXPORT_PATH'] = str(PROJECT_ROOT / 'runtime' / 'exports')
    
    # Launch the web application
    try:
        # Try to import and run the web app
        sys.path.insert(0, str(web_app_dir))
        
        # Run the Flask application
        subprocess.run([sys.executable, 'web_app.py'], cwd=web_app_dir)
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
