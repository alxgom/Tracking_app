import flet as ft
from ui.components.sidebar import Sidebar
from ui.components.stopwatch import Stopwatch
from ui.components.history import HistoryView
from ui.components.charts import AnalyticsView

def main(page: ft.Page):
    page.title = "Tracking App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="orange")
    page.padding = 20
    page.window_width = 1000
    page.window_height = 700
    
    # Initialize DB (just in case)
    from database.core import init_db
    init_db()

    def on_task_selected(task_id, task_name):
        print(f"Task selected: {task_name} (ID: {task_id})")
        
        # When stopwatch saves, tell history to refresh
        history_view = HistoryView(task_id=task_id)
        
        def refresh_history():
            history_view.load_history()
            
        stopwatch = Stopwatch(task_id=task_id, task_name=task_name, on_stop=refresh_history)
        
        dashboard_layout = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(content=stopwatch, expand=1),
                ft.Container(content=history_view, expand=1)
            ]
        )
        
        main_content.controls.clear()
        main_content.controls.append(dashboard_layout)
        # Reset alignments for active mode (no longer strictly center)
        main_content.alignment = ft.MainAxisAlignment.START
        main_content.horizontal_alignment = ft.CrossAxisAlignment.START
        page.update()

    def on_analytics_selected():
        print("Analytics view selected")
        analytics_view = AnalyticsView()
        main_content.controls.clear()
        main_content.controls.append(analytics_view)
        main_content.alignment = ft.MainAxisAlignment.START
        main_content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.update()

    sidebar = Sidebar(on_task_selected=on_task_selected, on_analytics_selected=on_analytics_selected)
    
    main_content = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Select a task from the sidebar to begin tracking 🚀", size=20, color="onSurfaceVariant", text_align=ft.TextAlign.CENTER)
        ]
    )

    page.add(
        ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                sidebar,
                ft.Container(width=1, bgcolor="outlineVariant"),
                ft.Container(content=main_content, expand=True, padding=ft.padding.only(left=20))
            ]
        )
    )
