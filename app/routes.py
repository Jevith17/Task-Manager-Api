# app/routes.py
from flask import Blueprint, request, jsonify
from app.services import TaskService, SubTaskService # Import SubTaskService
from dataclasses import asdict

api_bp = Blueprint('api', __name__)

task_service = TaskService()
sub_task_service = SubTaskService() # Instantiate new service


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title in request body'}), 400
    title = data['title']
    description = data.get('description')
    priority = data.get('priority', 3)
    deadline = data.get('deadline')
    try:
        new_task = task_service.create_task(title, description, priority, deadline)
        return jsonify(asdict(new_task)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = task_service.get_all_tasks()
        return jsonify([asdict(task) for task in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = task_service.get_task_by_id(task_id)
        if task:
            return jsonify(asdict(task)), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body cannot be empty'}), 400
    try:
        updated_task = task_service.update_task(task_id, data)
        if updated_task:
            return jsonify(asdict(updated_task)), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        success = task_service.delete_task(task_id)
        if success:
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@api_bp.route('/tasks/<int:task_id>/subtasks', methods=['POST'])
def create_sub_task(task_id):
    """Create a new sub-task for a given parent task."""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title in request body'}), 400

    title = data['title']
    try:
        new_sub_task = sub_task_service.create_sub_task(title, task_id)
        if new_sub_task:
            return jsonify(asdict(new_sub_task)), 201
        else:
            # This happens if the parent task_id does not exist
            return jsonify({'error': 'Parent task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/<int:task_id>/subtasks', methods=['GET'])
def get_sub_tasks(task_id):
    """Get all sub-tasks for a given parent task."""
    try:
        # We can leverage the existing TaskService to ensure the parent task exists
        task = task_service.get_task_by_id(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # The sub_tasks are already fetched and attached to the task object
        return jsonify([asdict(st) for st in task.sub_tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
