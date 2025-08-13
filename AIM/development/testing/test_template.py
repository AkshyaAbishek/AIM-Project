import requests
import json

# Test creating a sample Life Insurance template
url = "http://localhost:5000/api/save-mapping"

sample_life_template = {
    "name": "Test Life Insurance Template",
    "product_type": "life_insurance",
    "description": "Test template for life insurance mappings",
    "mappings": [
        {
            "source": "PolicyNumber",
            "target": "policy_number",
            "transformation": "trim",
            "required": True
        },
        {
            "source": "InsuredName",
            "target": "insured_name",
            "transformation": "trim",
            "required": True
        },
        {
            "source": "CoverageAmount",
            "target": "coverage_amount",
            "transformation": "currency_format",
            "required": True
        }
    ]
}

try:
    response = requests.post(url, json=sample_life_template)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test listing mappings
    list_url = "http://localhost:5000/api/mappings"
    list_response = requests.get(list_url)
    print(f"\nList Mappings Status: {list_response.status_code}")
    print(f"List Response: {list_response.json()}")
    
except Exception as e:
    print(f"Error: {e}")
