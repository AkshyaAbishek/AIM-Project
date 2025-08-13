"""
AIM - Actuarial Input Mapper GUI Application

This module provides a modern GUI interface for the palindrome validation system
following the project's coding guidelines with proper scroll bar controls.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Union, Any
import threading

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from aim_processor import AIMProcessor, ValidationError, MappingError
except ImportError as import_error:
    print(f"Import Error: {import_error}")
    sys.exit(1)


class PalindromeGUI:
    """
    Main GUI class for AIM Palindrome Processor.
    
    Provides a modern interface with proper scroll bar controls for palindrome
    validation following the project's coding guidelines for both number palindromes
    (121, 1221) and string palindromes ("racecar", "A man a plan a canal Panama").
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the GUI application with proper scroll bar configuration.
        
        Args:
            root: The main tkinter window
        """
        self.root = root
        self.processor = AIMProcessor()
        self.setup_main_window()
        self.create_main_interface()
        
    def setup_main_window(self) -> None:
        """Set up the main window with proper styling and scroll bar controls."""
        self.root.title("AIM - Actuarial Input Mapper - Palindrome Processor")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure style for modern appearance
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors following professional guidelines
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'background': '#F5F5F5',
            'text': '#333333'
        }
        
    def create_main_interface(self) -> None:
        """Create the main interface with tabs and scroll bar controls."""
        # Create main container with auto scroll bars
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create title header
        title_label = ttk.Label(
            main_frame, 
            text="🎯 AIM - Palindrome Processor", 
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Create notebook for tabs (main pages and sub pages)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs with scroll bar controls
        self.create_single_check_tab()
        self.create_batch_processing_tab()
        self.create_comprehensive_analysis_tab()
        self.create_settings_tab()
        
    def create_single_check_tab(self) -> None:
        """Create single palindrome check tab with auto scroll bars."""
        # Main tab frame
        single_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(single_frame, text="🔍 Single Check")
        
        # Configure grid
        single_frame.columnconfigure(0, weight=1)
        single_frame.rowconfigure(2, weight=1)
        
        # Input section
        input_label = ttk.Label(single_frame, text="Enter number or string to check for palindrome:", font=('Arial', 12))
        input_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.single_input = ttk.Entry(single_frame, font=('Arial', 11))
        self.single_input.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.single_input.bind('<Return>', lambda e: self.check_single_palindrome())
        
        # Buttons frame
        button_frame = ttk.Frame(single_frame)
        button_frame.grid(row=1, column=1, padx=(10, 0), pady=(0, 10))
        
        check_button = ttk.Button(
            button_frame, 
            text="Check Palindrome",
            command=self.check_single_palindrome
        )
        check_button.grid(row=0, column=0, pady=(0, 5))
        
        clear_button = ttk.Button(
            button_frame,
            text="Clear Results",
            command=self.clear_single_results
        )
        clear_button.grid(row=1, column=0)
        
        # Results section with auto scroll bars
        results_label = ttk.Label(single_frame, text="Results:", font=('Arial', 12, 'bold'))
        results_label.grid(row=2, column=0, columnspan=2, sticky=(tk.W), pady=(10, 5))
        
        # ScrolledText with auto scroll bars (only show when needed)
        self.single_results = scrolledtext.ScrolledText(
            single_frame,
            wrap=tk.WORD,
            height=20,
            font=('Consolas', 10),
            state=tk.DISABLED
        )
        self.single_results.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
    def create_batch_processing_tab(self) -> None:
        """Create batch processing tab with comprehensive scroll bar controls."""
        # Main tab frame
        batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(batch_frame, text="📊 Batch Processing")
        
        # Configure grid for responsive design
        batch_frame.columnconfigure(0, weight=1)
        batch_frame.columnconfigure(1, weight=1)
        batch_frame.rowconfigure(3, weight=1)
        
        # Input section
        ttk.Label(batch_frame, text="Batch Palindrome Processing", font=('Arial', 14, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E)
        )
        
        # Left panel - Input
        input_frame = ttk.LabelFrame(batch_frame, text="Input Data", padding="5")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Enter numbers/strings (one per line):").grid(
            row=0, column=0, sticky=(tk.W), pady=(0, 5)
        )
        
        # Input text area with auto scroll bars
        self.batch_input = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=15,
            font=('Consolas', 10)
        )
        self.batch_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Right panel - Controls and quick examples
        control_frame = ttk.LabelFrame(batch_frame, text="Controls & Examples", padding="5")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Process button
        process_button = ttk.Button(
            control_frame,
            text="🚀 Process All",
            command=self.process_batch_palindromes
        )
        process_button.grid(row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Load file button
        load_button = ttk.Button(
            control_frame,
            text="📁 Load from File",
            command=self.load_batch_file
        )
        load_button.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Example data buttons
        ttk.Label(control_frame, text="Quick Examples:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, pady=(10, 5), sticky=(tk.W)
        )
        
        ttk.Button(control_frame, text="Number Palindromes", 
                  command=self.load_number_examples).grid(row=3, column=0, pady=(0, 5), sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="String Palindromes", 
                  command=self.load_string_examples).grid(row=4, column=0, pady=(0, 5), sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="Mixed Examples", 
                  command=self.load_mixed_examples).grid(row=5, column=0, pady=(0, 5), sticky=(tk.W, tk.E))
        
        # Results section with auto scroll bars
        results_frame = ttk.LabelFrame(batch_frame, text="Processing Results", padding="5")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results display with auto scroll bars
        self.batch_results = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            height=12,
            font=('Consolas', 9),
            state=tk.DISABLED
        )
        self.batch_results.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_comprehensive_analysis_tab(self) -> None:
        """Create comprehensive analysis tab with JSON display and auto scroll bars."""
        # Main tab frame
        analysis_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(analysis_frame, text="📋 Analysis & JSON")
        
        # Configure grid
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(2, weight=1)
        
        # Header
        ttk.Label(analysis_frame, text="Comprehensive Palindrome Analysis", font=('Arial', 14, 'bold')).grid(
            row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E)
        )
        
        # Analysis controls
        control_frame = ttk.Frame(analysis_frame)
        control_frame.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="🔍 Generate Sample Analysis", 
                  command=self.generate_comprehensive_analysis).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(control_frame, text="💾 Export JSON", 
                  command=self.export_analysis_json).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="🧹 Clear Analysis", 
                  command=self.clear_analysis).grid(row=0, column=2)
        
        # Analysis display with auto scroll bars
        self.analysis_display = scrolledtext.ScrolledText(
            analysis_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            state=tk.DISABLED
        )
        self.analysis_display.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_settings_tab(self) -> None:
        """Create settings tab for configuration options."""
        # Main tab frame
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Palindrome checking options
        options_frame = ttk.LabelFrame(settings_frame, text="Palindrome Check Options", padding="10")
        options_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Case sensitivity
        self.ignore_case = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Ignore case differences", 
                       variable=self.ignore_case).grid(row=0, column=0, sticky=(tk.W), pady=(0, 5))
        
        # Space handling
        self.ignore_spaces = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Ignore spaces", 
                       variable=self.ignore_spaces).grid(row=1, column=0, sticky=(tk.W), pady=(0, 5))
        
        # Punctuation handling
        self.ignore_punctuation = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Ignore punctuation", 
                       variable=self.ignore_punctuation).grid(row=2, column=0, sticky=(tk.W), pady=(0, 5))
        
        # Display options
        display_frame = ttk.LabelFrame(settings_frame, text="Display Options", padding="10")
        display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # JSON formatting
        self.format_json = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_frame, text="Format JSON output", 
                       variable=self.format_json).grid(row=0, column=0, sticky=(tk.W), pady=(0, 5))
        
        # Show timestamps
        self.show_timestamps = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_frame, text="Show processing timestamps", 
                       variable=self.show_timestamps).grid(row=1, column=0, sticky=(tk.W), pady=(0, 5))
        
        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About AIM Palindrome Processor", padding="10")
        about_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        about_text = """AIM - Actuarial Input Mapper
