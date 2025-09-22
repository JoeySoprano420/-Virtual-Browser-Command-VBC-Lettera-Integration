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
