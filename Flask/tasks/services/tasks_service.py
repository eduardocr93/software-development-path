import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "tasks.json")

VALID_STATUS = ["To Do", "In Progress", "Completed"]

def read_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def validate_task(task, tasks, is_update=False):
    if not is_update:
        if "id" not in task:
            return "Missing identifier"

        if not isinstance(task["id"], int):
            return "Identifier must be an integer"

        if any(t["id"] == task["id"] for t in tasks):
            return "Identifier already exists"

        if not task.get("title"):
            return "Missing title"

        if not task.get("description"):
            return "Missing description"

        if task.get("status") not in VALID_STATUS:
            return "Invalid status"

    else:
        if "title" in task and not task["title"]:
            return "Title cannot be empty"

        if "description" in task and not task["description"]:
            return "Description cannot be empty"

        if "status" in task and task["status"] not in VALID_STATUS:
            return "Invalid status"

    return None