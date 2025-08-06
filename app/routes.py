# app/routes.py
from flask import Blueprint, request, jsonify
from app.services import TaskService
from dataclasses import asdict

# Create a Blueprint.
api_bp = Blueprint('api', __name__)

# Instantiate our service
task_service = TaskService()

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.
    Expects a JSON payload with 'title', 'description', 'priority', and 'deadline'.
    """
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title in request body'}), 400

    # Extract data with defaults for optional fields
    title = data['title']
    description = data.get('description')
    priority = data.get('priority', 3) # Default priority is Low
    deadline = data.get('deadline')

    try:
        new_task = task_service.create_task(title, description, priority, deadline)
        # asdict converts the dataclass object to a dictionary for JSON serialization
        return jsonify(asdict(new_task)), 201 # 201 Created
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    try:
        tasks = task_service.get_all_tasks()
        # Convert list of Task objects to list of dicts
        return jsonify([asdict(task) for task in tasks]), 200 # 200 OK
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieve a single task by its ID."""
    try:
        task = task_service.get_task_by_id(task_id)
        if task:
            return jsonify(asdict(task)), 200 # 200 OK
        else:
            return jsonify({'error': 'Task not found'}), 404 # 404 Not Found
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body cannot be empty'}), 400

    try:
        updated_task = task_service.update_task(task_id, data)
        if updated_task:
            return jsonify(asdict(updated_task)), 200 # 200 OK
        else:
            return jsonify({'error': 'Task not found'}), 404 # 404 Not Found
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    try:
        success = task_service.delete_task(task_id)
        if success:
            return jsonify({'message': 'Task deleted successfully'}), 200 # 200 OK
        else:
            return jsonify({'error': 'Task not found'}), 404 # 404 Not Found
    except Exception as e:
        return jsonify({'error': str(e)}), 500