#!/bin/bash

# Azure Web App Deployment Script for AIM Project
# This script prepares and deploys the AIM application to Azure App Service

echo "🚀 Starting Azure deployment for AIM Web Application..."

# Set variables
RESOURCE_GROUP="aim-web-app-rg"
APP_SERVICE_PLAN="aim-app-service-plan"
WEB_APP_NAME="aim-web-application"
LOCATION="East US"
RUNTIME="PYTHON|3.11"

# Step 1: Login to Azure (if not already logged in)
echo "📋 Checking Azure login status..."
az account show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "🔐 Please login to Azure..."
    az login
fi

# Step 2: Create Resource Group
echo "📦 Creating resource group..."
az group create \
    --name $RESOURCE_GROUP \
    --location "$LOCATION"

# Step 3: Create App Service Plan
echo "⚙️ Creating App Service Plan..."
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux

# Step 4: Create Web App
echo "🌐 Creating Web App..."
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $WEB_APP_NAME \
    --runtime "$RUNTIME"

# Step 5: Configure startup command
echo "🔧 Configuring startup command..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --startup-file "startup.py"

# Step 6: Configure app settings
echo "⚙️ Configuring application settings..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings \
        FLASK_ENV=production \
        SECRET_KEY=$(openssl rand -base64 32) \
        PYTHONPATH=/home/site/wwwroot

# Step 7: Enable local Git deployment (optional)
echo "📂 Setting up deployment..."
# You can use local Git, GitHub, or ZIP deployment
# For ZIP deployment, we'll prepare the files

# Step 8: Prepare deployment package
echo "📦 Preparing deployment package..."
mkdir -p deployment-package
cp -r templates deployment-package/
cp -r src deployment-package/
cp -r static deployment-package/ 2>/dev/null || echo "No static folder found"
cp web_app.py deployment-package/
cp startup.py deployment-package/
cp requirements-web.txt deployment-package/requirements.txt
cp web.config deployment-package/
cp .env.production deployment-package/.env

# Step 9: Deploy using ZIP
echo "🚀 Deploying application..."
cd deployment-package
zip -r ../aim-web-app.zip .
cd ..

az webapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --src aim-web-app.zip

# Step 10: Configure custom domain (optional)
# echo "🌍 Configuring custom domain..."
# az webapp config hostname add \
#     --webapp-name $WEB_APP_NAME \
#     --resource-group $RESOURCE_GROUP \
#     --hostname yourdomain.com

# Step 11: Enable HTTPS redirect
echo "🔒 Enabling HTTPS redirect..."
az webapp update \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --https-only true

# Step 12: Get the application URL
echo "✅ Deployment complete!"
APP_URL=$(az webapp show \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --query defaultHostName \
    --output tsv)

echo ""
echo "🎉 Your AIM Web Application is deployed!"
echo "🌐 URL: https://$APP_URL"
echo "📊 Resource Group: $RESOURCE_GROUP"
echo "⚙️ App Service Plan: $APP_SERVICE_PLAN"
echo ""
echo "Next steps:"
echo "1. Visit your application URL to test"
echo "2. Configure custom domain (if needed)"
echo "3. Set up SSL certificate (if using custom domain)"
echo "4. Configure backup and monitoring"
echo "5. Set up CI/CD pipeline (optional)"
echo ""
echo "To view logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo "To stop the app: az webapp stop --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo "To restart the app: az webapp restart --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
