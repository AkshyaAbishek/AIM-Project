#!/usr/bin/env python3
"""
Test script to debug the import template functionality
"""
import requests
import json
import os
import tempfile
import pandas as pd

def test_json_upload():
    """Test JSON template upload"""
    print("Testing JSON template upload...")
    
    # Create sample JSON template
    sample_template = {
        "name": "Test Life Insurance Template",
        "description": "Sample template for testing",
        "product_type": "life_insurance",
        "field_mappings": [
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
    
    # Save to temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_template, f, indent=2)
        json_file_path = f.name
    
    try:
        # Test the upload
        with open(json_file_path, 'rb') as f:
            files = {'template_file': f}
            response = requests.post('http://localhost:5000/api/upload-template', files=files)
        
        print(f"JSON Upload - Status Code: {response.status_code}")
        print(f"JSON Upload - Response: {response.json()}")
        
    except Exception as e:
        print(f"Error testing JSON upload: {e}")
    finally:
        # Clean up
        try:
            os.unlink(json_file_path)
        except:
            pass

def test_excel_upload():
    """Test Excel template upload"""
    print("\nTesting Excel template upload...")
    
    # Create sample Excel file
    data = {
        'Source Field': ['PolicyNumber', 'InsuredName', 'CoverageAmount', 'EffectiveDate'],
        'Target Field': ['policy_number', 'insured_name', 'coverage_amount', 'effective_date'],
        'Transformation': ['trim', 'trim', 'currency_format', 'date_format'],
        'Required': ['true', 'true', 'true', 'false']
    }
    
    df = pd.DataFrame(data)
    
    # Save to temporary Excel file
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        excel_file_path = f.name
    
    df.to_excel(excel_file_path, index=False)
    
    try:
        # Test the upload
        with open(excel_file_path, 'rb') as f:
            files = {'template_file': f}
            response = requests.post('http://localhost:5000/api/upload-template', files=files)
        
        print(f"Excel Upload - Status Code: {response.status_code}")
        print(f"Excel Upload - Response: {response.json()}")
        
    except Exception as e:
        print(f"Error testing Excel upload: {e}")
    finally:
        # Clean up
        try:
            os.unlink(excel_file_path)
        except:
            pass

def test_server_connection():
    """Test if the server is running"""
    print("Testing server connection...")
    try:
        response = requests.get('http://localhost:5000/')
        print(f"Server connection - Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Cannot connect to server: {e}")
        return False

if __name__ == "__main__":
    if test_server_connection():
        test_json_upload()
        test_excel_upload()
    else:
        print("Please start the web application first using: python web_app.py")
