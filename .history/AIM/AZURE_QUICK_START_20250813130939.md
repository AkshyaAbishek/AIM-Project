# Azure Deployment Quick Start Guide

## 🚀 Deploy AIM to Azure in 3 Steps

### Prerequisites
- Azure account with active subscription
- Azure CLI installed ([Download here](https://aka.ms/installazurecliwindows))
- Python 3.11+ installed locally

### Option 1: Automated Deployment (Recommended)

#### For Windows (PowerShell):
```powershell
# Run in PowerShell as Administrator
.\deploy-to-azure.ps1
```

#### For Linux/Mac (Bash):
```bash
# Make script executable
chmod +x deploy-to-azure.sh
# Run the script
./deploy-to-azure.sh
```

### Option 2: Manual Deployment

#### Step 1: Prepare Your Environment
```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "Your-Subscription-Name"
```

#### Step 2: Create Azure Resources
```bash
# Create resource group
az group create --name aim-web-app-rg --location "East US"

# Create App Service plan
az appservice plan create \
    --name aim-app-service-plan \
    --resource-group aim-web-app-rg \
    --sku B1 \
    --is-linux

# Create web app
az webapp create \
    --resource-group aim-web-app-rg \
    --plan aim-app-service-plan \
    --name your-unique-app-name \
    --runtime "PYTHON|3.11"
```

#### Step 3: Deploy Your Code
```bash
# Configure startup file
az webapp config set \
    --resource-group aim-web-app-rg \
    --name your-unique-app-name \
    --startup-file "startup.py"

# Set environment variables
az webapp config appsettings set \
    --resource-group aim-web-app-rg \
    --name your-unique-app-name \
    --settings FLASK_ENV=production SECRET_KEY=your-secret-key

# Deploy via ZIP (prepare ZIP file first)
az webapp deployment source config-zip \
    --resource-group aim-web-app-rg \
    --name your-unique-app-name \
    --src aim-web-app.zip
```

### Option 3: GitHub Actions CI/CD

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure Web App

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements-web.txt
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'your-app-name'
        publish-profile: ${{ secrets.AZUREAPPSERVICE_PUBLISHPROFILE }}
```

## 🔧 Configuration

### Environment Variables
Set these in Azure App Service Configuration:

```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key
DEBUG=False
DATABASE_URL=sqlite:///aim_data.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Custom Domain (Optional)
```bash
# Add custom domain
az webapp config hostname add \
    --webapp-name your-app-name \
    --resource-group aim-web-app-rg \
    --hostname yourdomain.com

# Enable managed SSL
az webapp config ssl bind \
    --certificate-thumbprint thumbprint \
    --ssl-type SNI \
    --name your-app-name \
    --resource-group aim-web-app-rg
```

## 📊 Monitoring & Troubleshooting

### View Application Logs
```bash
# Stream logs in real-time
az webapp log tail --resource-group aim-web-app-rg --name your-app-name

# Download log files
az webapp log download --resource-group aim-web-app-rg --name your-app-name
```

### Common Issues

#### App Won't Start
- Check startup file is set to `startup.py`
- Verify all dependencies in `requirements-web.txt`
- Check Python version compatibility

#### File Upload Issues
- Ensure `UPLOAD_FOLDER` environment variable is set
- Check file size limits in Azure App Service
- Verify file permissions

#### Database Issues
- For production, consider Azure SQL Database
- Check database file permissions
- Verify connection strings

## 💰 Cost Optimization

### App Service Plan Tiers
- **Free (F1)**: Development/testing only, limited resources
- **Basic (B1)**: Small production apps, $13-55/month
- **Standard (S1)**: Production apps with scaling, $56-220/month
- **Premium**: High-performance apps, auto-scaling

### Cost-Saving Tips
1. Use Basic tier for low-traffic applications
2. Enable auto-scaling to scale down during low usage
3. Monitor usage with Azure Cost Management
4. Consider Azure Functions for event-driven workloads

## 🔄 Updates and Maintenance

### Deploy Updates
```bash
# Create new deployment package
zip -r aim-web-app-update.zip templates/ src/ web_app.py startup.py requirements-web.txt

# Deploy update
az webapp deployment source config-zip \
    --resource-group aim-web-app-rg \
    --name your-app-name \
    --src aim-web-app-update.zip
```

### Backup Strategy
1. Enable Azure App Service backup
2. Export database regularly
3. Store backups in Azure Blob Storage
4. Test restore procedures

## 🚨 Security Best Practices

1. **Environment Variables**: Store secrets in App Service Configuration
2. **HTTPS**: Always enable HTTPS redirect
3. **Authentication**: Consider Azure AD integration
4. **Network**: Use VNet integration for sensitive data
5. **Monitoring**: Enable Application Insights

## 📞 Support

### Azure Resources
- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Python on Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python)
- [Azure Support](https://azure.microsoft.com/en-us/support/)

### Troubleshooting Commands
```bash
# Check app status
az webapp show --resource-group aim-web-app-rg --name your-app-name

# Restart app
az webapp restart --resource-group aim-web-app-rg --name your-app-name

# Scale app
az webapp scale --resource-group aim-web-app-rg --name your-app-name --instance-count 2

# Delete everything (when done testing)
az group delete --name aim-web-app-rg --yes --no-wait
```
