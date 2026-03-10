# app.py


import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import time

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id='interval', interval=100, n_intervals=0, disabled=True),  # Update every 100ms
    dcc.Store(id='start-time', data=None),  # To store the start time
    dcc.Store(id='elapsed-time', data=0),   # To store the elapsed time

    html.H1(id='display-time', children='00:00:00.0'),

    dbc.Button("Start", id="start-button", color="success", className="me-1"),
    dbc.Button("Stop", id="stop-button", color="danger", className="me-1", disabled=True),
    dbc.Button("Save", id="save-button", color="primary", className="me-1"),
    
    html.Div(id='saved-times', children=[])
])

@app.callback(
    Output('interval', 'disabled'),
    Output('start-button', 'disabled'),
    Output('stop-button', 'disabled'),
    Output('start-time', 'data'),
    Output('elapsed-time', 'data'),
    Input('start-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
    State('interval', 'disabled'),
    State('start-time', 'data'),
    State('elapsed-time', 'data'),
)
def start_stopwatch(start_clicks, stop_clicks, interval_disabled, start_time, elapsed_time):
    if start_clicks is None and stop_clicks is None:
        return interval_disabled, False, True, start_time, elapsed_time

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'start-button' and interval_disabled:  # Starting the stopwatch
        return False, True, False, time.time(), elapsed_time

    if button_id == 'stop-button' and not interval_disabled:  # Stopping the stopwatch
        elapsed_time += time.time() - start_time
        return True, False, True, start_time, elapsed_time

    return interval_disabled, False, True, start_time, elapsed_time

@app.callback(
    Output('display-time', 'children'),
    Input('interval', 'n_intervals'),
    State('start-time', 'data'),
    State('elapsed-time', 'data'),
    State('interval', 'disabled'),
)
def update_time(n_intervals, start_time, elapsed_time, interval_disabled):
    if start_time is None or interval_disabled:
        return format_time(elapsed_time)
    
    current_time = time.time()
    total_elapsed = elapsed_time + (current_time - start_time)
    
    return format_time(total_elapsed)

@app.callback(
    Output('saved-times', 'children'),
    Input('save-button', 'n_clicks'),
    State('elapsed-time', 'data'),
    State('start-time', 'data'),
    State('saved-times', 'children'),
    State('interval', 'disabled'),
)
def save_time(n_clicks, elapsed_time, start_time, saved_times, interval_disabled):
    if n_clicks is None or (elapsed_time == 0 and interval_disabled):
        return saved_times
    
    if not interval_disabled:
        current_time = time.time()
        total_elapsed = elapsed_time + (current_time - start_time)
    else:
        total_elapsed = elapsed_time

    new_time = html.Div(f"Saved Time: {format_time(total_elapsed)}")
    return saved_times + [new_time]

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = seconds - int(seconds)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds * 10)}"

if __name__ == '__main__':
    app.run_server(debug=True)
