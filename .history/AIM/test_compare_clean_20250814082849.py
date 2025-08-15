#!/usr/bin/env python3
"""
Test to verify that debug messages have been removed from the compare page
"""
import requests
from bs4 import BeautifulSoup

def test_compare_page_clean():
    print("🧪 Testing Compare Page - Debug Messages Removal")
    print("=" * 55)
    
    try:
        # Get the compare page
        response = requests.get('http://localhost:5000/compare')
        print(f"✅ Compare page loads: Status {response.status_code}")
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # List of debug messages that should NOT be present
        debug_messages_to_check = [
            "✅ SUCCESS: Found",
            "records for dropdown",
            "Debug Information",
            "Found.*processed records for dropdown",
            "Available Calculators:",
            "Records found:",
            "Calculators available:",
            "Database path:"
        ]
        
        # Check for presence of debug messages
        page_text = response.text.lower()
        found_debug_messages = []
        
        for message in debug_messages_to_check:
            if message.lower() in page_text:
                found_debug_messages.append(message)
        
        # Check for specific alert boxes that should be removed
        alert_boxes = soup.find_all('div', class_=['alert-success', 'alert-info', 'alert-secondary'])
        debug_alerts = []
        
        for alert in alert_boxes:
            alert_text = alert.get_text()
            if any(keyword in alert_text.lower() for keyword in ['debug', 'found', 'records for dropdown', 'available calculators']):
                debug_alerts.append(alert_text.strip())
        
        # Report results
        if not found_debug_messages and not debug_alerts:
            print("✅ SUCCESS: All debug messages have been removed!")
            print("✅ The compare page is now clean and user-friendly")
        else:
            print("❌ Some debug messages are still present:")
            for msg in found_debug_messages:
                print(f"   - Found: {msg}")
            for alert in debug_alerts:
                print(f"   - Alert box: {alert[:100]}...")
        
        # Check that the page still has the essential elements
        essential_elements = [
            'Data Compare',  # Page title
            'Source Data',   # Dropdown label
            'Calculator',    # Calculator selection
            'Start Comparison'  # Comparison button
        ]
        
        missing_elements = []
        for element in essential_elements:
            if element.lower() not in page_text:
                missing_elements.append(element)
        
        if not missing_elements:
            print("✅ All essential page elements are still present")
        else:
            print("⚠️  Some essential elements might be missing:")
            for element in missing_elements:
                print(f"   - Missing: {element}")
        
        print("\n📋 Manual Verification:")
        print("1. Visit http://localhost:5000/compare")
        print("2. Verify no debug messages are visible")
        print("3. Check that the page looks clean and professional")
        print("4. Ensure comparison functionality still works")
        
    except Exception as e:
        print(f"❌ Error testing compare page: {e}")

if __name__ == "__main__":
    test_compare_page_clean()
