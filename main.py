import os
import shutil
import time
from collections import defaultdict

action_log = []

def list_old_files(directory_path, days_unused=365, exclude_system=True):
    """
    Recursively lists files that haven't been accessed in the specified number of days,
    sorted by file size (largest to smallest).

    :param directory_path: Starting directory for the scan.
    :param days_unused: Number of days since last access to consider a file as "old."
    :param exclude_system: Exclude system-critical folders on Windows.
    :return: List of tuples (file_path, file_size), sorted by size in descending order.
    """
    cutoff_time = time.time() - (days_unused * 24 * 60 * 60)
    old_files = []

    # Exclude critical Windows system folders if applicable
    system_paths = [
        "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\System Volume Information"
    ] if exclude_system else []

    trash_path = os.path.join(directory_path, "Trash")

    for root, _, files in os.walk(directory_path):
        # Skip system-critical paths
        if any(root.startswith(path) for path in system_paths) or root.startswith(trash_path):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            try:
                last_access_time = os.stat(file_path).st_atime
                file_size = os.stat(file_path).st_size  # Get file size
                if last_access_time < cutoff_time:
                    old_files.append((file_path, file_size))  # Add as tuple
            except (FileNotFoundError, PermissionError):
                continue

    # Sort files by size (largest to smallest)
    return sorted(old_files, key=lambda x: x[1], reverse=True)

def find_duplicates(file_list):
    """
    Identifies duplicate files in a provided list based on file size and name.

    :param file_list: List of tuples (file_path, file_size).
    :return: Dictionary of duplicates with keys as (file_size, file_name) and
             values as lists of file paths.
    """
    duplicates = defaultdict(list)

    for file_path, file_size in file_list:
        file_name = os.path.basename(file_path)
        duplicates[(file_size, file_name)].append(file_path)

    return {key: paths for key, paths in duplicates.items() if len(paths) > 1}


def length_old_files(file_list):
    """
    Calculate the total number of old files in the provided file list.

    This function takes a list of file paths or file names and returns the count
    of how many files are present in the list. It is used to determine the total
    length of the list of old files for further processing or evaluation.

    :param file_list: A list containing file paths or file names that represent
        old files for consideration.
    :type file_list: list[str]
    :return: The total count of files in the given file list.
    :rtype: int
    """
    return len(file_list)

def move_to_trash(file_path, trash_folder):
    """
    Moves the given file to a specified trash folder and logs the action.

    :param file_path: Path of the file to move.
    :param trash_folder: Path of the trash folder.
    """
    try:
        os.makedirs(trash_folder, exist_ok=True)
        file_name = os.path.basename(file_path)
        destination = os.path.join(trash_folder, file_name)

        # Handle duplicate file names in trash
        if os.path.exists(destination):
            base, ext = os.path.splitext(file_name)
            destination = os.path.join(trash_folder, f"{base}_copy{ext}")

        shutil.move(file_path, destination)
        action_log.append(("delete", destination, file_path))
        print(f"Moved to trash: {file_path}")
    except Exception as e:
        print(f"Error moving file to trash: {e}")


def undo_last_action():
    """
    Restores the most recently deleted file from the trash.

    """
    if not action_log:
        print("No actions to undo.")
        return

    try:
        action, trash_path, original_path = action_log.pop()
        if action == "delete":
            shutil.move(trash_path, original_path)
            print(f"Restored: {original_path}")
    except Exception as e:
        print(f"Error restoring file: {e}")

def open_file(file_path):
    """
    Opens the specified file using the default application on the system.

    :param file_path: Path of the file to open.
    """
    try:
        print(f"Opening file: {file_path}")
        if os.name == "nt": #windows
            os.startfile(file_path)
        else:
            print("File opening not supported on this platform.")

    except Exception as e:
        print(f"Error opening file: {e}")


def main():
    """
    Main function to manage scanning, identifying, and handling old files within a specified base directory.
    This function performs the following operations:

    1. Scans the supplied base directory for files not accessed within a specified time frame.
    2. Identifies duplicate files and offers user options for handling them.
    3. Prompts users to interactively decide actions for non-duplicate old files, such as keeping,
       deleting, opening, or undoing an action.

    The function utilizes helper functions like `list_old_files`, `find_duplicates`, `move_to_trash`,
    and `undo_last_action` to process files. The user is given the ability to make interactive decisions
    about file management through the console interface.

    The base directory path, old file criteria (defined by days of non-usage), and handling of duplicates
    are customizable to suit the requirements for cleaning up old files effectively.

    :return: None
    """
    """
    Main function to manage scanning, identifying, and handling old files within a specified base directory.
    This function performs the following operations:

    1. Scans the supplied base directory for files not accessed within a specified time frame.
    2. Identifies duplicate files and offers user options for handling them.
    3. Prompts users to interactively decide actions for non-duplicate old files, such as keeping,
       deleting, opening, or undoing an action.

    The function utilizes helper functions like `list_old_files`, `find_duplicates`, `move_to_trash`,
    and `undo_last_action` to process files. The user is given the ability to make interactive decisions
    about file management through the console interface.

    The base directory path, old file criteria (defined by days of non-usage), and handling of duplicates
    are customizable to suit the requirements for cleaning up old files effectively.

    :return: None
    """
    # Specify base path for scanning
    base_path = "C:\\"  # Full system scan
    trash_folder = os.path.join(base_path, "Trash")

    print("Scanning for old files...")
    old_files = list_old_files(base_path, days_unused=365)

    if not old_files:
        print("No old files found.")
        return

    print(f"Found {len(old_files)} old files.")

    # Ask if the user wants to skip duplicates
    skip_duplicates = input("Skip duplicates and go directly to the largest file? [y/n]: ").lower()
    if skip_duplicates == "y":
        print("\nSkipping duplicates...\n")
    else:
        # Find and handle duplicates
        duplicates = find_duplicates(old_files)
        if duplicates:
            print("\nFound duplicate files:")
            for (size, name), paths in duplicates.items():
                print(f"\nFile: {name} | Size: {size / (1024 * 1024):.2f} MB")
                print(f"Copies: {len(paths)}")
                for path in paths:
                    print(f" - {path}")
                while True:
                    action = input(f"Action for {name} [k=keep all, d=delete all, s=selective]: ").lower()
                    if action == "d":
                        for path in paths:
                            move_to_trash(path, trash_folder)
                        break
                    elif action == "k":
                        print(f"Kept all copies of: {name}")
                        break
                    elif action == "s":
                        for path in paths:
                            sub_action = input(f"File: {path}\nAction [k=keep, d=delete]: ").lower()
                            if sub_action == "d":
                                move_to_trash(path, trash_folder)
                            elif sub_action == "k":
                                print(f"Kept: {path}")
                            else:
                                print("Invalid input, skipping.")
                        break
                    else:
                        print("Invalid input. Please try again.")

    print("\nProcessing remaining files...")
    # Interactive loop for non-duplicate files
    for file_path, file_size in old_files:
        while True:
            print(f"\nFile: {file_path} | Size: {file_size / (1024 * 1024):.2f} MB")
            action = input("Action [k=keep, d=delete, o=open, u=undo, q=quit]: ").lower()

            if action == "d":
                move_to_trash(file_path, trash_folder)
                break
            elif action == "k":
                print(f"Kept: {file_path}")
                break
            elif action == "o":
                os.startfile(file_path)
                print("File opened. Choose again:")
            elif action == "u":
                undo_last_action()
                break
            elif action == "q":
                print("Exiting...")
                return
            else:
                print("Invalid input. Please try again.")

    print("Process complete.")

if __name__ == "__main__":
    main()