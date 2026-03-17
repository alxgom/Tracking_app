"""
One-time script to clean up the tasks table:
- For each unique task name, keep the FIRST entry (lowest id).
- Re-assign all time logs of duplicate tasks to the surviving task.
- Delete the duplicates.
- Also removes any tasks whose names are clearly junk (empty string, whitespace-only).
"""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")

from database.core import SessionLocal
from database.models import Task, TimeLog

with SessionLocal() as db:
    all_tasks = db.query(Task).order_by(Task.name, Task.id).all()

    print(f"Total tasks before cleanup: {len(all_tasks)}")
    for t in all_tasks:
        print(f"  id={t.id}  name={repr(t.name)}")

    # Group by lowercased name
    seen = {}   # name_lower -> keeper Task
    to_delete = []

    for task in all_tasks:
        key = task.name.strip().lower()
        if not key:          # junk empty names
            to_delete.append(task)
            continue
        if key not in seen:
            seen[key] = task
        else:
            # Re-assign this task's logs to the keeper
            keeper = seen[key]
            db.query(TimeLog).filter(TimeLog.task_id == task.id).update(
                {TimeLog.task_id: keeper.id}, synchronize_session=False
            )
            to_delete.append(task)

    print(f"\nDeleting {len(to_delete)} duplicate/junk task(s):")
    for t in to_delete:
        print(f"  id={t.id}  name={repr(t.name)}")
        db.delete(t)

    db.commit()

    remaining = db.query(Task).order_by(Task.name).all()
    print(f"\nTasks after cleanup ({len(remaining)}):")
    for t in remaining:
        print(f"  id={t.id}  name={repr(t.name)}")

print("\nDone.")
