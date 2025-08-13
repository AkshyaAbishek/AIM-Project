# What Should Be in Your Files - Complete Guide

## 🎯 Quick Start Checklist

### ✅ Before You Begin
1. **Close all Excel applications**
2. **Run `setup_and_run.bat` to create safe directories**
3. **Have some FAST UI data added to the application**

## 📂 File Requirements

### 1. **Actuarial Calculator Excel File** (Input)

#### Minimum Requirements:
- ✅ Valid Excel file (.xlsx or .xls)
- ✅ At least one worksheet with data
- ✅ First row contains column headers (field names)
- ✅ Accessible location (Documents, Desktop, etc.)

#### Example Structure:
```
| Policy_Number | Insured_First_Name | Insured_Last_Name | Birth_Date | Gender | Coverage_Amount | Premium_Amount |
|---------------|-------------------|------------------|------------|---------|----------------|----------------|
| POL001        | John              | Doe              | 1985-06-15 | M       | 250000         | 150.00         |
| POL002        | Jane              | Smith            | 1990-03-20 | F       | 500000         | 300.00         |
```

#### Common Field Names to Include:
```
Personal Information:
- Insured_First_Name, First_Name, Given_Name
- Insured_Last_Name, Last_Name, Surname, Family_Name
- Birth_Date, Date_of_Birth, DOB
- Gender, Sex

Policy Information:
- Policy_Number, Contract_Number, Policy_ID
- Coverage_Amount, Face_Amount, Sum_Assured, Benefit_Amount
- Policy_Date, Effective_Date, Issue_Date, Start_Date
- Premium_Amount, Annual_Premium, Monthly_Premium

Classification:
- Product_Type, Plan_Code, Product_Code
- Risk_Class, Underwriting_Class, Rating_Class
- Premium_Mode, Payment_Frequency, Billing_Mode
```

### 2. **FAST UI Data** (Should be in your application database)

#### Add through "Add new JSON data" button:

#### Basic Life Insurance Example:
```json
{
  "applicant_first_name": "John",
  "applicant_last_name": "Doe",
  "applicant_birth_date": "1985-06-15",
  "applicant_gender": "M",
  "policy_face_amount": "250000",
  "policy_effective_date": "2024-01-01",
  "premium_mode": "M"
}
```

#### Comprehensive Example:
```json
{
  "applicant_first_name": "Jane",
  "applicant_last_name": "Smith",
  "applicant_birth_date": "1990-03-20",
  "applicant_gender": "F",
  "applicant_ssn": "123-45-6789",
  "policy_number": "POL002024",
  "policy_face_amount": "500000",
  "policy_effective_date": "2024-02-15",
  "premium_amount": "300.00",
  "premium_mode": "Q",
  "product_type": "Term Life",
  "risk_class": "Preferred",
  "smoking_status": "Non-Smoker",
  "agent_code": "A001",
  "issue_state": "CA"
}
```

## 🗂️ File Location Recommendations

### ✅ SAFE Locations (Use These):
```
📁 Documents folder:
   C:\Users\[YourName]\Documents\AIM_Excel_Mappings\

📁 Desktop:
   C:\Users\[YourName]\Desktop\

📁 Created by setup script:
   C:\Users\[YourName]\Documents\AIM_Excel_Mappings\
   C:\Users\[YourName]\Desktop\AIM_Temp\
```

### ❌ AVOID These Locations:
```
❌ C:\Program Files\
❌ C:\Windows\
❌ C:\System32\
❌ Network drives (unless you have write permissions)
❌ Folders with special characters in path
```

## 📋 Step-by-Step Setup Process

### Step 1: Prepare Your Calculator Excel
1. **Open Excel and create/open your calculator file**
2. **Ensure first row has clear column headers**
3. **Add some sample data (at least 2-3 rows)**
4. **Save to a safe location** (Documents or Desktop)
5. **Close Excel completely**

### Step 2: Add FAST UI Data
1. **Run the AIM application**
2. **Click "1. Add new JSON data"**
3. **Enter sample JSON data** (use examples above)
4. **Choose "Save data only" or "Save and process immediately"**
5. **Repeat with 2-3 different records for better mapping**

### Step 3: Create Excel Mapping
1. **Click "2. Excel Field Mapping"**
2. **Select product type** (life/annuity/health)
3. **Choose OUTPUT path**: `Documents\AIM_Excel_Mappings\my_mapping.xlsx`
4. **Choose CALCULATOR path**: Your prepared Excel file
5. **Click "Create Mapping"**

## 🛠️ If You Get "Permission Denied"

### Quick Fixes:
1. **Use the setup script**: Run `setup_and_run.bat`
2. **Try Desktop**: Save to `C:\Users\[YourName]\Desktop\`
3. **Close Excel**: Make sure no Excel files are open
4. **Simple filename**: Use `mapping.xlsx` instead of complex names
5. **Run as admin**: Right-click → "Run as administrator"

### Alternative Approach:
```batch
1. Open File Explorer
2. Navigate to C:\Users\[YourName]\Documents
3. Create new folder: "AIM_Mappings"
4. Use this folder as your output location
```

## 📊 Expected Output Files

### Generated Excel File Structure:
```
📄 your_mapping.xlsx
├── 📋 Field_Mapping (Main sheet)
│   ├── FAST_UI_Field column
│   ├── FAST_UI_Value column  
│   ├── Actuarial_Field column
│   └── Actuarial_Value column
├── 📋 Instructions (How-to guide)
└── 📋 Calculator_Fields (Reference)
```

### Example Mapping Output:
| FAST_UI_Field | FAST_UI_Value | Actuarial_Field | Actuarial_Value |
|---------------|---------------|-----------------|-----------------|
| applicant_first_name | John | Insured_First_Name | =B2 |
| applicant_last_name | Doe | Insured_Last_Name | =B3 |
| policy_face_amount | 250000 | Coverage_Amount | =B4 |
| premium_mode | M | Payment_Frequency | =IF(B5="M",12,1) |

## 🔧 Testing Your Setup

### Quick Test:
1. **Create test calculator Excel**:
   ```
   | Policy_ID | Customer_Name | Amount |
   |-----------|---------------|--------|
   | P001      | Test User     | 100000 |
   ```

2. **Add test FAST UI data**:
   ```json
   {
     "policy_number": "P001",
     "applicant_name": "Test User",
     "face_amount": "100000"
   }
   ```

3. **Run mapping tool** and verify it creates Excel file

## 📞 Still Having Issues?

### Check These:
- [ ] Excel applications are completely closed
- [ ] You have write permissions to the folder
- [ ] File path doesn't contain special characters
- [ ] Calculator Excel file is readable
- [ ] You have some FAST UI data in the database

### Get Help:
- Check `TROUBLESHOOTING_GUIDE.md`
- Try the sample files created by `setup_and_run.bat`
- Use simple test data first, then add complexity

Remember: The tool will work even with minimal data - you can always enhance the mapping manually in Excel later!
