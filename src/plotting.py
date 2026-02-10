# src/plotting.py
"""Visualization functions for temperature data."""
import matplotlib.pyplot as plt

def plot_temperature_timeseries(df, column='temperature', save_path=None):
    """
    Create a time series plot of temperature data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Temperature data with datetime index
    column : str
        Column name for temperature values
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df[column], linewidth=0.8, alpha=0.7)
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Ocean Temperature Over Time')
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


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