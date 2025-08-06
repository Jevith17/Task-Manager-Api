
import os

class Config:
    DATABASE_URI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'task_manager.db')