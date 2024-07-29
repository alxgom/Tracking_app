import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

#from structure.stopwatch import Stopwatch
from structure import l_and_s 
#change plot label to dates, show only values 

class TaskTrackerApp():
    def __init__(self, master):
        self.master = master
        master.title("Task Tracker")
        #self.current_date = datetime.now().date()
        self.current_date = datetime.today().strftime('%Y-%m-%d')
        self.date_active = self.current_date

        # Set the file path for the tasks.csv file
        self.file_path = os.path.join(os.path.join(os.path.dirname(__file__), "tasks"), "tasks.csv")

        self.lns = l_and_s(self.file_path, self.current_date) #set everything needed to make updates to file

        self.check_for_file()
        self.tasks = self.lns.load_tasks()  # Load tasks from file  


        ''' build Tkinter stuff'''
        self.date_display = tk.Label(master, text='Today: \t '+self.current_date)
        self.date_display.grid(row=0, column=1, sticky="w")

        self.date_active_display = tk.Label(master, text='Active: \t '+self.date_active)
        self.date_active_display.grid(row=0, column=0, sticky="w")

        self.choice_display = tk.Label(self.master,text='Date:\t'+ self.date_active+
                                       '\n'+'Variable:\t \n Value:\t' )
        self.choice_display.grid(row=2, column=1)

        self.add_button = tk.Button(master, text="Add Task", command=self.show_add_task_window)
        self.add_button.grid(row=1, column=1)

        self.change_date_button = tk.Button(master, text="Change Date", command=self.show_calendar)
        self.change_date_button.grid(row=1, column=0)
        
        self.listbox = tk.Listbox(master)
        self.listbox.grid(row=2, column=0, columnspan=1, sticky="nsew")
        self.populate_listbox()

        self.selected_tasks = []
    
        self.add_value_button = tk.Button(master, text="Add value", command=self.add_value)
        self.add_value_button.grid(row=1, column=2)

        self.time_interval_entry = tk.Entry(master)
        self.time_interval_entry.grid(row=2, column=2)
        self.time_interval_entry.get()

        self.canvas = None
        self.display_tasks_with_checkbox()
        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        # Bind the closing event to the quit method
        master.protocol("WM_DELETE_WINDOW", self.quit)

        # Add the stopwatch component
        #self.stopwatch = Stopwatch(self)
        #self.stopwatch.pack()

       
    def check_for_file(self):
        if os.path.exists(self.file_path):
            print("File exists.")
        else: 
            self.lns.make_tasks()

    def show_calendar(self):
        top = tk.Toplevel(self.master)
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack()
        def select_date():
            self.date_active = cal.get_date()
            self.date_active_display.config(text = 'Active: \t ' + self.date_active)
            self.update_choice_disp()
            #print("Selected Date:", self.date_active)
            top.destroy()
        select_button = tk.Button(top, text="Select", command=select_date)
        select_button.pack()

    def plot_time_spent(self):
        selected_tasks = [task for task, var in self.selected_tasks if var.get() == 1]
        maxval=0

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig, ax = plt.subplots(figsize=(3, 2))
        for task in selected_tasks:
           # time_spent = self.tasks.loc[self.tasks[task] == task].values
            ax.plot(self.tasks.index.values, self.tasks[task]/60, marker='o', markersize=4, label=task)
        # Set the x-axis format to show hours and minutes
            maxval=max(maxval,self.tasks[task].max()/60)    
        plt.yticks(range(0, int(maxval)+1)) 

        def time_formatter(y, _):
            hours = int(y)
            minutes = int((y - int(y)) * 60)
            return f"{hours:02d}:{minutes:02d}"

        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d'))
        plt.gca().yaxis.set_major_formatter(time_formatter)
        print(maxval)      
        #ax.set_xlabel("Date")
        ax.set_ylabel("Time [Hs]")
        #ax.set_title("Time Spent on Selected Tasks")
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        # Rotate x-axis labels if needed
        plt.xticks(rotation=45)
        ax.legend(fontsize='small')
        plt.tight_layout()
        ax.grid(True)

        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=4, columnspan=2, rowspan=6, sticky="w")



    def display_tasks_with_checkbox(self):
        #for widget in self.master.winfo_children():
            #   widget.destroy()
        self.tasklabel = tk.Label(self.master, text="Select tasks to plot:")
        self.tasklabel.grid(row=4, column=0, sticky="w")
        self.selected_tasks = []
        self.taskoptions = self.tasks.columns
        for t in range(len(self.taskoptions)):
            var = tk.IntVar()
            task_checkbutton = tk.Checkbutton(self.master, text=self.taskoptions[t], variable=var)
        #for index, row in self.tasks.iterrows():
            #   var = tk.IntVar()
            # task_checkbutton = tk.Checkbutton(self.master, text=row['Task'], variable=var)
            task_checkbutton.grid(row=5+t, column=1, sticky="w")
            self.selected_tasks.append((self.taskoptions[t], var))
        #self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        #self.add_button.pack()
        self.plot_button = tk.Button(self.master, text="Plot Time Spent", command=self.plot_time_spent)
        self.plot_button.grid(row=4, column=1, sticky="w")


    def new_variable(self,  string_var):
        '''Create a new variable for a new task, then retun the updated dataframe.'''
        if string_var in self.tasks.columns: 
            print('variable already used')
        else: self.tasks[string_var] = 0 
        #return self.tasks #maybe not needed



    def add_task(self, task_name):
        if task_name:
            self.new_variable(task_name)
            self.update_everyting()

    
    def update_everyting(self): 
        '''update dataframe , csv, and tkinter'''
        self.lns.save_tasks()
        self.tasks = self.lns.load_tasks()
        self.display_tasks_with_checkbox()
        self.populate_listbox()



    def populate_listbox(self): #not sure how to work this out
        self.listbox.delete(0, tk.END)  # Clear existing items
        for item in self.tasks.columns:
            self.listbox.insert(tk.END, item)
    
   

   

    def on_select(self, event):
            # Get the index of the selected item
            index = self.listbox.curselection()[0]
            # Get the value of the selected item
            self.selected_item = self.listbox.get(index)
            self.update_choice_disp()

    def update_choice_disp(self):
        self.val = self.tasks.loc[self.date_active, self.selected_item]
        self.choice_display.config(text='Date:\t'+ self.date_active +
                            '\n'+'Variable:\t' + self.selected_item +
                                '\n Value:\t' + str(self.val))


    def add_value(self):
        
        self.tasks.loc[self.date_active, self.selected_item] += int(self.time_interval_entry.get())
        self.val = self.tasks.loc[self.date_active, self.selected_item]
        self.update_everyting()


    def show_add_task_window(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Add Task")

        label_task_name = tk.Label(add_task_window, text="Task Name:")
        label_task_name.grid(row=0, column=0, padx=3, pady=3)
        
        entry_task_name = tk.Entry(add_task_window)
        entry_task_name.grid(row=0, column=1, padx=3, pady=3)

        add_button = tk.Button(add_task_window, text="Add", command=lambda: self.add_task(entry_task_name.get()))
        add_button.grid(row=2, column=1, padx=3, pady=3)
        

    def quit(self):
            self.master.quit()  # Quit the Tkinter application


def main():
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()


"""
self.update_button = tk.Button(master, text="Update Time Spent", command=self.update_time)
self.update_button.grid(row=2, column=2)
self.date_label = tk.Label(master, text="Current Date:")
self.date_label.grid(row=3, column=0, sticky="w")
"""



if __name__ == "__main__":
    main()
