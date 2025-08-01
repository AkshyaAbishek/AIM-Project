# Excel Field Mapping Troubleshooting Guide

## Permission Denied Error - Solutions

### 1. **File Path Issues**

#### Problem: "Permission Denied" when selecting destination path
#### Causes & Solutions:

**A. Protected System Directories**
- ❌ Don't save to: `C:\Program Files\`, `C:\Windows\`, `C:\System32\`
- ✅ Use instead: `C:\Users\[YourName]\Documents\`, `C:\Users\[YourName]\Desktop\`

**B. File Already Open**
- ❌ Excel file is currently open in Excel
- ✅ Close the file in Excel before running the mapping

**C. Read-only Location**
- ❌ Network drives or restricted folders
- ✅ Save to local Documents or Desktop folder

**D. File Name Issues**
- ❌ Special characters in filename: `<>:"|?*`
- ✅ Use simple names: `field_mapping.xlsx`

### 2. **Recommended File Locations**

#### For Output Excel File (New Mapping File):
```
✅ C:\Users\[YourName]\Documents\AIM_Mappings\
✅ C:\Users\[YourName]\Desktop\
✅ C:\Users\[YourName]\Downloads\
✅ Any folder you have write permissions to
```

#### For Actuarial Calculator Excel (Existing File):
```
✅ C:\Users\[YourName]\Documents\
✅ C:\Users\[YourName]\Desktop\
✅ Any accessible location with your calculator file
```

### 3. **What Should Be in Your Files**

#### A. Actuarial Calculator Excel File Requirements:

**Minimum Requirements:**
- Must be a valid Excel file (.xlsx or .xls)
- Should have at least one sheet with data
- First row should contain column headers (field names)

**Example Structure:**
```
| Policy_Number | Insured_Name | Premium_Amount | Coverage_Amount | Policy_Date |
|---------------|--------------|----------------|-----------------|-------------|
| POL001        | John Doe     | 150.00         | 250000          | 2024-01-01  |
| POL002        | Jane Smith   | 300.00         | 500000          | 2024-02-15  |
```

**Common Field Names in Actuarial Calculators:**
- `Policy_Number`, `Contract_Number`
- `Insured_First_Name`, `Insured_Last_Name`
- `Birth_Date`, `Date_of_Birth`
- `Gender`, `Sex`
- `Premium_Amount`, `Annual_Premium`
- `Coverage_Amount`, `Face_Amount`, `Sum_Assured`
- `Policy_Date`, `Effective_Date`
- `Risk_Class`, `Underwriting_Class`
- `Product_Type`, `Plan_Code`

#### B. FAST UI Data in Your Database:

**Should contain fields like:**
- `applicant_first_name`, `applicant_last_name`
- `applicant_birth_date`, `applicant_gender`
- `policy_face_amount`, `policy_effective_date`
- `premium_mode`, `premium_amount`
- `policy_number`

### 4. **Step-by-Step Process**

#### Step 1: Prepare Your Files
1. **Close any open Excel files**
2. **Create a folder** for your mappings (e.g., `Documents\AIM_Mappings`)
3. **Ensure your calculator Excel is accessible**

#### Step 2: Run the Mapping Tool
1. Click "2. Excel Field Mapping"
2. Enter product type: `life` (or annuity/health)
3. **For Output Path**: Click Browse → Navigate to `Documents` → Create filename like `life_insurance_mapping.xlsx`
4. **For Calculator Path**: Click Browse → Select your existing calculator Excel

#### Step 3: Verify Permissions
- Try creating a test file in the same folder first
- Ensure you have write permissions to the destination folder

### 5. **Sample Files for Testing**

If you don't have files ready, use these samples:

#### Sample Actuarial Calculator (save as Excel):
```csv
Policy_Number,Insured_First_Name,Insured_Last_Name,Birth_Date,Gender,Coverage_Amount,Premium_Amount,Policy_Date
POL001,John,Doe,1985-06-15,M,250000,150.00,2024-01-01
POL002,Jane,Smith,1990-03-20,F,500000,300.00,2024-02-15
POL003,Bob,Johnson,1978-11-10,M,1000000,450.00,2024-03-01
```

#### Sample FAST UI Data (add through the app):
```json
{
  "applicant_first_name": "John",
  "applicant_last_name": "Doe",
  "applicant_birth_date": "1985-06-15",
  "applicant_gender": "M",
  "policy_face_amount": "250000",
  "premium_amount": "150.00",
  "policy_effective_date": "2024-01-01",
  "premium_mode": "M"
}
```

### 6. **Quick Fix Commands**

If you're still having issues, try these:

#### Check Folder Permissions:
```cmd
# Right-click on folder → Properties → Security → Check permissions
```

#### Create Safe Directory:
```cmd
mkdir C:\Users\%USERNAME%\Documents\AIM_Mappings
```

#### Alternative Paths to Try:
- `C:\Users\[YourName]\Documents\`
- `C:\Users\[YourName]\Desktop\`
- `C:\Temp\` (if it exists)

### 7. **Common Error Messages & Solutions**

| Error | Cause | Solution |
|-------|-------|----------|
| "Permission denied" | Protected folder | Use Documents folder |
| "File in use" | Excel file open | Close Excel application |
| "Invalid path" | Special characters | Use simple filename |
| "Access denied" | Read-only folder | Choose different location |

### 8. **Testing Approach**

1. **Start Simple**: Use Desktop as destination
2. **Use Sample Data**: Create minimal test files first
3. **Check Output**: Verify the Excel file is created successfully
4. **Gradually Add Complexity**: Once working, use real data files

### 9. **If All Else Fails**

**Create Default Location:**
```
C:\Users\[YourName]\Documents\AIM_Excel_Mappings\
```

**Use Default Filename:**
```
field_mapping_[timestamp].xlsx
```

The tool will create a working Excel mapping template even with minimal data!
