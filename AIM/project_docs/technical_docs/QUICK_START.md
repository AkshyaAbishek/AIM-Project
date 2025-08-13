# AIM - Actuarial Input Mapper - Quick Start Guide

## 🚀 Easy Launch Options

### Option 1: Professional Launch Script (Recommended)
**File:** `launch_aim_pro.bat`
- Enhanced user interface with colors and graphics
- Comprehensive system checks and error handling
- Automatic Python download link if needed
- Professional console appearance
- Detailed status messages

### Option 2: Standard Launch Script
**File:** `launch_aim.bat`
- Detailed startup information and diagnostics
- Checks Python installation and virtual environment
- Shows helpful error messages and troubleshooting tips
- Keeps window open for problem analysis

### Option 3: PowerShell Launch Script
**File:** `launch_aim.ps1`
- Modern PowerShell-based launcher
- Colored output and professional formatting
- Advanced error handling and verbose mode
- Run with: `PowerShell -ExecutionPolicy Bypass -File launch_aim.ps1`

### Option 4: Quick Launch Script
**File:** `start.bat`
- Minimal output for instant launch
- Quick and clean startup
- Automatically closes on success
- Best for regular daily use

## 📋 System Requirements

- **Python 3.7+** installed on your system
- **tkinter** (usually included with Python)
- **Required packages** (install automatically when needed):
  - sqlite3 (built-in)
  - hashlib (built-in)
  - json (built-in)
  - datetime (built-in)

## 🛠️ Setup Instructions

1. **Download/Clone** the AIM project to your computer
2. **Navigate** to the AIM folder
3. **Double-click** either `launch_aim.bat` or `start.bat`
4. The **GUI window** will open automatically

## 🎮 Using the Application

Once the GUI opens, you'll see 6 main options:

1. **🟢 Add new JSON data** - Input your actuarial data
2. **🟢 Show field mapping** - View data transformation rules
3. **🟢 View stored data** - Browse and search your saved data
4. **🟠 Check duplicates** - Find duplicate names in your database
5. **🟢 Help** - Get detailed help for each feature
6. **🔴 Clear Database** - Remove all stored data (use with caution!)

## 💾 Data Storage

- All data is automatically saved to **`aim_data.db`** (SQLite database)
- Data persists between sessions
- Duplicate data is automatically prevented
- Search through all stored records easily

## 🔧 Troubleshooting

### Python Not Found Error
- Install Python from: https://www.python.org/downloads/
- Make sure Python is added to your PATH during installation
- Restart your computer after installation

### Application Won't Start
- Try running `launch_aim.bat` for detailed error information
- Check that all files are in the same folder
- Ensure you have write permissions in the folder (for database creation)

### GUI Not Appearing
- Check if your system supports tkinter (should be included with Python)
- Try running from command prompt: `python example.py`
- Look for error messages in the console

## 📞 Features Overview

### ✅ Duplicate Prevention
- **MD5 hash comparison** prevents exact duplicate data
- **Warning dialogs** alert you to duplicate attempts
- **Name-based analysis** finds multiple policies for same person

### 🔍 Search Capabilities
- Search by **any field value** (names, amounts, dates)
- **Case-insensitive** searching
- **Real-time results** with match counter
- **Export functionality** for data backup

### 🎨 User Interface
- **Color-coded buttons** for easy identification
- **Modern dialog boxes** for all interactions
- **Comprehensive help system** with examples
- **Status indicators** showing database statistics

## 📁 File Structure
```
AIM/
├── launch_aim.bat          # Full launch script with diagnostics
├── start.bat               # Quick launch script
├── example.py              # Main application file
├── aim_data.db            # SQLite database (created automatically)
├── src/                   # Source code modules
└── data/                  # Sample data files
```

## 🎯 Quick Start Checklist

- [ ] Python installed
- [ ] Downloaded AIM files
- [ ] Double-clicked `launch_aim.bat`
- [ ] GUI window opened
- [ ] Ready to input actuarial data!

---

**Need help?** Click the "Help" button in the application for detailed feature explanations and examples.
