#!/usr/bin/env python3
"""
Test if the JavaScript functions are properly attached and accessible
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_javascript_functions():
    """Test if the import template functions are working in the browser"""
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:5000/field-mapping")
        
        # Wait for page to load
        WebDriverWait(driver, 10).wait(
            EC.presence_of_element_located((By.ID, "templateFileInput"))
        )
        
        # Test if functions are attached to window
        functions_to_test = [
            'triggerFileUpload',
            'handleFileUpload', 
            'handleJSONUpload',
            'handleExcelUpload',
            'loadTemplateData',
            'showAlert'
        ]
        
        print("Testing JavaScript functions:")
        for func_name in functions_to_test:
            try:
                result = driver.execute_script(f"return typeof window.{func_name}")
                print(f"  {func_name}: {result}")
                if result != 'function':
                    print(f"    ❌ {func_name} is not a function!")
                else:
                    print(f"    ✅ {func_name} is properly defined")
            except Exception as e:
                print(f"    ❌ Error testing {func_name}: {e}")
        
        # Test clicking the import button
        print("\nTesting Import Template button:")
        try:
            import_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Import Template')]")
            print("  ✅ Import Template button found")
            
            # Test if clicking triggers the function (should trigger file dialog)
            driver.execute_script("arguments[0].click();", import_button)
            print("  ✅ Button click executed without errors")
            
        except Exception as e:
            print(f"  ❌ Error with Import Template button: {e}")
            
        # Check for any JavaScript console errors
        print("\nChecking for JavaScript console errors:")
        logs = driver.get_log('browser')
        for log in logs:
            if log['level'] == 'SEVERE':
                print(f"  ❌ Error: {log['message']}")
            
        if not any(log['level'] == 'SEVERE' for log in logs):
            print("  ✅ No severe JavaScript errors found")
            
    except Exception as e:
        print(f"Error running browser test: {e}")
        print("Note: This test requires Chrome/Chromium and selenium. Install with: pip install selenium")
        
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    test_javascript_functions()
