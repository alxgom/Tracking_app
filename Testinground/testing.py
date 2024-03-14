import pandas as pd 
import os
from datetime import datetime

# Determine the current date
current_date = datetime.now().date()

# Create a DateTime index
dates = pd.date_range(start='2024-01-01', end=current_date)
# Create a DataFrame with DateTime index
df = pd.DataFrame(index=dates)

# Add columns for each variable
"""
df['variable_1'] = [1, 2, 1]
df['variable_2'] = [2, 3, 4]
"""
def update_dates(df,current_date):
    if current_date not in df.index:
        missing_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), end=current_date)
        for date in missing_dates:
            df.loc[date] = [None] * len(df.columns)


file_path = os.path.join(os.path.dirname(__file__), "test.csv")


# Save DataFrame to CSV file
df.to_csv(file_path)

#def read_csv(): 

print(df)


# Read CSV file into a DataFrame
df_loaded = pd.read_csv(file_path, index_col=0)  # Assuming the first column is the index
df_loaded.index = pd.to_datetime(df_loaded.index)  # Ensure index is in datetime format

update_dates(df_loaded, current_date)

print(df_loaded.index.size)

def new_variable(df, string_var):
    if string_var in df.columns: 
        print('variable already used')
    else: 
        df['string_var'] = '' 
        df.to_csv(file_path)



new_variable(df_loaded, 'Test_1')

print(df_loaded)
#latest_index = df.index[-1]
"""
    if 
df_loaded['variable_1'] = [1, 2, 1]
"""
