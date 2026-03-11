import flet as ft
from datetime import datetime, timedelta
from database import crud
from database.core import SessionLocal

class HistoryView(ft.Container):
    def __init__(self, task_id=None):
        super().__init__()
        self.task_id = task_id # If None, show all
        
        # Form inputs
        self.date_picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31),
            on_change=self.date_changed
        )
        self.date_btn = ft.ElevatedButton(
            "Select Date", icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: self.date_picker.pick_date()
        )
        self.duration_field = ft.TextField(label="Minutes", width=100, keyboard_type=ft.KeyboardType.NUMBER)
        
        # Container styling
        self.padding = 20
        self.border_radius = 10
        self.bgcolor = "surfaceVariant"
        
        self.history_list = ft.ListView(expand=True, spacing=10)
        
        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Text("Manual Entry & History", size=20, weight=ft.FontWeight.W_600),
                ft.Row(
                    controls=[
                        self.date_btn,
                        self.duration_field,
                        ft.ElevatedButton("Add Log", on_click=self.add_manual_log, icon=ft.icons.ADD)
                    ]
                ),
                ft.Divider(height=20, color="outlineVariant"),
                self.history_list
            ]
        )
        self.selected_date = datetime.now()
        
    def did_mount(self):
        self.page.overlay.append(self.date_picker)
        self.load_history()

    def date_changed(self, e):
        if self.date_picker.value:
            self.selected_date = self.date_picker.value
            self.date_btn.text = self.selected_date.strftime("%Y-%m-%d")
            self.update()

    def add_manual_log(self, e):
        if not self.task_id or not self.duration_field.value.isdigit():
            # Should show snackbar error here ideally
            return
            
        minutes = int(self.duration_field.value)
        with SessionLocal() as db:
            crud.add_time_log(db, task_id=self.task_id, duration_minutes=minutes, date=self.selected_date)
            
        self.duration_field.value = ""
        self.load_history()

    def delete_log(self, log_id):
        with SessionLocal() as db:
            crud.delete_time_log(db, log_id)
        self.load_history()

    def load_history(self):
        self.history_list.controls.clear()
        with SessionLocal() as db:
            logs = crud.get_recent_history(db)
            
            # Filter if task_id provided (though crud could do this, filtering in mem for now)
            if self.task_id:
                logs = [l for l in logs if l.task_id == self.task_id]
                
            for log in logs:
                self.history_list.controls.append(
                    ft.Container(
                        padding=10,
                        border_radius=8,
                        bgcolor="surface",
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column([
                                    ft.Text(log.task.name, weight=ft.FontWeight.BOLD),
                                    ft.Text(log.date.strftime("%b %d, %Y"), size=12, color="onSurfaceVariant")
                                ]),
                                ft.Row([
                                    ft.Text(f"{log.duration_minutes} min", size=16),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE_OUTLINE, 
                                        icon_color="error",
                                        tooltip="Delete",
                                        on_click=lambda e, lid=log.id: self.delete_log(lid)
                                    )
                                ])
                            ]
                        )
                    )
                )
        try:
            self.update()
        except RuntimeError:
            pass
