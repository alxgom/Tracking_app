import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.core import Base
from database import crud
from datetime import datetime

# Setup in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_task(db):
    task = crud.add_task(db, name="Test Task", color="#123456")
    assert task.name == "Test Task"
    assert task.color == "#123456"
    assert task.id is not None

def test_get_active_tasks(db):
    crud.add_task(db, name="Task 1")
    crud.add_task(db, name="Task 2")
    tasks = crud.get_active_tasks(db)
    assert len(tasks) == 2

def test_add_time_log(db):
    task = crud.add_task(db, name="Test Task")
    log = crud.add_time_log(db, task_id=task.id, duration_minutes=45, notes="Working hard")
    assert log.task_id == task.id
    assert log.duration_minutes == 45
    assert log.notes == "Working hard"

def test_sql_injection_attempt(db):
    # This test verifies that ORM handles special characters correctly
    evil_name = "Task'); DROP TABLE tasks; --"
    task = crud.add_task(db, name=evil_name)
    assert task.name == evil_name
    
    # Verify the table still exists and only one task was added
    tasks = crud.get_active_tasks(db)
    assert len(tasks) == 1
    assert tasks[0].name == evil_name
