# app/repositories.py
from datetime import datetime
from app.database import get_db

class TaskRepository:
    """
    Repository for all database operations related to Tasks.
    """
    def get_all(self):
        db = get_db()
        cursor = db.execute(
            "SELECT id, title, description, priority, status, deadline, created_at, updated_at"
            " FROM tasks ORDER BY priority ASC, deadline ASC"
        )
        return cursor.fetchall()

    def get_by_id(self, task_id):
        db = get_db()
        cursor = db.execute(
            "SELECT id, title, description, priority, status, deadline, created_at, updated_at"
            " FROM tasks WHERE id = ?",
            (task_id,)
        )
        return cursor.fetchone()

    def create(self, title, description, priority, deadline):
        db = get_db()
        
        now = datetime.utcnow()
        cursor = db.execute(
            "INSERT INTO tasks (title, description, priority, deadline, created_at, updated_at)"
            " VALUES (?, ?, ?, ?, ?, ?)"
            " RETURNING id",
            (title, description, priority, deadline, now, now)
        )
        new_id = cursor.fetchone()['id']
        db.commit()
        return new_id

    def update(self, task_id, title, description, priority, status, deadline):
        db = get_db()
        db.execute(
            "UPDATE tasks SET title = ?, description = ?, priority = ?, status = ?, deadline = ?, updated_at = ?"
            " WHERE id = ?",
            (title, description, priority, status, deadline, datetime.utcnow(), task_id)
        )
        db.commit()

    def delete(self, task_id):
        db = get_db()
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()



class SubTaskRepository:
    """
    Repository for database operations related to SubTasks.
    """
    def get_by_task_id(self, task_id):
        db = get_db()
        cursor = db.execute(
            "SELECT id, title, status, task_id, created_at, updated_at FROM sub_tasks WHERE task_id = ?",
            (task_id,)
        )
        return cursor.fetchall()

    def create(self, title, task_id):
        db = get_db()
        now = datetime.utcnow()
        cursor = db.execute(
            "INSERT INTO sub_tasks (title, task_id, created_at, updated_at)"
            " VALUES (?, ?, ?, ?)"
            " RETURNING id",
            (title, task_id, now, now)
        )
        new_id = cursor.fetchone()['id']
        db.commit()
        return new_id

    def get_by_id(self, sub_task_id):
        db = get_db()
        cursor = db.execute(
            "SELECT id, title, status, task_id, created_at, updated_at FROM sub_tasks WHERE id = ?",
            (sub_task_id,)
        )
        return cursor.fetchone()

    def update(self, sub_task_id, title, status):
        db = get_db()
        db.execute(
            "UPDATE sub_tasks SET title = ?, status = ?, updated_at = ? WHERE id = ?",
            (title, status, datetime.utcnow(), sub_task_id)
        )
        db.commit()

    def delete(self, sub_task_id):
        db = get_db()
        db.execute("DELETE FROM sub_tasks WHERE id = ?", (sub_task_id,))
        db.commit()
