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

# Import database manager
from db_manager import WebDatabaseManager
db_manager = WebDatabaseManager()

# Main Routes
@app.route('/')
def index():
    """Dashboard route"""
    try:
        stats = {
            'total_records': db_manager.get_record_count(),
            'average_quality': db_manager.get_average_quality_score(),
            'recent_activity': db_manager.get_recent_activity_count(),
            'status_counts': db_manager.get_status_counts(),
            'product_counts': db_manager.get_product_counts(),
            'product_distribution': db_manager.get_product_counts(),  # Same as product_counts
        }
        recent_records = db_manager.get_recent_records(5)  # Get 5 most recent records
        return render_template('index.html', stats=stats, recent_records=recent_records)
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/upload')
def upload_file():
    """File upload page"""
    return render_template('upload.html')

@app.route('/view-data')
def view_data():
    """Data viewing page"""
    try:
        records = db_manager.get_all_records()
        return render_template('view_data.html', records=records)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/compare')
def compare():
    """Data comparison page"""
    return render_template('compare.html')

@app.route('/field-mapping')
def field_mapping():
    """Field mapping page"""
    return render_template('field_mapping.html')

@app.route('/help')
def help_page():
    """Help documentation page"""
    return render_template('help.html')

# API Endpoints
@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file based on type
            if filename.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            elif filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
            
            # Create a record in the database
            record_data = {
                'name': filename,
                'product_type': request.form.get('product_type', 'unknown'),
                'data_hash': hashlib.md5(df.to_json().encode()).hexdigest(),
                'json_data': df.to_json(orient='records'),
                'file_source': filepath
            }
            
            record_id = db_manager.add_record(record_data)
            return jsonify({'success': True, 'record_id': record_id})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-data/<int:record_id>', methods=['POST'])
def api_process_data(record_id):
    """Process a specific data record"""
    try:
        record = db_manager.get_record(record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        # Process the record using AIM processor
        result = aim_processor.process_fast_ui_input(
            json.loads(record['json_data']), 
            record['product_type']
        )
        
        # Update record with processing results
        db_manager.update_record(record_id, {
            'processed_data': json.dumps(result),
            'status': 'processed',
            'validation_status': 'validated'
        })
        
        return jsonify({'success': True, 'result': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def api_stats():
    """Get dashboard statistics"""
    try:
        stats = {
            'total_records': db_manager.get_record_count(),
            'average_quality': db_manager.get_average_quality_score(),
            'recent_activity': db_manager.get_recent_activity_count(),
            'status_counts': db_manager.get_status_counts(),
            'product_counts': db_manager.get_product_counts()
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mapping', methods=['POST'])
def api_mapping():
    """Save field mapping"""
    try:
        mapping_data = request.json
        product_type = mapping_data.get('product_type')
        mappings = mapping_data.get('mappings')
        
        if not product_type or not mappings:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Save mapping to database or file system
        filename = f"mapping_template_{product_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
        
        with open(filepath, 'w') as f:
            json.dump(mappings, f, indent=4)
        
        return jsonify({'success': True, 'filepath': filepath})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/template/<product_type>')
def api_get_template(product_type):
    """Get Excel template for a product type"""
    try:
        # Create Excel template
        if product_type == 'life':
            df = pd.DataFrame(columns=['Policy Number', 'Insured Name', 'Face Amount', 'Premium', 'Issue Date'])
        elif product_type == 'annuity':
            df = pd.DataFrame(columns=['Contract Number', 'Owner Name', 'Premium', 'Interest Rate', 'Issue Date'])
        else:
            return jsonify({'error': 'Invalid product type'}), 400
        
        # Save to BytesIO
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f"{product_type}_template.xlsx"
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
