from sqlalchemy.orm import Session
from datetime import datetime
from .models import Task, TimeLog

def get_active_tasks(db: Session):
    return db.query(Task).filter(Task.is_archived == False).order_by(Task.sort_order).all()

def add_task(db: Session, name: str, color: str = "#f44336"):
    new_task = Task(name=name, color=color)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def add_time_log(db: Session, task_id: int, duration_minutes: int, date: datetime = None):
    if date is None:
        date = datetime.utcnow()
    new_log = TimeLog(task_id=task_id, duration_minutes=duration_minutes, date=date)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_recent_history(db: Session, limit: int = 15):
    # Fetch recent logs joining with tasks
    return db.query(TimeLog).join(Task).order_by(TimeLog.date.desc(), TimeLog.id.desc()).limit(limit).all()

def update_time_log(db: Session, log_id: int, new_duration: int, new_date: datetime = None):
    log = db.query(TimeLog).filter(TimeLog.id == log_id).first()
    if log:
        log.duration_minutes = new_duration
        if new_date:
            log.date = new_date
        db.commit()
        db.refresh(log)
    return log

def delete_time_log(db: Session, log_id: int):
    log = db.query(TimeLog).filter(TimeLog.id == log_id).first()
    if log:
        db.delete(log)
        db.commit()
        return True
    return False
