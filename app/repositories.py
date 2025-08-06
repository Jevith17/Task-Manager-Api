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
        tasks = cursor.fetchall()
        return tasks

    def get_by_id(self, task_id):
        db = get_db()
        cursor = db.execute(
            "SELECT id, title, description, priority, status, deadline, created_at, updated_at"
            " FROM tasks WHERE id = ?",
            (task_id,)
        )
        task = cursor.fetchone()
        return task

    def create(self, title, description, priority, deadline):
        db = get_db()
        cursor = db.execute(
            "INSERT INTO tasks (title, description, priority, deadline, updated_at)"
            " VALUES (?, ?, ?, ?, ?)"
            " RETURNING id", # RETURNING is helpful to get the new ID
            (title, description, priority, deadline, datetime.utcnow())
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
