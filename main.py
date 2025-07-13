"""
Demo Notes - Tkinter SQLite Desktop Application

A simple note-taking desktop application built with Python's Tkinter GUI framework
and SQLite database. Features CRUD operations, data validation, and export functionality.

ARCHITECTURE OVERVIEW:
====================
- Single file design using functional programming
- SQLite database with open/close per operation for robustness
- Tkinter for cross-platform GUI (Windows 11, Ubuntu 22.04)
- Modal dialogs for user interactions
- Real-time character validation and error handling

CODE STRUCTURE:
===============
1. IMPORTS & CONSTANTS: Required libraries and global constants
2. DATABASE FUNCTIONS: All SQLite operations (init, CRUD operations)
3. UI FUNCTIONS: GUI operations, event handlers, dialogs
4. EXPORT FUNCTIONS: Excel and Markdown export functionality
5. MAIN WINDOW: Window creation, layout, and styling
6. APPLICATION ENTRY: Main function and startup logic

KEY DESIGN PATTERNS:
===================
- Function return pattern: (success_boolean, data_or_error_message)
- Event-driven GUI with callback functions
- Modal dialogs for data entry with validation
- Real-time user feedback through UI labels
- File dialogs for export operations
- Keyboard shortcuts for common operations

DEPENDENCIES:
=============
- tkinter: Built-in GUI framework (cross-platform)
- sqlite3: Built-in database (no external server needed)
- openpyxl: Excel file creation (only external dependency)
- datetime: Timestamp generation for exports

Author: Generated with Claude Code
Date: 2025-07-13
"""

# Standard library imports for GUI, database, and file operations
import tkinter as tk                    # Main GUI framework
from tkinter import ttk, messagebox, filedialog  # Enhanced widgets and dialogs
import sqlite3                         # Embedded database
import os                              # File system operations
from datetime import datetime          # Timestamp generation for exports
import openpyxl                        # Excel file creation
from openpyxl.worksheet.table import Table, TableStyleInfo  # Excel formatting

# Global constant for database filename
# Database will be created in the same directory as the executable
DB_FILE = "notes.db"

# =============================================================================
# DATABASE FUNCTIONS
# These functions handle all SQLite database operations using the pattern:
# 1. Open connection to database file
# 2. Execute SQL operation
# 3. Commit changes (for write operations)
# 4. Close connection
# 5. Return (success_boolean, data_or_error_message)
# =============================================================================

