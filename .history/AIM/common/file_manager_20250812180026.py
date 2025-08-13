"""
File Utilities - Common file operations and Excel handling
"""
import os
import json
from tkinter import filedialog, messagebox
import pandas as pd


class FileManager:
    """Handles file operations, Excel processing, and path management"""
    
    @staticmethod
    def browse_save_excel(path_var):
        """Browse for Excel file save location with enhanced error handling."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Save Excel File As"
            )
            if filename:
                path_var.set(filename)
        except Exception as e:
            messagebox.showerror("File Error", f"Error selecting save location: {e}")
    
    @staticmethod
    def browse_open_excel(path_var):
        """Browse for Excel file to open."""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Select Excel File"
            )
            if filename:
                path_var.set(filename)
        except Exception as e:
            messagebox.showerror("File Error", f"Error selecting file: {e}")
    
    @staticmethod
    def export_data_to_json(data_store, filename=None):
        """Export data to JSON file."""
        if not data_store:
            messagebox.showinfo("No Data", "No data to export.")
            return False
        
        try:
            if not filename:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                    title="Export Data As"
                )
            
            if filename:
                from datetime import datetime
                export_data = {
                    "export_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total_records": len(data_store),
                    "data": data_store
                }
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                messagebox.showinfo("Export Success", f"Data exported successfully to:\n{filename}")
                return True
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {e}")
            return False
    
    @staticmethod
    def read_excel_fields(file_path):
        """Read field names from Excel file."""
        try:
            # Read the first few rows to get field names
            df = pd.read_excel(file_path, nrows=0)  # Just get column headers
            return list(df.columns)
        except Exception as e:
            messagebox.showerror("Excel Error", f"Error reading Excel file: {e}")
            return []
    
    @staticmethod
    def create_excel_template(file_path, field_data, product_type="life"):
        """Create Excel mapping template with enhanced structure."""
        try:
            # Create the main mapping data
            mapping_data = []
            for i, (ui_field, ui_value) in enumerate(field_data.items(), 1):
                mapping_data.append({
                    'FAST UI Field': ui_field,
                    'FAST UI Value': ui_value,
                    'Actuarial Field': '',  # To be filled by user
                    'Actuarial Value': '',  # To be filled by user
                    'Values_Match': ''  # TRUE/FALSE comparison
                })
            
            # Create DataFrame
            df = pd.DataFrame(mapping_data)
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Main mapping sheet
                df.to_excel(writer, sheet_name='Field_Mapping', index=False)
                
                # Instructions sheet
                instructions_df = pd.DataFrame({
                    'Instructions': [
                        f'Field Mapping Template for {product_type.title()} Insurance',
                        '',
                        '1. Fill in the "Actuarial Field" column with your calculator field names',
                        '2. Fill in the "Actuarial Value" column with transformation logic',
                        '3. The "Values_Match" column will show TRUE/FALSE for comparison',
                        '4. Use Excel formulas to automate the Values_Match column',
                        '5. Review false matches to identify mapping issues',
                        '',
                        'Example Values_Match formula: =IF(B2=D2,"TRUE","FALSE")',
                        '',
                        'This template helps ensure accurate field mapping between',
                        'your FAST UI data and actuarial calculator requirements.'
                    ]
                })
                instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
            
            return True, f"Excel template created successfully: {file_path}"
            
        except Exception as e:
            return False, f"Error creating Excel template: {e}"
    
    @staticmethod
    def validate_file_path(file_path, extension=".xlsx"):
        """Validate file path and extension."""
        if not file_path:
            return False, "Please select a file path"
        
        if not file_path.lower().endswith(extension):
            return False, f"File must have {extension} extension"
        
        # Check if directory exists for save operations
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            return False, f"Directory does not exist: {directory}"
        
        return True, "File path is valid"
    
    @staticmethod
    def suggest_field_mapping(ui_field, calculator_fields):
        """Suggest best matching calculator field for a UI field."""
        if not calculator_fields:
            return ""
        
        ui_field_lower = ui_field.lower()
        
        # Common field mappings
        field_mappings = {
            'first_name': ['first_name', 'fname', 'given_name', 'insured_first'],
            'last_name': ['last_name', 'lname', 'surname', 'insured_last'],
            'birth_date': ['birth_date', 'dob', 'date_of_birth', 'birthdate'],
            'gender': ['gender', 'sex'],
            'face_amount': ['face_amount', 'coverage', 'sum_assured', 'benefit_amount'],
            'premium': ['premium', 'premium_amount', 'annual_premium'],
            'effective_date': ['effective_date', 'policy_date', 'start_date'],
            'policy_number': ['policy_number', 'policy_no', 'contract_number'],
        }
        
        # Find best match
        for key, suggestions in field_mappings.items():
            if key in ui_field_lower:
                for suggestion in suggestions:
                    for calc_field in calculator_fields:
                        if suggestion in calc_field.lower():
                            return calc_field
        
        # If no direct match, try partial matching
        for calc_field in calculator_fields:
            calc_field_lower = calc_field.lower()
            # Check if any word from ui_field is in calc_field
            ui_words = ui_field_lower.replace('_', ' ').split()
            for word in ui_words:
                if len(word) > 3 and word in calc_field_lower:  # Only match words longer than 3 chars
                    return calc_field
        
        return ""  # No suggestion found
