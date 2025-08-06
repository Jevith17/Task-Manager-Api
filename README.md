# Task Manager REST API

A simple and effective RESTful API for managing tasks and sub-tasks, built with Python, Flask, and SQLite. This project emphasizes Clean Architecture principles to ensure code is scalable, maintainable, and testable.

## Features

*   **CRUD Operations:** Full Create, Read, Update, Delete functionality for tasks.
*   **Sub-Tasks:** Link sub-tasks to parent tasks in a relational manner.
*   **Priority Sorting:** Tasks are sorted by priority (High, Medium, Low).
*   **Status Tracking:** Tasks and sub-tasks have statuses (`pending`, `in_progress`, `completed`).
*   **Deadlines:** Assign optional deadlines to tasks.
*   **Clean Architecture:** Code is organized into distinct layers (Models, Repositories, Services, Routes) for clarity and separation of concerns.

---

## Project Setup

Follow these steps to run the project locally.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/task-manager-api.git
    cd task-manager-api
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    # On Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Initialize the database:**
    (This only needs to be done once.)
    ```bash
    # Set the FLASK_APP environment variable
    # On Mac/Linux:
    export FLASK_APP=run.py
    # On Windows:
    set FLASK_APP=run.py

    # Run the init-db command
    flask init-db
    ```

4.  **Run the application:**
    ```bash
    flask run
    ```
    The API will now be running at `http://127.0.0.1:5000`.

---

## API Reference

All endpoints are prefixed with `/api`.

### Tasks

#### `POST /api/tasks`

Create a new task.

*   **Body (JSON):**
    ```json
    {
        "title": "My New High-Priority Task",
        "description": "A detailed description of what needs to be done.",
        "priority": 1,
        "deadline": "2025-12-31T23:59:59"
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
        "id": 1,
        "title": "My New High-Priority Task",
        "description": "A detailed description of what needs to be done.",
        "priority": 1,
        "status": "pending",
        "deadline": "2025-12-31T23:59:59",
        "created_at": "...",
        "updated_at": "...",
        "sub_tasks": []
    }
    ```

#### `GET /api/tasks`

Retrieve all tasks, sorted by priority and deadline.

*   **Success Response (200 OK):** An array of task objects.

#### `GET /api/tasks/<task_id>`

Retrieve a single task by its ID, including its sub-tasks.

*   **Success Response (200 OK):** A single task object.
*   **Error Response (404 Not Found):** If the task does not exist.

#### `PUT /api/tasks/<task_id>`

Update an existing task. You can send any combination of fields to update.

*   **Body (JSON):**
    ```json
    {
        "status": "completed",
        "priority": 2
    }
    ```
*   **Success Response (200 OK):** The full, updated task object.

#### `DELETE /api/tasks/<task_id>`

Delete a task and all of its associated sub-tasks.

*   **Success Response (200 OK):**
    ```json
    {
        "message": "Task deleted successfully"
    }
    ```

### Sub-Tasks

#### `POST /api/tasks/<task_id>/subtasks`

Create a new sub-task for a parent task.

*   **Body (JSON):**
    ```json
    {
        "title": "First step for the parent task"
    }
    ```
*   **Success Response (201 Created):** The new sub-task object.
*   **Error Response (404 Not Found):** If the parent `task_id` does not exist.

#### `GET /api/tasks/<task_id>/subtasks`

Retrieve all sub-tasks for a specific parent task.

*   **Success Response (200 OK):** An array of sub-task objects.