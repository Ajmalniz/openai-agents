from fastapi import FastAPI, HTTPException
from models import Task
import asyncio

app = FastAPI(title="Task Management API")

tasks = []  # In-memory database

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks")
async def list_tasks():
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return {"tasks": tasks}

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = tasks.pop(task_id)
    return {"message": "Task deleted", "task": deleted_task}