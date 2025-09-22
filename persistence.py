import json, os

STATE_FILE = ".vbc_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

global_state = load_state()

def set_var(name, value, persistent=False):
    global_state[name] = value
    if persistent:
        save_state(global_state)
    return value

def get_var(name, default=None):
    return global_state.get(name, default)

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, filepath, on_reload):
        self.filepath = filepath
        self.on_reload = on_reload

    def on_modified(self, event):
        if event.src_path.endswith(self.filepath):
            print(f"[HOT-RELOAD] {self.filepath} changed, reloading...")
            self.on_reload()

def watch_file(filepath, on_reload):
    event_handler = ReloadHandler(filepath, on_reload)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    return observer

