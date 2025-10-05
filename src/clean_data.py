import pandas as pd

def clean_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = ['ph', 'turbidity', 'temperature']
    for col in numeric_cols:
        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
    return df
