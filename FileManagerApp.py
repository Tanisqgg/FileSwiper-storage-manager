import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLabel, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from main import list_old_files, find_duplicates, move_to_trash, undo_last_action
# Import backend functions:
# list_old_files: Scans the file system and lists files not used for a specified duration.
# find_duplicates: Identifies and organizes duplicate files by file size and name.
# move_to_trash: Moves files to a trash folder for soft deletion.
# undo_last_action: Rolls back the last performed action.


class FileManagerApp(QMainWindow):
    def __init__(self):
        """
        Initialize the main application window, layouts, buttons, and variables.

        Sets up:
        - Window properties like title and size.
        - Central widget and main layout.
        - Status label, file list widget, and control buttons.
        """
        super().__init__()

        # Window settings
        self.setWindowTitle("Modern File Manager")
        self.setGeometry(400, 400, 900, 700)

        # Variables
        self.old_files = []
        self.duplicates = {}
        self.current_file_index = 0
        self.trash_folder = "C:\\Trash"  # Directory used to temporarily store deleted files.

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Status Label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.status_label)

        # File List
        self.file_list = QListWidget()
        self.file_list.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.file_list)

        # Button Layout
        self.button_layout = QHBoxLayout()

        self.scan_button = QPushButton("Scan Files")
        self.scan_button.setFont(QFont("Arial", 12))
        self.scan_button.clicked.connect(self.scan_files)
        self.button_layout.addWidget(self.scan_button)

        self.view_duplicates_button = QPushButton("View Duplicates")
        self.view_duplicates_button.setFont(QFont("Arial", 12))
        self.view_duplicates_button.clicked.connect(self.show_duplicates)
        self.button_layout.addWidget(self.view_duplicates_button)

        self.process_button = QPushButton("Process Files")
        self.process_button.setFont(QFont("Arial", 12))
        self.process_button.clicked.connect(self.process_files)
        self.button_layout.addWidget(self.process_button)

        self.undo_button = QPushButton("Undo Last Action")
        self.undo_button.setFont(QFont("Arial", 12))
        self.undo_button.clicked.connect(self.undo_action)
        self.button_layout.addWidget(self.undo_button)

        self.layout.addLayout(self.button_layout)

    def scan_files(self):
        """
        Scan for old files in a specified directory.

        Uses a backend function `list_old_files` to find files not used for a year.
        Displays found files in the file list widget.
        Also identifies duplicates and saves them for user review.
        """
        self.status_label.setText("Scanning files...")
        QApplication.processEvents()  # Allow the GUI to update while scanning

        try:
            self.old_files = list_old_files("C:\\", days_unused=365)
            self.duplicates = find_duplicates(self.old_files)
            self.file_list.clear()
            for file, size in self.old_files:
                self.file_list.addItem(f"{file} ({size / (1024 * 1024):.2f} MB)")

            self.status_label.setText(f"Scan Complete: {len(self.old_files)} old files found.")
        except Exception as e:
            # Handle errors during scanning and show a message box with the error details.
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.status_label.setText("Status: Error during scanning.")

    def show_duplicates(self):
        """
        Display duplicate files in the file list widget.

        Uses pre-computed duplicates dictionary to list files with identical content.
        Shows file paths associated with each duplicate group.
        """

        if not self.duplicates:  # Check if duplicates exist before proceeding.
            QMessageBox.information(self, "No Duplicates", "No duplicate files found.")
            return

        self.file_list.clear()
        for (size, name), paths in self.duplicates.items():
            self.file_list.addItem(f"{name} ({size / (1024 * 1024):.2f} MB) - Copies: {len(paths)}")
            for path in paths:
                self.file_list.addItem(f"  - {path}")

        self.status_label.setText("Displayed duplicate files.")

    def process_files(self):
        """
        Process old files by presenting user actions.

        Prompts the user with file details and provides an option for deletion.
        Moves files to a trash folder or skips them based on user input.
        Handles files sequentially one-by-one.
        """
        if self.current_file_index >= len(self.old_files):
            QMessageBox.information(self, "Completed", "All files processed.")
            return

        file_path, file_size = self.old_files[self.current_file_index]

        # Prompt user for action
        reply = QMessageBox.question(
            self,
            "File Action",
            f"File: {file_path}\nSize: {file_size / (1024 * 1024):.2f} MB\n\nDo you want to delete this file?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            move_to_trash(file_path, self.trash_folder)
            self.status_label.setText(f"Deleted: {file_path}")
        else:
            self.status_label.setText(f"Kept: {file_path}")

        self.current_file_index += 1

    def undo_action(self):
        """
        Undo the last performed file-related action.

        Uses a backend function `undo_last_action` to revert operations.
        """
        try:
            undo_last_action()
            self.status_label.setText("Last action undone.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.status_label.setText("Status: Error during undo.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileManagerApp()
    window.show()
    sys.exit(app.exec_())
