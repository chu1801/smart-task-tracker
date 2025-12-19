from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Smart Task Tracker")

# --------------------
# Data Model
# --------------------
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

class TaskCreate(BaseModel):
    title: str

# --------------------
# In-memory storage
# --------------------
tasks: List[Task] = []
task_id_counter = 1

# --------------------
# Routes
# --------------------
@app.get("/")
def root():
    return {"message": "Smart Task Tracker API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter

    new_task = Task(
        id=task_id_counter,
        title=task.title,
        completed=False
    )
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskCreate):
    for task in tasks:
        if task.id == task_id:
            task.title = updated_task.title
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
