import pandas as pd

class WaterQualityEvaluator:
    def __init__(self, ph_range=(6.5, 8.5), turbidity_threshold=1.0):
        self.ph_range = ph_range
        self.turbidity_threshold = turbidity_threshold

    def is_safe(self, row: pd.Series) -> bool:
        
        # Check for missing values in critical columns
        if pd.isna(row['pH']) or pd.isna(row['turbidity']):
            return False
        
        # Check pH range
        if not (self.ph_range[0] <= row['pH'] <= self.ph_range[1]):
            return False

        # Check turbidity threshold
        if row['turbidity'] > self.turbidity_threshold:
            return False

        # If all checks passed, it's safe
        return True

    def evaluate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluate an entire DataFrame and add a 'safe' column.
        """
        df['safe'] = df.apply(self.is_safe, axis=1)
        return df
