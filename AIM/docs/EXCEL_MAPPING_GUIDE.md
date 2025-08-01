# Excel Field Mapping Feature Documentation

## Overview
The enhanced "Excel Field Mapping" feature creates a comprehensive Excel template that maps FAST UI fields to your Actuarial Calculator fields, enabling seamless data transformation and processing.

## How It Works

### 1. Setup Process
1. Click "2. Excel Field Mapping" button in the main GUI
2. Select product type (life/annuity/health)
3. Choose output path for the new Excel mapping file
4. Select your existing Actuarial Calculator Excel file
5. Click "Create Mapping" to generate the template

### 2. Generated Excel Structure

#### Sheet 1: Field_Mapping (Main Mapping)
| Column | Description | Example |
|--------|-------------|---------|
| FAST_UI_Field | Source field names from FAST UI | `applicant_first_name` |
| FAST_UI_Value | Sample values from your stored data | `John` |
| Actuarial_Field | Target field names in calculator | `Insured_First_Name` |
| Actuarial_Value | Transformation logic/formulas | `=B2` or direct value |

#### Sheet 2: Instructions
- Step-by-step guide for completing the mapping
- Best practices for field mapping
- Excel formula examples

#### Sheet 3: Calculator_Fields
- Complete list of available fields from your calculator Excel
- Reference for accurate field naming
- Field type information

### 3. Field Mapping Intelligence

#### Automatic Suggestions
The system intelligently suggests actuarial fields based on:
- **Direct Name Matching**: `first_name` → `Insured_First_Name`
- **Semantic Similarity**: `face_amount` → `Coverage_Amount`
- **Common Patterns**: `premium` → `Premium_Amount`

#### Supported Field Types
- **Personal Information**: Names, birth dates, gender
- **Policy Details**: Face amounts, effective dates, policy numbers
- **Financial Data**: Premiums, coverage amounts, risk classes
- **Administrative**: Agent codes, issue states, product types

### 4. Manual Completion Process

#### Step 1: Review Suggestions
- Check suggested actuarial field mappings
- Verify field names match your calculator exactly
- Update any incorrect suggestions

#### Step 2: Add Transformation Logic
- Use Excel formulas for data transformation
- Set direct values for constant mappings
- Add validation rules as needed

#### Step 3: Testing
- Use sample data to test mappings
- Verify formulas work correctly
- Check data type compatibility

## Example Mapping Scenarios

### Scenario 1: Direct Field Mapping
```
FAST UI: applicant_first_name = "John"
Calculator: Insured_First_Name
Mapping: Direct copy (=B2)
```

### Scenario 2: Value Transformation
```
FAST UI: applicant_gender = "M"
Calculator: Gender_Code
Mapping: =IF(B2="M","Male","Female")
```

### Scenario 3: Calculated Fields
```
FAST UI: applicant_birth_date = "1985-06-15"
Calculator: Age_At_Issue
Mapping: =YEAR(TODAY())-YEAR(B2)
```

### Scenario 4: Premium Conversion
```
FAST UI: premium_mode = "M"
Calculator: Premium_Frequency
Mapping: =IF(B2="M",12,IF(B2="Q",4,1))
```

## Advanced Features

### 1. Multi-Sheet Support
- Handles complex calculator workbooks
- Maps to specific sheets and ranges
- Supports named ranges

### 2. Data Validation
- Checks field compatibility
- Validates data types
- Provides error highlighting

### 3. Formula Templates
- Pre-built transformation formulas
- Common actuarial calculations
- Industry standard mappings

## Best Practices

### 1. Field Naming
- Use exact field names from calculator
- Maintain consistent naming conventions
- Avoid spaces and special characters

### 2. Data Types
- Ensure compatible data types
- Use proper date formats
- Handle null/empty values

### 3. Testing
- Test with sample data first
- Validate all transformations
- Check edge cases

### 4. Documentation
- Document custom formulas
- Maintain mapping versions
- Track changes and updates

## Integration with Processing

### 1. Using the Mapping
- Save completed Excel mapping
- Reference in data processing workflows
- Apply to new data batches

### 2. Automation
- Use mapping for bulk data conversion
- Apply transformations automatically
- Generate audit trails

### 3. Validation
- Verify mapping accuracy
- Check data integrity
- Monitor transformation results

## Troubleshooting

### Common Issues
1. **Field Not Found**: Check exact spelling in calculator
2. **Formula Errors**: Verify Excel syntax and references
3. **Data Type Mismatch**: Ensure compatible formats
4. **Missing Values**: Handle null/empty data

### Solutions
- Use Calculator_Fields sheet for reference
- Test formulas with sample data
- Add error handling in transformations
- Document known limitations

## File Locations
- **Output Excel**: User-specified location
- **Calculator Excel**: User-provided existing file
- **Sample Calculator**: `sample_actuarial_calculator.xlsx` (for testing)

## Dependencies
- pandas (data manipulation)
- openpyxl (Excel file operations)
- tkinter (GUI components)

## Future Enhancements
- Template library for common mappings
- Field type detection and validation
- Automated testing framework
- Version control for mappings
