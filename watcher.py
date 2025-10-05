import os
import shutil
import re
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent

# Configuration
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(PROJECT_DIR, "Screenshots")
DEST_DIR = os.path.join(PROJECT_DIR, "screenshots_sorted")
CONFIG_FILE = os.path.join(PROJECT_DIR, "config", "app_map.json")

# Load app map
with open(CONFIG_FILE, "r") as f:
    APP_NAME_MAP = json.load(f)

# Regex for screenshot filenames
SCREENSHOT_REGEX = re.compile(
    r"Screenshot_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d+_(.+)\.(png|jpg)"
)

# Helper functions
def wait_for_complete_file(filepath, timeout=30):
    """Wait until file stops growing or timeout reached"""
    start = time.time()
    last_size = -1
    while time.time() - start < timeout:
        if not os.path.exists(filepath):
            return False
        size = os.path.getsize(filepath)
        if size == last_size:
            return True
        last_size = size
        time.sleep(0.5)
    return True

def move_to_folder(filepath, folder_name):
    target_folder = os.path.join(DEST_DIR, folder_name)
    os.makedirs(target_folder, exist_ok=True)
    shutil.move(filepath, os.path.join(target_folder, os.path.basename(filepath)))
    print(f"✅ {os.path.basename(filepath)} -> {folder_name}/", flush=True)

def process_file(filepath):
    if not os.path.exists(filepath):
        return
    filename = os.path.basename(filepath)

    # Ignore temp files
    if filename.endswith(".tmp"):
        return

    if not wait_for_complete_file(filepath):
        print(f"⚠️ File not ready: {filename}", flush=True)
        return

    match = SCREENSHOT_REGEX.search(filename)
    if match:
        package_name = match.group(1)
        # Only use app_map.json keys, else Unsorted
        if package_name in APP_NAME_MAP:
            app_name = APP_NAME_MAP[package_name]
            move_to_folder(filepath, app_name)
        else:
            move_to_folder(filepath, "Unsorted")
    else:
        move_to_folder(filepath, "Unsorted")

# Event Handler
class ScreenshotEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(0.5)
            process_file(event.src_path)

    def on_moved(self, event):
        if isinstance(event, FileMovedEvent):
            if event.dest_path.endswith((".png", ".jpg")):
                time.sleep(0.5)
                process_file(event.dest_path)

# Batch sort existing files
def batch_sort_existing():
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(DEST_DIR, exist_ok=True)
    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f))]
    for file in files:
        process_file(os.path.join(SOURCE_DIR, file))
    if files:
        print("Batch sort completed for existing files.", flush=True)

# Main
if __name__ == "__main__":
    batch_sort_existing()

    event_handler = ScreenshotEventHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)

    print(f"Watching folder: {SOURCE_DIR}\nPress Ctrl+C to stop.", flush=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print("\nWatcher stopped by user.", flush=True)
    observer.join()
