# AIM Application Launcher - PowerShell Version
# Updated for new organized project structure

param(
    [string]$Mode = "web",
    [switch]$Help
)

if ($Help) {
    Write-Host @"
🚀 AIM Application Launcher

Usage: .\launch_aim.ps1 [options]

Options:
  -Mode <mode>    Launch mode: 'web' (default), 'desktop', or 'test'
  -Help           Show this help message

Examples:
  .\launch_aim.ps1                # Launch web application
  .\launch_aim.ps1 -Mode desktop  # Launch desktop application
  .\launch_aim.ps1 -Mode test     # Run test suite

"@
    exit 0
}

# Get script directory (project root)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "🚀 AIM Application Launcher" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Function to ensure directories exist
function Ensure-Directories {
    $directories = @(
        "runtime\uploads",
        "runtime\exports",
        "runtime\logs",
        "runtime\temp_uploads",
        "runtime\saved_mappings",
        "database"
    )
    
    foreach ($dir in $directories) {
        $fullPath = Join-Path $ProjectRoot $dir
        if (!(Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Host "✓ Created directory: $dir" -ForegroundColor Green
        }
    }
}

# Function to check and setup database
function Setup-Database {
    $newDbPath = Join-Path $ProjectRoot "database\aim_data.db"
    $oldDbPath = Join-Path $ProjectRoot "aim_data.db"
    
    if (!(Test-Path $newDbPath)) {
        if (Test-Path $oldDbPath) {
            Copy-Item $oldDbPath $newDbPath
            Write-Host "✓ Copied database to new location" -ForegroundColor Green
        } else {
            Write-Host "ℹ Database will be created at startup" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✓ Database found at: database\aim_data.db" -ForegroundColor Green
    }
}

# Function to check Python and requirements
function Check-Python {
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
        
        # Check if Flask is installed
        $flaskCheck = python -c "import flask; print('Flask', flask.__version__)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Flask installed: $flaskCheck" -ForegroundColor Green
        } else {
            Write-Host "⚠ Installing required packages..." -ForegroundColor Yellow
            pip install -r requirements.txt
        }
    } catch {
        Write-Host "❌ Python not found. Please install Python 3.x" -ForegroundColor Red
        exit 1
    }
}

# Main execution
try {
    Write-Host "📂 Project Root: $ProjectRoot" -ForegroundColor Blue
    
    # Setup environment
    Ensure-Directories
    Setup-Database
    Check-Python
    
    # Set environment variables
    $env:AIM_PROJECT_ROOT = $ProjectRoot
    $env:AIM_DATABASE_PATH = Join-Path $ProjectRoot "database\aim_data.db"
    $env:AIM_UPLOAD_PATH = Join-Path $ProjectRoot "runtime\uploads"
    $env:AIM_EXPORT_PATH = Join-Path $ProjectRoot "runtime\exports"
    
    Write-Host "=" * 50 -ForegroundColor Gray
    
    switch ($Mode.ToLower()) {
        "web" {
            Write-Host "🌐 Starting AIM Web Application..." -ForegroundColor Cyan
            $webAppPath = Join-Path $ProjectRoot "core\web"
            Set-Location $webAppPath
            python web_app.py
        }
        "desktop" {
            Write-Host "🖥️ Starting AIM Desktop Application..." -ForegroundColor Cyan
            $appPath = Join-Path $ProjectRoot "app"
            if (Test-Path $appPath) {
                Set-Location $appPath
                python example.py
            } else {
                Write-Host "❌ Desktop application not found in app directory" -ForegroundColor Red
            }
        }
        "test" {
            Write-Host "🧪 Running Test Suite..." -ForegroundColor Cyan
            $testPath = Join-Path $ProjectRoot "development\testing"
            Set-Location $testPath
            python -m pytest . -v
        }
        default {
            Write-Host "❌ Unknown mode: $Mode" -ForegroundColor Red
            Write-Host "Use -Help for usage information" -ForegroundColor Yellow
            exit 1
        }
    }
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    # Return to original directory
    Set-Location $ProjectRoot
}

Write-Host "`n🎉 AIM Application finished" -ForegroundColor Green
