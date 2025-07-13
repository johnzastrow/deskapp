# Changelog

## [1.0.0] - 2025-07-13

### Initial Release
- Complete Tkinter SQLite desktop note-taking application
- All core features implemented and tested

### Features
- SQLite database with auto-creation (notes.db)
- CRUD operations for notes (Create, Read, Update, Delete)
- 900px wide resizable window titled "Demo Notes"
- Data grid with proper styling and row height
- Modal dialogs for adding/editing notes
- Character validation (warning at 200, error at 255 characters)
- Confirmation dialogs for delete and save operations
- Excel export with timestamps (.xlsx format)
- Markdown export with GitHub table formatting
- Keyboard shortcuts: Ctrl+N (new), Ctrl+S (save)
- Double-click editing support
- Error handling with red UI labels
- File dialogs for export location selection

### Technical Details
- Single file architecture (main.py)
- Functional programming approach
- Open/close database connections per operation
- Cross-platform support (Windows 11, Ubuntu 22.04)
- Minimal dependencies (only openpyxl)

### Bug Fixes During Development
- Fixed tree/scrollbar packing issues
- Resolved modal dialog grab errors
- Corrected file dialog parameter names
- Improved data grid visual spacing
- Added proper styling to prevent text overlap