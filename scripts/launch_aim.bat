@echo off
REM AIM - Actuarial Input Mapper - Launch Script
REM This batch file launches the AIM GUI application

echo.
echo ========================================
echo  AIM - Actuarial Input Mapper
echo  Launch Script
echo ========================================
echo.

REM Change to the AIM directory
cd /d "%~dp0"

REM Check if Python virtual environment exists
if exist "..\\.venv\\Scripts\\python.exe" (
    echo Using virtual environment Python...
    set PYTHON_CMD=..\.venv\Scripts\python.exe
) else (
    echo Using system Python...
    set PYTHON_CMD=python
)

REM Display current directory and Python version
echo Current directory: %CD%
echo.
echo Checking Python installation...
%PYTHON_CMD% --version
if errorlevel 1 (
    echo.
    echo ERROR: Python not found!
    echo Please install Python or check your PATH environment variable.
    echo.
    echo You can download Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo Starting AIM GUI Application...
echo.
echo ==========================================
echo  GUI will open automatically
echo  Close this window to exit the application
echo ==========================================
echo.

REM Run the AIM application
%PYTHON_CMD% example.py

REM Check if the application exited with an error
if errorlevel 1 (
    echo.
    echo ==========================================
    echo  Application ended with an error
    echo ==========================================
    echo.
    echo Possible issues:
    echo - Missing required Python packages
    echo - Configuration file problems
    echo - Database access issues
    echo.
    echo Check the error messages above for details.
    echo.
    pause
) else (
    echo.
    echo ==========================================
    echo  Application closed normally
    echo ==========================================
    echo.
)

echo Press any key to close this window...
pause >nul
