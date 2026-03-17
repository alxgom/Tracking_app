---
description: Environment and Database Setup Phase
---

# Phase 1: Environment & Database Setup

This workflow handles the initialization of the Flet tracking app environment and the SQLAlchemy database architecture.

// turbo-all
1. Run `poetry add flet sqlalchemy` to install required dependencies.
2. Run `poetry remove pandas` to remove the heavy unused dependency.
3. Create a folder `database` in the root of the project.
4. Create the `database/core.py` file to initialize the SQLite engine and session factory. Use `sqlite:///data/tracking.db`.
5. Create the `database/models.py` file containing the `Task` and `TimeLog` SQLAlchemy models as defined in the implementation plan.
6. Create the `database/crud.py` file to implement the CRUD logic for tasks and timelogs.
7. Create a quick test script in `tests/test_db.py` to assert that the models and CRUD operations work correctly.
8. Run the test script to verify data integrity.
