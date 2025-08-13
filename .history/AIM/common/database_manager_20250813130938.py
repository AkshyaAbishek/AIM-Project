"""
Database Utilities - Common database operations
"""
import sqlite3
import json
import hashlib
from datetime import datetime
from tkinter import messagebox


class DatabaseManager:
    """Handles all database operations for the AIM application"""
    
    def __init__(self, db_path="aim_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_type TEXT NOT NULL,
                    data TEXT NOT NULL,
                    data_hash TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
    
    def get_data_hash(self, data):
        """Generate MD5 hash for data to prevent duplicates."""
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_string.encode()).hexdigest()
    
    def save_data(self, data, product_type):
        """Save data to database with duplicate prevention."""
        try:
            data_hash = self.get_data_hash(data)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check for duplicates
            cursor.execute('SELECT id FROM user_data WHERE data_hash = ?', (data_hash,))
            if cursor.fetchone():
                conn.close()
                return False, f"⚠️ Duplicate data detected! This exact data already exists in the database."
            
            # Insert new data
            cursor.execute('''
                INSERT INTO user_data (product_type, data, data_hash, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (product_type, json.dumps(data), data_hash, timestamp))
            
            conn.commit()
            conn.close()
            return True, "Data saved successfully!"
            
        except sqlite3.IntegrityError:
            return False, "Data already exists in database (duplicate detected)."
        except Exception as e:
            return False, f"Database error: {e}"
    
    def load_all_data(self):
        """Load all data from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT product_type, data, timestamp 
                FROM user_data 
                ORDER BY timestamp DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            data_store = []
            for row in rows:
                product_type, data_json, timestamp = row
                data_store.append({
                    'product_type': product_type,
                    'data': json.loads(data_json),
                    'timestamp': timestamp
                })
            
            return data_store
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")
            return []
    
    def get_database_stats(self):
        """Get database statistics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total count
            cursor.execute('SELECT COUNT(*) FROM user_data')
            total_count = cursor.fetchone()[0]
            
            # Count by product type
            cursor.execute('''
                SELECT product_type, COUNT(*) 
                FROM user_data 
                GROUP BY product_type
            ''')
            by_product = dict(cursor.fetchall())
            
            conn.close()
            return total_count, by_product
            
        except Exception as e:
            print(f"Database stats error: {e}")
            return 0, {}
    
    def clear_database(self):
        """Clear all data from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_data')
            conn.commit()
            conn.close()
            return True, "Database cleared successfully!"
        except Exception as e:
            return False, f"Error clearing database: {e}"
    
    def search_data(self, search_term, field_filter=None):
        """Search data based on content or field."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if field_filter:
                cursor.execute('''
                    SELECT product_type, data, timestamp 
                    FROM user_data 
                    WHERE product_type = ? AND data LIKE ?
                    ORDER BY timestamp DESC
                ''', (field_filter, f'%{search_term}%'))
            else:
                cursor.execute('''
                    SELECT product_type, data, timestamp 
                    FROM user_data 
                    WHERE data LIKE ?
                    ORDER BY timestamp DESC
                ''', (f'%{search_term}%',))
            
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                product_type, data_json, timestamp = row
                results.append({
                    'product_type': product_type,
                    'data': json.loads(data_json),
                    'timestamp': timestamp
                })
            
            return results
            
        except Exception as e:
            return []
    
    def check_duplicate_names(self, data_store):
        """Check for duplicate names in the stored data."""
        name_occurrences = {}
        duplicates = []
        
        for i, data_entry in enumerate(data_store, 1):
            data = data_entry['data']
            
            # Look for common name fields
            first_name = data.get('applicant_first_name', data.get('first_name', ''))
            last_name = data.get('applicant_last_name', data.get('last_name', ''))
            
            if first_name and last_name:
                full_name = f"{first_name} {last_name}".lower()
                
                if full_name in name_occurrences:
                    name_occurrences[full_name].append((i, data_entry))
                else:
                    name_occurrences[full_name] = [(i, data_entry)]
        
        # Find duplicates
        for name, entries in name_occurrences.items():
            if len(entries) > 1:
                duplicates.append((name, entries))
        
        return duplicates
