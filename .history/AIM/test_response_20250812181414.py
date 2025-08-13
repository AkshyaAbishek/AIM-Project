import requests
import time

print("Testing AIM web application...")

try:
    response = requests.get("http://localhost:5000")
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.content)}")
    print(f"Content Type: {response.headers.get('content-type')}")
    print("\nFirst 500 characters of content:")
    print(response.text[:500])
    print("\nLast 200 characters of content:")
    print(response.text[-200:])
    
except Exception as e:
    print(f"Error: {e}")
