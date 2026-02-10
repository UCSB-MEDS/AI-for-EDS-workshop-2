# src/analysis.py
"""Core analysis functions for temperature trends."""
import numpy as np

def calculate_mean_temperature(df, column='temperature'):
    """
    Calculate mean temperature from dataframe.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Temperature data
    column : str
        Column name for temperature values
        
    Returns:
    --------
    float
        Mean temperature
    """
    return df[column].mean()


def calculate_monthly_means(df, column='temperature'):
    """
    Calculate monthly average temperatures.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Temperature data with datetime index
    column : str
        Column name for temperature values
        
    Returns:
    --------
    pd.Series
        Monthly mean temperatures
    """
    # TODO: Using Copilot, implement this function to return monthly means.
    pass


def calculate_trend(df, column='temperature'):
    """
    Calculate linear trend in temperature data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Temperature data
    column : str
        Column name for temperature values
        
    Returns:
    --------
    float
        Trend coefficient (degrees per year)
    """
    # Simple linear regression
    x = np.arange(len(df))
    y = df[column].values
    coefficients = np.polyfit(x, y, 1)
    return coefficients[0] * 365  # Convert to per-year