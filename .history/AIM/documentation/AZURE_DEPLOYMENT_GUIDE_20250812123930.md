# Azure Web Application Deployment Guide for AIM Project

## 📋 **Overview**

This guide will help you deploy the AIM (Actuarial Input Mapper) project as a web application on Azure App Service. We'll convert the current tkinter desktop application to a Flask web application that can run in the cloud.

## 🔄 **Deployment Strategy**

### **Option 1: Flask Web Application (Recommended)**
Convert the tkinter GUI to a web-based Flask application with HTML/CSS/JavaScript frontend.

### **Option 2: Streamlit Application**
Use Streamlit for rapid web app development with minimal code changes.

### **Option 3: FastAPI + React**
Modern API backend with React frontend for enterprise-grade deployment.

## 🚀 **Step-by-Step Deployment Process**

### **Phase 1: Convert to Web Application**

#### **1.1 Install Required Dependencies**
```bash
pip install flask
pip install streamlit
pip install gunicorn
pip install azure-storage-blob
pip install python-dotenv
```

#### **1.2 Create Web Application Structure**
```
AIM-Web/
├── app.py                 # Flask main application
├── requirements.txt       # Dependencies for Azure
├── startup.py            # Azure startup script
├── web.config            # IIS configuration
├── static/               # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── mapping.html
│   └── results.html
├── config/               # Configuration files
└── data/                 # Data files
```

### **Phase 2: Azure Setup**

#### **2.1 Create Azure Resources**
1. **Azure App Service Plan**
2. **Azure App Service (Web App)**
3. **Azure SQL Database** (optional, for enterprise)
4. **Azure Storage Account** (for file uploads)
5. **Azure Application Insights** (for monitoring)

#### **2.2 Configure Azure App Service**
- Runtime: Python 3.9 or 3.10
- Operating System: Linux
- Pricing Tier: Standard S1 or higher

### **Phase 3: Database Migration**

#### **3.1 SQLite to Azure SQL (Production)**
```python
# Database configuration for Azure
import os
from sqlalchemy import create_engine

# Local development
if os.getenv('ENVIRONMENT') == 'development':
    DATABASE_URL = 'sqlite:///aim_data.db'
else:
    # Azure SQL Database
    DATABASE_URL = os.getenv('AZURE_SQL_CONNECTION_STRING')
```

#### **3.2 File Storage Migration**
```python
# Azure Blob Storage for file uploads
from azure.storage.blob import BlobServiceClient

class AzureFileManager:
    def __init__(self):
        self.blob_service = BlobServiceClient.from_connection_string(
            os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        )
    
    def upload_file(self, file_data, filename):
        blob_client = self.blob_service.get_blob_client(
            container='uploads', 
            blob=filename
        )
        blob_client.upload_blob(file_data, overwrite=True)
        return blob_client.url
```

## 📁 **Required Files for Deployment**

### **1. requirements.txt** (Azure Dependencies)
```
Flask==2.3.3
gunicorn==21.2.0
pandas==2.0.3
openpyxl==3.1.2
SQLAlchemy==2.0.20
python-dotenv==1.0.0
azure-storage-blob==12.17.0
azure-identity==1.13.0
pyodbc==4.0.39
Werkzeug==2.3.7
Jinja2==3.1.2
numpy==1.24.3
scikit-learn==1.3.0
sentence-transformers==2.2.2
```

### **2. startup.py** (Azure Startup Script)
```python
import os
import sys

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == '__main__':
    # Azure App Service will set the PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### **3. web.config** (IIS Configuration)
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified"/>
    </handlers>
    <httpPlatform processPath="python" arguments="startup.py" stdoutLogEnabled="true" stdoutLogFile="\\?\%home%\LogFiles\python.log" startupTimeLimit="60" requestTimeout="120">
      <environmentVariables>
        <environmentVariable name="PYTHONPATH" value="\\?\%home%\site\wwwroot"/>
      </environmentVariables>
    </httpPlatform>
  </system.webServer>
</configuration>
```

### **4. .env** (Environment Variables)
```bash
# Azure Configuration
AZURE_SQL_CONNECTION_STRING=your_azure_sql_connection_string
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
AZURE_APPLICATION_INSIGHTS_KEY=your_insights_key

# Application Configuration
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB max file size
```

