# app/services.py
from app.repositories import TaskRepository
from app.models import Task
from typing import List, Optional

class TaskService:
    """
    Service layer for handling business logic related to Tasks.
    """
    def __init__(self):
        self.repository = TaskRepository()

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks, converting them to Task model objects."""
        db_tasks = self.repository.get_all()
        # Convert database rows to Task objects
        tasks = [Task(**task) for task in db_tasks]
        return tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a single task by its ID."""
        db_task = self.repository.get_by_id(task_id)
        if db_task:
            return Task(**db_task)
        return None

    def create_task(self, title: str, description: str, priority: int, deadline: str) -> Task:
        """Create a new task."""
        new_task_id = self.repository.create(title, description, priority, deadline)
        # Fetch the newly created task to return its full details
        new_task_data = self.repository.get_by_id(new_task_id)
        return Task(**new_task_data)

    def update_task(self, task_id: int, data: dict) -> Optional[Task]:
        """Update an existing task."""
        task = self.get_task_by_id(task_id)
        if not task:
            return None # Task not found

        # Merge existing data with new data
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)
        task.deadline = data.get('deadline', task.deadline)

        self.repository.update(
            task_id, task.title, task.description, task.priority, task.status, task.deadline
        )
        return self.get_task_by_id(task_id) # Return the updated task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task. Returns True on success, False on failure."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False # Task to delete was not found

        self.repository.delete(task_id)
        return True