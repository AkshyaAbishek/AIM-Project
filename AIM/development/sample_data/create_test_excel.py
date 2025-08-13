import pandas as pd
import os

# Create a sample Excel template for testing
data = {
    'Source Field': ['PolicyNumber', 'InsuredName', 'DateOfBirth', 'Gender', 'CoverageAmount'],
    'Target Field': ['policy_number', 'insured_name', 'birth_date', 'gender', 'coverage_amount'],
    'Transformation': ['trim', 'trim', 'date_format', 'uppercase', 'currency_format'],
    'Required': ['true', 'true', 'true', 'true', 'true']
}

df = pd.DataFrame(data)
excel_file_path = os.path.join(os.path.dirname(__file__), 'test_template.xlsx')
df.to_excel(excel_file_path, index=False)

print(f"✅ Test Excel template created: {excel_file_path}")
print("This file can be used to test Excel template import functionality.")
print("\nTo test:")
print("1. Go to http://localhost:5000/field-mapping")
print("2. Click 'Import Template'")
print("3. Select test_template.xlsx")
print("4. Verify that the template data is loaded correctly")
