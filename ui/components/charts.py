import flet as ft
from datetime import datetime, timedelta
from database import crud
from database.core import SessionLocal

class AnalyticsView(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.padding = 30
        self.expand = True
        self.bgcolor = "surface"
        self.border_radius = 10
        
        self.chart_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.END,
            expand=True
        )
        
        self.content = ft.Column(
            controls=[
                ft.Text("Last 7 Days Activity", size=24, weight=ft.FontWeight.W_600),
                ft.Text("Total minutes logged per day", size=14, color="onSurfaceVariant"),
                ft.Container(height=40),
                ft.Container(
                    content=self.chart_row,
                    height=300,
                    padding=20,
                    bgcolor="surfaceVariant",
                    border_radius=12,
                    alignment=ft.Alignment(0, 1)
                )
            ]
        )

    def did_mount(self):
        self.load_data()

    def load_data(self):
        self.chart_row.controls.clear()
        
        with SessionLocal() as db:
            logs = crud.get_recent_history(db, limit=100) # Fetch enough for 7 days
            
        # Group by date (last 7 days)
        today = datetime.now().date()
        daily_totals = {today - timedelta(days=i): 0 for i in range(6, -1, -1)}
        
        for log in logs:
            log_date = log.date.date()
            if log_date in daily_totals:
                daily_totals[log_date] += log.duration_minutes
                
        max_minutes = max(daily_totals.values()) if daily_totals.values() else 1
        if max_minutes == 0:
            max_minutes = 1 # Avoid division by zero
            
        # Build UI Bars
        for d, total in daily_totals.items():
            height_pct = total / max_minutes
            bar_height = max(10, 180 * height_pct) # Max height is 180px
            
            day_str = d.strftime("%a") # Mon, Tue...
            
            bar_col = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.END,
                spacing=5,
                controls=[
                    ft.Text(f"{total}m", size=12, color="onSurfaceVariant"),
                    ft.Container(
                        width=30,
                        height=bar_height,
                        bgcolor="primary",
                        border_radius=ft.border_radius.vertical(top=6),
                        tooltip=f"{d.strftime('%b %d')}: {total} minutes"
                    ),
                    ft.Text(day_str, size=14, weight=ft.FontWeight.W_500)
                ]
            )
            self.chart_row.controls.append(bar_col)
            
        try:
            self.update()
        except RuntimeError:
            pass
