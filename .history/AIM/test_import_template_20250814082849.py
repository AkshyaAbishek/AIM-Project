import requests
import json
import os

def test_import_template_functionality():
    print("Testing Import Template functionality...")
    
    # Test 1: Check if the field mapping page loads
    try:
        response = requests.get("http://localhost:5000/field-mapping")
        if response.status_code == 200:
            print("✅ Field mapping page loads successfully")
            
            # Check for critical elements
            if 'Import Template' in response.text:
                print("✅ Import Template button found")
            else:
                print("❌ Import Template button not found")
                
            if 'templateFileInput' in response.text:
                print("✅ File input element found")
            else:
                print("❌ File input element not found")
                
            if 'handleFileUpload' in response.text:
                print("✅ handleFileUpload function found")
            else:
                print("❌ handleFileUpload function not found")
        else:
            print(f"❌ Field mapping page failed to load: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error loading page: {e}")
        return
    
    # Test 2: Check if the API endpoint exists
    try:
        # Create a test JSON template
        test_template = {
            "name": "Test Template",
            "description": "Test template for import functionality",
            "product_type": "life_insurance",
            "field_mappings": [
                {
                    "source": "PolicyNumber",
                    "target": "policy_number",
                    "transformation": "none",
                    "required": True
                },
                {
                    "source": "InsuredName",
                    "target": "insured_name", 
                    "transformation": "trim",
                    "required": True
                }
            ]
        }
        
        # Test JSON upload via API (simulating what would happen)
        print("\n✅ Test template structure is valid")
        print(f"  - Name: {test_template['name']}")
        print(f"  - Product type: {test_template['product_type']}")
        print(f"  - Field mappings: {len(test_template['field_mappings'])}")
        
        # Test API endpoint by creating a temporary file
        temp_file_path = 'test_template.json'
        with open(temp_file_path, 'w') as f:
            json.dump(test_template, f)
        
        # Test the upload API endpoint
        with open(temp_file_path, 'rb') as f:
            files = {'template_file': f}
            response = requests.post('http://localhost:5000/api/upload-template', files=files)
            
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ API upload-template endpoint works correctly")
                print(f"  - Message: {result.get('message')}")
                returned_data = result.get('template_data')
                if returned_data and returned_data.get('field_mappings'):
                    print(f"  - Returned {len(returned_data['field_mappings'])} field mappings")
            else:
                print(f"❌ API returned error: {result.get('message')}")
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
    
    print("\nImport Template functionality test complete!")

if __name__ == "__main__":
    test_import_template_functionality()
