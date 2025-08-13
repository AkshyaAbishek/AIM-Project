import requests
from bs4 import BeautifulSoup

def test_calculator_dropdown():
    try:
        response = requests.get("http://localhost:5000/compare")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for the calculator dropdown
            dropdown = soup.find('ul', class_='dropdown-menu')
            if dropdown:
                print("✅ Found calculator dropdown menu")
                
                # Look for calculator items
                calculator_items = dropdown.find_all('li')
                print(f"Found {len(calculator_items)} dropdown items:")
                
                for item in calculator_items:
                    link = item.find('a')
                    if link and 'setCalculator' in str(link):
                        print(f"  - Calculator: {link.get_text(strip=True)}")
                    elif item.find('h6'):
                        print(f"  - Header: {item.get_text(strip=True)}")
                
                if len(calculator_items) <= 1:  # Only header, no calculators
                    print("❌ No calculator items found in dropdown")
                    print("This suggests available_calculators is empty")
                else:
                    print("✅ Calculator items found in dropdown")
            else:
                print("❌ Calculator dropdown menu not found")
                
            # Check for JavaScript functions
            if 'window.setCalculator' in response.text:
                print("✅ setCalculator function found in page")
            else:
                print("❌ setCalculator function not found in page")
                
            if 'window.performComparison' in response.text:
                print("✅ performComparison function found in page")
            else:
                print("❌ performComparison function not found in page")
                
        else:
            print(f"❌ Failed to load page: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_calculator_dropdown()
