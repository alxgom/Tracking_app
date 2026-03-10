import tkinter as tk
import time

class Stopwatch(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.running = False
        self.elapsed_time = 0
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="00:00", font=("Helvetica", 24))
        self.label.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start_stop)
        self.start_button.pack(side="left")

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(side="right")

    def start_stop(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
        else:
            self.running = True
            self.start_button.config(text="Stop")
            self.start_time = time.time() - self.elapsed_time
            self.update_time()

    def update_time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(self.elapsed_time), 60)
            time_string = f"{minutes:02d}:{seconds:02d}"
            self.label.config(text=time_string)
            self.after(1000, self.update_time)

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.label.config(text="00:00")
        self.start_button.config(text="Start")