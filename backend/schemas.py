from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

# --- Time Logs ---
class TimeLogBase(BaseModel):
    duration_minutes: int = Field(gt=0, le=1440) # Max 24 hours
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=1000)

class TimeLogCreate(TimeLogBase):
    task_id: int

class TimeLog(TimeLogBase):
    id: int
    task_id: int
    model_config = ConfigDict(from_attributes=True)

# --- Tasks ---
class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field("#f44336", pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")

class Task(TaskBase):
    id: int
    is_archived: bool
    sort_order: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Extended Responses ---
class TimeLogResponse(TimeLog):
    task: Task
    model_config = ConfigDict(from_attributes=True)
