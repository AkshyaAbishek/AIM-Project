#!/usr/bin/env python3
"""
Local Testing Script for AIM Web Application
Run this script to test your web application locally before deploying to Azure
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major != 3 or version.minor < 8:
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'web_app.py',
        'startup.py',
        'requirements-web.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/upload.html',
        'templates/process_results.html',
        'templates/field_mapping.html',
        'templates/view_data.html',
        'templates/error.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("\n✅ All required files present")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements-web.txt'
        ], check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e.stderr}")
        return False

def start_development_server():
    """Start the Flask development server"""
    print("\n🚀 Starting development server...")
    
    # Set environment variables for development
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = 'True'
    os.environ['SECRET_KEY'] = 'development-secret-key'
    
    try:
        # Start the server in a subprocess
        process = subprocess.Popen([
            sys.executable, 'web_app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if server is running
        if process.poll() is None:
            print("✅ Development server started successfully")
            print("🌐 Application running at: http://localhost:5000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_application():
    """Test basic application functionality"""
    print("\n🧪 Testing application...")
    
    base_url = "http://localhost:5000"
    
    # Test routes
    test_cases = [
        {"url": f"{base_url}/", "name": "Homepage"},
        {"url": f"{base_url}/upload", "name": "Upload page"},
        {"url": f"{base_url}/field-mapping", "name": "Field mapping page"},
        {"url": f"{base_url}/view-data", "name": "View data page"}
    ]
    
    results = []
    for test in test_cases:
        try:
            response = requests.get(test["url"], timeout=5)
            if response.status_code == 200:
                print(f"✅ {test['name']}: OK")
                results.append(True)
            else:
                print(f"❌ {test['name']}: HTTP {response.status_code}")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {test['name']}: {e}")
            results.append(False)
    
    return all(results)

def create_sample_data():
    """Create sample data for testing"""
    print("\n📝 Creating sample data...")
    
    sample_data = {
        "policy_number": "POL-2024-001",
        "insured_name": "John Doe",
        "birth_date": "1985-01-15",
        "gender": "M",
        "coverage_amount": 100000,
        "premium_amount": 1200,
        "effective_date": "2024-01-01",
        "product_code": "LIFE_TERM"
    }
    
    # Create uploads directory if it doesn't exist
    uploads_dir = Path('uploads')
    uploads_dir.mkdir(exist_ok=True)
    
    # Save sample JSON file
    import json
    sample_file = uploads_dir / 'sample_data.json'
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✅ Sample data created: {sample_file}")
    return True

def run_pre_deployment_tests():
    """Run comprehensive pre-deployment tests"""
    print("🔍 AIM Web Application - Pre-Deployment Testing")
    print("=" * 50)
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Check required files
    if not check_required_files():
        return False
    
    # Step 3: Install dependencies
    if not install_dependencies():
        return False
    
    # Step 4: Create sample data
    create_sample_data()
    
    # Step 5: Start development server
    server_process = start_development_server()
    if not server_process:
        return False
    
    try:
        # Step 6: Test application
        if test_application():
            print("\n✅ All tests passed! Application is ready for deployment.")
            
            print("\n📋 Deployment Checklist:")
            print("1. ✅ Python version compatible")
            print("2. ✅ All required files present")
            print("3. ✅ Dependencies installed")
            print("4. ✅ Application starts successfully")
            print("5. ✅ All routes accessible")
            
            print("\n🚀 Ready to deploy to Azure!")
            print("Run: ./deploy-to-azure.ps1 (Windows) or ./deploy-to-azure.sh (Linux/Mac)")
            
            return True
        else:
            print("\n❌ Some tests failed. Please fix issues before deployment.")
            return False
            
    finally:
        # Stop the development server
        if server_process:
            server_process.terminate()
            server_process.wait()
            print("\n🛑 Development server stopped")

def main():
    """Main function"""
    try:
        success = run_pre_deployment_tests()
        
        if success:
            print("\n🎉 Pre-deployment testing completed successfully!")
            
            # Ask user if they want to continue with deployment
            response = input("\nDo you want to proceed with Azure deployment? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                print("\n🚀 Starting Azure deployment...")
                if os.name == 'nt':  # Windows
                    subprocess.run(['powershell', '-File', 'deploy-to-azure.ps1'])
                else:  # Linux/Mac
                    subprocess.run(['bash', 'deploy-to-azure.sh'])
            else:
                print("\n👍 You can run the deployment later using:")
                print("   Windows: .\\deploy-to-azure.ps1")
                print("   Linux/Mac: ./deploy-to-azure.sh")
        else:
            print("\n💡 Please fix the issues above and run this script again.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
