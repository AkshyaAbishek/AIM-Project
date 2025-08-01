# AIM - Actuarial Input Mapper - PowerShell Launcher
# This script provides a modern PowerShell-based launch experience

param(
    [switch]$Verbose
)

# Set window title and clear console
$Host.UI.RawUI.WindowTitle = "AIM - Actuarial Input Mapper"
Clear-Host

# Display banner
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║    🎯 AIM - Actuarial Input Mapper                       ║" -ForegroundColor White
Write-Host "║    📊 Professional Data Management Tool                   ║" -ForegroundColor White
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

if ($Verbose) {
    Write-Host "📁 Current directory: $pwd" -ForegroundColor Gray
}

# Check for virtual environment
$venvPython = Join-Path $scriptPath "..\.venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    Write-Host "✅ Using Python Virtual Environment" -ForegroundColor Green
    $pythonCmd = $venvPython
} else {
    Write-Host "✅ Using System Python Installation" -ForegroundColor Green
    $pythonCmd = "python"
}

Write-Host ""
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow

# Test Python availability
try {
    $pythonVersion = & $pythonCmd --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python command failed"
    }
} catch {
    Write-Host ""
    Write-Host "❌ ERROR: Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "💡 Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    
    $response = Read-Host "Would you like to open the Python download page? (y/n)"
    if ($response -match '^[Yy]') {
        Start-Process "https://www.python.org/downloads/"
    }
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting AIM GUI Application..." -ForegroundColor Cyan
Write-Host ""
Write-Host "┌─────────────────────────────────────────────────────────┐" -ForegroundColor White
Write-Host "│  🖥️  GUI window will open automatically                 │" -ForegroundColor White
Write-Host "│  📝  You can minimize this console window               │" -ForegroundColor White
Write-Host "│  🔄  Application is loading, please wait...             │" -ForegroundColor White
Write-Host "└─────────────────────────────────────────────────────────┘" -ForegroundColor White
Write-Host ""

# Launch the application
try {
    if ($Verbose) {
        Write-Host "🔧 Executing: $pythonCmd example.py" -ForegroundColor Gray
    }
    
    & $pythonCmd "example.py"
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "✅ Application closed successfully" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 Thank you for using AIM!" -ForegroundColor Cyan
        Start-Sleep -Seconds 2
    } else {
        Write-Host "❌ Application encountered an error (Exit Code: $exitCode)" -ForegroundColor Red
        Write-Host ""
        Write-Host "🔧 Troubleshooting tips:" -ForegroundColor Yellow
        Write-Host "• Check that all required files are present" -ForegroundColor White
        Write-Host "• Ensure you have write permissions in this folder" -ForegroundColor White
        Write-Host "• Try running as administrator if needed" -ForegroundColor White
        Write-Host "• Check the error messages above for details" -ForegroundColor White
        Write-Host ""
        Write-Host "📧 If problems persist, check the QUICK_START.md file" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter to continue"
    }
} catch {
    Write-Host "❌ Failed to start application: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to continue"
    exit 1
}
