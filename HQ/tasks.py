import os
import json
from pathlib import Path
from datetime import datetime
from HQ.blane_state import (
    load_state, save_state, initialize_state, update_context,
    log_message, is_task_ready, finalize_state
)

PROJECTS_ROOT = "./HQ/projects/"
TASKS_ROOT = "./HQ/tasks/"

def advance_task_setup():
    state = load_state()
    field = state["awaiting_input"]
    if not field:
        print("(Blane) > All fields received. You can run 'set finalize' to save.")
        return
    prompt = f"(Blane) > What is the {field} for this task?"
    log_message("blane", prompt)
    print(prompt)

def check_task_completion(field, value):
    update_context(field, value)
    log_message("user", f"{field} = {value}")
    if is_task_ready():
        state = finalize_state()
        create_task_from_state(state)
        print(f"(Blane) > Task {state['task_id']} is ready and created.")


def create_task_from_state(state):
    context = state["context"]
    task_id = state["task_id"]
    project = context["project"]
    project_path = Path("projects") / project
    goal_path = project_path / "HQ" / "goals" / f"{project}.goal.md"
    task_path = Path("tasks") / f"{task_id}.json"

    # Ensure the project and goals directories exist
    goal_path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure the tasks directory exists
    task_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the .goal file
    with goal_path.open("w", encoding="utf-8") as f:
        f.write(generate_goal_file(context))

    # Write the task metadata
    with task_path.open("w", encoding="utf-8") as f:
        json.dump({
            "task_id": task_id,
            "type": context["type"],
            "project": project,
            "created": datetime.now().isoformat(),
            "deliverables": context["deliverables"],
            "constraints": context["constraints"],
            "status": "initialized"
        }, f, indent=2)

def generate_goal_file(data):
    return f"""# 🎯 .goal File – {data['project']}

## 🧠 Project Name
{data['project']}

## 🔧 Project Type
{data['type']}

## 💼 Summary
<Write a one-line summary here>

## 📦 Expected Deliverables
{data['deliverables']}

## 🔍 Known Constraints
{data['constraints']}

## ✅ Definition of Done
<Write completion criteria here>

## 🔂 Phases and Milestones
- Phase 1: Plan
- Phase 2: Execute
- Phase 3: Review

## 🧠 Preferred Meeting Format
Classic 4-phase structure

## 🔍 Review Requirements
Stakeholder and reviewer sign-off
"""

def show_task_status():
    print("(Blane) > Listing active tasks:")
    if not os.path.exists(TASKS_ROOT):
        print("  No tasks found.")
        return
    for file in os.listdir(TASKS_ROOT):
        if file.endswith(".json"):
            with open(os.path.join(TASKS_ROOT, file), encoding="utf-8") as f:
                task = json.load(f)
                print(f"  {task['task_id']} – {task['project']} – {task['status']}")
