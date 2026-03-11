import flet as ft
from database import crud
from database.core import SessionLocal

class Sidebar(ft.Container):
    def __init__(self, on_task_selected, on_analytics_selected=None):
        super().__init__()
        self.on_task_selected = on_task_selected
        self.on_analytics_selected = on_analytics_selected
        
        # Styling
        self.width = 250
        self.padding = ft.padding.all(10)
        self.border_radius = 10
        self.bgcolor = "surfaceVariant"
        
        # Components
        self.tasks_list = ft.ListView(expand=True, spacing=2)
        self.add_task_field = ft.TextField(label="New Task Name", autofocus=True, on_submit=self.save_task)
        
        self.add_task_dialog = ft.AlertDialog(
            title=ft.Text("Add New Task"),
            content=self.add_task_field,
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Add", on_click=self.save_task)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.content = ft.Column(
            controls=[
                ft.Text("Tasks", size=20, weight=ft.FontWeight.W_600),
                ft.ElevatedButton("+ Add Task", on_click=self.open_dialog, width=230, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                ft.ElevatedButton("📊 Analytics", on_click=self.trigger_analytics, width=230, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), bgcolor="secondaryContainer", color="onSecondaryContainer")),
                ft.Divider(height=20, color="outlineVariant"),
                self.tasks_list
            ]
        )
        self.load_tasks()

    def trigger_analytics(self, e):
        if self.on_analytics_selected:
            self.on_analytics_selected()

    def open_dialog(self, e):
        self.add_task_field.value = ""
        self.page.show_dialog(self.add_task_dialog)
        self.add_task_field.focus()

    def close_dialog(self, e):
        self.add_task_dialog.open = False
        self.page.update()

    def save_task(self, e):
        print("Save Task Triggered. Value:", self.add_task_field.value)
        if not self.add_task_field.value:
            print("No value, returning.")
            return
            
        try:
            with SessionLocal() as db:
                crud.add_task(db, name=self.add_task_field.value)
                print("Task added to DB.")
        except Exception as ex:
            print("DB Error during save_task:", ex)
            
        self.close_dialog(e)
        self.load_tasks()

    def load_tasks(self):
        self.tasks_list.controls.clear()
        with SessionLocal() as db:
            tasks = crud.get_active_tasks(db)
            for t in tasks:
                self.tasks_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon("circle", color=t.color, size=12),
                                ft.Text(t.name, size=14, expand=True, no_wrap=True)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(horizontal=12, vertical=10),
                        border_radius=8,
                        on_click=lambda e, task_id=t.id, task_name=t.name: self.on_task_selected(task_id, task_name),
                    )
                )
        try:
            self.tasks_list.update()
        except Exception:
            try:
                self.update()
            except RuntimeError:
                pass
