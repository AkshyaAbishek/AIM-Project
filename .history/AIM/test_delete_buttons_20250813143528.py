#!/usr/bin/env python3
"""
Test the delete button functionality after importing a template
"""
import requests
import json
import tempfile
import os

def test_delete_functionality():
    print("🧪 Testing Delete Button Functionality")
    print("=" * 40)
    
    # Test that the import works first
    test_template = {
        "name": "Delete Test Template",
        "description": "Testing delete functionality",
        "product_type": "life_insurance",
        "field_mappings": [
            {"source": "Field1", "target": "policy_number", "transformation": "trim", "required": True},
            {"source": "Field2", "target": "insured_name", "transformation": "trim", "required": True},
            {"source": "Field3", "target": "coverage_amount", "transformation": "currency_format", "required": False}
        ]
    }
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_template, f)
            json_file_path = f.name
        
        # Test upload
        with open(json_file_path, 'rb') as f:
            files = {'template_file': f}
            response = requests.post('http://localhost:5000/api/upload-template', files=files)
        
        data = response.json()
        if data.get('success'):
            print("✅ Template upload successful")
            print(f"   Template contains {len(data.get('template_data', {}).get('field_mappings', []))} field mappings")
            print("\n📋 Manual Test Steps:")
            print("1. Go to http://localhost:5000/field-mapping")
            print("2. Import the test template using the Import Template button")
            print("3. Verify that 3 rows are added to the mapping table")
            print("4. Click the delete button (trash icon) on any row")
            print("5. Verify that the row is removed")
            print("6. Try to delete when only one row remains - should show alert")
            
            print("\n🔧 Expected Behavior:")
            print("- Delete buttons should work on all imported rows")
            print("- At least one row must remain (protection)")
            print("- No JavaScript errors in browser console")
            
        else:
            print("❌ Template upload failed:", data.get('message'))
            
        os.unlink(json_file_path)
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    
    print("\n🔍 If delete buttons still don't work:")
    print("- Open browser developer tools (F12)")
    print("- Check Console tab for JavaScript errors")
    print("- Verify event delegation is working")
    print("- Check if .delete-row-btn class is present on buttons")

if __name__ == "__main__":
    test_delete_functionality()
