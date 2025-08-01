@echo off
REM AIM GUI Launcher with Enhanced User Experience
title AIM - Actuarial Input Mapper

REM Set console colors (Blue background, White text)
color 1F

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║                                                          ║
echo  ║    🎯 AIM - Actuarial Input Mapper                       ║
echo  ║    📊 Professional Data Management Tool                   ║
echo  ║                                                          ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check for Python virtual environment
if exist "..\\.venv\\Scripts\\python.exe" (
    echo  ✅ Using Python Virtual Environment
    set PYTHON_CMD=..\.venv\Scripts\python.exe
) else (
    echo  ✅ Using System Python Installation
    set PYTHON_CMD=python
)

echo.
echo  🔍 Checking Python installation...

REM Verify Python is available
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ❌ ERROR: Python not found!
    echo.
    echo  📥 Please install Python from: https://www.python.org/downloads/
    echo  💡 Make sure to check "Add Python to PATH" during installation
    echo.
    echo  Press any key to open Python download page...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=*" %%i in ('%PYTHON_CMD% --version') do set PYTHON_VERSION=%%i
echo  ✅ Found: %PYTHON_VERSION%

echo.
echo  🚀 Starting AIM GUI Application...
echo.
echo  ┌─────────────────────────────────────────────────────────┐
echo  │  🖥️  GUI window will open automatically                 │
echo  │  📝  You can minimize this console window               │
echo  │  🔄  Application is loading, please wait...             │
echo  └─────────────────────────────────────────────────────────┘
echo.

REM Start the application and capture the exit code
%PYTHON_CMD% example.py
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE% equ 0 (
    echo  ✅ Application closed successfully
    echo.
    echo  💡 Thank you for using AIM!
    timeout /t 3 >nul
) else (
    echo  ❌ Application encountered an error (Exit Code: %EXIT_CODE%^)
    echo.
    echo  🔧 Troubleshooting tips:
    echo  • Check that all required files are present
    echo  • Ensure you have write permissions in this folder
    echo  • Try running as administrator if needed
    echo  • Check the error messages above for details
    echo.
    echo  📧 If problems persist, check the QUICK_START.md file
    echo.
    pause
)

REM Reset console colors
color
