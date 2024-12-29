#  Tinder like File Management app

A Python-based tool for scanning, organizing, and managing old and duplicate files in your file system.
This program shows the user's files which have not been used in more than a year in descending order of file size so that the user can decide whether to keep that file or delete it.
Unknown Files such as videos and other old files can be opened before confirming to be deleted or not.

## Features

- **Scan for Old Files:** Identify files that haven't been accessed for a specified number of days.
- **Find Duplicate Files:** Detect duplicates based on file size and file name.
- **Process Files:** Delete, keep, or open files interactively.
- **Undo Actions:** Restore deleted files using a soft delete mechanism (Trash folder).
- **User-Friendly GUI:** Built with PyQt5 for an intuitive and modern interface.

## Project Structure

- **`main.py`:** Backend logic for file scanning, duplicate detection, and file actions (delete, restore, open).
- **`FileManagerApp.py`:** GUI application implementation using PyQt5, providing user interactivity with the file system.

---

## How It Works

### Backend Functionality (`main.py`)

1. **List Old Files (`list_old_files`)**
   - Scans a directory for files not accessed in the specified time frame.
   - Returns a list of files, sorted by size for easy management.

2. **Find Duplicates (`find_duplicates`)**
   - Identifies duplicate files based on size and file name.
   - Groups duplicates for batch processing or selective deletion.

3. **Move to Trash (`move_to_trash`)**
   - Soft deletes files by moving them to a specified Trash folder.

4. **Undo Actions (`undo_last_action`)**
   - Restores the latest deleted file from the Trash folder.

5. **Interactive Processing:** Enables users to control file actions via a console interface in the backend.

---

### Graphical User Interface (GUI) (`FileManagerApp.py`)

1. **Scan Files**
   - Initiates a system-wide scan to detect old files based on the backend functionality.

2. **View Duplicates**
   - Displays duplicate files for user review and action.

3. **Process Files**
   - Provides user options to delete, keep, or skip files interactively.

4. **Undo Last Action**
   - Reverts the most recent file deletion.

---

## Requirements

- Python 3.8+
- PyQt5

---

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Tanisqgg/FileSwiper-storage-manager.git
   cd modern-file-manager
   ```

2. Install dependencies:
   ```bash
   pip install pyqt5
   ```

3. Run the GUI Application:
   ```bash
   python FileManagerApp.py
   ```

4. Or run the backend script for CLI-based interaction:
   ```bash
   python main.py
   ```

---

## Usage

### GUI Instructions:

1. Click **Scan Files** to start scanning your file system for old files.
2. Select **View Duplicates** to examine duplicates and decide actions.
3. Use **Process Files** to take actions on each file (delete/keep/undo).
4. The **Undo Last Action** button allows soft-deleted files to be restored.

---

### Backend CLI Instructions:

1. Customize the `base_path` variable in the `main()` function to define the scan directory.
2. Run the script:
   ```bash
   python main.py
   ```
3. Follow interactive prompts to manage files.

---

## Key Notes

- **Trash Folder:** Deleted files are moved to a "Trash" folder for recovery. Customize its location in the code if needed.
- **Critical System Folders:** The application excludes system-critical directories (like `C:\Windows`) during scans.
- **Cross-Platform Support:** The GUI relies on PyQt5 and may work on platforms other than Windows with minor changes.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request to contribute.

---
