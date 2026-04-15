from flask import Blueprint, request, jsonify
from services.tasks_service import read_tasks, write_tasks, validate_task

tasks_bp = Blueprint("tasks", __name__)


def find_task(tasks, task_id):
    return next((t for t in tasks if t["id"] == task_id), None)


@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = read_tasks()
    status = request.args.get("status")

    if status:
        tasks = [t for t in tasks if t["status"] == status]

    return jsonify(tasks)


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    tasks = read_tasks()
    new_task = request.json

    error = validate_task(new_task, tasks)
    if error:
        return jsonify({"error": error}), 400

    tasks.append(new_task)
    write_tasks(tasks)

    return jsonify(new_task), 201


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = read_tasks()
    task = find_task(tasks, task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json

    error = validate_task(data, tasks, is_update=True)
    if error:
        return jsonify({"error": error}), 400

    task.update(data)
    write_tasks(tasks)

    return jsonify(task)


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = read_tasks()
    task = find_task(tasks, task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks = [t for t in tasks if t["id"] != task_id]
    write_tasks(tasks)

    return jsonify({"message": "Task deleted"})