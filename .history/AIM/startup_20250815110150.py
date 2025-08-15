"""
Azure App Service startup script for AIM Web Application
This script is called by Azure App Service to start the Flask application
"""

import os
import sys
from web_app import app

# Azure App Service specific configuration
if __name__ == "__main__":
    # Get port from environment variable (Azure sets this)
    port = int(os.environ.get('PORT', 8000))
    
    # Set Flask environment
    os.environ.setdefault('FLASK_ENV', 'production')
    
    # Configure for production
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'production-secret-key-change-this'),
        DEBUG=False,
        TESTING=False
    )
    
    # Start the application
    app.run(host='0.0.0.0', port=port, debug=False)
