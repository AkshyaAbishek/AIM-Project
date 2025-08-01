@echo off
echo ====================================================
echo   AIM Excel Mapping Setup Helper
echo ====================================================
echo.

REM Create safe directories for Excel mapping
echo 1. Creating AIM Excel Mapping directories...
mkdir "%USERPROFILE%\Documents\AIM_Excel_Mappings" 2>nul
mkdir "%USERPROFILE%\Desktop\AIM_Temp" 2>nul

echo    ✓ Created: %USERPROFILE%\Documents\AIM_Excel_Mappings
echo    ✓ Created: %USERPROFILE%\Desktop\AIM_Temp

echo.
echo 2. Setting up sample actuarial calculator...
cd /d "%~dp0"

REM Run Python to create sample calculator if it doesn't exist
if not exist "sample_actuarial_calculator.xlsx" (
    echo    Creating sample calculator Excel file...
    C:/Users/2013041/VibeCode/.venv/Scripts/python.exe create_sample_calculator.py
    echo    ✓ Sample calculator created
) else (
    echo    ✓ Sample calculator already exists
)

echo.
echo 3. Recommended file locations:
echo.
echo    📁 For OUTPUT Excel (new mapping file):
echo       %USERPROFILE%\Documents\AIM_Excel_Mappings\
echo       %USERPROFILE%\Desktop\AIM_Temp\
echo.
echo    📁 For CALCULATOR Excel (existing file):
echo       %~dp0sample_actuarial_calculator.xlsx
echo       Or your own calculator Excel file
echo.
echo 4. Usage tips:
echo    • Always close Excel before running the mapping tool
echo    • Use simple filenames without special characters
echo    • Save to Documents or Desktop folders for best results
echo    • Check the Troubleshooting Guide if you get errors
echo.

pause
echo.
echo ====================================================
echo   Starting AIM Application...
echo ====================================================
C:/Users/2013041/VibeCode/.venv/Scripts/python.exe example.py
