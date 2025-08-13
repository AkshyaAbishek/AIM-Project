# Azure Web App Deployment Script for AIM Project (PowerShell)
# This script prepares and deploys the AIM application to Azure App Service

Write-Host "🚀 Starting Azure deployment for AIM Web Application..." -ForegroundColor Green

# Set variables
$RESOURCE_GROUP = "aim-web-app-rg"
$APP_SERVICE_PLAN = "aim-app-service-plan"
$WEB_APP_NAME = "aim-web-application-$(Get-Random -Minimum 1000 -Maximum 9999)"
$LOCATION = "East US"
$RUNTIME = "PYTHON|3.11"

# Step 1: Check Azure CLI installation
Write-Host "🔍 Checking Azure CLI installation..." -ForegroundColor Yellow
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it from https://aka.ms/installazurecliwindows" -ForegroundColor Red
    exit 1
}

# Step 2: Login to Azure (if not already logged in)
Write-Host "📋 Checking Azure login status..." -ForegroundColor Yellow
$loginStatus = az account show 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔐 Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Step 3: Create Resource Group
Write-Host "📦 Creating resource group: $RESOURCE_GROUP..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Step 4: Create App Service Plan
Write-Host "⚙️ Creating App Service Plan: $APP_SERVICE_PLAN..." -ForegroundColor Yellow
az appservice plan create `
    --name $APP_SERVICE_PLAN `
    --resource-group $RESOURCE_GROUP `
    --sku B1 `
    --is-linux

# Step 5: Create Web App
Write-Host "🌐 Creating Web App: $WEB_APP_NAME..." -ForegroundColor Yellow
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $APP_SERVICE_PLAN `
    --name $WEB_APP_NAME `
    --runtime $RUNTIME

# Step 6: Configure startup command
Write-Host "🔧 Configuring startup command..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --startup-file "startup.py"

# Step 7: Generate secret key
$SECRET_KEY = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString()))

# Step 8: Configure app settings
Write-Host "⚙️ Configuring application settings..." -ForegroundColor Yellow
az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --settings `
        FLASK_ENV=production `
        SECRET_KEY=$SECRET_KEY `
        PYTHONPATH=/home/site/wwwroot

# Step 9: Prepare deployment package
Write-Host "📦 Preparing deployment package..." -ForegroundColor Yellow

# Create deployment directory
$deploymentDir = "deployment-package"
if (Test-Path $deploymentDir) {
    Remove-Item -Recurse -Force $deploymentDir
}
New-Item -ItemType Directory -Path $deploymentDir

# Copy necessary files and directories
Copy-Item -Recurse -Path "templates" -Destination $deploymentDir -Force
Copy-Item -Recurse -Path "src" -Destination $deploymentDir -Force
if (Test-Path "static") {
    Copy-Item -Recurse -Path "static" -Destination $deploymentDir -Force
}
Copy-Item -Path "web_app.py" -Destination $deploymentDir -Force
Copy-Item -Path "startup.py" -Destination $deploymentDir -Force
Copy-Item -Path "requirements-web.txt" -Destination "$deploymentDir\requirements.txt" -Force
Copy-Item -Path "web.config" -Destination $deploymentDir -Force
Copy-Item -Path ".env.production" -Destination "$deploymentDir\.env" -Force

# Step 10: Create ZIP file for deployment
Write-Host "📁 Creating deployment ZIP file..." -ForegroundColor Yellow
$zipFile = "aim-web-app.zip"
if (Test-Path $zipFile) {
    Remove-Item $zipFile -Force
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($deploymentDir, $zipFile)

# Step 11: Deploy using ZIP
Write-Host "🚀 Deploying application to Azure..." -ForegroundColor Yellow
az webapp deployment source config-zip `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --src $zipFile

# Step 12: Enable HTTPS redirect
Write-Host "🔒 Enabling HTTPS redirect..." -ForegroundColor Yellow
az webapp update `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --https-only true

# Step 13: Get the application URL
Write-Host "📋 Getting application details..." -ForegroundColor Yellow
$APP_URL = az webapp show `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --query defaultHostName `
    --output tsv

# Clean up deployment files
Remove-Item -Recurse -Force $deploymentDir
Remove-Item $zipFile -Force

# Display results
Write-Host ""
Write-Host "🎉 Your AIM Web Application is deployed!" -ForegroundColor Green
Write-Host "🌐 URL: https://$APP_URL" -ForegroundColor Cyan
Write-Host "📊 Resource Group: $RESOURCE_GROUP" -ForegroundColor White
Write-Host "⚙️ App Service Plan: $APP_SERVICE_PLAN" -ForegroundColor White
Write-Host "🌐 Web App Name: $WEB_APP_NAME" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit your application URL to test" -ForegroundColor White
Write-Host "2. Configure custom domain (if needed)" -ForegroundColor White
Write-Host "3. Set up SSL certificate (if using custom domain)" -ForegroundColor White
Write-Host "4. Configure backup and monitoring" -ForegroundColor White
Write-Host "5. Set up CI/CD pipeline (optional)" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "View logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME" -ForegroundColor White
Write-Host "Stop the app: az webapp stop --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME" -ForegroundColor White
Write-Host "Restart the app: az webapp restart --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME" -ForegroundColor White
Write-Host "Delete resources: az group delete --name $RESOURCE_GROUP --yes --no-wait" -ForegroundColor White

# Save deployment info to file
$deploymentInfo = @"
AIM Web Application Deployment Information
==========================================

Deployment Date: $(Get-Date)
Resource Group: $RESOURCE_GROUP
App Service Plan: $APP_SERVICE_PLAN
Web App Name: $WEB_APP_NAME
Application URL: https://$APP_URL

Azure CLI Commands:
- View logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME
- Stop app: az webapp stop --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME
- Restart app: az webapp restart --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME
- Delete resources: az group delete --name $RESOURCE_GROUP --yes --no-wait

"@

$deploymentInfo | Out-File -FilePath "deployment-info.txt" -Encoding UTF8
Write-Host "📄 Deployment information saved to deployment-info.txt" -ForegroundColor Green
