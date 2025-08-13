# VibeCode Project

This repository contains various Python projects and tools developed for data processing, analysis, and automation.

## Projects Included

### 1. AIM (Actuarial Input Manager)
A comprehensive GUI application for managing actuarial data with features including:
- **JSON Data Management**: Add, view, and manage JSON data
- **Bulk Data Loading**: Excel-based bulk data import with preview
- **Field Mapping**: Automated field mapping between FAST UI and Actuarial Calculator
- **Database Integration**: SQLite database for persistent storage
- **Data Validation**: Duplicate checking and data validation
- **Export Functionality**: Export data to various formats

**Key Features:**
- ✅ User-friendly GUI interface
- ✅ Bulk JSON upload with Excel templates
- ✅ Real-time data preview and validation
- ✅ Scrollable interfaces with loading indicators
- ✅ Comprehensive help documentation
- ✅ Database backup and restore functionality

### 2. Actuarial Input Builder
A modular system for building and processing actuarial inputs with configurable mappings and validation.

### 3. General Utilities
- **Prime Checker**: Prime number validation utilities
- **Palindrome Checker**: String and number palindrome detection

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd VibeCode
   ```

2. **Set up Python virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the AIM Application:
```bash
cd AIM/app
python example.py
```

### Key Dependencies:
- `tkinter` - GUI framework
- `pandas` - Data manipulation and Excel operations
- `openpyxl` - Excel file handling
- `sqlite3` - Database operations

## Project Structure

```
VibeCode/
├── AIM/                    # Actuarial Input Manager
│   ├── app/               # Main application files
│   ├── backup/            # Backup files
│   ├── data/              # Data files and samples
│   ├── docs/              # Documentation
│   └── src/               # Source code modules
├── ActurialInputBuilder/   # Input builder system
├── General/               # General utilities
└── requirements.txt       # Python dependencies
```

## Recent Enhancements (August 2025)

- ✅ **Scrollable Bulk Load Preview**: Added full scrollbar support for bulk data preview
- ✅ **Separate Save Buttons**: Clear "Save to Database" and "Close Preview" options
- ✅ **Loading Indicators**: Comprehensive progress feedback for all operations
- ✅ **Enhanced Field Mapping**: Improved Excel integration with better error handling
- ✅ **User Experience Improvements**: Better visual feedback and guidance

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please open an issue in this repository.

---

**Last Updated**: August 1, 2025
**Version**: 2.0 (Enhanced with scrollable UI and improved UX)
