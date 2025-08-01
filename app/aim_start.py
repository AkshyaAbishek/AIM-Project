"""
AIM - Actuarial Input Mapper - Main Entry Point

This script serves as the main entry point for the AIM application,
providing both console and GUI interfaces for:
- Loading actuarial data from Excel/JSON
- Mapping fields according to standardized templates
- Validating input data against product rules
- Processing insurance product calculations
- Exporting results in required formats
"""

import json
import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
import pandas as pd
import sqlite3
import hashlib
from typing import Dict, List, Union, Any, Optional, Callable

# Add src directory to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from aim_processor import AIMProcessor, ValidationError, MappingError # type: ignore


class MessageFormatter:
    """
    Centralized message formatting for AIM operations.
    
    Provides consistent formatting for success, error, and info messages
    related to actuarial data processing, field mapping, and validation results.
    """
    
    @staticmethod
    def success(message: str) -> str:
        """Format success message with consistent emoji and styling."""
        return f"✅ {message}"
    
    @staticmethod
    def error(message: str) -> str:
        """Format error message with consistent emoji and styling."""
        return f"❌ {message}"
    
    @staticmethod
    def info(message: str) -> str:
        """Format info message with consistent emoji and styling."""
        return f"📊 {message}"
    
    @staticmethod
    def warning(message: str) -> str:
        """Format warning message with consistent emoji and styling."""
        return f"⚠️ {message}"
    
    @staticmethod
    def section_header(title: str, width: int = 50) -> str:
        """Create consistent section headers."""
        return f"\n{title}\n{'=' * width}"
    
    @staticmethod
    def subsection_header(title: str, width: int = 40) -> str:
        """Create consistent subsection headers."""
        return f"\n{title}\n{'-' * width}"


