# src/plotting.py
"""Visualization functions for temperature data."""
import matplotlib.pyplot as plt
from dash import Dash, dcc, html
import plotly.express as px
import webbrowser

def plot_temperature_timeseries(df, column='temperature'):
    app = Dash(__name__)
    
    fig = px.line(df.reset_index(), x='index', y=column)
    fig.update_layout(
        title='Ocean Temperature Time Series<br>(January 2021 - December 2024)',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        template='plotly_white',
        title_x=0.5,
        font=dict(size=14),
        hovermode='x unified'
    )
    fig.update_traces(line=dict(width=2, color='#1f77b4'))
    
    app.layout = html.Div([
        dcc.Graph(figure=fig, style={'height': '80vh'})
    ], style={'padding': '20px'})
    
    webbrowser.open('http://127.0.0.1:8050')
    app.run(debug=False)
    




def plot_monthly_comparison(monthly_data, save_path=None):
    """
    Create a bar plot comparing monthly average temperatures.
    
    Parameters:
    -----------
    monthly_data : pd.Series
        Monthly temperature averages
    save_path : str, optional
        Path to save figure
    """
    # TODO: Students will complete this with Copilot help
    fig, ax = plt.subplots(figsize=(10, 6))
    # Add implementation here
    pass