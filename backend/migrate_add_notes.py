"""One-time migration: add notes column to timelogs table."""
from database.core import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Check if column already exists
    cols = conn.execute(text("PRAGMA table_info(timelogs)")).fetchall()
    col_names = [c[1] for c in cols]
    print("Current columns:", col_names)

    if "notes" not in col_names:
        conn.execute(text("ALTER TABLE timelogs ADD COLUMN notes TEXT"))
        conn.commit()
        print("SUCCESS: notes column added.")
    else:
        print("Column already exists, skipping.")
