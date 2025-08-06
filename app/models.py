# app/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class SubTask:
    id: int
    title: str
    status: str
    task_id: int
    created_at: datetime
    updated_at: datetime

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str]
    priority: int
    status: str
    deadline: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    sub_tasks: Optional[List[SubTask]] = None 