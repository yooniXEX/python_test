import sqlite3
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# --- БАЗА ---
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        is_done INTEGER,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# --- МОДЕЛИ ---
class Task(BaseModel):
    user_id: int
    title: str

class UpdateTask(BaseModel):
    user_id: int
    task_id: int
    is_done: bool

# --- API ---
@app.get("/api/tasks")
def get_tasks(user_id: int):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT id, title, is_done FROM tasks WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()

    return {
        "tasks": [
            {"id": r[0], "title": r[1], "done": bool(r[2])}
            for r in rows
        ]
    }

@app.post("/api/add")
def add_task(task: Task):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (user_id, title, is_done, created_at) VALUES (?, ?, ?, ?)",
        (task.user_id, task.title, 0, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return {"ok": True}

@app.post("/api/update")
def update_task(data: UpdateTask):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute(
        "UPDATE tasks SET is_done=? WHERE id=? AND user_id=?",
        (int(data.is_done), data.task_id, data.user_id)
    )
    conn.commit()
    conn.close()
    return {"ok": True}
