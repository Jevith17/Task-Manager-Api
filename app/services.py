# app/services.py
from app.repositories import TaskRepository, SubTaskRepository # Import new repository
from app.models import Task, SubTask # Import SubTask model
from typing import List, Optional

class SubTaskService:
    def __init__(self):
        self.repository = SubTaskRepository()

    def get_sub_tasks_for_task(self, task_id: int) -> List[SubTask]:
        db_sub_tasks = self.repository.get_by_task_id(task_id)
        return [SubTask(**sub_task) for sub_task in db_sub_tasks]

    def create_sub_task(self, title: str, task_id: int) -> Optional[SubTask]:
        # First, check if the parent task exists
        task_repo = TaskRepository()
        if not task_repo.get_by_id(task_id):
            return None # Parent task not found

        new_sub_task_id = self.repository.create(title, task_id)
        new_sub_task_data = self.repository.get_by_id(new_sub_task_id)
        return SubTask(**new_sub_task_data)



class TaskService:
    def __init__(self):
        self.repository = TaskRepository()
        self.sub_task_service = SubTaskService() # Instantiate sub-task service

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks, including their sub-tasks."""
        db_tasks = self.repository.get_all()
        tasks = []
        for db_task in db_tasks:
            task = Task(**db_task)
            # Fetch and attach sub-tasks
            task.sub_tasks = self.sub_task_service.get_sub_tasks_for_task(task.id)
            tasks.append(task)
        return tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a single task by its ID, including its sub-tasks."""
        db_task = self.repository.get_by_id(task_id)
        if db_task:
            task = Task(**db_task)
            # Fetch and attach sub-tasks
            task.sub_tasks = self.sub_task_service.get_sub_tasks_for_task(task.id)
            return task
        return None
    
    
    def create_task(self, title: str, description: str, priority: int, deadline: str) -> Task:
        """Create a new task."""
        new_task_id = self.repository.create(title, description, priority, deadline)
        new_task_data = self.repository.get_by_id(new_task_id)
        task = Task(**new_task_data)
        task.sub_tasks = [] # A new task has no sub-tasks
        return task

    def update_task(self, task_id: int, data: dict) -> Optional[Task]:
        """Update an existing task."""
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)
        task.deadline = data.get('deadline', task.deadline)

        self.repository.update(
            task_id, task.title, task.description, task.priority, task.status, task.deadline
        )
        return self.get_task_by_id(task_id)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task. Returns True on success, False on failure."""
        task = self.repository.get_by_id(task_id) # Check existence before deleting
        if not task:
            return False

        self.repository.delete(task_id)
        return True