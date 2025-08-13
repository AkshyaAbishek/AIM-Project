import requests
import json

def test_comparison_display():
    print("Testing comparison result display...")
    
    try:
        # First test that the page loads and has the results section
        response = requests.get("http://localhost:5000/compare")
        if response.status_code == 200:
            if 'id="comparisonResults"' in response.text:
                print("✅ Comparison results section found in HTML")
            else:
                print("❌ Comparison results section not found")
                
            if 'id="summaryStats"' in response.text:
                print("✅ Summary stats section found in HTML")
            else:
                print("❌ Summary stats section not found")
                
            if 'id="comparisonTableBody"' in response.text:
                print("✅ Comparison table body found in HTML")
            else:
                print("❌ Comparison table body not found")
        
        # Test the API directly
        print("\nTesting API response structure...")
        api_url = "http://localhost:5000/api/compare-data"
        api_data = {
            "record_id": 1,
            "calculator_path": "/calculators/life_insurance/standard.json"
        }
        
        api_response = requests.post(api_url, json=api_data)
        if api_response.status_code == 200:
            result = api_response.json()
            if result.get('success'):
                comparison = result.get('comparison', {})
                stats = comparison.get('stats', {})
                fields = comparison.get('fields', [])
                
                print(f"✅ API returns comparison data:")
                print(f"  - Total fields: {stats.get('total_fields', 0)}")
                print(f"  - Matching: {stats.get('matching_fields', 0)}")
                print(f"  - Missing: {stats.get('missing_fields', 0)}")
                print(f"  - Completion: {stats.get('completion_percentage', 0)}%")
                print(f"  - Field details: {len(fields)} fields")
                
                if len(fields) > 0:
                    print(f"  - Sample field: {fields[0].get('field_name')} = {fields[0].get('status')}")
                    
                print("\n✅ API structure is correct for display")
            else:
                print(f"❌ API error: {result.get('message')}")
        else:
            print(f"❌ API failed: {api_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_comparison_display()
