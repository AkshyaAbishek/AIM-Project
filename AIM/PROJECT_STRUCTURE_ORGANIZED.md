# 📁 AIM Project - Organized Structure Guide

## 🎯 Overview

The AIM (Actuarial Input Mapper) project has been completely reorganized into a professional, modular structure that separates concerns and improves maintainability, development workflow, and deployment processes.

## 📂 New Project Structure

```
AIM/
├── 📁 core/                         # Core application components
│   └── 📁 web/                      # Web application (Flask)
│       ├── web_app.py               # Main Flask application
│       ├── startup.py               # Application startup script
│       ├── start_app.py             # App launcher
│       ├── run_app.py               # Run configuration
│       ├── web.config               # Web server configuration
│       ├── 📁 templates/            # HTML templates
│       │   ├── base.html            # Base template
│       │   ├── index.html           # Dashboard
│       │   ├── field_mapping.html   # Field mapping interface
│       │   ├── compare.html         # Data comparison
│       │   ├── upload.html          # File upload
│       │   └── ...                  # Other templates
│       └── 📁 static/               # Static assets (CSS, JS, images)
│           ├── 📁 css/              # Stylesheets
│           ├── 📁 js/               # JavaScript files
│           └── 📁 img/              # Images
│
├── 📁 src/                          # Source code modules
│   ├── aim_processor.py             # Main processing engine
│   ├── __init__.py                  # Package initialization
│   ├── 📁 config/                   # Configuration management
│   ├── 📁 mappers/                  # Field mapping modules
│   ├── 📁 parsers/                  # Data parsing modules
│   └── 📁 validators/               # Input validation modules
│
├── 📁 common/                       # Shared utilities
│   ├── database_manager.py          # Database operations
│   ├── file_manager.py              # File handling utilities
│   └── ui_utils.py                  # UI components and styling
│
├── 📁 config/                       # Configuration files
│   ├── annuity_template.json        # Annuity product template
│   └── life_template.json           # Life insurance template
│
├── 📁 database/                     # Database files
│   └── aim_data.db                  # SQLite database
│
├── 📁 runtime/                      # Runtime data and generated files
│   ├── 📁 uploads/                  # User uploaded files
│   ├── 📁 exports/                  # Generated export files
│   ├── 📁 logs/                     # Application logs
│   │   ├── aim_processor.log        # Processing logs
│   │   ├── app_error.log            # Error logs
│   │   └── app_output.log           # Output logs
│   ├── 📁 backups/                  # Backup files
│   ├── 📁 temp_uploads/             # Temporary upload files
│   └── 📁 saved_mappings/           # Saved field mappings
│
├── 📁 development/                  # Development and testing files
│   ├── 📁 testing/                  # Test files and scripts
│   │   ├── test_app.py              # Application tests
│   │   ├── test_db.py               # Database tests
│   │   ├── test_import_*.py         # Import functionality tests
│   │   ├── test_compare_*.py        # Comparison tests
│   │   ├── test_*.html              # Test HTML files
│   │   ├── test_*.json              # Test data files
│   │   ├── test_*.xlsx              # Test Excel files
│   │   ├── check_*.py               # Check scripts
│   │   ├── debug_*.py               # Debug scripts
│   │   ├── diagnose_*.py            # Diagnostic scripts
│   │   └── 📁 tests/                # Organized test suites
│   └── 📁 sample_data/              # Sample data generation
│       ├── add_sample_data.py       # Add sample data script
│       ├── add_test_data.py         # Add test data script
│       ├── add_compare_test.py      # Add comparison test data
│       └── create_test_excel.py     # Create test Excel files
│
├── 📁 deployment/                   # Deployment configuration
│   ├── deploy-to-azure-main.ps1     # PowerShell Azure deployment
│   ├── deploy-to-azure-main.sh      # Shell Azure deployment
│   ├── deploy-to-azure.ps1          # Original deployment script
│   ├── deploy-to-azure.sh           # Original deployment script
│   └── web.config                   # Web server config
│
├── 📁 project_docs/                 # Project documentation
│   ├── 📁 analysis/                 # Project analysis and reports
│   │   ├── PROJECT_ANALYSIS_COMPREHENSIVE.md  # Complete project analysis
│   │   ├── IMPORT_TEMPLATE_FIX_SUMMARY.md     # Import fixes summary
│   │   ├── COMPARE_PAGE_CLEANUP_SUMMARY.md    # Compare page cleanup
│   │   ├── UPLOAD_FIXES_SUMMARY.md            # Upload fixes summary
│   │   └── DEBUG_ANALYSIS.md                  # Debug analysis
│   ├── 📁 guides/                   # User and developer guides
│   │   ├── PROJECT_STRUCTURE_GUIDE.md         # This file
│   │   └── AZURE_QUICK_START.md               # Azure deployment guide
│   ├── 📁 user_documentation/       # User guides and help
│   │   └── 📁 guides/               # Detailed user guides
│   └── 📁 technical_docs/           # Technical documentation
│
├── 📁 scripts/                      # Launch and utility scripts
│   ├── launch_aim.bat               # Windows launcher
│   ├── launch_aim_pro.bat           # Professional launcher
│   ├── setup_and_run.bat            # Setup and run script
│   └── start.bat                    # Quick start script
│
├── 📁 tutorials/                    # Learning materials
│   ├── 📁 python_basics/            # Python fundamentals
│   ├── 📁 project_examples/         # Project-specific examples
│   └── README.md                    # Tutorial guide
│
├── 📁 utils/                        # Utility tools
│   └── create_sample_calculator.py  # Sample calculator creator
│
├── 📁 data/                         # Data files and templates
│   └── 📁 sample/                   # Sample data files
│
├── 📁 app/                          # Legacy application files
│   └── ...                         # Original desktop application
│
├── 📁 .vscode/                      # VS Code configuration
├── 📁 .git/                         # Git repository
├── 📁 __pycache__/                  # Python cache files
│
├── launch_aim.py                    # New main launcher script
├── launch_aim.ps1                   # PowerShell launcher
├── README.md                        # Project overview
├── requirements.txt                 # Python dependencies
├── requirements-web.txt             # Web-specific dependencies
├── requirements-ai.txt              # AI/ML dependencies
├── .env.production                  # Production environment variables
├── .gitignore                       # Git ignore rules
└── aim_data.db                      # Database (legacy location)
```

