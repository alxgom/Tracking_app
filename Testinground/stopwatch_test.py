import tkinter as tk
import time

class Stopwatch(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stopwatch")
        self.geometry("200x100")
        
        self.hours = 0
        self.minutes = 0
        self.running = False

        self.label = tk.Label(self, text="00:00", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.start_button = tk.Button(self, text="Start", command=self.start_stop)
        self.start_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(side="right", padx=10)

        self.update_time()

    def start_stop(self):
        self.running = not self.running
        if self.running:
            self.start_time = time.time()
            self.start_button.config(text="Stop")
        else:
            self.start_button.config(text="Start")

    def update_time(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.hours = int(elapsed_time // 3600)
            self.minutes = int((elapsed_time % 3600) // 60)
            time_string = f"{self.hours:02d}:{self.minutes:02d}"
            self.label.config(text=time_string)
        self.after(1000, self.update_time)

    def reset(self):
        self.running = False
        self.hours = 0
        self.minutes = 0
        self.label.config(text="00:00")
        self.start_button.config(text="Start")

if __name__ == "__main__":
    app = Stopwatch()
    app.mainloop()
