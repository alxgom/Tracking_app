---
description: Core UI and Layout Phase
---

# Phase 2: Core UI & Layout

This workflow handles the initialization of the Flet Material Design GUI skeleton.

1. Create a `ui` folder in the root of the project.
2. Create the `ui/main_window.py` file. Set up `ft.app(target=main)` and implement `ft.Row` to split the window into a Sidebar and Main Content area.
3. Create `ui/components/sidebar.py` wrapping a `ft.ListView` to display tasks using `ft.ListTile`.
4. Implement the "+ Add Task" button using an `ft.AlertDialog` to create and save a new `Task` to the database.
5. Wire the database `crud.py` functions to the sidebar so the task list automatically populates on startup.
6. Run the application to verify the sidebar alignment and Material Design layout behaves as expected when resizing.
