---
description: Dashboard and Data Entry Phase
---

# Phase 3: Dashboard & Data Entry

This workflow implements the core stopwatch and the manual/history entry UI in Flet.

1. Create `ui/components/stopwatch.py`.
2. Implement a large `ft.Text` for the time display driven by an async `asyncio.sleep` loop.
3. Add Start, Pause, and Save `ft.ElevatedButton`s. When Save is hit, commit the elapsed duration to the `TimeLog` table.
4. Create `ui/components/history.py` to display the "Recent Entries". Use a `ft.Column` containing `ft.Card`s or `ft.DataTable`.
5. Create an inline form explicitly for "Manual Entry" above the history list using `ft.TextField`.
6. Implement the "Inline Edit" flow on the history table. When a user clicks "Edit" on a row, swap the UI elements in that row to allow updating the Date or Minutes, then save to the database.
7. Run the application and execute the Data Integrity Tests defined in the implementation plan.
