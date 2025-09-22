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

def run_with_hot_reload(path, mode="web"):
    def reload():
        source = open(path).read()
        exe_path = compile_let(source, output="prog.out", build_exec=False)
        if mode == "web":
            html = render_ui(ast)  # re-render UI
            with open("hotreload.html","w") as f: f.write(html)
            webbrowser.open("hotreload.html")
    reload()
    obs = watch_file(path, reload)
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()

import sqlite3, json

DB_FILE = "vbc_state.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS vars
                 (name TEXT PRIMARY KEY, type TEXT, value TEXT)""")
    conn.commit()
    return conn

def set_var_db(name, val, type_):
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO vars VALUES (?,?,?)",
              (name, type_, json.dumps(val)))
    conn.commit()

def get_var_db(name):
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT type,value FROM vars WHERE name=?",(name,))
    row = c.fetchone()
    if row: return json.loads(row[1])
    return None

CREATE TABLE vars_history (
    name TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    value TEXT
);

def save_var_history(name, val):
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT INTO vars_history (name,value) VALUES (?,?)",
              (name, json.dumps(val)))
    conn.commit()

def undo_var(name):
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT value FROM vars_history WHERE name=? ORDER BY timestamp DESC LIMIT 2", (name,))
    rows = c.fetchall()
    if len(rows) >= 2:
        prev = json.loads(rows[1][0])
        set_var_db(name, prev, type(prev).__name__)
        return prev
    return None

def redo_var(name):
    conn = init_db()
    c = conn.cursor()
    # Get the current value
    current = get_var_db(name)
    if current is None:
        return None

    # Fetch all historical values for the variable, ordered by timestamp
    c.execute("SELECT value FROM vars_history WHERE name=? ORDER BY timestamp ASC", (name,))
    rows = c.fetchall()
    values = [json.loads(row[0]) for row in rows]

    # Find the index of the current value in the history
    try:
        idx = values.index(current)
    except ValueError:
        return None  # Current value not found in history

    # If there's a next value, apply it
    if idx + 1 < len(values):
        next_val = values[idx + 1]
        set_var_db(name, next_val, type(next_val).__name__)
        return next_val

    return None  # No forward value available

CREATE TABLE vars_branches (
    name TEXT,
    branch_id TEXT,
    parent_id TEXT,
    value TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

import uuid

def fork_var(name):
    val = get_var_db(name)
    branch_id = str(uuid.uuid4())
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT INTO vars_branches (name,branch_id,parent_id,value) VALUES (?,?,?,?)",
              (name, branch_id, "root", json.dumps(val)))
    conn.commit()
    return branch_id

def merge_var(name, strategy="max"):
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT value FROM vars_branches WHERE name=?",(name,))
    rows = [json.loads(r[0]) for r in c.fetchall()]
    if not rows: return None
    if strategy=="max": return max(rows)
    if strategy=="min": return min(rows)
    if strategy=="sum": return sum(rows)
    return rows[0]



