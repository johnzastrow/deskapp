# Demo Notes - Tkinter SQLite Desktop App

A simple, feature-complete desktop note-taking application built with Python Tkinter and SQLite. Production-ready with comprehensive functionality and designed to run as a single executable on Windows 11 and Ubuntu Linux 22.04.

## Project Status

**Current Version**: 1.0.0 (Released 2025-07-13)  
**Build Status**: ✅ Complete and Fully Tested  
**Code Lines**: 649 lines in single `main.py` file  
**Requirements**: All 18 core requirements implemented ✅

## Features

### Core Functionality
- **SQLite Database**: Auto-creates `notes.db` with notes table (note_id, note)
- **CRUD Operations**: Create, Read, Update, Delete notes with full validation
- **Data Grid**: Treeview displays all notes with proper spacing and styling
- **Modal Dialogs**: Dedicated windows for adding/editing notes with character validation

### User Interface
- **900px wide resizable window** titled "Demo Notes"
- **Buttons above data grid**: New Record, Edit, Delete, Excel Export, MD Export, Close
- **Character validation**: Warning at 200 chars, error at 255 chars with real-time feedback
- **Error handling**: Red labels display database errors and validation messages
- **Keyboard shortcuts**: Ctrl+N (new record), Ctrl+S (save in dialog)
- **Double-click editing**: Double-click any row to edit instantly

### Export Features
- **Excel Export**: Exports to .xlsx with timestamps using openpyxl (sheet: "Exported Notes")
- **Markdown Export**: Exports to .md with GitHub table formatting
- **File dialogs**: User selects save location with default filenames (notes_export.xlsx, notes_export.md)

### Data Validation & UX
- **Confirmation dialogs**: Required for delete and save operations
- **Real-time character counting**: Shows current/max characters while typing
- **Error prevention**: Prevents saving empty notes or notes over 255 characters
- **Status feedback**: All operations provide immediate user feedback

## Architecture & Design Decisions

### Technical Architecture
- **Single file design**: All 649 lines in `main.py` using functional programming approach
- **Database strategy**: SQLite with open/close per operation for maximum robustness
- **GUI Framework**: Tkinter (built-in with Python) for cross-platform compatibility
- **Dependencies**: Minimal - only openpyxl for Excel export functionality
- **Target Platforms**: Windows 11 and Ubuntu Linux 22.04

### Key Design Patterns
- **Function return pattern**: (success_boolean, data_or_error_message) for consistent error handling
- **Event-driven GUI**: Callback functions for all user interactions
- **Modal dialogs**: Data entry with real-time validation and confirmation
- **File dialogs**: User-controlled export location selection
- **Inline error display**: Red labels for immediate feedback instead of status bars

### Development History
**Major Issues Resolved During Development:**
1. Tree/scrollbar packing issues - Fixed parent-child relationships
2. Modal dialog grab errors - Added update_idletasks() before grab_set()
3. File dialog parameters - Corrected initialvalue to initialfile
4. Data grid visual overlap - Enhanced row height and styling
5. Grid lines visibility - Added proper styling for better visual separation

## Installation & Setup

### Prerequisites
```bash
# Install tkinter (Linux only)
sudo apt install python3-tk

# Install dependencies with uv
uv add openpyxl
```

### Running the Application
```bash
uv run python main.py
```

### Building Executable
```bash
# Install PyInstaller
uv add pyinstaller

# Build single executable
pyinstaller --onefile main.py
```

# Windows executable
Using the main.exe in the dist folder

Or build it yourself using

1. `uv venv`
2. `uv pip install pyinstaller`
3. `uv run pyinstaller --onefile main.py`  main.py informs the .exe name


## Requirements Met

All 18 core requirements from `requirements.md` and `CLAUDE.md` have been implemented:

**✅ Data Management (2/2)**
- SQLite database in same directory as executable
- No database migration/versioning needed

**✅ UI Layout & Design (3/3)**
- 900px wide resizable window
- Data grid without sorting/filtering
- Modal dialogs using Tkinter

**✅ Export Functionality (2/2)**
- Excel export using openpyxl library
- Exports include timestamps

**✅ Error Handling & UX (3/3)**
- Database errors displayed as red labels
- Character validation (200 char warning, 255 char error)
- Confirmation dialogs for delete and save operations

**✅ Packaging & Distribution (2/2)**
- PyInstaller packaging support
- Windows 11 and Ubuntu Linux 22.04 compatibility

**✅ Additional Implementation Details (6/6)**
- Single main.py file with functional programming style
- Database filename: notes.db with auto-creation
- Always display full note text in grid
- Buttons placed above data grid
- Export defaults with user file selection
- Keyboard shortcuts: Ctrl+N (new), Ctrl+S (save)

## Usage

1. **Adding Notes**: Click "New Record" or press Ctrl+N
2. **Editing Notes**: Double-click a row or select and click "Edit"
3. **Deleting Notes**: Select a row and click "Delete" (requires confirmation)
4. **Exporting Data**: Use "Excel Export" or "MD Export" buttons
5. **Saving**: Use "Save" button in dialogs or press Ctrl+S

## Development Environment

- **Package Management**: uv (for dependencies)
- **Testing**: All functionality manually tested and verified
- **Code Quality**: Syntax validated, no compilation errors
- **Documentation**: Comprehensive inline documentation and architecture overview

The application is production-ready and automatically creates the database and table on first run, making it ready to use immediately.