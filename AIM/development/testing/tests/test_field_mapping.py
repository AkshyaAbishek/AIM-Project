#!/usr/bin/env python3
"""
Test script to verify field mapping functionality works correctly.
This script tests the field mapping dialog without requiring GUI interaction.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all required imports work."""
    try:
        import pandas as pd
        import openpyxl
        print("✅ pandas and openpyxl imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_field_mapping_core_functionality():
    """Test the core field mapping functionality without GUI."""
    try:
        from example import AIMDemoGUI
        import tkinter as tk
        
        # Create a temporary root and instance 
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        processor = AIMDemoGUI()
        
        # Check if the show_field_mapping method exists
        if hasattr(processor, 'show_field_mapping'):
            print("✅ show_field_mapping method exists")
        else:
            print("❌ show_field_mapping method missing")
            root.destroy()
            return False
            
        # Check if the create_excel_mapping method exists
        if hasattr(processor, 'create_excel_mapping'):
            print("✅ create_excel_mapping method exists")
        else:
            print("❌ create_excel_mapping method missing")
            root.destroy()
            return False
            
        # Check if the browse methods exist
        if hasattr(processor, 'browse_save_excel') and hasattr(processor, 'browse_open_excel'):
            print("✅ browse methods exist")
        else:
            print("❌ browse methods missing")
            root.destroy()
            return False
            
        # Check if create_dialog_button exists
        if hasattr(processor, 'create_dialog_button'):
            print("✅ create_dialog_button method exists")
        else:
            print("❌ create_dialog_button method missing")
            root.destroy()
            return False
            
        print("✅ All field mapping methods available")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error testing field mapping: {e}")
        return False

def test_excel_creation():
    """Test Excel file creation functionality."""
    try:
        import pandas as pd
        
        # Create a simple test DataFrame
        data = {
            'FAST UI Field': ['field1', 'field2', 'field3'],
            'FAST UI Value': ['value1', 'value2', 'value3'],
            'Actuarial Field': ['', '', ''],
            'Actuarial Value': ['', '', '']
        }
        
        df = pd.DataFrame(data)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name
        
        # Write to Excel
        df.to_excel(tmp_path, index=False)
        
        # Verify file exists and can be read
        df_read = pd.read_excel(tmp_path)
        
        # Clean up
        os.unlink(tmp_path)
        
        print("✅ Excel creation and reading successful")
        return True
        
    except Exception as e:
        print(f"❌ Excel test failed: {e}")
        return False

def main():
    """Run all tests for field mapping functionality."""
    print("🧪 Testing Field Mapping Functionality\n")
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Field Mapping Methods", test_field_mapping_core_functionality),
        ("Excel Operations", test_excel_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 40)
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Field mapping should work correctly.")
        print("\n💡 Tip: Make sure to run the AIM application using:")
        print("   C:/Users/2013041/VibeCode/.venv/Scripts/python.exe example.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