Palindrome Processor v1.0

Features:
• Number palindromes (121, 1221)
• String palindromes ("racecar", "A man a plan a canal Panama")
• Efficient string slicing algorithms
• Edge case handling (empty strings, negatives)
• Comprehensive JSON analysis
• Auto scroll bars throughout interface"""
        
        ttk.Label(about_frame, text=about_text, justify=tk.LEFT).grid(row=0, column=0, sticky=(tk.W))
        
    def check_single_palindrome(self) -> None:
        """Check single palindrome input and display results with JSON."""
        input_text = self.single_input.get().strip()
        
        if not input_text:
            messagebox.showwarning("Input Required", "Please enter a number or string to check.")
            return
            
        try:
            # Try to convert to integer first, otherwise treat as string
            try:
                test_value = int(input_text)
            except ValueError:
                test_value = input_text
            
            # Process using AIM processor
            result = self.processor.process_data(test_value)
            
            # Display results
            self.display_single_result(result, test_value)
            
        except (ValidationError, MappingError) as error:
            messagebox.showerror("Processing Error", f"Error processing input: {error}")
        except Exception as error:
            messagebox.showerror("Unexpected Error", f"Unexpected error: {error}")
    
    def display_single_result(self, result: Dict[str, Any], input_value: Union[str, int]) -> None:
        """Display single palindrome result with comprehensive information."""
        self.single_results.config(state=tk.NORMAL)
        self.single_results.delete(1.0, tk.END)
        
        # Header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.single_results.insert(tk.END, f"🎯 AIM Palindrome Analysis - {timestamp}\n")
        self.single_results.insert(tk.END, "=" * 60 + "\n\n")
        
        # Basic result
        is_palindrome = result['is_palindrome']
        status = "✅ IS PALINDROME" if is_palindrome else "❌ NOT PALINDROME"
        self.single_results.insert(tk.END, f"Input: {input_value} ({result['type']})\n")
        self.single_results.insert(tk.END, f"Result: {status}\n\n")
        
        # Additional details
        if result['type'] == 'string' and 'longest_palindrome' in result:
            self.single_results.insert(tk.END, f"Longest palindrome substring: '{result['longest_palindrome']}'\n")
        elif result['type'] == 'number' and result.get('next_palindrome'):
            self.single_results.insert(tk.END, f"Next palindrome: {result['next_palindrome']}\n")
        
        # JSON representation
        self.single_results.insert(tk.END, "\n📋 Complete JSON Analysis:\n")
        self.single_results.insert(tk.END, "-" * 30 + "\n")
        
        if self.format_json.get():
            json_output = json.dumps(result, indent=2, default=str)
        else:
            json_output = json.dumps(result, default=str)
            
        self.single_results.insert(tk.END, json_output)
        self.single_results.insert(tk.END, "\n\n")
        
        self.single_results.config(state=tk.DISABLED)
        
    def clear_single_results(self) -> None:
        """Clear single palindrome results display."""
        self.single_results.config(state=tk.NORMAL)
        self.single_results.delete(1.0, tk.END)
        self.single_results.config(state=tk.DISABLED)
        self.single_input.delete(0, tk.END)
        
    def process_batch_palindromes(self) -> None:
        """Process batch palindromes in a separate thread to avoid UI freezing."""
        input_text = self.batch_input.get(1.0, tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("Input Required", "Please enter data to process.")
            return
        
        # Disable button during processing
        # (You would find the button widget and disable it)
        
        # Process in separate thread
        thread = threading.Thread(target=self._process_batch_worker, args=(input_text,))
        thread.daemon = True
        thread.start()
        
    def _process_batch_worker(self, input_text: str) -> None:
        """Worker function for batch processing."""
        try:
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            
            # Convert to appropriate types
            processed_data = []
            for line in lines:
                try:
                    processed_data.append(int(line))
                except ValueError:
                    processed_data.append(line)
            
            # Process using AIM processor
            result = self.processor.process_data(processed_data)
            
            # Update UI in main thread
            self.root.after(0, self._display_batch_results, result)
            
        except Exception as error:
            self.root.after(0, lambda: messagebox.showerror("Processing Error", str(error)))
    
    def _display_batch_results(self, result: Dict[str, Any]) -> None:
        """Display batch processing results."""
        self.batch_results.config(state=tk.NORMAL)
        self.batch_results.delete(1.0, tk.END)
        
        # Header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.batch_results.insert(tk.END, f"📊 Batch Processing Results - {timestamp}\n")
        self.batch_results.insert(tk.END, "=" * 70 + "\n\n")
        
        # Summary
        self.batch_results.insert(tk.END, f"📝 Total Items: {result['total_items']}\n")
        self.batch_results.insert(tk.END, f"✅ Palindromes Found: {result['palindrome_count']}\n")
        self.batch_results.insert(tk.END, f"📈 Success Rate: {result['palindrome_percentage']}%\n\n")
        
        # Individual results
        self.batch_results.insert(tk.END, "📋 Individual Results:\n")
        self.batch_results.insert(tk.END, "-" * 40 + "\n")
        
        for i, item_result in enumerate(result['results'], 1):
            status = "✅" if item_result['is_palindrome'] else "❌"
            self.batch_results.insert(tk.END, f"{i:2d}. {item_result['input']} → {status}\n")
        
        # Complete JSON if requested
        if self.format_json.get():
            self.batch_results.insert(tk.END, f"\n📋 Complete JSON Analysis:\n")
            self.batch_results.insert(tk.END, "-" * 30 + "\n")
            json_output = json.dumps(result, indent=2, default=str)
            self.batch_results.insert(tk.END, json_output)
        
        self.batch_results.config(state=tk.DISABLED)
        
    def load_number_examples(self) -> None:
        """Load number palindrome examples."""
        examples = "121\n1221\n12321\n123\n1001\n7\n88\n909\n-121\n0"
        self.batch_input.delete(1.0, tk.END)
        self.batch_input.insert(1.0, examples)
        
    def load_string_examples(self) -> None:
        """Load string palindrome examples."""
        examples = """racecar
