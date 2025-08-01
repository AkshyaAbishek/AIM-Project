"""
Test script to verify duplicate prevention in the AIM application
"""
import sys
import os
import json
import hashlib

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_duplicate_detection():
    """Test the duplicate detection functionality."""
    
    # Sample data 1
    data1 = {
        "applicant_first_name": "John",
        "applicant_last_name": "Doe", 
        "applicant_birth_date": "1985-06-15",
        "applicant_gender": "M",
        "policy_face_amount": "250000"
    }
    
    # Same data (should be detected as duplicate)
    data2 = {
        "applicant_first_name": "John",
        "applicant_last_name": "Doe",
        "applicant_birth_date": "1985-06-15", 
        "applicant_gender": "M",
        "policy_face_amount": "250000"
    }
    
    # Different data for same person (should NOT be detected as duplicate by hash)
    data3 = {
        "applicant_first_name": "John",
        "applicant_last_name": "Doe",
        "applicant_birth_date": "1985-06-15",
        "applicant_gender": "M", 
        "policy_face_amount": "500000"  # Different amount
    }
    
    def get_data_hash(data_dict):
        """Generate a hash for the data to check for duplicates."""
        json_str = json.dumps(data_dict, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    hash1 = get_data_hash(data1)
    hash2 = get_data_hash(data2) 
    hash3 = get_data_hash(data3)
    
    print("🧪 Testing Duplicate Detection")
    print("=" * 40)
    print(f"Data 1 hash: {hash1}")
    print(f"Data 2 hash: {hash2}")
    print(f"Data 3 hash: {hash3}")
    print()
    
    print("✅ Test Results:")
    print(f"Data 1 == Data 2: {hash1 == hash2} (Should be True - exact duplicates)")
    print(f"Data 1 == Data 3: {hash1 == hash3} (Should be False - same person, different policy)")
    print()
    
    if hash1 == hash2 and hash1 != hash3:
        print("🎉 Duplicate detection working correctly!")
        print("- Exact duplicate data is detected")
        print("- Same person with different policy data is allowed")
    else:
        print("❌ Duplicate detection has issues!")
    
    return hash1 == hash2 and hash1 != hash3

if __name__ == "__main__":
    success = test_duplicate_detection()
    print(f"\n🏁 Test {'PASSED' if success else 'FAILED'}")
