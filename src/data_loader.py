# src/data_loader.py
"""Load and validate ocean temperature data."""
import pandas as pd

def load_temperature_data(filepath):
    """
    Load ocean temperature data from CSV.
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame
        Temperature data with datetime index
    """
    df = pd.read_csv(filepath)
    return df


def validate_data(df):
    """Check for missing values and valid temperature ranges."""
    messages = []
    if df.isnull().any().any():
        messages.append("Contains missing values")
    temp_col = 'temperature'
    if (df[temp_col] < -2).any() or (df[temp_col] > 35).any():
        messages.append("Temperature values outside expected range (-2 to 35°C)")
    if messages:
        return "Warning: " + "; ".join(messages)
    else:
        return "Passed - No issues detected"