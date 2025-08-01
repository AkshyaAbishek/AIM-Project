"""
AIM - Actuarial Input Mapper - Example Usage (Optimized)

This script demonstrates how to use AIM to process palindrome validation
with optimized code structure and eliminated redundancies.
"""

import json
import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from tkinter import ttk
import sqlite3
import hashlib
from typing import Dict, List, Union, Any, Optional, Callable

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aim_processor import AIMProcessor, ValidationError, MappingError # type: ignore


class MessageFormatter:
    """
    Centralized message formatting to eliminate redundant print patterns.
    
    Provides consistent formatting for success, error, and info messages
    following the palindrome project's coding guidelines.
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
    Helper class to eliminate redundant processor operations.
    
    Centralizes common AIM processor operations following DRY principles
    and the palindrome checking guidelines.
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
        """Get supported products with consistent error handling."""
        try:
            if hasattr(self.processor, 'get_supported_products'):
                products = self.processor.get_supported_products()
                print(self.formatter.success(f"Supported products: {', '.join(products)}"))
                return products
            else:
                # Default products for palindrome processing
                default_products = ["palindrome_numbers", "palindrome_strings", "mixed_data"]
                print(self.formatter.info(f"Using default products: {', '.join(default_products)}"))
                return default_products
        except Exception as error:
            print(self.formatter.error(f"Error getting supported products: {error}"))
            return []
    
    def load_sample_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load sample data with consistent error handling and fallback.
        
        Args:
            file_path: Path to the sample data file
            
        Returns:
            Dict containing sample data for palindrome testing
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(self.formatter.success(f"Loaded sample data with {len(data)} top-level fields"))
            print(f"   Sample fields: {list(data.keys())[:5]}...")
            return data
        except FileNotFoundError:
            print(self.formatter.warning("Sample data file not found, using palindrome examples"))
            return self._get_default_palindrome_data()
        except Exception as error:
            print(self.formatter.error(f"Error loading sample data: {error}"))
            return self._get_default_palindrome_data()
    
    def _get_default_palindrome_data(self) -> Dict[str, Any]:
        """Get default palindrome test data following the coding guidelines."""
        return {
            "number_palindromes": [121, 1221, 12321, 7, 0],
            "string_palindromes": ["racecar", "level", "A man a plan a canal Panama"],
            "non_palindromes": [123, "hello", "world"],
            "edge_cases": [-121, "", "a"],
            "generation_timestamp": datetime.now().isoformat()
        }
    
    def process_data_with_validation(self, data: Any, data_type: str = "mixed") -> Dict[str, Any]:
        """
        Process data with comprehensive validation and consistent error handling.
        
        Args:
            data: Data to process for palindrome validation
            data_type: Type of data being processed
            
        Returns:
            Dict containing processing results
        """
        try:
            result = self.processor.process_data(data)
            
            if result:
                print(self.formatter.success(f"Processing successful for {data_type}"))
                if isinstance(result, dict) and 'processed_at' in result:
                    print(f"   ⏱️ Processing completed at: {result['processed_at']}")
                if isinstance(result, dict) and 'palindrome_count' in result:
                    print(f"   🎯 Palindromes found: {result['palindrome_count']}")
                return result
            else:
                print(self.formatter.error(f"Processing failed for {data_type}"))
                return {"status": "failed", "data_type": data_type}
                
        except (ValidationError, MappingError) as processing_error:
            print(self.formatter.error(f"Processing error for {data_type}: {processing_error}"))
            return {"status": "error", "error": str(processing_error), "data_type": data_type}
        except Exception as unexpected_error:
            print(self.formatter.error(f"Unexpected error during processing: {unexpected_error}"))
            return {"status": "error", "error": str(unexpected_error), "data_type": data_type}


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


def run_optimized_example():
    """
    Run optimized example processing using helper classes to eliminate redundancy.
    
    Demonstrates palindrome validation with streamlined code structure
    following the project's coding guidelines.
    """
    formatter = MessageFormatter()
    helper = ProcessorHelper()
    
    print(formatter.section_header("🎯 AIM - Actuarial Input Mapper - Example Usage"))
    
    # Initialize processor
    print("\n1. Initializing AIM Processor...")
    if not helper.initialize_processor():
        return
    
    # Get supported products
    print("\n2. Checking supported products...")
    supported_products = helper.get_supported_products()
    
    # Load sample data
    print("\n3. Loading sample palindrome data...")
    sample_file = os.path.join("data", "sample", "life_insurance_sample.json")
    palindrome_data = helper.load_sample_data(sample_file)
    
    # Process different data types
    print(formatter.subsection_header("4. Processing palindrome data categories"))
    
    data_categories = [
        ("Number Palindromes", palindrome_data.get("number_palindromes", [121, 1221, 123])),
        ("String Palindromes", palindrome_data.get("string_palindromes", ["racecar", "hello"])),
        ("Edge Cases", palindrome_data.get("edge_cases", [-121, "", "a"]))
    ]
    
    all_results = {}
    for category_name, category_data in data_categories:
        print(f"\n   Processing {category_name}...")
        result = helper.process_data_with_validation(category_data, category_name)
        all_results[category_name] = result
    
    # Show final summary
    print(formatter.section_header("📋 Final Processing Summary"))
    successful_categories = sum(1 for result in all_results.values() 
                              if isinstance(result, dict) and result.get("status") != "failed")
    print(formatter.info(f"Successfully processed {successful_categories}/{len(data_categories)} categories"))
    
    return all_results


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
        print("1. Process palindrome data")
        print("2. Enter custom data")
        print("3. Show data statistics")
        print("4. Exit")
        return input("\nEnter your choice (1-4): ").strip()
    
    while True:
        show_current_status()
        choice = get_user_choice()
        
        if choice == "1":
            # Sample palindrome processing
            sample_data = [121, "racecar", 123, "hello", 1221, "level"]
            print(formatter.subsection_header("Processing sample palindrome data"))
            result = helper.process_data_with_validation(sample_data, "sample_mixed")
            user_data_store.append(result)
            
        elif choice == "2":
            # Custom data entry
            print("\n📝 Enter your data (JSON format or simple values):")
            print("Example: [121, \"racecar\", 123] or just: racecar")
            
            user_input = input("Data: ").strip()
            if user_input:
                try:
                    # Try JSON first
                    try:
                        custom_data = json.loads(user_input)
                    except json.JSONDecodeError:
                        # Treat as simple string or number
                        try:
                            custom_data = int(user_input)
                        except ValueError:
                            custom_data = user_input
                    
                    result = helper.process_data_with_validation(custom_data, "custom")
                    user_data_store.append(result)
                    
                except Exception as error:
                    print(formatter.error(f"Error processing custom data: {error}"))
        
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
    following the palindrome project guidelines.
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
                    CREATE TABLE IF NOT EXISTS palindrome_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_hash TEXT UNIQUE,
                        data_json TEXT,
                        data_type TEXT,
                        timestamp TEXT,
                        is_palindrome BOOLEAN,
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
                    INSERT OR REPLACE INTO palindrome_data 
                    (data_hash, data_json, data_type, timestamp, is_palindrome, processing_result)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    data_hash,
                    json.dumps(data, default=str),
                    data_type,
                    datetime.now().isoformat(),
                    result.get('is_palindrome', False),
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
                cursor.execute("SELECT COUNT(*) FROM palindrome_data")
                total_count = cursor.fetchone()[0]
                
                # Get palindrome count
                cursor.execute("SELECT COUNT(*) FROM palindrome_data WHERE is_palindrome = 1")
                palindrome_count = cursor.fetchone()[0]
                
                # Get by data type
                cursor.execute("SELECT data_type, COUNT(*) FROM palindrome_data GROUP BY data_type")
                type_counts = dict(cursor.fetchall())
                
                return {
                    "total_processed": total_count,
                    "palindromes_found": palindrome_count,
                    "palindrome_percentage": round((palindrome_count / total_count) * 100, 2) if total_count > 0 else 0,
                    "by_data_type": type_counts,
                    "last_updated": datetime.now().isoformat()
                }
                
        except Exception as error:
            print(self.formatter.error(f"Error getting statistics: {error}"))
            return {"error": str(error)}


def main():
    """
    Main function with optimized structure and eliminated redundancy.
    
    Demonstrates the improved code structure following DRY principles
    and the palindrome checking coding guidelines.
    """
    formatter = MessageFormatter()
    
    print(formatter.section_header("🚀 Starting AIM Optimized Examples"))
    
    try:
        # Run optimized example
        results = run_optimized_example()
        
        # Ask for interactive demo
        response = input("\n🎮 Would you like to try the interactive demo? (y/n): ").strip().lower()
        
        if response in ['y', 'yes']:
            run_interactive_demo()
        
        # Show final statistics if we have results
        if results:
            data_manager = OptimizedDataManager()
            
            # Save all results to database
            for category, result in results.items():
                if isinstance(result, dict) and result.get("status") != "failed":
                    data_manager.save_processing_result(
                        category, 
                        "category_processing", 
                        result
                    )
            
            # Show final statistics
            stats = data_manager.get_processing_statistics()
            print(formatter.section_header("📊 Final Statistics"))
            print(formatter.info(f"Total processed: {stats.get('total_processed', 0)}"))
            print(formatter.info(f"Palindromes found: {stats.get('palindromes_found', 0)}"))
            print(formatter.info(f"Success rate: {stats.get('palindrome_percentage', 0)}%"))
        
    except KeyboardInterrupt:
        print(formatter.warning("\nExample terminated by user"))
    except Exception as error:
        print(formatter.error(f"Example failed with error: {error}"))
        import traceback
        traceback.print_exc()
    
    print(formatter.section_header("🏁 Example completed"))


if __name__ == "__main__":
    main()
