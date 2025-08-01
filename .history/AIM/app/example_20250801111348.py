"""
AIM - Actuarial Input Mapper Interactive Demo

This module provides a modern GUI-based demo for the AIM processor, allowing users to easily map and process their FAST UI data inputs.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import sys
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Any

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from aim_processor import AIMProcessor

class AIMDemoGUI:
    """GUI-based interactive demo for AIM processor."""
    def __init__(self):
        self.processor = AIMProcessor()
        self.user_data_store = []
        self.root = tk.Tk()
        self.root.title("AIM - Actuarial Input Mapper Demo")
        self.root.geometry("850x650")
        self.db_path = "aim_data.db"
        self.init_database()
        self.load_data_from_db()
        self.setup_ui()

    def init_database(self):
        """Initialize the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_hash TEXT UNIQUE,
                    product_type TEXT NOT NULL,
                    json_data TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

    def get_data_hash(self, data_dict):
        """Generate a hash for the data to check for duplicates."""
        return str(hash(json.dumps(data_dict, sort_keys=True)))

    def save_data_to_db(self, data, product_type):
        """Save data to database, checking for duplicates."""
        try:
            data_hash = self.get_data_hash(data)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM user_data WHERE data_hash = ?', (data_hash,))
            existing = cursor.fetchone()
            if existing:
                conn.close()
                return False, "This data already exists in the database."
            cursor.execute('''
                INSERT INTO user_data (data_hash, product_type, json_data, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (data_hash, product_type, json.dumps(data), timestamp))
            conn.commit()
            conn.close()
            return True, "Data saved successfully to database."
        except Exception as e:
            return False, f"Database error: {e}"

    def load_data_from_db(self):
        """Load all data from database into memory."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT product_type, json_data, timestamp FROM user_data ORDER BY created_at')
            rows = cursor.fetchall()
            self.user_data_store = []
            for row in rows:
                self.user_data_store.append({
                    'product_type': row[0],
                    'data': json.loads(row[1]),
                    'timestamp': row[2]
                })
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")

    def get_db_stats(self):
        """Get database statistics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM user_data')
            total_count = cursor.fetchone()[0]
            cursor.execute('SELECT product_type, COUNT(*) FROM user_data GROUP BY product_type')
            by_product = cursor.fetchall()
            conn.close()
            return total_count, dict(by_product)
        except Exception as e:
            return 0, {}

    def update_db_stats(self):
        """Update database statistics display."""
        total_count, by_product = self.get_db_stats()
        if total_count > 0:
            product_info = ", ".join([f"{prod}: {count}" for prod, count in by_product.items()])
            self.db_stats_var.set(f"💾 Database: {total_count} total records ({product_info})")
        else:
            self.db_stats_var.set("💾 Database: Empty")

    def setup_ui(self):
        """Set up the main user interface with enhanced styling."""
        self.root.configure(bg="#f0f4f8")
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill="x", pady=0)
        title_frame.pack_propagate(False)
        title_label = tk.Label(title_frame, text="🎮 AIM Interactive Demo", font=("Segoe UI", 20, "bold"), fg="#ecf0f1", bg="#2c3e50")
        title_label.pack(expand=True)
        subtitle_label = tk.Label(title_frame, text="Actuarial Input Mapper - Professional Edition", font=("Segoe UI", 10), fg="#bdc3c7", bg="#2c3e50")
        subtitle_label.pack()
        status_frame = tk.Frame(self.root, bg="#ecf0f1", relief="flat", bd=1)
        status_frame.pack(fill="x", padx=20, pady=10)
        self.status_var = tk.StringVar()
        self.update_status()
        status_label = tk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 11), fg="#2c3e50", bg="#ecf0f1")
        status_label.pack(pady=8)
        self.db_stats_var = tk.StringVar()
        self.update_db_stats()
        db_stats_label = tk.Label(status_frame, textvariable=self.db_stats_var, font=("Segoe UI", 10), fg="#27ae60", bg="#ecf0f1")
        db_stats_label.pack(pady=2)
        buttons_container = tk.Frame(self.root, bg="#f0f4f8")
        buttons_container.pack(pady=10, padx=20, fill="x")
        buttons_header = tk.Label(buttons_container, text="📋 Select an Operation", font=("Segoe UI", 12, "bold"), fg="#2c3e50", bg="#f0f4f8")
        buttons_header.pack(pady=(0, 8))
        buttons_frame = tk.Frame(buttons_container, bg="#ffffff", relief="raised", bd=1)
        buttons_frame.pack(pady=5, padx=10, fill="x")
        buttons_frame.configure(bg="#ffffff", padx=10, pady=10)
        self.create_button(buttons_frame, "📝 Add JSON Data", self.enter_custom_data, 0, 0, "#3498db", "#2980b9")
        self.create_button(buttons_frame, "📦 Bulk JSON Load", self.bulk_json_load, 0, 1, "#9b59b6", "#8e44ad")
        self.create_button(buttons_frame, "📊 Life Field Mapping", lambda: self.show_field_mapping("life"), 0, 2, "#e67e22", "#d35400")
        self.create_button(buttons_frame, "📋 View Stored Data", self.show_stored_data, 1, 0, "#1abc9c", "#16a085")
        self.create_button(buttons_frame, "🔍 Check Duplicates", self.show_duplicate_check, 1, 1, "#f39c12", "#e67e22")
        self.create_button(buttons_frame, "📊 Annuity Field Mapping", lambda: self.show_field_mapping("annuity"), 1, 2, "#8e44ad", "#7d3c98")
        self.create_button(buttons_frame, "❓ Help", self.show_help, 2, 0, "#34495e", "#2c3e50")
        self.create_button(buttons_frame, "🗑️ Clear Database", self.clear_database, 2, 1, "#e74c3c", "#c0392b")
        results_container = tk.Frame(self.root, bg="#f0f4f8")
        results_container.pack(padx=20, pady=(5, 15), fill="both", expand=True)
        results_header_frame = tk.Frame(results_container, bg="#34495e", height=35)
        results_header_frame.pack(fill="x")
        results_header_frame.pack_propagate(False)
        results_label = tk.Label(results_header_frame, text="📄 Results & Output", font=("Segoe UI", 11, "bold"), fg="#ecf0f1", bg="#34495e")
        results_label.pack(expand=True)
        text_frame = tk.Frame(results_container, bg="#ffffff", relief="sunken", bd=1)
        text_frame.pack(fill="both", expand=True)
        self.results_text = scrolledtext.ScrolledText(text_frame, height=12, width=80, font=("Consolas", 9), bg="#ffffff", fg="#2c3e50", insertbackground="#2c3e50", selectbackground="#3498db", relief="flat", bd=5)
        self.results_text.pack(padx=8, pady=8, fill="both", expand=True)
        self.log_result("🎉 Welcome to AIM - Actuarial Input Mapper!")
        self.log_result("=" * 50)
        self.log_result("Select an operation from the buttons above to get started.")
        self.log_result("💡 Tip: Use 'Help' for detailed guidance on each feature.")

    def update_status(self):
        """Update the status display."""
        if self.user_data_store:
            self.status_var.set(f"📊 Current session: {len(self.user_data_store)} datasets loaded from database")
        else:
            self.status_var.set("📊 No data loaded from database yet")

    def create_button(self, parent, text, command, row, col, bg_color="#3498db", hover_color="#2980b9"):
        """Create a styled button with hover effects and modern design."""
        btn = tk.Button(parent, text=text, command=command, font=("Segoe UI", 11),
                        bg=bg_color, fg="#ffffff", activebackground=hover_color, activeforeground="#ffffff",
                        relief="raised", bd=2, padx=12, pady=6, cursor="hand2")
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        def on_enter(e):
            btn['bg'] = hover_color
        def on_leave(e):
            btn['bg'] = bg_color
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def log_result(self, message):
        """Add a message to the results area."""
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)

    def clear_results(self):
        """Clear the results area."""
        self.results_text.delete(1.0, tk.END)

    def enter_custom_data(self):
        """Handle entering custom JSON data (save only, no processing)."""
        dialog = tk.Toplevel(self.root)
        dialog.title("📝 Add JSON Data")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Product type selection
        tk.Label(dialog, text="Product Type:", font=("Arial", 12, "bold")).pack(pady=10)
        product_var = tk.StringVar(value="life")
        product_frame = tk.Frame(dialog)
        product_frame.pack(pady=5)
        
        tk.Radiobutton(product_frame, text="Life Insurance", variable=product_var, value="life").pack(side="left", padx=10)
        tk.Radiobutton(product_frame, text="Annuity", variable=product_var, value="annuity").pack(side="left", padx=10)
        tk.Radiobutton(product_frame, text="Health", variable=product_var, value="health").pack(side="left", padx=10)
        
        # JSON input area
        tk.Label(dialog, text="JSON Data:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
        text_area = scrolledtext.ScrolledText(dialog, width=70, height=20, font=("Consolas", 10))
        text_area.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Sample data
        sample_data = {
            "applicant_first_name": "John",
            "applicant_last_name": "Doe",
            "date_of_birth": "1980-01-15",
            "gender": "M",
            "coverage_amount": 250000,
            "premium_amount": 150.50
        }
        text_area.insert(tk.END, json.dumps(sample_data, indent=2))
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def save_data():
            try:
                json_text = text_area.get(1.0, tk.END).strip()
                data = json.loads(json_text)
                success, message = self.save_data_to_db(data, product_var.get())
                if success:
                    self.load_data_from_db()
                    self.update_status()
                    self.update_db_stats()
                    self.log_result(f"✅ {message}")
                    dialog.destroy()
                else:
                    messagebox.showwarning("Duplicate Data", message)
            except json.JSONDecodeError as e:
                messagebox.showerror("JSON Error", f"Invalid JSON format: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {e}")
        
        tk.Button(button_frame, text="💾 Save to Database", command=save_data, 
                 bg="#27ae60", fg="white", font=("Arial", 11)).pack(side="left", padx=10)
        tk.Button(button_frame, text="❌ Cancel", command=dialog.destroy, 
                 bg="#e74c3c", fg="white", font=("Arial", 11)).pack(side="left", padx=10)

    def bulk_json_load(self):
        """Handle bulk JSON data loading via Excel template."""
        messagebox.showinfo("Feature", "Bulk JSON Load feature - Coming soon!")

    def show_field_mapping(self, product_type):
        """Create Excel field mapping template for FAST UI to Actuarial Calculator mapping."""
        try:
            import pandas as pd
        except ImportError:
            messagebox.showerror("Missing Module", 
                               "pandas module is required for Excel operations.\n"
                               "Please install it using: pip install pandas openpyxl")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title(f"📊 {product_type.title()} Field Mapping")
        dialog.geometry("700x550")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#f8f9fa")
        
        # Header
        header_frame = tk.Frame(dialog, bg="#34495e", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"📊 Excel Field Mapping - {product_type.title()}", 
                font=("Segoe UI", 14, "bold"), fg="#ecf0f1", bg="#34495e").pack(expand=True)
        
        # Main content
        content_frame = tk.Frame(dialog, bg="#f8f9fa")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = tk.Text(content_frame, height=8, width=70, wrap=tk.WORD)
        instructions.pack(pady=10, padx=20, fill="both", expand=True)
        
        instructions.insert(tk.END, "📋 Instructions:\n\n")
        instructions.insert(tk.END, "1. Choose where to save the new Excel mapping file\n")
        instructions.insert(tk.END, "2. Select your existing Actuarial Calculator Excel file\n")
        instructions.insert(tk.END, "3. The system will create a mapping template with 4 columns:\n")
        instructions.insert(tk.END, "   • FAST UI Field: Source field names\n")
        instructions.insert(tk.END, "   • FAST UI Value: Sample values from your data\n")
        instructions.insert(tk.END, "   • Actuarial Field: Target fields from calculator\n")
        instructions.insert(tk.END, "   • Actuarial Value: Mapped values for calculator\n\n")
        instructions.insert(tk.END, "4. You can manually complete the mapping in Excel")
        instructions.config(state=tk.DISABLED)
        
        # Path selection
        paths_frame = tk.Frame(content_frame, bg="#f8f9fa")
        paths_frame.pack(pady=20, padx=20, fill="x")
        
        # Output Excel path
        tk.Label(paths_frame, text="1. Output Excel File Path:", 
                font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        output_frame = tk.Frame(paths_frame)
        output_frame.pack(fill="x", pady=(0, 15))
        
        output_path_var = tk.StringVar()
        tk.Entry(output_frame, textvariable=output_path_var, width=60, 
                font=("Segoe UI", 9), relief="solid", bd=1).pack(side="left", padx=(0, 5))
        
        tk.Button(output_frame, text="📁 Browse", 
                 command=lambda: self.browse_save_excel(output_path_var),
                 bg="#2196F3", fg="white").pack(side="left")
        
        # Calculator Excel path
        tk.Label(paths_frame, text="2. Actuarial Calculator Excel Path:", 
                font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        calc_frame = tk.Frame(paths_frame)
        calc_frame.pack(fill="x", pady=(0, 15))
        
        calculator_path_var = tk.StringVar()
        tk.Entry(calc_frame, textvariable=calculator_path_var, width=60, 
                font=("Segoe UI", 9), relief="solid", bd=1).pack(side="left", padx=(0, 5))
        
        tk.Button(calc_frame, text="📁 Browse", 
                 command=lambda: self.browse_open_excel(calculator_path_var),
                 bg="#2196F3", fg="white").pack(side="left")
        
        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(pady=10)
        
        def create_mapping():
            output_path = output_path_var.get().strip()
            calculator_path = calculator_path_var.get().strip()
            
            if not output_path:
                messagebox.showerror("Error", "Please select output Excel file path")
                return
            
            if not calculator_path:
                messagebox.showerror("Error", "Please select actuarial calculator Excel file")
                return
            
            dialog.destroy()
            self.create_excel_mapping(product_type.lower(), output_path, calculator_path)
        
        tk.Button(button_frame, text="📊 Create Mapping", command=create_mapping,
                 bg="#27ae60", fg="white", font=("Arial", 11)).pack(side="left", padx=8)
        
        tk.Button(button_frame, text="❌ Cancel", command=dialog.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 11)).pack(side="left", padx=8)

    def show_stored_data(self):
        """Show stored user data with search functionality."""
        if not self.user_data_store:
            messagebox.showinfo("No Data", "No user data stored yet. Use 'Add JSON Data' to add data.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("📋 Database Records")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        tk.Label(dialog, text="📋 Stored Database Records", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Data display area
        text_area = scrolledtext.ScrolledText(dialog, width=90, height=30, font=("Consolas", 9))
        text_area.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Display all data
        for i, entry in enumerate(self.user_data_store, 1):
            text_area.insert(tk.END, f"{i}. Product Type: {entry['product_type']}\n")
            text_area.insert(tk.END, f"   Timestamp: {entry['timestamp']}\n")
            text_area.insert(tk.END, f"   Data: {json.dumps(entry['data'], indent=2)}\n")
            text_area.insert(tk.END, "-" * 60 + "\n")
        
        # Close button
        tk.Button(dialog, text="✅ Close", command=dialog.destroy, 
                 bg="#27ae60", fg="white", font=("Arial", 11)).pack(pady=10)

    def show_duplicate_check(self):
        """Show duplicate name checker dialog."""
        messagebox.showinfo("Feature", "Duplicate Check feature - Coming soon!")

    def show_help(self):
        """Show help dialog."""
        help_text = """
🎮 AIM Interactive Demo - Help

📝 Add JSON Data: Enter custom JSON data and save to database
📦 Bulk JSON Load: Load multiple records via Excel template  
📊 Field Mapping: Create Excel mapping templates
📋 View Stored Data: Display all saved records
🔍 Check Duplicates: Find duplicate entries
🗑️ Clear Database: Remove all stored data

💡 Tips:
- Data is automatically saved to SQLite database
- Use valid JSON format when entering data
- All operations are logged in the results area
        """
        messagebox.showinfo("Help", help_text)

    def clear_database(self):
        """Clear all data from the database."""
        result = messagebox.askyesno("Clear Database", 
                                   "Are you sure you want to clear all data?\nThis action cannot be undone.")
        if result:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM user_data')
                conn.commit()
                conn.close()
                
                self.load_data_from_db()
                self.update_status()
                self.update_db_stats()
                self.clear_results()
                self.log_result("🗑️ Database cleared successfully!")
                messagebox.showinfo("Success", "Database cleared successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to clear database: {e}")
    # ...existing code...
    def run(self):
        """Start the GUI application."""
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.root.mainloop()

if __name__ == "__main__":
    gui = AIMDemoGUI()
    gui.run()
