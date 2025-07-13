# Demo Notes - Tkinter SQLite Desktop App

A simple, attractive desktop note-taking application built with Python Tkinter and SQLite. Designed to run as a single executable on Windows 11 and Ubuntu Linux 22.04 with minimal dependencies.

## Features

### Core Functionality
- **SQLite Database**: Auto-creates `notes.db` with notes table (note_id, note)
- **CRUD Operations**: Create, Read, Update, Delete notes
- **Data Grid**: Displays all notes with proper spacing and styling
- **Modal Dialogs**: Dedicated windows for adding/editing notes

### User Interface
- **900px wide resizable window** titled "Demo Notes"
- **Buttons above data grid**: New Record, Edit, Delete, Excel Export, MD Export, Close
- **Character validation**: Warning at 200 chars, error at 255 chars
- **Error handling**: Red labels display database errors and validation messages
- **Keyboard shortcuts**: Ctrl+N (new record), Ctrl+S (save in dialog)
- **Double-click editing**: Double-click any row to edit

### Export Features
- **Excel Export**: Exports to .xlsx with timestamps using openpyxl
- **Markdown Export**: Exports to .md with GitHub table formatting
- **File dialogs**: User selects save location with default filenames

### Data Validation
- **Confirmation dialogs**: Required for delete and save operations
- **Real-time character counting**: Shows current/max characters while typing
- **Error prevention**: Prevents saving empty notes or notes over 255 characters

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

## Technical Details

- **Single file architecture**: All code in `main.py` using functional programming
- **Database**: SQLite with open/close per operation for robustness
- **GUI Framework**: Tkinter (built-in with Python)
- **Dependencies**: Only openpyxl for Excel export functionality
- **Target Platforms**: Windows 11 and Ubuntu Linux 22.04

## Usage

1. **Adding Notes**: Click "New Record" or press Ctrl+N
2. **Editing Notes**: Double-click a row or select and click "Edit"
3. **Deleting Notes**: Select a row and click "Delete" (requires confirmation)
4. **Exporting Data**: Use "Excel Export" or "MD Export" buttons
5. **Saving**: Use "Save" button in dialogs or press Ctrl+S

The application automatically creates the database and table on first run, making it ready to use immediately.