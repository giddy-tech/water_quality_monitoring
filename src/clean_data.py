import pandas as pd

def clean_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sensor data by handling missing or invalid values.

    Returns:
        pd.DataFrame: Cleaned data.
    """
    # Ensure numeric columns are numeric, coerce errors to NaN
    numeric_cols = ['pH', 'turbidity', 'dissolved_oxygen', 'temperature']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows where critical columns are missing
    df = df.dropna(subset=['pH', 'turbidity'])

    # Optionally, fill non-critical columns with mean if missing
    df['dissolved_oxygen'] = df['dissolved_oxygen'].fillna(df['dissolved_oxygen'].mean())
    df['temperature'] = df['temperature'].fillna(df['temperature'].mean())

    # Reset index for cleanliness
    df = df.reset_index(drop=True)
    
    return df
