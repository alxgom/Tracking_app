import pandas as pd
 

def load_tasks(self):
        try:
            self.tasks = pd.read_csv(self.file_path)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        self.tasks.to_csv(self.file_path, index=False)

    def add_task(self):
        task_name = self.task_name_entry.get()
        if task_name:
            self.tasks.loc[len(self.tasks)] = [task_name, 0]
            self.save_tasks()
            self.display_tasks_with_checkbox()
