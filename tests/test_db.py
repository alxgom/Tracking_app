import os
import sys

# Add parent dir to path so we can import our packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from database.core import Base, engine, SessionLocal, init_db
from database.models import Task, TimeLog
import database.crud as crud

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create schema
        init_db()
    
    def setUp(self):
        self.db = SessionLocal()
        # Clean up tables before each test
        self.db.query(TimeLog).delete()
        self.db.query(Task).delete()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_create_and_read_task(self):
        task = crud.add_task(self.db, "Test Task")
        self.assertEqual(task.name, "Test Task")
        
        # Verify it's active
        active_tasks = crud.get_active_tasks(self.db)
        self.assertEqual(len(active_tasks), 1)
        self.assertEqual(active_tasks[0].id, task.id)

    def test_time_log_crud(self):
        task = crud.add_task(self.db, "Coding")
        
        # Add log
        log1 = crud.add_time_log(self.db, task.id, 45)
        log2 = crud.add_time_log(self.db, task.id, 15)
        
        history = crud.get_recent_history(self.db)
        self.assertEqual(len(history), 2)
        
        # Update log
        updated = crud.update_time_log(self.db, log1.id, 60)
        self.assertEqual(updated.duration_minutes, 60)
        
        # Delete log
        success = crud.delete_time_log(self.db, log2.id)
        self.assertTrue(success)
        
        history_after = crud.get_recent_history(self.db)
        self.assertEqual(len(history_after), 1)

if __name__ == "__main__":
    unittest.main()
