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

    # ...existing code for all other methods (enter_custom_data, bulk_json_load, show_field_mapping, show_stored_data, show_duplicate_check, show_help, clear_database, etc.)...

    def run(self):
        """Start the GUI application."""
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.root.mainloop()

if __name__ == "__main__":
    gui = AIMDemoGUI()
    gui.run()
