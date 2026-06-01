import os
import shutil
import argparse
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Define categories and their corresponding file extensions
FILE_CATEGORIES = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.csv', '.ppt', '.pptx'],
    "Videos": ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    "Audio": ['.mp3', '.wav', '.aac', '.ogg', '.flac'],
    "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    "Scripts": ['.py', '.sh', '.bat', '.js', '.html', '.css', '.json', '.yaml', '.yml'],
    "3D_Models": ['.obj', '.stl', '.fbx', '.blend', '.gltf', '.glb'],
    "Executables": ['.exe', '.msi', '.app', '.dmg', '.apk']
}

def organize_directory(target_dir):
    """Scans a directory and organizes files into categorized folders."""
    target_path = Path(target_dir)

    if not target_path.exists():
        logging.error(f"Error: The directory '{target_dir}' does not exist.")
        return

    if not target_path.is_dir():
         logging.error(f"Error: '{target_dir}' is not a directory.")
         return

    logging.info(f"Scanning directory: {target_dir}")

    files_moved = 0
    errors = 0

    for item in target_path.iterdir():
        # Skip directories to avoid recursive mess
        if item.is_dir():
            continue

        # Get file extension in lowercase
        file_ext = item.suffix.lower()

        # Skip files without extensions or hidden files (like .DS_Store)
        if not file_ext or item.name.startswith('.'):
             continue

        category = "Others" # Default category

        # Determine category based on extension
        for cat, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                category = cat
                break

        # Create destination folder if it doesn't exist
        dest_folder = target_path / category
        if not dest_folder.exists():
            dest_folder.mkdir(exist_ok=True)
            logging.info(f"Created category folder: {category}")

        dest_path = dest_folder / item.name

        # Handle naming conflicts
        counter = 1
        while dest_path.exists():
            # If a file with same name exists, append a number
            new_name = f"{item.stem}_{counter}{item.suffix}"
            dest_path = dest_folder / new_name
            counter += 1

        # Move the file
        try:
            shutil.move(str(item), str(dest_path))
            logging.info(f"Moved: {item.name} -> {category}/")
            files_moved += 1
        except Exception as e:
            logging.error(f"Failed to move {item.name}: {e}")
            errors += 1

    logging.info(f"Organization complete! Moved {files_moved} files. Errors: {errors}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Data Organizer: Automatically sort files into folders based on extensions.")
    parser.add_argument("directory", help="The path to the directory you want to organize.")

    args = parser.parse_args()

    organize_directory(args.directory)
