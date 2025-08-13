import os
import json
import sqlite3
from typing import Dict, Any, List, Optional

class WebDatabaseManager:
    """Database manager for web application"""
    
    def __init__(self, db_path: str = "aim_data.db"):
        # Ensure we're using the correct path
        if not os.path.isabs(db_path):
            db_path = os.path.join(os.path.dirname(__file__), db_path)
        self.db_path = db_path
        print(f"Database path: {self.db_path}")
        self.init_database()
    
    def init_database(self):
        """Initialize database with web-optimized schema"""
        try:
            print(f"Initializing database at: {self.db_path}")
            with sqlite3.connect(self.db_path) as conn:
                # Create user_data table with all fields
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT DEFAULT 'Unnamed Record',
                        product_type TEXT,
                        data_hash TEXT UNIQUE,
                        json_data TEXT,
                        raw_data TEXT,
                        processed_data TEXT,
                        field_mappings TEXT,
                        calculator_path TEXT,
                        source_file TEXT,
                        file_source TEXT,
                        session_id TEXT,
                        source_record_id TEXT,
                        validation_status TEXT DEFAULT 'pending',
                        status TEXT DEFAULT 'pending',
                        quality_score REAL DEFAULT 0.0,
                        processing_notes TEXT,
                        notes TEXT,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create processing_logs table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS processing_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        operation_type TEXT NOT NULL,
                        operation_details TEXT,
                        status TEXT CHECK(status IN ('success', 'warning', 'error')),
                        error_message TEXT,
                        processing_time_ms INTEGER,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        session_id TEXT
                    )
                """)
                
                # Create indexes
                print("Creating indexes...")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_user_data_hash ON user_data(data_hash)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_user_data_session ON user_data(session_id)")
                conn.commit()
            
            print("Database initialization completed successfully")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
            import traceback
            traceback.print_exc()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics for dashboard"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total records
                cursor.execute("SELECT COUNT(*) FROM user_data")
                total_records = cursor.fetchone()[0]
                
                # Records by product type
                cursor.execute("SELECT COALESCE(product_type, 'Unknown'), COUNT(*) FROM user_data GROUP BY product_type")
                product_counts = dict(cursor.fetchall())
                
                # Status counts
                cursor.execute("""
                    SELECT 
                        COALESCE(status, 'pending') as status,
                        COUNT(*) as count
                    FROM user_data 
                    GROUP BY status
                """)
                status_counts = dict(cursor.fetchall())
                
                # Calculate averages
                cursor.execute("SELECT AVG(COALESCE(quality_score, 0)) FROM user_data")
                avg_quality = cursor.fetchone()[0] or 0
                
                # Recent activity (last 24 hours)
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM user_data 
                    WHERE created_date >= datetime('now', '-1 day')
                """)
                recent_activity = cursor.fetchone()[0]
                
                # Processed, pending, error counts
                processed = status_counts.get('processed', 0)
                pending = status_counts.get('pending', 0)
                error = status_counts.get('error', 0)
                
                return {
                    'total_records': total_records,
                    'status_counts': status_counts,
                    'product_distribution': product_counts,
                    'average_quality': round(float(avg_quality), 1),
                    'recent_activity': recent_activity,
                    'processed_records': processed,
                    'pending_records': pending,
                    'error_records': error
                }
                
        except Exception as e:
            print(f"Database error in get_statistics: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            return {
                'total_records': 0,
                'status_counts': {'processed': 0, 'pending': 0, 'error': 0},
                'product_distribution': {},
                'average_quality': 0.0,
                'recent_activity': 0,
                'processed_records': 0,
                'pending_records': 0,
                'error_records': 0
            }
    
    def get_all_data(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all data from the database, optionally filtered by session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build query based on whether session_id is provided
                if session_id:
                    cursor.execute("""
                        SELECT id, name, product_type, json_data, created_date, validation_status,
                               quality_score, status, processing_notes
                        FROM user_data 
                        WHERE session_id = ?
                        ORDER BY id DESC
                    """, (session_id,))
                else:
                    cursor.execute("""
                        SELECT id, name, product_type, json_data, created_date, validation_status,
                               quality_score, status, processing_notes
                        FROM user_data 
                        ORDER BY id DESC
                    """)
                
                rows = cursor.fetchall()
                data = []
                for row in rows:
                    try:
                        data.append({
                            'id': row[0],
                            'name': row[1],
                            'product_type': row[2],
                            'data': json.loads(row[3]) if row[3] else {},
                            'created_date': row[4],
                            'validation_status': row[5],
                            'quality_score': row[6],
                            'status': row[7],
                            'processing_notes': row[8]
                        })
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON for record {row[0]}: {e}")
                        continue
                    
                return data
        except Exception as e:
            print(f"Error getting data: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_record_count(self) -> int:
        """Get total number of records"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM user_data")
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting record count: {e}")
            return 0

    def get_average_quality_score(self) -> float:
        """Get average quality score"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT AVG(quality_score) FROM user_data")
                avg = cursor.fetchone()[0]
                return round(float(avg if avg is not None else 0), 2)
        except Exception as e:
            print(f"Error getting average quality score: {e}")
            return 0.0

    def get_recent_activity_count(self) -> int:
        """Get count of records from last 24 hours"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM user_data 
                    WHERE created_date > datetime('now', '-1 day')
                """)
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return 0

    def get_status_counts(self) -> Dict[str, int]:
        """Get counts by validation status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT validation_status, COUNT(*) 
                    FROM user_data 
                    GROUP BY validation_status
                """)
                return dict(cursor.fetchall())
        except Exception as e:
            print(f"Error getting status counts: {e}")
            return {'pending': 0, 'validated': 0, 'error': 0}

    def get_product_counts(self) -> Dict[str, int]:
        """Get counts by product type"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT product_type, COUNT(*) 
                    FROM user_data 
                    GROUP BY product_type
                """)
                return dict(cursor.fetchall())
        except Exception as e:
            print(f"Error getting product counts: {e}")
            return {}

    def get_all_records(self) -> List[Dict[str, Any]]:
        """Get all records from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user_data ORDER BY created_date DESC")
                columns = [description[0] for description in cursor.description]
                records = []
                for row in cursor.fetchall():
                    record = dict(zip(columns, row))
                    # Try to parse JSON data
                    try:
                        if record.get('json_data'):
                            record['json_data'] = json.loads(record['json_data'])
                    except:
                        pass  # Keep as string if not valid JSON
                    records.append(record)
                return records
        except Exception as e:
            print(f"Error getting all records: {e}")
            return []
