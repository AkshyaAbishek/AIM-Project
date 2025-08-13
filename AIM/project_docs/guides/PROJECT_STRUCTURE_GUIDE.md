# AIM Project - File Organization Guide

This document explains the new organized folder structure of the AIM (Actuarial Input Mapper) project.

## 📁 Project Structure

```
AIM/
├── 📂 src/                          # Core application source code
│   ├── aim_processor.py             # Main AIM processing logic
│   ├── 📂 config/                   # Configuration management
│   ├── 📂 mappers/                  # Field mapping modules
│   ├── 📂 parsers/                  # Data parsing modules
│   └── 📂 validators/               # Input validation modules
│
├── 📂 common/                       # Shared utilities and common functions
│   ├── ui_utils.py                  # UI components and styling
│   ├── database_manager.py          # Database operations
│   └── file_manager.py              # File handling utilities
│
├── 📂 tutorials/                    # Learning materials for Python and the project
│   ├── 📂 python_basics/            # Python fundamentals
│   │   ├── PYTHON_TUTORIAL_INTERACTIVE.py
│   │   └── PYTHON_BASICS_EXPLAINED.py
│   ├── 📂 project_examples/         # Project-specific examples
│   │   └── YOUR_FILE_EXPLAINED.py
│   └── 📂 README/
│       └── (this file will be moved here)
│
├── 📂 documentation/                # Project documentation
│   ├── 📂 guides/                   # User guides and documentation
│   │   ├── EXCEL_MAPPING_GUIDE.md
│   │   ├── TROUBLESHOOTING_GUIDE.md
│   │   ├── FILE_REQUIREMENTS_GUIDE.md
│   │   └── (other .md files)
│   └── 📂 technical/                # Technical documentation
│
├── 📂 scripts/                      # Batch files and scripts
│   ├── launch_aim.bat               # Launch application
│   ├── launch_aim_pro.bat           # Launch professional version
│   ├── setup_and_run.bat            # Setup and run script
│   └── start.bat                    # Quick start script
│
├── 📂 data/                         # Sample data and templates
│   └── 📂 sample/
│       └── life_insurance_sample.json
│
├── 📂 tests/                        # Test files
│   ├── test_import.py
│   └── test_duplicates.py
│
├── 📂 utils/                        # Utility scripts
│   └── create_sample_calculator.py
│
├── 📂 exports/                      # Generated exports and outputs
├── 📂 backup/                       # Backup files
└── 📂 .vscode/                      # VS Code configuration
```

## 🎯 Quick Start Guide

### For Python Beginners:
1. **Start here**: `tutorials/python_basics/PYTHON_TUTORIAL_INTERACTIVE.py`
2. **Read this**: `tutorials/python_basics/PYTHON_BASICS_EXPLAINED.py`
3. **Understand the project**: `tutorials/project_examples/YOUR_FILE_EXPLAINED.py`

### For Running the Application:
1. **Quick start**: Run `scripts/start.bat`
2. **Full setup**: Run `scripts/setup_and_run.bat`
3. **Professional version**: Run `scripts/launch_aim_pro.bat`

### For Documentation:
1. **User guides**: Check `documentation/guides/`
2. **Technical docs**: Check `documentation/technical/`
3. **Troubleshooting**: `documentation/guides/TROUBLESHOOTING_GUIDE.md`

## 📚 Learning Path

### Step 1: Python Basics
- Start with `tutorials/python_basics/PYTHON_TUTORIAL_INTERACTIVE.py`
- Run the examples and modify them
- Read through `tutorials/python_basics/PYTHON_BASICS_EXPLAINED.py`

### Step 2: Understanding the Project
- Read `tutorials/project_examples/YOUR_FILE_EXPLAINED.py`
- Explore the `src/` folder to see real implementation
- Look at `common/` folder to understand shared utilities

### Step 3: Running the Application
- Use scripts in `scripts/` folder
- Follow guides in `documentation/guides/`
- Try the interactive demo with `example.py`

## 🔧 Development Structure

### Core Application (`src/`)
- **aim_processor.py**: Main processing engine
- **config/**: Configuration and settings management
- **mappers/**: Field mapping and transformation logic
- **parsers/**: Data parsing from various formats
- **validators/**: Input validation and error checking

### Shared Code (`common/`)
- **ui_utils.py**: Reusable UI components and styling
- **database_manager.py**: Database operations and data persistence
- **file_manager.py**: File handling, Excel operations, imports/exports

### Learning Materials (`tutorials/`)
- **python_basics/**: Python language fundamentals
- **project_examples/**: Project-specific code explanations
- Designed for beginners to understand both Python and this project

## 📖 File Descriptions

### Main Application Files
- `example.py` - Interactive GUI demo application
- `aim_processor.py` - Core processing logic
- `requirements.txt` - Python package dependencies

### Tutorial Files
- `PYTHON_TUTORIAL_INTERACTIVE.py` - Hands-on Python examples
- `PYTHON_BASICS_EXPLAINED.py` - Comprehensive Python guide
- `YOUR_FILE_EXPLAINED.py` - Project-specific code explanation

### Documentation Files
- `EXCEL_MAPPING_GUIDE.md` - How to use Excel mapping features
- `TROUBLESHOOTING_GUIDE.md` - Common issues and solutions
- `FILE_REQUIREMENTS_GUIDE.md` - File format requirements

### Script Files
- `launch_aim.bat` - Launch the main application
- `setup_and_run.bat` - Setup environment and run
- `start.bat` - Quick start script

## 🎨 Benefits of This Organization

1. **Separation of Concerns**: Code, tutorials, docs, and scripts are separated
2. **Easy Learning**: Clear learning path from basics to advanced
3. **Better Maintenance**: Related files are grouped together
4. **Scalability**: Easy to add new features in appropriate folders
5. **Professional Structure**: Follows industry best practices

## 🚀 Next Steps

1. **For Beginners**: Start with the tutorial files
2. **For Developers**: Explore the src/ and common/ folders
3. **For Users**: Use the scripts/ folder to run the application
4. **For Documentation**: Check documentation/guides/ for help

---
*This structure makes the project more professional, maintainable, and beginner-friendly!*