class ProcessorHelper:
    """
    Helper class to handle common AIM processor operations.
    
    Centralizes common AIM processor operations for actuarial input mapping
    following DRY principles.
    """
    
    def __init__(self):
        """Initialize the processor helper with AIM processor instance."""
        self.processor = AIMProcessor()
        self.formatter = MessageFormatter()
    
    def initialize_processor(self) -> bool:
        """
        Initialize processor with error handling and consistent messaging.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Processor is already initialized in __init__
            print(self.formatter.success("AIM Processor initialized successfully"))
            return True
        except Exception as error:
            print(self.formatter.error(f"Failed to initialize AIM Processor: {error}"))
            return False
    
    def get_supported_products(self) -> List[str]:
        """Get supported insurance products with consistent error handling."""
        try:
            products = self.processor.get_supported_products()
            print(self.formatter.success(f"Supported products: {', '.join(products)}"))
            return products
        except Exception as error:
            print(self.formatter.error(f"Error getting supported products: {error}"))
            return []
    
    def load_sample_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load input data with consistent error handling.
        
        Args:
            file_path: Path to the input data file
            
        Returns:
            Dict containing actuarial input data
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(self.formatter.success(f"Loaded input data with {len(data)} top-level fields"))
            print(f"   Fields: {list(data.keys())[:5]}...")
            return data
        except FileNotFoundError:
            print(self.formatter.error(f"Input file not found: {file_path}"))
            return {}
        except json.JSONDecodeError:
            print(self.formatter.error(f"Invalid JSON format in file: {file_path}"))
            return {}
        except Exception as error:
            print(self.formatter.error(f"Error loading input data: {error}"))
            return {}
    
    def process_data_with_validation(self, data: Dict[str, Any], product_type: str = "life_insurance") -> Dict[str, Any]:
        """
        Process actuarial input data with field mapping and validation.
        
        Args:
            data: Input data dictionary containing actuarial fields
            product_type: Type of insurance product (life_insurance, annuity, etc.)
            
        Returns:
            Dict containing:
                - mapped_fields: Fields after template mapping
                - validation_results: Results of data validation
                - calculations: Product-specific calculations
                - errors: Any validation or processing errors
        """
        try:
            # Validate input data structure
            if not isinstance(data, dict):
                raise ValueError("Input data must be a dictionary")

            print(self.formatter.info(f"Processing {product_type} data with {len(data)} fields..."))
            
            # Process the data through AIM processor
            result = self.processor.process_data(data, product_type)
            
            if result:
                print(self.formatter.success("Data processing completed successfully"))
                print(f"⏱️  Completed at: {datetime.now().isoformat()}")
                
                # Log detailed results
                if isinstance(result, dict):
                    for key, value in result.items():
                        print(f"   📊 {key}: {value}")
                return result
            else:
                print(self.formatter.error(f"Processing failed for {product_type}"))
                return {"status": "failed", "product_type": product_type}
                
        except (ValidationError, MappingError) as processing_error:
            print(self.formatter.error(f"Processing error for {product_type}: {processing_error}"))
            return {"status": "error", "error": str(processing_error), "product_type": product_type}
        except Exception as unexpected_error:
            print(self.formatter.error(f"Unexpected error during processing: {unexpected_error}"))
            return {"status": "error", "error": str(unexpected_error), "product_type": product_type}


class ButtonFactory:
    """
    Factory class to eliminate redundant button creation code.
    
    Provides consistent button styling and hover effects following
    modern UI design principles.
    """
    
    @staticmethod
    def create_hover_effects(button: tk.Button, normal_color: str, hover_color: str) -> None:
        """
        Create consistent hover effects for buttons to eliminate code duplication.
        
        Args:
            button: The button widget to add effects to
            normal_color: Normal background color
            hover_color: Hover background color
        """
        def on_enter(event):
            button.configure(bg=hover_color)
        
        def on_leave(event):
            button.configure(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    @classmethod
    def create_styled_button(cls, parent: tk.Widget, text: str, command: Callable,
                           bg_color: str = "#3498db", hover_color: str = "#2980b9",
                           width: int = 18, height: int = 2, **kwargs) -> tk.Button:
        """
        Create a styled button with consistent design and hover effects.
        
        Eliminates redundancy between create_button and create_dialog_button methods.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button command function
            bg_color: Background color
            hover_color: Hover background color
            width: Button width
            height: Button height
            **kwargs: Additional button configuration options
            
        Returns:
            tk.Button: Configured button widget
        """
        # Default button configuration
        default_config = {
            'font': ("Segoe UI", 9, "bold"),
            'width': width,
            'height': height,
            'bg': bg_color,
            'fg': "white",
            'relief': "flat",
            'bd': 0,
            'cursor': "hand2",
            'activebackground': hover_color,
            'activeforeground': "white"
        }
        
        # Update with any provided kwargs
        default_config.update(kwargs)
        
        # Create button
        button = tk.Button(parent, text=text, command=command, **default_config)
        
        # Add hover effects
        cls.create_hover_effects(button, bg_color, hover_color)
        
        return button
    
    @classmethod
    def create_grid_button(cls, parent: tk.Widget, text: str, command: Callable,
                          row: int, col: int, **kwargs) -> tk.Button:
        """
        Create a styled button and place it in grid layout.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button command function
            row: Grid row
            col: Grid column
            **kwargs: Additional configuration options
            
        Returns:
            tk.Button: Configured and placed button widget
        """
        button = cls.create_styled_button(parent, text, command, **kwargs)
        button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        return button


def run_processor_console():
    """
    Run the AIM processor in console mode.
    
    Provides a command-line interface for processing actuarial input files
    and managing the AIM processor.
    """
    formatter = MessageFormatter()
    helper = ProcessorHelper()
    
    print(formatter.section_header("🎯 AIM - Actuarial Input Mapper"))
    
    # Initialize processor
    print("\n1. Initializing AIM Processor...")
    if not helper.initialize_processor():
        return
    
    # Get supported products
    print("\n2. Checking supported products...")
    supported_products = helper.get_supported_products()
    
    # Load and process input file
    print("\n3. Select an input file to process...")
    sample_file = os.path.join("data", "sample", "life_insurance_sample.json")
    input_data = helper.load_sample_data(sample_file)
    
    if input_data:
        print(formatter.subsection_header("4. Processing input data"))
        result = helper.process_data_with_validation(input_data, "life_insurance")
        
        # Show processing summary
        print(formatter.section_header("📋 Processing Summary"))
        if result and result.get("status") != "failed":
            print(formatter.success("Processing completed successfully"))
            for key, value in result.items():
                print(formatter.info(f"{key}: {value}"))
        else:
            print(formatter.error("Processing failed"))
            if isinstance(result, dict):
                print(formatter.info(f"Error: {result.get('error', 'Unknown error')}"))
        
        return result
    else:
        print(formatter.error("No input data to process"))
        return None


def run_interactive_demo():
    """Run optimized interactive demo with eliminated redundancy."""
    formatter = MessageFormatter()
    helper = ProcessorHelper()
    
    print(formatter.section_header("🎮 Interactive Demo Mode"))
    
    # Storage for user data
    user_data_store = []
    
    def show_current_status():
        """Helper function to show current status - eliminates repeated code."""
        if user_data_store:
            print(formatter.info(f"Current user data store: {len(user_data_store)} datasets"))
        else:
            print(formatter.info("No user data stored yet"))
    
    def get_user_choice() -> str:
        """Helper function to get user choice - eliminates repeated input logic."""
        print("\nOptions:")
        print("1. Process Actuarial Data")
        print("2. Configure Field Mappings")
        print("3. View Processing History")
        print("4. Data Validation Report")
        print("5. Exit")
        return input("\nEnter your choice (1-4): ").strip()
    
    while True:
        show_current_status()
        choice = get_user_choice()
        
        if choice == "1":
            # Process actuarial data
            file_path = filedialog.askopenfilename(
                title="Select Input File",
                filetypes=[
                    ("All Supported", "*.json;*.xlsx;*.xls"),
                    ("JSON files", "*.json"),
                    ("Excel files", "*.xlsx;*.xls"),
                    ("All files", "*.*")
                ]
            )
            if file_path:
                try:
                    if file_path.lower().endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(file_path)
                        data = df.to_dict(orient='records')
                        data = {"records": data, "source": "excel"}
                    else:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                    
                    if not isinstance(data, dict):
                        data = {"data": data}
                    
                    print(formatter.subsection_header("Processing Actuarial Data"))
                    result = helper.process_data_with_validation(data)
                    user_data_store.append(result)
                    
                    if result.get("status") == "success":
                        if messagebox.askyesno("Success", "Would you like to export the results?"):
                            export_path = filedialog.asksaveasfilename(
                                title="Export Results",
                                defaultextension=".json",
                                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                            )
                            if export_path:
                                with open(export_path, 'w') as f:
                                    json.dump(result, f, indent=4)
                                print(formatter.success(f"Results exported to: {export_path}"))
                except Exception as error:
                    print(formatter.error(f"Error processing file: {error}"))
            
        elif choice == "2":
            # Configure field mappings
            print(formatter.subsection_header("Field Mapping Configuration"))
            print("\n📝 Choose product type:")
            products = helper.get_supported_products()
            
            for i, product in enumerate(products, 1):
                print(f"{i}. {product}")
            
            product_choice = input("\nSelect product type (number): ").strip()
            try:
                selected_product = products[int(product_choice) - 1]
                print(f"\nConfiguring mappings for: {selected_product}")
                
                # Open mapping file in Excel
                file_path = filedialog.askopenfilename(
                    title="Select Field Mapping Excel File",
                    filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
                )
                
                if file_path:
                    try:
                        df = pd.read_excel(file_path)
                        mappings = df.to_dict(orient='records')
                        result = helper.process_data_with_validation(
                            {"mappings": mappings, "product_type": selected_product},
                            "field_mapping"
                        )
                        user_data_store.append(result)
                    except Exception as error:
                        print(formatter.error(f"Error processing mapping file: {error}"))
            except (ValueError, IndexError):
                print(formatter.error("Invalid product selection"))
        
        elif choice == "3":
            # Show statistics
            print(formatter.subsection_header("Data Statistics"))
            print(formatter.info(f"Total processing sessions: {len(user_data_store)}"))
            
            successful_sessions = sum(1 for result in user_data_store 
                                    if isinstance(result, dict) and result.get("status") != "failed")
            print(formatter.info(f"Successful sessions: {successful_sessions}"))
            
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print(formatter.error("Invalid choice"))


class OptimizedDataManager:
    """
    Optimized data manager that eliminates redundant database operations.
    
    Consolidates database functionality with proper error handling
    following AIM actuarial data processing guidelines.
    """
    
    def __init__(self):
        """Initialize the optimized data manager."""
        self.db_path = "aim_data.db"
        self.formatter = MessageFormatter()
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize database with consistent error handling."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS processed_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_hash TEXT UNIQUE,
                        data_json TEXT,
                        product_type TEXT,
                        timestamp TEXT,
                        status TEXT,
                        processing_result TEXT
                    )
                ''')
                conn.commit()
                print(self.formatter.success("Database initialized successfully"))
        except Exception as error:
            print(self.formatter.error(f"Database initialization error: {error}"))
    
    def save_processing_result(self, data: Any, data_type: str, result: Dict[str, Any]) -> bool:
        """
        Save processing result with optimized duplicate checking.
        
        Args:
            data: Original data processed
            data_type: Type of data processed
            result: Processing result
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            data_hash = hashlib.md5(str(data).encode()).hexdigest()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO actuarial_data 
                    (data_hash, data_json, product_type, timestamp, is_valid, processing_result)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    data_hash,
                    json.dumps(data, default=str),
                    data_type,
                    datetime.now().isoformat(),
                    result.get('is_valid', False),
                    json.dumps(result, default=str)
                ))
                conn.commit()
                return True
                
        except Exception as error:
            print(self.formatter.error(f"Error saving to database: {error}"))
            return False
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total count
                cursor.execute("SELECT COUNT(*) FROM actuarial_data")
                total_count = cursor.fetchone()[0]
                
                # Get valid records count
                cursor.execute("SELECT COUNT(*) FROM actuarial_data WHERE is_valid = 1")
                valid_count = cursor.fetchone()[0]
                
                # Get by data type
                cursor.execute("SELECT product_type, COUNT(*) FROM actuarial_data GROUP BY product_type")
                type_counts = dict(cursor.fetchall())
                
                return {
                    "total_processed": total_count,
                    "valid_records": valid_count,
                    "validation_rate": round((valid_count / total_count) * 100, 2) if total_count > 0 else 0,
                    "by_data_type": type_counts,
                    "last_updated": datetime.now().isoformat()
                }
                
        except Exception as error:
            print(self.formatter.error(f"Error getting statistics: {error}"))
            return {"error": str(error)}


