from flask import Flask, render_template, jsonify, redirect, url_for
from db_manager import WebDatabaseManager
import os

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXPORT_FOLDER'] = 'exports'
app.config['DATABASE_PATH'] = 'aim_data.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# Initialize database manager
db_manager = WebDatabaseManager()

@app.route('/')
def index():
    """Dashboard route"""
    try:
        # Get statistics from database
        stats = {
            'total_records': db_manager.get_record_count(),
            'average_quality': db_manager.get_average_quality_score(),
            'recent_activity': db_manager.get_recent_activity_count(),
            'status_counts': db_manager.get_status_counts(),
            'product_counts': db_manager.get_product_counts()
        }
        return render_template('index.html', stats=stats)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}"

@app.route('/help')
def help_page():
    """Help documentation page"""
    return render_template('help.html')

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
        return f"Error loading data: {str(e)}"

@app.route('/compare')
def compare():
    """Data comparison page"""
    return render_template('compare.html')

@app.route('/field-mapping')
def field_mapping():
    """Field mapping page"""
    return render_template('field_mapping.html')

@app.route('/process-data/<int:record_id>')
def process_data(record_id):
    """Process specific data record"""
    try:
        # For now, just redirect to view data
        return redirect(url_for('view_data'))
    except Exception as e:
        return f"Error processing data: {str(e)}"

@app.route('/api/stats')
def get_stats():
    """API endpoint for dashboard statistics"""
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

if __name__ == '__main__':
    app.run(debug=True)
