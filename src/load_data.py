import pandas as pd

def load_sensor_data(file_path: str):
    """
    Load sensor CSV data into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame()
