# Requirement answers

  1. Where should the SQLite database file be stored? A: The sqlite database should stored in the same directory as the code or executable.

  2. Should we handle database migration/versioning? A: No, do not handle migration and versioning at this time.

  UI Layout & Design:
  3. Preferred window size and resizable? A: the window size should be 900px wide and be resizable
  4. Want sorting/filtering in the data grid? A: the data grid does not require filtering or sorting. 
  5. Edit dialog - modal or separate window? A: the edit dialog is best a modal if possible using tkinter

  Export Functionality:
  6. Excel export - openpyxl library OK or prefer CSV for fewer dependencies? A: Use openpyxl.
  7. Should exports include timestamps? A: Yes, the exports should include timestamps

  Error Handling & UX:
  8. How to handle database errors? A: display errors as labels in the user interface in red letters
  9. Any data validation on notes (max length, required)? A: warn users when the notes entry in the field hits 200 characters, issue an error when the entry hits 255. The warnings and errors should be displayed as labels in the UI.
  10. Confirmations beyond delete? A: also confirm when saving an edit.

  Packaging & Distribution:
  11. Packaging tool preference (PyInstaller, etc.)? A: use pyinstaller 
  12. Target Windows versions? A: target Windows 11 and Ubuntu Linux 22.04
1.  ● Here are some additional implementation details we should consider:

  Code Structure & Organization:
  1. Single main.py file or split into modules?
  2. Class-based or functional programming style?

  Database Details:
  3. Database filename convention?
  4. Auto-create database/table on first run?
  5. Connection handling strategy?

  UI Component Specifics:
  6. Treeview columns - show note_id and truncated note? A: alwats display the full note text.
  7. How to handle long notes in grid display?
  8. Button layout preferences? A: Place buttons above the data grid
  9. Status bar vs inline labels for messages? A: Use inline labels

  Export File Details:
  10. Export filename format? A: default to saving in the directory of the application, but ask the user where to save and the file name. The default file names should be `notes_export.md` and `notes_export`.xlsx 
  11. Excel sheet name and formatting? A: the sheet name should be `Exported Notes` without any formatting
  12. Markdown table format and columns? A: use Github formatting

  Error Scenarios:
  13. Read-only export location handling? A: Yes, report all errors with the database
  14. Database locked by another process? A: yes, report any locks 
  15. Empty database export behavior? A: create any databases and tables or other database objects if they are not present

  User Experience:
  16. Default focus on startup? A: use a reasonable, free to use, and easily available set of icons
  17. Keyboard shortcuts? A: Ctrl + N should create open the new record screen. Ctrl + S should save the new or edited record.
  18. Window icon and title? A: The title should be "Demo Notes". 
