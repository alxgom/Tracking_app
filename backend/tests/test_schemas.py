import pytest
from pydantic import ValidationError
from schemas import TaskCreate, TaskUpdate, TimeLogCreate

def test_task_create_valid():
    task = TaskCreate(name="Research", color="#ff0000")
    assert task.name == "Research"
    assert task.color == "#ff0000"

def test_task_create_invalid_name():
    with pytest.raises(ValidationError):
        TaskCreate(name="", color="#ff0000")

def test_task_create_invalid_color():
    with pytest.raises(ValidationError):
        TaskCreate(name="Work", color="invalid-color")

def test_task_update_valid():
    task = TaskUpdate(name="Coding")
    assert task.name == "Coding"
    assert task.color is None

def test_timelog_create_valid():
    log = TimeLogCreate(task_id=1, duration_minutes=30, notes="Meeting")
    assert log.duration_minutes == 30
    assert log.notes == "Meeting"

def test_timelog_create_invalid_duration():
    with pytest.raises(ValidationError):
        TimeLogCreate(task_id=1, duration_minutes=0)
    with pytest.raises(ValidationError):
        TimeLogCreate(task_id=1, duration_minutes=2000)