## 🌐 **Flask Web Application Code**

I'll create the main Flask application that converts your tkinter functionality to web-based:

### **Main Application Structure**
The Flask app will include:
1. **File Upload Interface** - Replace tkinter file dialogs
2. **Data Processing Forms** - Replace tkinter input dialogs
3. **Progress Tracking** - Replace tkinter progress bars
4. **Results Display** - Replace tkinter message boxes
5. **Excel Download** - Replace file save dialogs

### **Key Features Conversion**
- **Data Entry** → Web Forms
- **File Browsing** → File Upload
- **Progress Indicators** → AJAX Progress Bars
- **Error Messages** → Flash Messages
- **Excel Export** → Download Links

## 🚀 **Deployment Commands**

### **Option A: Azure CLI Deployment**
```bash
# Login to Azure
az login

# Create resource group
az group create --name AIM-RG --location "East US"

# Create App Service plan
az appservice plan create --name AIM-Plan --resource-group AIM-RG --sku S1 --is-linux

# Create web app
az webapp create --resource-group AIM-RG --plan AIM-Plan --name aim-webapp --runtime "PYTHON|3.9"

# Deploy code
az webapp deployment source config-zip --resource-group AIM-RG --name aim-webapp --src aim-webapp.zip
```

### **Option B: GitHub Actions Deployment**
```yaml
# .github/workflows/azure-deploy.yml
name: Deploy to Azure Web App

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'aim-webapp'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### **Option C: VS Code Extension**
1. Install "Azure App Service" extension
2. Right-click on your project folder
3. Select "Deploy to Web App..."
4. Follow the deployment wizard

## 📊 **Monitoring and Management**

### **Application Insights Integration**
```python
from applicationinsights import TelemetryClient
from applicationinsights.flask.ext import AppInsights

# Initialize Application Insights
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = os.getenv('AZURE_APPLICATION_INSIGHTS_KEY')
appinsights = AppInsights(app)

# Custom telemetry
tc = TelemetryClient(os.getenv('AZURE_APPLICATION_INSIGHTS_KEY'))

def track_processing_event(operation_name, duration, success):
    tc.track_event(
        'DataProcessing',
        properties={
            'operation': operation_name,
            'duration_ms': duration,
            'success': success
        }
    )
```

### **Logging Configuration**
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # Production logging
    file_handler = RotatingFileHandler('logs/aim.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

## 🔒 **Security Considerations**

### **Authentication and Authorization**
```python
from flask_login import LoginManager, login_required
from azure.identity import DefaultAzureCredential

# Azure AD integration
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/secure-area')
@login_required
def secure_area():
    return render_template('secure.html')
```

### **Data Protection**
```python
# Encrypt sensitive data
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY').encode()
        self.cipher = Fernet(self.key)
    
    def encrypt_data(self, data):
        return self.cipher.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data).decode()
```

## 💰 **Cost Estimation**

### **Azure Resources Monthly Cost**
- **App Service (S1)**: ~$55/month
- **Azure SQL Database (S1)**: ~$30/month
- **Storage Account**: ~$5/month
- **Application Insights**: ~$10/month
- **Total**: ~$100/month

### **Scaling Options**
- **Development**: Free tier (F1) - $0/month
- **Testing**: Basic (B1) - $13/month
- **Production**: Standard (S1) - $55/month
- **Enterprise**: Premium (P1V2) - $146/month

## 🎯 **Next Steps**

1. **Choose Deployment Option**: Flask, Streamlit, or FastAPI
2. **Create Azure Account**: Set up subscription and resource group
3. **Convert Application**: Transform tkinter to web interface
4. **Test Locally**: Ensure web app works before deployment
5. **Deploy to Azure**: Use one of the deployment methods
6. **Configure Monitoring**: Set up Application Insights
7. **Security Setup**: Implement authentication and HTTPS
8. **Performance Testing**: Load test the application
9. **User Training**: Update documentation for web interface
10. **Go Live**: Launch and monitor the production application

Would you like me to create the Flask web application code or help you with any specific deployment option?
