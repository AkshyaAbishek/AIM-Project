@echo off
REM Quick Launch Script for AIM - Actuarial Input Mapper

cd /d "%~dp0"

REM Try virtual environment first, then system Python
if exist "..\\.venv\\Scripts\\python.exe" (
    ..\.venv\Scripts\python.exe example.py
) else (
    python example.py
)

REM Keep window open if there was an error
if errorlevel 1 pause
