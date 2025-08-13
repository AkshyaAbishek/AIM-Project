#!/usr/bin/env python3
"""
Simple test to verify the import template functionality is working
"""
import requests
import os

def test_import_template():
    print("Testing Import Template Functionality")
    print("=====================================")
    
    # Test 1: Check if the field mapping page loads
    try:
        response = requests.get('http://localhost:5000/field-mapping')
        print(f"✅ Field mapping page loads: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Field mapping page failed to load: {e}")
        return False
    
    # Test 2: Test JSON upload
    json_file_path = os.path.join(os.path.dirname(__file__), 'test_template.json')
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'rb') as f:
                files = {'template_file': f}
                response = requests.post('http://localhost:5000/api/upload-template', files=files)
            
            data = response.json()
            if data.get('success'):
                print(f"✅ JSON template upload works: {data.get('message')}")
                print(f"   Template name: {data.get('template_data', {}).get('name')}")
                print(f"   Field mappings: {len(data.get('template_data', {}).get('field_mappings', []))}")
            else:
                print(f"❌ JSON template upload failed: {data.get('message')}")
                
        except Exception as e:
            print(f"❌ Error testing JSON upload: {e}")
    else:
        print(f"❌ Test template file not found: {json_file_path}")
    
    # Test 3: Test API endpoints
    try:
        # Test mappings endpoint
        response = requests.get('http://localhost:5000/api/mappings')
        print(f"✅ Mappings API endpoint works: Status {response.status_code}")
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
    
    print("\nManual Test Instructions:")
    print("1. Open http://localhost:5000/field-mapping in your browser")
    print("2. Open browser developer tools (F12)")
    print("3. Check the Console tab for any error messages")
    print("4. Click the 'Import Template' button")
    print("5. Select the test_template.json file")
    print("6. Verify that the template is loaded correctly")
    
    return True

if __name__ == "__main__":
    test_import_template()
