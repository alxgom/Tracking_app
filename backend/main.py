from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import models, crud
from database.core import engine, get_db, init_db
import schemas

# Create tables if not exist
init_db()

app = FastAPI(title="Tracking App API")

# Enable CORS for the frontend Vite server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_active_tasks(db)
    return tasks

@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.add_task(db=db, name=task.name, color=task.color)

@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db=db, task_id=task_id, name=task.name, color=task.color)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}

@app.get("/history", response_model=List[schemas.TimeLogResponse])
def read_history(limit: int = 15, db: Session = Depends(get_db)):
    return crud.get_recent_history(db=db, limit=limit)

@app.post("/history", response_model=schemas.TimeLog)
def add_time_log(log: schemas.TimeLogCreate, db: Session = Depends(get_db)):
    return crud.add_time_log(db=db, task_id=log.task_id, duration_minutes=log.duration_minutes, date=log.date, notes=log.notes)

@app.delete("/history/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    success = crud.delete_time_log(db=db, log_id=log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"ok": True}
