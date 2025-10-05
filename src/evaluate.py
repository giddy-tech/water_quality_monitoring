import pandas as pd

class WaterQualityEvaluator:
    def __init__(self, ph_range=(6.5, 8.5), turbidity_threshold=1.0):
        self.ph_range = ph_range
        self.turbidity_threshold = turbidity_threshold

    def is_safe(self, row: pd.Series) -> bool:
        if pd.isnull(row['ph']):
            return False
        if pd.isnull(row['turbidity']):
            return False

        ph_safe = self.ph_range[0] <= row['ph'] <= self.ph_range[1]
        turbidity_safe = row['turbidity'] <= self.turbidity_threshold

        return ph_safe and turbidity_safe

    def get_reason(self, row: pd.Series) -> str:
        """
        Returns the reason why a row is unsafe.
        """
        if pd.isnull(row['ph']):
            return "missing pH"
        if pd.isnull(row['turbidity']):
            return "missing turbidity"
        if row['ph'] < self.ph_range[0]:
            return "pH too low"
        if row['ph'] > self.ph_range[1]:
            return "pH too high"
        if row['turbidity'] > self.turbidity_threshold:
            return "turbidity too high"
        return ""
