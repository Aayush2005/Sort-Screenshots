import os
import shutil
import re
import json

# --- Configuration ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(PROJECT_DIR, "Screenshots")
DEST_DIR = os.path.join(PROJECT_DIR, "screenshots_sorted")
CONFIG_FILE = os.path.join(PROJECT_DIR, "config", "app_map.json")

# Load app map
with open(CONFIG_FILE, "r") as f:
    APP_NAME_MAP = json.load(f)

# Regex for your screenshot filenames
SCREENSHOT_REGEX = re.compile(
    r"Screenshot_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d+_(.+)\.(png|jpg)"
)

def move_to_folder(filepath, folder_name):
    target_folder = os.path.join(DEST_DIR, folder_name)
    os.makedirs(target_folder, exist_ok=True)
    shutil.move(filepath, os.path.join(target_folder, os.path.basename(filepath)))
    print(f"✅ {os.path.basename(filepath)} -> {folder_name}/")

def process_file(filepath):
    filename = os.path.basename(filepath)
    match = SCREENSHOT_REGEX.search(filename)

    if match:
        package_name = match.group(1)
        # Only move to app folder if package exists in map
        if package_name in APP_NAME_MAP:
            move_to_folder(filepath, APP_NAME_MAP[package_name])
        else:
            move_to_folder(filepath, "Unsorted")
    else:
        move_to_folder(filepath, "Unsorted")

def main():
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(DEST_DIR, exist_ok=True)

    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f))]
    if not files:
        print("No files to sort in SOURCE_DIR.")
        return

    for file in files:
        process_file(os.path.join(SOURCE_DIR, file))

    print("🟢 Batch sort completed.")

if __name__ == "__main__":
    main()