level
A man a plan a canal Panama
Was it a car or a cat I saw?
hello
world
madam
radar"""
        self.batch_input.delete(1.0, tk.END)
        self.batch_input.insert(1.0, examples)
        
    def load_mixed_examples(self) -> None:
        """Load mixed palindrome examples."""
        examples = """121
racecar
12321
A man a plan a canal Panama
hello
1001
level
123
madam"""
        self.batch_input.delete(1.0, tk.END)
        self.batch_input.insert(1.0, examples)
        
    def load_batch_file(self) -> None:
        """Load batch data from file."""
        file_path = filedialog.askopenfilename(
            title="Load Palindrome Data",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.batch_input.delete(1.0, tk.END)
                    self.batch_input.insert(1.0, content)
            except Exception as error:
                messagebox.showerror("File Error", f"Error loading file: {error}")
                
    def generate_comprehensive_analysis(self) -> None:
        """Generate comprehensive analysis with sample data."""
        sample_data = {
            "numbers": [121, 1221, 123, 1001, 7, 0, -121],
            "strings": ["racecar", "level", "A man a plan a canal Panama", "hello", ""],
            "mixed": [121, "racecar", 123, "hello", 1001, "level"]
        }
        
        # Process each category
        all_results = {}
        for category, data in sample_data.items():
            result = self.processor.process_data(data)
            all_results[category] = result
        
        # Create comprehensive analysis
        comprehensive_analysis = {
            "analysis_timestamp": datetime.now().isoformat(),
            "processor_type": "AIM Palindrome Processor GUI",
            "categories_analyzed": all_results,
            "processor_statistics": self.processor.get_processing_statistics(),
            "gui_settings": {
                "ignore_case": self.ignore_case.get(),
                "ignore_spaces": self.ignore_spaces.get(),
                "ignore_punctuation": self.ignore_punctuation.get(),
                "format_json": self.format_json.get()
            }
        }
        
        # Display in analysis tab
        self.analysis_display.config(state=tk.NORMAL)
        self.analysis_display.delete(1.0, tk.END)
        
        self.analysis_display.insert(tk.END, "🔍 COMPREHENSIVE PALINDROME ANALYSIS\n")
        self.analysis_display.insert(tk.END, "=" * 80 + "\n\n")
        
        json_output = json.dumps(comprehensive_analysis, indent=2, default=str)
        self.analysis_display.insert(tk.END, json_output)
        
        self.analysis_display.config(state=tk.DISABLED)
        
    def export_analysis_json(self) -> None:
        """Export analysis to JSON file."""
        content = self.analysis_display.get(1.0, tk.END).strip()
        
        if not content or content == "":
            messagebox.showwarning("No Data", "No analysis data to export. Generate analysis first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Analysis",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Extract JSON from the display
                lines = content.split('\n')
                json_start = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith('{'):
                        json_start = i
                        break
                
                if json_start >= 0:
                    json_content = '\n'.join(lines[json_start:])
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(json_content)
                    messagebox.showinfo("Export Successful", f"Analysis exported to {file_path}")
                else:
                    messagebox.showerror("Export Error", "Could not find JSON content to export.")
                    
            except Exception as error:
                messagebox.showerror("Export Error", f"Error exporting file: {error}")
                
    def clear_analysis(self) -> None:
        """Clear analysis display."""
        self.analysis_display.config(state=tk.NORMAL)
        self.analysis_display.delete(1.0, tk.END)
        self.analysis_display.config(state=tk.DISABLED)


def main():
    """Main function to launch the AIM Palindrome GUI application."""
    root = tk.Tk()
    app = PalindromeGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
