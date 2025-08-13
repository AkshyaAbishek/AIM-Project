import requests
import json

# Test that the compare page loads without errors
def test_compare_page():
    try:
        response = requests.get("http://localhost:5000/compare")
        print(f"Compare page status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Compare page loads successfully")
            # Check if page contains the dropdown
            if 'available_calculators' in response.text:
                print("✅ Available calculators are being passed to template")
            else:
                print("❌ Available calculators not found in template")
                
            # Check if JavaScript functions are included
            if 'setCalculator' in response.text and 'performComparison' in response.text:
                print("✅ JavaScript functions are included in page")
            else:
                print("❌ JavaScript functions missing from page")
        else:
            print(f"❌ Compare page failed to load: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing compare page: {e}")

# Test the comparison API
def test_comparison_api():
    try:
        url = "http://localhost:5000/api/compare-data"
        data = {
            "record_id": 1,
            "calculator_path": "/calculators/life_insurance/standard.json"
        }
        response = requests.post(url, json=data)
        print(f"API status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Comparison API works successfully")
                print(f"  - Total fields: {result['comparison']['stats']['total_fields']}")
                print(f"  - Matching fields: {result['comparison']['stats']['matching_fields']}")
            else:
                print(f"❌ API returned error: {result.get('message')}")
        else:
            print(f"❌ API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    print("Testing Calculator Reference functionality...")
    print("\n1. Testing compare page loading:")
    test_compare_page()
    print("\n2. Testing comparison API:")
    test_comparison_api()
    print("\nTest complete!")
