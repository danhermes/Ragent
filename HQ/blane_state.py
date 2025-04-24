import json
import os
from datetime import datetime

STATE_FILE = "./HQ/blane_state.json"

DEFAULT_FIELDS = ["type", "project", "deliverables", "constraints"]

def initialize_state():
    state = {
        "task_id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "project": "",
        "status": "pending",
        "awaiting_input": "type",
        "context": {field: "" for field in DEFAULT_FIELDS},
        "conversation": []
    }
    save_state(state)
    return state

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def load_state():
    if not os.path.exists(STATE_FILE):
        return initialize_state()
    with open(STATE_FILE, encoding="utf-8") as f:
        return json.load(f)

def log_message(role, message):
    state = load_state()
    state["conversation"].append({"role": role, "message": message})
    save_state(state)

def update_context(field, value):
    state = load_state()
    state["context"][field] = value
    next_field = next_unfilled_field(state["context"])
    state["awaiting_input"] = next_field
    save_state(state)

def next_unfilled_field(context):
    for field in DEFAULT_FIELDS:
        if not context.get(field):
            return field
    return None  # all fields filled

def is_task_ready():
    state = load_state()
    return all(state["context"].get(field) for field in DEFAULT_FIELDS)

def finalize_state():
    state = load_state()
    state["status"] = "ready"
    save_state(state)
    return state
