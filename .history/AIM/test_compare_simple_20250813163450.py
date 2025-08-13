#!/usr/bin/env python3
"""
Simple test to verify that debug messages have been removed from the compare page
"""
import requests

def test_compare_page_clean():
    print("🧪 Testing Compare Page - Debug Messages Removal")
    print("=" * 55)
    
    try:
        # Get the compare page
        response = requests.get('http://localhost:5000/compare')
        print(f"✅ Compare page loads: Status {response.status_code}")
        
        # Get the page content
        page_content = response.text
        
        # List of debug messages that should NOT be present
        debug_phrases = [
            "✅ SUCCESS: Found",
            "records for dropdown",
            "Debug Information",
            "Available Calculators:",
            "Records found:",
            "Calculators available:",
            "Database path:",
            "These records should appear in the",
            "If you don't see these in the dropdown"
        ]
        
        # Check for presence of debug messages
        found_debug_messages = []
        
        for phrase in debug_phrases:
            if phrase in page_content:
                found_debug_messages.append(phrase)
        
        # Report results
        if not found_debug_messages:
            print("✅ SUCCESS: All target debug messages have been removed!")
            print("✅ The compare page is now clean and user-friendly")
        else:
            print("❌ Some debug messages are still present:")
            for msg in found_debug_messages:
                print(f"   - Found: '{msg}'")
        
        # Check that the page still has the essential elements
        essential_elements = [
            'Data Compare',
            'Source Data',
            'Calculator',
            'Start Comparison'
        ]
        
        missing_elements = []
        for element in essential_elements:
            if element not in page_content:
                missing_elements.append(element)
        
        if not missing_elements:
            print("✅ All essential page elements are still present")
        else:
            print("⚠️  Some essential elements might be missing:")
            for element in missing_elements:
                print(f"   - Missing: {element}")
        
        # Count remaining alert boxes (should be minimal)
        alert_count = page_content.count('class="alert')
        print(f"📊 Remaining alert boxes: {alert_count}")
        
        if alert_count <= 2:  # Allow for some essential alerts like error handling
            print("✅ Alert box count is reasonable")
        else:
            print("⚠️  There might still be unnecessary alert boxes")
        
        print("\n📋 Manual Verification Steps:")
        print("1. Visit http://localhost:5000/compare")
        print("2. Verify the page looks clean and professional")
        print("3. No debug information should be visible")
        print("4. Test that comparison functionality still works")
        print("5. Check browser console for any JavaScript errors")
        
        return len(found_debug_messages) == 0
        
    except Exception as e:
        print(f"❌ Error testing compare page: {e}")
        return False

if __name__ == "__main__":
    success = test_compare_page_clean()
    if success:
        print("\n🎯 CLEANUP SUCCESSFUL: Compare page is now clean!")
    else:
        print("\n⚠️  Some debug messages may still need removal")
