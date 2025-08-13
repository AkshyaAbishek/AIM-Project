"""
AIM Web Application - Flask Implementation
Converts the tkinter desktop application to a web-based interface for Azure deployment
"""

import os
import json
import hashlib
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from werkzeug.utils import secure_filename
import pandas as pd
from io import BytesIO

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file, session, send_from_directory
from flask import Response
import sqlite3
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Using simplified AIM processor for web deployment")

class AIMProcessor:
    def process_fast_ui_input(self, data, product_type):
        return {"status": "success", "message": "Processed successfully"}

class ValidationError(Exception):
    pass

class MappingError(Exception):
    pass

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Original simple paths
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXPORT_FOLDER'] = 'exports'
app.config['DATABASE_PATH'] = 'aim_data.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# Initialize AIM processor
aim_processor = AIMProcessor()

# Import and initialize database manager
from db_manager import WebDatabaseManager
db_manager = WebDatabaseManager()

def create_excel_template(product_type: str, sample_data: Dict = None) -> str:
    """Create an Excel template file for the given product type"""
    try:
        # Sample template data based on product type
        if product_type == 'life_insurance':
            template_data = {
                'Field Name': ['policy_number', 'insured_name', 'premium_amount', 'coverage_amount', 'policy_start_date'],
                'Data Type': ['string', 'string', 'float', 'float', 'date'],
                'Required': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
                'Example': ['LIFE001234', 'John Doe', '1200.50', '100000.00', '2024-01-01']
            }
        elif product_type == 'annuity':
            template_data = {
                'Field Name': ['contract_number', 'annuitant_name', 'premium_amount', 'annuity_value', 'start_date'],
                'Data Type': ['string', 'string', 'float', 'float', 'date'],
                'Required': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
                'Example': ['ANN001234', 'Jane Smith', '5000.00', '250000.00', '2024-01-01']
            }
        else:
            template_data = {
                'Field Name': ['id', 'name', 'amount', 'date'],
                'Data Type': ['string', 'string', 'float', 'date'],
                'Required': ['Yes', 'Yes', 'Yes', 'Yes'],
                'Example': ['ID001', 'Sample Name', '1000.00', '2024-01-01']
            }
        
        # Create DataFrame
        df = pd.DataFrame(template_data)
        
        # Create temporary file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'mapping_template_{product_type}_{timestamp}.xlsx'
        filepath = os.path.join(app.config.get('EXPORT_FOLDER', 'runtime/exports'), filename)
        
        # Ensure export directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write to Excel file
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Field_Mapping', index=False)
        
        return filename
        
    except ImportError:
        # Fallback if pandas not available
        print("Warning: pandas not available for Excel template creation")
        return None
    except Exception as e:
        print(f"Error creating Excel template: {e}")
        return None

@app.route('/')
@app.route('/index')
def index():
    """Main dashboard page"""
    try:
        print("Starting index route...")
        
        # Ensure session ID exists
        if 'session_id' not in session:
            session['session_id'] = os.urandom(16).hex()
            print(f"Created new session ID: {session['session_id']}")
        
        print("Getting statistics...")
        stats = db_manager.get_statistics()
        print(f"Stats: {stats}")
        
        print("Getting recent data...")
        recent_data = db_manager.get_all_data()  # Removed session ID filter for now
        print(f"Recent data count: {len(recent_data)}")
        
        # Debug: Print first record to check structure
        if recent_data:
            print(f"Sample record structure: {list(recent_data[0].keys())}")
            print(f"Sample validation_status: {recent_data[0].get('validation_status')}")
        
        # Make sure we have all required stats
        if not isinstance(stats, dict):
            stats = {}
        
        default_stats = {
            'total_records': 0,
            'average_quality': 0.0,
            'product_distribution': {},
            'status_counts': {'processed': 0, 'pending': 0, 'error': 0},
            'recent_activity': 0,
            'processed_records': 0,
            'pending_records': 0,
            'error_records': 0
        }
        
        # Update defaults with actual stats
        for key, value in stats.items():
            default_stats[key] = value
        
        print(f"Final stats for template: {default_stats}")
        return render_template('index.html', stats=default_stats, recent_data=recent_data)
        
    except Exception as e:
        print(f"Error in index route: {e}")
        print(f"Error type: {type(e)}")
        print("Full traceback:")
        traceback.print_exc()
        
        # Return safe defaults
        safe_stats = {
            'total_records': 0,
            'average_quality': 0.0,
            'product_distribution': {},
            'status_counts': {'processed': 0, 'pending': 0, 'error': 0},
            'recent_activity': 0,
            'processed_records': 0,
            'pending_records': 0,
            'error_records': 0
        }
        return render_template('index.html', stats=safe_stats, recent_data=[])

@app.route('/help')
def help_page():
    """Help and documentation page"""
    return render_template('help.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """File upload interface"""
    if request.method == 'POST':
        # Process file upload
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
            
        if file:
            # Get form data
            product_type = request.form.get('product_type', 'unknown')
            
            # Save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Store data
            try:
                result = db_manager.store_data(
                    name=filename,
                    product_type=product_type,
                    json_data={'filename': filename, 'product_type': product_type},
                    session_id=session.get('session_id', 'unknown'),
                    file_source=filepath
                )
                
                if result.get('success'):
                    flash('File uploaded successfully!', 'success')
                    return redirect(url_for('process_data', record_id=result['record_id']))
                else:
                    flash(f"Upload failed: {result.get('message', 'Unknown error')}", 'error')
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
            
    # GET request - show upload form
    return render_template('upload.html', product_types=['life_insurance', 'annuity', 'other'])

@app.route('/process/<int:record_id>')
def process_data(record_id):
    """Process data page"""
    # Get record
    try:
        record = db_manager.get_data_by_id(record_id)
        if not record:
            flash('Record not found', 'error')
            return redirect(url_for('index'))
            
        return render_template('process.html', record=record)
        
    except Exception as e:
        flash(f'Error loading record: {str(e)}', 'error')
        return redirect(url_for('index'))

# Main startup
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("Server started at http://localhost:5000")