def init_database():
    """
    Initialize the database and create the notes table if it doesn't exist.
    
    This function is called once at application startup to ensure the database
    exists and has the proper table structure. Uses CREATE TABLE IF NOT EXISTS
    to avoid errors if the database already exists.
    
    Returns:
        tuple: (success: bool, error_message: str)
               success=True if database created successfully, error_message if failed
    """
    try:
        # Open connection to SQLite database file (creates file if doesn't exist)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create notes table with auto-incrementing ID and text field
        # IF NOT EXISTS prevents error if table already exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT NOT NULL
            )
        ''')
        
        # Commit the transaction to save changes
        conn.commit()
        # Always close connection to free resources
        conn.close()
        return True, ""
    except Exception as e:
        # Return error details if database operation fails
        return False, str(e)

def get_notes():
    """
    Retrieve all notes from the database ordered by note_id.
    
    This is a read-only operation that fetches all records from the notes table.
    Used to populate the main data grid and for export operations.
    
    Returns:
        tuple: (success: bool, notes_list_or_error: list|str)
               If successful: (True, [(note_id, note_text), ...])
               If failed: (False, error_message)
    """
    try:
        # Open database connection
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Select all notes ordered by ID (oldest first)
        cursor.execute("SELECT note_id, note FROM notes ORDER BY note_id")
        
        # Fetch all results as list of tuples: [(id, text), (id, text), ...]
        notes = cursor.fetchall()
        
        # Close connection (no commit needed for read operations)
        conn.close()
        return True, notes
    except Exception as e:
        # Return error message if database operation fails
        return False, str(e)

def add_note(note_text):
    """
    Add a new note to the database.
    
    Inserts a new record with auto-generated note_id and provided text.
    Uses parameterized query to prevent SQL injection attacks.
    
    Args:
        note_text (str): The text content of the note to add
        
    Returns:
        tuple: (success: bool, error_message: str)
               success=True if note added successfully, error_message if failed
    """
    try:
        # Open database connection
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Insert new note using parameterized query (? placeholder prevents SQL injection)
        # note_id will be auto-generated by AUTOINCREMENT
        cursor.execute("INSERT INTO notes (note) VALUES (?)", (note_text,))
        
        # Commit the transaction to save the new record
        conn.commit()
        conn.close()
        return True, ""
    except Exception as e:
        # Return error details if insert operation fails
        return False, str(e)

def update_note(note_id, note_text):
    """
    Update an existing note in the database.
    
    Modifies the text content of a note with the specified ID.
    Uses parameterized query for security.
    
    Args:
        note_id (int): The ID of the note to update
        note_text (str): The new text content for the note
        
    Returns:
        tuple: (success: bool, error_message: str)
               success=True if note updated successfully, error_message if failed
    """
    try:
        # Open database connection
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Update existing note using parameterized query
        # Parameters are ordered: new_text, note_id_to_match
        cursor.execute("UPDATE notes SET note = ? WHERE note_id = ?", (note_text, note_id))
        
        # Commit the transaction to save changes
        conn.commit()
        conn.close()
        return True, ""
    except Exception as e:
        # Return error details if update operation fails
        return False, str(e)

def delete_note(note_id):
    """
    Delete a note from the database.
    
    Permanently removes a note record with the specified ID.
    This operation cannot be undone.
    
    Args:
        note_id (int): The ID of the note to delete
        
    Returns:
        tuple: (success: bool, error_message: str)
               success=True if note deleted successfully, error_message if failed
    """
    try:
        # Open database connection
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Delete note using parameterized query
        cursor.execute("DELETE FROM notes WHERE note_id = ?", (note_id,))
        
        # Commit the transaction to save changes
        conn.commit()
        conn.close()
        return True, ""
    except Exception as e:
        # Return error details if delete operation fails
        return False, str(e)

# =============================================================================
# USER INTERFACE FUNCTIONS
# These functions handle GUI operations, user interactions, and data display
# =============================================================================

def refresh_notes_grid(tree, error_label):
    """
    Refresh the notes grid with current data from database.
    
    This function is called whenever the data changes (add, edit, delete operations)
    to ensure the UI displays the most current information.
    
    Args:
        tree (ttk.Treeview): The data grid widget to refresh
        error_label (tk.Label): Label widget for displaying error messages
    """
    # Clear all existing items from the tree view
    # tree.get_children() returns all top-level items
    for item in tree.get_children():
        tree.delete(item)
    
    # Fetch current notes from database
    success, notes = get_notes()
    if not success:
        # If database error, display error message and exit
        show_error(error_label, f"Database error: {notes}")
        return
    
    # Insert each note as a row in the tree view
    # notes is a list of tuples: [(note_id, note_text), ...]
    for note_id, note_text in notes:
        # Insert at end ("") with values for both columns
        tree.insert("", "end", values=(note_id, note_text))

def validate_note_length(text_widget, validation_label):
    """
    Validate note text length and show warnings/errors in real-time.
    
    This function provides immediate feedback to users about character limits:
    - Black text: Normal (under 200 characters)
    - Orange text: Warning (200-254 characters) 
    - Red text: Error (255+ characters, prevents saving)
    
    Args:
        text_widget (tk.Text): The text input widget to validate
        validation_label (tk.Label): Label to display validation message
        
    Returns:
        bool: True if text length is valid (under 255), False if over limit
    """
    # Get text content from Text widget
    # "1.0" = line 1, character 0 (start)
    # "end-1c" = end minus 1 character (excludes automatic newline)
    content = text_widget.get("1.0", "end-1c")
    length = len(content)
    
    # Check length and update validation label with appropriate color
    if length >= 255:
        # Error state: prevent saving
        validation_label.config(text="Error: Note exceeds 255 characters", fg="red")
        return False
    elif length >= 200:
        # Warning state: allow saving but warn user
        validation_label.config(text=f"Warning: {length}/255 characters", fg="orange")
        return True
    else:
        # Normal state: display character count
        validation_label.config(text=f"{length}/255 characters", fg="black")
        return True

def note_edit_dialog(parent, note_id=None, note_text="", tree=None, error_label=None):
    """
    Create modal dialog for adding/editing notes.
    
    This function creates a popup window with a text editor for note content.
    It handles both new note creation (note_id=None) and editing existing notes.
    The dialog includes real-time character validation and keyboard shortcuts.
    
    Dialog Features:
    - Modal (blocks interaction with main window)
    - Resizable text area with scrollbar
    - Real-time character counting and validation
    - Save/Cancel buttons with confirmation
    - Ctrl+S keyboard shortcut for saving
    
    Args:
        parent (tk.Tk): Parent window for modal dialog
        note_id (int, optional): ID of note to edit (None for new note)
        note_text (str, optional): Existing text content (empty for new note)
        tree (ttk.Treeview, optional): Main data grid to refresh after save
        error_label (tk.Label, optional): Label for displaying errors
    """
    dialog = tk.Toplevel(parent)
    dialog.title("New Note" if note_id is None else f"Edit Note {note_id}")
    dialog.geometry("500x400")
    dialog.resizable(True, True)
    dialog.transient(parent)
    
    # Wait for dialog to be created before grabbing
    dialog.update_idletasks()
    dialog.grab_set()
    
    # Center the dialog
    dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    
    # Note label
    tk.Label(dialog, text="Note:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
    
    # Text widget with scrollbar
    text_frame = tk.Frame(dialog)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15)
    text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=text_scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Insert existing text if editing
    if note_text:
        text_widget.insert("1.0", note_text)
    
    # Validation label
    validation_label = tk.Label(dialog, text="0/255 characters", fg="black")
    validation_label.pack(anchor="w", padx=10, pady=(0, 5))
    
    # Update validation on text change
    def on_text_change(event=None):
        validate_note_length(text_widget, validation_label)
    
    text_widget.bind("<KeyRelease>", on_text_change)
    text_widget.bind("<Button-1>", on_text_change)
    text_widget.bind("<ButtonRelease-1>", on_text_change)
    
    # Initial validation
    on_text_change()
    
    # Button frame
    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)
    
    def on_save():
        """Handle save button click."""
        content = text_widget.get("1.0", "end-1c").strip()
        
        if len(content) >= 255:
            messagebox.showerror("Error", "Note text exceeds 255 characters")
            return
        
        if not content:
            messagebox.showerror("Error", "Note cannot be empty")
            return
        
        # Confirm save
        if messagebox.askyesno("Confirm Save", "Are you sure you want to save this note?"):
            if note_id is None:
                # Add new note
                success, error = add_note(content)
                action = "added"
            else:
                # Update existing note
                success, error = update_note(note_id, content)
                action = "updated"
            
            if success:
                if tree and error_label:
                    refresh_notes_grid(tree, error_label)
                dialog.destroy()
            else:
                messagebox.showerror("Database Error", f"Failed to save note: {error}")
    
    def on_cancel():
        """Handle cancel button click."""
        dialog.destroy()
    
    # Save button
    btn_save = tk.Button(button_frame, text="Save", command=on_save)
    btn_save.pack(side=tk.LEFT, padx=5)
    
    # Cancel button
    btn_cancel = tk.Button(button_frame, text="Cancel", command=on_cancel)
    btn_cancel.pack(side=tk.LEFT, padx=5)
    
    # Focus on text widget
    text_widget.focus_set()
    
    # Handle Ctrl+S shortcut
    def handle_ctrl_s(event):
        on_save()
    
    dialog.bind("<Control-s>", handle_ctrl_s)
    dialog.bind("<Control-S>", handle_ctrl_s)

def on_new_record(tree, error_label):
    """Handle new record button click."""
    root = tree.winfo_toplevel()
    note_edit_dialog(root, tree=tree, error_label=error_label)

def on_edit_record(tree, error_label):
    """Handle edit record action."""
    selection = tree.selection()
    if not selection:
        show_error(error_label, "Please select a record to edit")
        return
    
    item = tree.item(selection[0])
    note_id, note_text = item['values']
    root = tree.winfo_toplevel()
    note_edit_dialog(root, note_id=note_id, note_text=note_text, tree=tree, error_label=error_label)

def on_delete_record(tree, error_label):
    """Handle delete record action."""
    selection = tree.selection()
    if not selection:
        show_error(error_label, "Please select a record to delete")
        return
    
    item = tree.item(selection[0])
    note_id, note_text = item['values']
    
    # Confirmation dialog
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete note {note_id}?"):
        success, error = delete_note(note_id)
        if success:
            refresh_notes_grid(tree, error_label)
        else:
            show_error(error_label, f"Delete failed: {error}")

# =============================================================================
# EXPORT FUNCTIONS
# These functions handle exporting data to different file formats
# Both functions use file dialogs to let users choose save location
# =============================================================================

def export_to_excel(tree, error_label):
    """Export notes to Excel file."""
    filename = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        initialfile="notes_export.xlsx"
    )
    
    if not filename:
        return
    
    success, notes = get_notes()
    if not success:
        show_error(error_label, f"Database error: {notes}")
        return
    
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Exported Notes"
        
        # Headers
        ws.append(["Note ID", "Note", "Export Date"])
        
        # Data with timestamp
        export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for note_id, note_text in notes:
            ws.append([note_id, note_text, export_time])
        
        wb.save(filename)
        show_error(error_label, f"Exported to {filename}")
        
    except Exception as e:
        show_error(error_label, f"Export failed: {e}")

def export_to_markdown(tree, error_label):
    """Export notes to Markdown file."""
    filename = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Markdown files", "*.md")],
        initialfile="notes_export.md"
    )
    
    if not filename:
        return
    
    success, notes = get_notes()
    if not success:
        show_error(error_label, f"Database error: {notes}")
        return
    
    try:
        export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Exported Notes\n\n")
            f.write(f"Export Date: {export_time}\n\n")
            f.write("| Note ID | Note |\n")
            f.write("|---------|------|\n")
            
            for note_id, note_text in notes:
                # Escape pipe characters in note text
                escaped_note = note_text.replace("|", "\\|")
                f.write(f"| {note_id} | {escaped_note} |\n")
        
        show_error(error_label, f"Exported to {filename}")
        
    except Exception as e:
        show_error(error_label, f"Export failed: {e}")

# =============================================================================
# MAIN WINDOW CREATION
# This section creates the main application window with all UI components
# =============================================================================

def create_main_window():
    """Create the main application window."""
    root = tk.Tk()
    root.title("Demo Notes")
    root.geometry("900x600")
    root.minsize(900, 400)
    
    # Error label for displaying messages
    error_label = tk.Label(root, text="", fg="red", font=("Arial", 10))
    error_label.pack(pady=5)
    
    # Button frame above the data grid
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    # Pack tree and scrollbar frame first
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Create data grid (Treeview) inside tree_frame
    columns = ("ID", "Note")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    tree.heading("ID", text="Note ID")
    tree.heading("Note", text="Note")
    tree.column("ID", width=100, minwidth=50)
    tree.column("Note", width=700, minwidth=200)
    
    # Configure grid lines and row height
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)  # Increase row height to prevent overlap
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    
    # Configure grid lines (platform dependent)
    try:
        style.configure("Treeview", 
                       fieldbackground="#ffffff",
                       background="#ffffff", 
                       foreground="#000000")
        # Try to enable grid lines if supported
        style.map("Treeview", 
                  background=[('selected', '#0078d4')])
    except:
        pass
    
    # Add scrollbar to tree inside tree_frame
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack tree and scrollbar
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Buttons
    btn_new = tk.Button(button_frame, text="New Record", 
                       command=lambda: on_new_record(tree, error_label))
    btn_new.pack(side=tk.LEFT, padx=5)
    
    btn_edit = tk.Button(button_frame, text="Edit", 
                        command=lambda: on_edit_record(tree, error_label))
    btn_edit.pack(side=tk.LEFT, padx=5)
    
    btn_delete = tk.Button(button_frame, text="Delete", 
                          command=lambda: on_delete_record(tree, error_label))
    btn_delete.pack(side=tk.LEFT, padx=5)
    
    btn_excel = tk.Button(button_frame, text="Excel Export", 
                         command=lambda: export_to_excel(tree, error_label))
    btn_excel.pack(side=tk.LEFT, padx=5)
    
    btn_markdown = tk.Button(button_frame, text="MD Export", 
                            command=lambda: export_to_markdown(tree, error_label))
    btn_markdown.pack(side=tk.LEFT, padx=5)
    
    btn_close = tk.Button(button_frame, text="Close", command=root.quit)
    btn_close.pack(side=tk.LEFT, padx=5)
    
    # Double-click to edit
    tree.bind("<Double-1>", lambda event: on_edit_record(tree, error_label))
    
    # Keyboard shortcuts
    def handle_ctrl_n(event):
        on_new_record(tree, error_label)
    
    root.bind("<Control-n>", handle_ctrl_n)
    root.bind("<Control-N>", handle_ctrl_n)
    
    return root, error_label, tree

def show_error(error_label, message):
    """Display error message in the UI."""
    error_label.config(text=message)
    error_label.after(5000, lambda: error_label.config(text=""))

# =============================================================================
# APPLICATION ENTRY POINT
# Main function that initializes database and starts the GUI application
# =============================================================================

def main():
    """Main application entry point."""
    success, error = init_database()
    if not success:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Database Error", f"Failed to initialize database: {error}")
        return
    
    root, error_label, tree = create_main_window()
    
    # Load initial data
    refresh_notes_grid(tree, error_label)
    
    root.mainloop()

if __name__ == "__main__":
    main()