## 🚀 How to Run the Application

### Method 1: Using the New Launcher (Recommended)
```bash
# From the AIM root directory
python launch_aim.py
```

### Method 2: Using PowerShell Script
```powershell
# Windows PowerShell
.\launch_aim.ps1
```

### Method 3: Using Batch Scripts
```cmd
# Windows Command Prompt
scripts\start.bat
```

### Method 4: Direct Flask Run
```bash
# Navigate to web app directory
cd core\web
python web_app.py
```

## 📋 Key Benefits of New Structure

### 🎯 **Separation of Concerns**
- **Core**: Application logic and web interface
- **Runtime**: Generated files, logs, uploads
- **Development**: Testing and debugging tools
- **Documentation**: All project documentation organized

### 🔧 **Development Workflow**
- **Clear Testing**: All test files in `development/testing/`
- **Easy Debugging**: Debug scripts and logs separated
- **Sample Data**: Development data generation tools organized
- **Documentation**: Comprehensive docs in `project_docs/`

### 🚀 **Deployment Ready**
- **Clean Separation**: Runtime data separate from code
- **Azure Ready**: Deployment scripts in `deployment/`
- **Environment Config**: Environment-specific configurations
- **Scalable**: Structure supports growth and team development

### 📊 **Maintenance & Operations**
- **Log Management**: All logs in `runtime/logs/`
- **Backup Strategy**: Backups in `runtime/backups/`
- **Database Management**: Database files in `database/`
- **File Organization**: Clear file organization and naming

## 🔄 Migration Guide

### **Updated Import Paths**
The new launcher (`launch_aim.py`) automatically handles all path configurations. However, if you need to run components directly:

```python
# Old import (from root)
from src.aim_processor import AIMProcessor

# New import (handled automatically by launcher)
from aim_processor import AIMProcessor
```

### **Database Path**
- **Old**: `aim_data.db` (in root)
- **New**: `database/aim_data.db`
- **Automatic**: Launcher copies database to new location if needed

### **Upload/Export Paths**
- **Uploads**: `runtime/uploads/` (was `uploads/`)
- **Exports**: `runtime/exports/` (was `exports/`)
- **Logs**: `runtime/logs/` (was root directory)

## 🛠️ Development Guidelines

### **Adding New Features**
1. **Core Logic**: Add to `src/` modules
2. **Web Interface**: Update `core/web/` templates and routes
3. **Tests**: Add to `development/testing/`
4. **Documentation**: Update `project_docs/`

### **File Naming Conventions**
- **Test Files**: `test_*.py`
- **Debug Files**: `debug_*.py`
- **Config Files**: `*_config.json` or `*.config`
- **Template Files**: `*_template.*`

### **Directory Guidelines**
- **Never commit**: `runtime/` contents (except directory structure)
- **Version Control**: All `src/`, `core/`, `config/` contents
- **Backup Important**: `database/` and `project_docs/`

## 📈 Performance & Scalability

### **Optimized Structure**
- **Fast Access**: Frequently used files in `core/`
- **Efficient Logging**: Centralized in `runtime/logs/`
- **Clean Separation**: Runtime data doesn't interfere with code
- **Docker Ready**: Structure supports containerization

### **Resource Management**
- **Upload Limits**: Configurable in web app settings
- **Log Rotation**: Can be implemented in `runtime/logs/`
- **Backup Automation**: Scripts can target `runtime/backups/`
- **Database Scaling**: Can move to separate server easily

## 🎯 Next Steps

1. **Test the New Structure**: Run `python launch_aim.py`
2. **Update Bookmarks**: Use new launcher for consistency
3. **Review Documentation**: Check `project_docs/` for latest info
4. **Customize as Needed**: Adapt structure for your specific needs

---

## 🏆 Result: Professional Project Organization

This new structure transforms the AIM project into a **professional, enterprise-ready application** with:

- ✅ **Clear Separation of Concerns**
- ✅ **Scalable Architecture**  
- ✅ **Easy Maintenance**
- ✅ **Development-Friendly**
- ✅ **Deployment-Ready**
- ✅ **Documentation-Rich**

*The organized structure supports both current needs and future growth, making AIM a truly professional actuarial data processing solution.*
