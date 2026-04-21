from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

app = FastAPI()

# --- CORS (ОБЯЗАТЕЛЬНО) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB ---
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# --- MODEL ---
class Task(BaseModel):
    user_id: int
    title: str

# --- API ---
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/tasks")
def get_tasks(user_id: int):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT id, title FROM tasks WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()

    return {"tasks": [{"id": r[0], "title": r[1]} for r in rows]}

@app.post("/api/add")
def add_task(task: Task):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (user_id, title, created_at) VALUES (?, ?, ?)",
        (task.user_id, task.title, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return {"ok": True}
