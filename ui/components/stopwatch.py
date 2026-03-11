import flet as ft
from datetime import datetime, timedelta
import threading
import time
from database import crud
from database.core import SessionLocal

class Stopwatch(ft.Container):
    def __init__(self, task_id, task_name, on_stop=None):
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name
        self.on_stop = on_stop # callback to refresh history

        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self._stop_event = threading.Event()

        # UI Elements
        self.time_display = ft.Text("00:00:00", size=60, weight=ft.FontWeight.BOLD, color="primary")
        self.btn_start_pause = ft.FloatingActionButton(
            icon=ft.icons.PLAY_ARROW_ROUNDED, 
            on_click=self.toggle_timer,
            bgcolor="primaryContainer",
            tooltip="Start Tracking"
        )
        self.btn_save = ft.FloatingActionButton(
            icon=ft.icons.SAVE_ROUNDED, 
            on_click=self.save_time, 
            bgcolor="secondaryContainer",
            tooltip="Save to Database"
        )
        self.btn_reset = ft.IconButton(
            icon=ft.icons.REPLAY_ROUNDED, 
            on_click=self.reset_timer,
            tooltip="Reset Timer"
        )

        # Container styling
        self.padding = 30
        self.border_radius = 20
        self.bgcolor = "surfaceVariant"
        
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(f"Tracking: {self.task_name}", size=24, color="onSurfaceVariant", weight=ft.FontWeight.W_500),
                ft.Container(height=20),
                self.time_display,
                ft.Container(height=30),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        self.btn_start_pause,
                        self.btn_save,
                        self.btn_reset
                    ]
                )
            ]
        )

    def did_mount(self):
        self.running_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.running_thread.start()

    def will_unmount(self):
        self._stop_event.set()

    def toggle_timer(self, e):
        if self.running:
            # pause
            self.running = False
            self.elapsed_time += datetime.now() - self.start_time
            self.btn_start_pause.icon = ft.icons.PLAY_ARROW_ROUNDED
        else:
            # start
            self.running = True
            self.start_time = datetime.now()
            self.btn_start_pause.icon = ft.icons.PAUSE_ROUNDED
        
        self.update()

    def reset_timer(self, e):
        self.running = False
        self.total_elapsed = timedelta()
        self.elapsed_time = timedelta()
        self.start_time = None
        self.time_display.value = "00:00:00"
        self.btn_start_pause.icon = ft.icons.PLAY_ARROW_ROUNDED
        self.update()

    def save_time(self, e):
        self.running = False
        
        # Calculate total minutes to save
        total = self.elapsed_time
        if self.start_time:
            total += datetime.now() - self.start_time
            
        minutes = int(total.total_seconds() // 60)
        
        # Require at least 1 minute to save
        if minutes > 0:
            with SessionLocal() as db:
                crud.add_time_log(db, task_id=self.task_id, duration_minutes=minutes)
            
            if self.on_stop:
                self.on_stop() # trigger UI refresh for history
                
        self.reset_timer(e)

    def update_timer(self):
        while not self._stop_event.is_set():
            if self.running and self.start_time:
                current_elapsed = self.elapsed_time + (datetime.now() - self.start_time)
                
                # Format as HH:MM:SS
                total_seconds = int(current_elapsed.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                new_display = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                if self.time_display.value != new_display:
                    self.time_display.value = new_display
                    try:
                        self.update()
                    except RuntimeError:
                        pass
                    
            time.sleep(0.5)
