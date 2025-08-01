import pandas as pd
import os

# Create a sample actuarial calculator Excel file for testing
def create_sample_calculator():
    # Sample actuarial calculator fields
    calculator_data = {
        'Policy_Number': ['POL001', 'POL002', 'POL003'],
        'Insured_First_Name': ['John', 'Jane', 'Bob'],
        'Insured_Last_Name': ['Doe', 'Smith', 'Johnson'],
        'Birth_Date': ['1985-06-15', '1990-03-20', '1978-11-10'],
        'Gender': ['M', 'F', 'M'],
        'Coverage_Amount': [250000, 500000, 1000000],
        'Premium_Amount': [150.00, 300.00, 450.00],
        'Policy_Date': ['2024-01-01', '2024-02-15', '2024-03-01'],
        'Risk_Class': ['Standard', 'Preferred', 'Standard'],
        'Premium_Mode': ['Monthly', 'Quarterly', 'Annual'],
        'Product_Type': ['Term Life', 'Whole Life', 'Term Life'],
        'Agent_Code': ['A001', 'A002', 'A001'],
        'Issue_State': ['CA', 'NY', 'TX'],
        'Smoking_Status': ['Non-Smoker', 'Non-Smoker', 'Smoker']
    }
    
    df = pd.DataFrame(calculator_data)
    
    # Save to Excel file
    output_path = os.path.join(os.getcwd(), 'sample_actuarial_calculator.xlsx')
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Policy_Data', index=False)
        
        # Add a calculation sheet
        calc_data = {
            'Field_Name': ['Coverage_Amount', 'Premium_Amount', 'Age_At_Issue'],
            'Formula': ['=Policy_Data!F2', '=Policy_Data!G2', '=YEAR(Policy_Data!H2)-YEAR(Policy_Data!D2)'],
            'Description': ['Policy face amount', 'Annual premium', 'Calculated age at issue']
        }
        df_calc = pd.DataFrame(calc_data)
        df_calc.to_excel(writer, sheet_name='Calculations', index=False)
    
    print(f"Sample actuarial calculator created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_sample_calculator()