def main():
    """
    Main function for running the AIM processor in console mode.
    
    Provides a command-line interface for:
    - Loading actuarial input files (Excel/JSON)
    - Mapping fields according to product templates
    - Validating input data
    - Processing insurance calculations
    - Exporting results
    """
    formatter = MessageFormatter()
    processor_helper = ProcessorHelper()
    
    print(formatter.section_header("🚀 Starting AIM Console Mode"))
    
    try:
        # Initialize processor
        if not processor_helper.initialize_processor():
            print(formatter.error("Failed to initialize AIM processor"))
            return

        # Show supported products
        products = processor_helper.get_supported_products()
        if not products:
            print(formatter.error("No supported products found"))
            return
            
        print(formatter.section_header("\n📋 Available Operations"))
        print("1. Process JSON Input File")
        print("2. Process Excel Input File")
        print("3. Field Mapping Configuration")
        print("4. Validate Input Data")
        print("5. Export Results")
        
        choice = input("\nSelect operation (1-5): ").strip()
        
        if choice == "1":
            # Process JSON input
            file_path = filedialog.askopenfilename(
                title="Select JSON Input File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                data = processor_helper.load_sample_data(file_path)
                if data:
                    result = processor_helper.process_data_with_validation(data)
                    
                    if result.get("status") != "failed":
                        # Ask to export results
                        if messagebox.askyesno("Success", "Would you like to export the results?"):
                            export_path = filedialog.asksaveasfilename(
                                title="Export Results",
                                defaultextension=".json",
                                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                            )
                            if export_path:
                                with open(export_path, 'w') as f:
                                    json.dump(result, f, indent=4)
                                print(formatter.success(f"Results exported to: {export_path}"))
                    
        elif choice == "2":
            # Process Excel input
            file_path = filedialog.askopenfilename(
                title="Select Excel Input File",
                filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    df = pd.read_excel(file_path)
                    data = df.to_dict(orient='records')
                    if data:
                        result = processor_helper.process_data_with_validation({"records": data})
                        # Similar export logic as above
                except Exception as error:
                    print(formatter.error(f"Failed to process Excel file: {error}"))
    except KeyboardInterrupt:
        print(formatter.warning("\nOperation terminated by user"))
    except Exception as error:
        print(formatter.error(f"Operation failed with error: {error}"))
        import traceback
        traceback.print_exc()
    
    print(formatter.section_header("🏁 Operation completed"))


if __name__ == "__main__":
    print("\nAIM Project Launcher")
    print("====================")
    print("1. Console Mode (Optimized Example)")
    print("2. GUI Mode")
    mode = input("Select mode (1=Console, 2=GUI): ").strip()
    if mode == "2":
        # Import and run the GUI from example.py
        import importlib.util
        gui_path = os.path.join(os.path.dirname(__file__), "example.py")
        spec = importlib.util.spec_from_file_location("example", gui_path)
        gui_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gui_module)
        gui_module.main()  # This will create the Tk root and run mainloop
    else:
        main()
