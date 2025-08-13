import requests
import json

# Test the compare-data API endpoint
url = "http://localhost:5000/api/compare-data"
data = {
    "record_id": 1,
    "calculator_path": "/calculators/life_insurance/standard.json"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
