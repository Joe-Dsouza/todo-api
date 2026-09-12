from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DB_FILE = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, like a dict
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)
    # Seed only if empty
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Set up FastAPI project", 1),
                ("Write CRUD endpoints", 0),
                ("Push code to GitHub", 0),
            ]
        )
    conn.commit()
    conn.close()

init_db()
class NewTask(BaseModel):
    title: str | None = None

@app.get("/")
def read_root():
    return {
        "name" : "Task API",
        "version" : "1.0",
        "endpoints" : ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status" : "ok"}

@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return dict(row)

@app.post("/tasks", status_code=201)
def create_task(new_task: NewTask):
    if not new_task.title or not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (new_task.title, 0)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"id": new_id, "title": new_task.title, "done": False}

class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: UpdateTask):
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                if not update.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")