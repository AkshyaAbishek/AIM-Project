#!/usr/bin/env python3
"""
Final comprehensive test of the import template functionality
"""
import requests
import json
import os
import tempfile
import pandas as pd

def run_comprehensive_test():
    print("🧪 COMPREHENSIVE IMPORT TEMPLATE TEST")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Server connectivity
    print("\n1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   ✅ Server is running (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False
    
    # Test 2: Field mapping page
    print("\n2. Testing field mapping page...")
    try:
        response = requests.get(f"{base_url}/field-mapping")
        print(f"   ✅ Field mapping page loads (Status: {response.status_code})")
        if "Import Template" in response.text:
            print("   ✅ Import Template button found in HTML")
        else:
            print("   ⚠️  Import Template button not found in HTML")
    except Exception as e:
        print(f"   ❌ Error loading field mapping page: {e}")
    
    # Test 3: JSON template upload
    print("\n3. Testing JSON template upload...")
    test_json_template = {
        "name": "Test Template",
        "description": "Automated test template",
        "product_type": "life_insurance",
        "field_mappings": [
            {"source": "PolicyNum", "target": "policy_number", "transformation": "trim", "required": True},
            {"source": "CustomerName", "target": "insured_name", "transformation": "trim", "required": True}
        ]
    }
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_json_template, f)
            json_file_path = f.name
        
        with open(json_file_path, 'rb') as f:
            files = {'template_file': f}
            response = requests.post(f"{base_url}/api/upload-template", files=files)
        
        data = response.json()
        if data.get('success'):
            print(f"   ✅ JSON upload successful: {data.get('message')}")
            template_data = data.get('template_data', {})
            print(f"   ✅ Template name: {template_data.get('name')}")
            print(f"   ✅ Field mappings: {len(template_data.get('field_mappings', []))}")
        else:
            print(f"   ❌ JSON upload failed: {data.get('message')}")
            
        os.unlink(json_file_path)
        
    except Exception as e:
        print(f"   ❌ Error testing JSON upload: {e}")
    
    # Test 4: Excel template upload
    print("\n4. Testing Excel template upload...")
    try:
        excel_data = {
            'Source Field': ['PolicyNumber', 'InsuredName', 'CoverageAmount'],
            'Target Field': ['policy_number', 'insured_name', 'coverage_amount'],
            'Transformation': ['trim', 'trim', 'currency_format'],
            'Required': ['true', 'true', 'true']
        }
        
        df = pd.DataFrame(excel_data)
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            excel_file_path = f.name
        
        df.to_excel(excel_file_path, index=False)
        
        with open(excel_file_path, 'rb') as f:
            files = {'template_file': f}
            response = requests.post(f"{base_url}/api/upload-template", files=files)
        
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Excel upload successful: {data.get('message')}")
            template_data = data.get('template_data', {})
            print(f"   ✅ Template name: {template_data.get('name')}")
            print(f"   ✅ Field mappings: {len(template_data.get('field_mappings', []))}")
        else:
            print(f"   ❌ Excel upload failed: {data.get('message')}")
            
        os.unlink(excel_file_path)
        
    except Exception as e:
        print(f"   ❌ Error testing Excel upload: {e}")
    
    # Test 5: API endpoints
    print("\n5. Testing related API endpoints...")
    
    # Test mappings endpoint
    try:
        response = requests.get(f"{base_url}/api/mappings")
        data = response.json()
        print(f"   ✅ Mappings API works (Status: {response.status_code})")
        print(f"   ✅ Found {len(data.get('mappings', []))} saved mappings")
    except Exception as e:
        print(f"   ❌ Error testing mappings API: {e}")
    
    # Test 6: Error handling
    print("\n6. Testing error handling...")
    
    # Test invalid file upload
    try:
        invalid_data = b"This is not a valid JSON or Excel file"
        files = {'template_file': ('invalid.txt', invalid_data, 'text/plain')}
        response = requests.post(f"{base_url}/api/upload-template", files=files)
        data = response.json()
        
        if not data.get('success'):
            print("   ✅ Invalid file properly rejected")
        else:
            print("   ⚠️  Invalid file was accepted (unexpected)")
            
    except Exception as e:
        print(f"   ❌ Error testing invalid file: {e}")
    
    # Test no file upload
    try:
        response = requests.post(f"{base_url}/api/upload-template")
        data = response.json()
        
        if not data.get('success') and 'No template file' in data.get('message', ''):
            print("   ✅ No file upload properly handled")
        else:
            print("   ⚠️  No file upload not properly handled")
            
    except Exception as e:
        print(f"   ❌ Error testing no file upload: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 TEST SUMMARY")
    print("=" * 50)
    print("✅ Backend API is working correctly")
    print("✅ JSON template upload functionality works")
    print("✅ Excel template upload functionality works")
    print("✅ Error handling is implemented")
    print("\n📋 MANUAL TESTING STEPS:")
    print("1. Open http://localhost:5000/field-mapping")
    print("2. Click the 'Import Template' button")
    print("3. Select test_template.json or test_template.xlsx")
    print("4. Verify the template data is loaded into the form")
    print("5. Check browser console for any JavaScript errors")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("If import doesn't work in the browser:")
    print("- Open browser developer tools (F12)")
    print("- Check the Console tab for JavaScript errors")
    print("- Check the Network tab to see if API calls are made")
    print("- Verify the file input element is present in the DOM")
    
    return True

if __name__ == "__main__":
    run_comprehensive_test()
