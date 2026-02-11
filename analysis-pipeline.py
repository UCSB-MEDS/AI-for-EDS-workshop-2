
"""Main script to run ocean temperature analysis."""
from src.data_loader import load_temperature_data, validate_data
from src.analysis import calculate_mean_temperature, calculate_trend
from src.plotting import plot_temperature_timeseries

def main():
    """Run the complete analysis pipeline."""
    print("=" * 50)
    print("Ocean Temperature Analysis")
    print("=" * 50)
    
    # Load data
    print("\n1. Loading data...")
    data_path = "data/ocean_temps.csv"
    df = load_temperature_data(data_path)
    
    # Validate
    print("\n2. Validating data...")
    validate_data(df)
    
    # Calculate statistics
    print("\n3. Calculating statistics...")
    mean_temp = calculate_mean_temperature(df)
    print(f"   Mean temperature: {mean_temp:.2f}°C")
    
    trend = calculate_trend(df)
    print(f"   Temperature trend: {trend:.4f}°C per year")
    
    # Visualize
    print("\n4. Creating visualizations...")
    plot_temperature_timeseries(df)
    
    print("\n✓ Analysis complete!")


if __name__ == "__main__":
    main()