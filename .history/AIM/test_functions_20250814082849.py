import requests
import time

def test_page_functions():
    print("Testing Calculator Reference functionality after fixes...")
    
    try:
        # Test page loading
        response = requests.get("http://localhost:5000/compare")
        if response.status_code == 200:
            print("✅ Compare page loads successfully")
            
            # Check for critical function definitions
            functions_to_check = [
                'window.setCalculator = setCalculator',
                'window.loadSourceData = loadSourceData', 
                'window.performComparison = performComparison'
            ]
            
            missing_functions = []
            for func in functions_to_check:
                if func in response.text:
                    print(f"✅ Found: {func}")
                else:
                    missing_functions.append(func)
                    print(f"❌ Missing: {func}")
            
            # Check for syntax errors indicators
            if '>>>' in response.text:
                print("❌ Found potential syntax error: '>>>' in HTML")
            else:
                print("✅ No '>>>' syntax errors found")
                
            # Check for dropdown structure
            if 'Available Calculators' in response.text:
                print("✅ Calculator dropdown header found")
            else:
                print("❌ Calculator dropdown header not found")
                
            if len(missing_functions) == 0:
                print("\n🎉 All critical functions are properly defined!")
                print("The 'function not available' errors should now be resolved.")
            else:
                print(f"\n❌ {len(missing_functions)} functions still missing")
                
        else:
            print(f"❌ Page failed to load: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing page: {e}")

if __name__ == "__main__":
    test_page_functions()
