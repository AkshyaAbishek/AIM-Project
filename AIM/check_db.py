import sqlite3
import os

def check_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('aim_data.db')
        cursor = conn.cursor()
        
        # Get table schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='user_data'")
        schema = cursor.fetchone()
        print("Table Schema:")
        print(schema[0] if schema else "Table not found!")
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()
        print(f"\nTotal Records: {count[0]}")
        
        # Get sample records
        cursor.execute("SELECT * FROM user_data LIMIT 3")
        records = cursor.fetchall()
        if records:
            columns = [description[0] for description in cursor.description]
            print("\nColumns:", columns)
            print("\nSample Records:")
            for record in records:
                print(record)
                
        conn.close()
        print("\nDatabase check completed successfully!")
        
    except Exception as e:
        print(f"Error checking database: {str(e)}")

if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    check_database()
