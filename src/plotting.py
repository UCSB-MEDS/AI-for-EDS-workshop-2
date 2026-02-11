# src/plotting.py
"""Visualization functions for temperature data."""
import matplotlib.pyplot as plt
import plotly.express as px
import webbrowser
import os


def plot_temperature_timeseries(df, column='temperature', save_path='output/temp_plot.html'):
    """
    Create a time series plot of temperature data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Temperature data with datetime index
    column : str
        Column name for temperature values
    save_path : str
        Path to save figure (default: 'output/temp_plot.html')
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    fig = px.line(df.reset_index(), x='index', y=column)
    fig.update_layout(
        title='Ocean Temperature Over Time',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        width=1200,
        height=600
    )
    fig.update_traces(line=dict(width=0.8), opacity=0.7)
    
    fig.write_html(save_path)
    webbrowser.open('file://' + os.path.realpath(save_path))



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