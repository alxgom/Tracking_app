import pandas as pd
import tkinter as tk
import os
from datetime import datetime

'''  Functions to read and update the csv file. 
    It also update the tasks property of the main code.'''
class l_and_s:
    def __init__(self, file_path, current_date):
        self.file_path = file_path
        self.current_date = current_date       
        #self.task = tasks

    def update_dates(self, df, current_date): 
        #Updates the dates in the task file. Fills any empty date with 0. 
        if current_date not in df.index:
            missing_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), end=current_date)
            for date in missing_dates:
                df.loc[date] = [0] * len(df.columns)
            self.save_tasks()

    def load_tasks(self): 
        #load tasks and dates from the csv file. Then returns it to self. 
        #The tasks are imported as a pd dataframe
        try:
            self.tasks = pd.read_csv(self.file_path, index_col = 0)
            self.tasks.index = pd.to_datetime(self.tasks.index)  # Ensure index is in datetime format
            self.update_dates( self.tasks, self.current_date)
            # self.update_dates(self.tasks, self.current_date) #update last date to current date
        except FileNotFoundError:
            pass
        return self.tasks
            #reutnr tasks to the __main__ self. 

    def make_tasks(self):
        self.dates = pd.date_range(start='2024-03-01', end=self.current_date)
        self.tasks = pd.DataFrame(index=self.dates)
        print(self.tasks)
        # Create a DataFrame with DateTime index
        self.save_tasks()

    def save_tasks(self): #save self.tasks to csv file.
        self.tasks.to_csv(self.file_path)


    


   
