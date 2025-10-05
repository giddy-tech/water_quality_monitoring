import os
import sys

# Add the project's root directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Construct path to the CSV file
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sensor_data.csv')

import pandas as pd
from src.clean_data import clean_sensor_data
from src.load_data import load_sensor_data

from src.evaluate import WaterQualityEvaluator


class Sensor:
    """Model a sensor reading."""
    def __init__(self, sensor_id, location, ph, turbidity, temperature):
        self.sensor_id = sensor_id
        self.location = location
        self.ph = ph
        self.turbidity = turbidity
        self.temperature = temperature
        self.is_safe = None
        self.reason = None


def main():
    # --- 1. Load data ---
    df = load_sensor_data("data/sensor_data.csv")
    df = clean_sensor_data(df)

    # --- 2. Convert to Sensor objects ---
    sensors = []
    for _, row in df.iterrows():
        sensor = Sensor(
            sensor_id=row['sensor_id'],
            location=row['location'],
            ph=row['ph'],
            turbidity=row['turbidity'],
            temperature=row['temperature']
        )
        sensors.append(sensor)

    # --- 3. Evaluate water quality ---
    evaluator = WaterQualityEvaluator()
    for sensor in sensors:
        # Check safety
        sensor.is_safe = evaluator.is_safe({
            'ph': sensor.ph,
            'turbidity': sensor.turbidity
        })

        # Determine reason (prioritize pH)
        if sensor.is_safe:
            sensor.reason = ""
        else:
            if pd.isnull(sensor.ph):
                sensor.reason = "missing pH"
            elif sensor.ph < evaluator.ph_range[0]:
                sensor.reason = "pH too low"
            elif sensor.ph > evaluator.ph_range[1]:
                sensor.reason = "pH too high"
            elif pd.isnull(sensor.turbidity):
                sensor.reason = "missing turbidity"
            elif sensor.turbidity > evaluator.turbidity_threshold:
                sensor.reason = "turbidity too high"

    # --- 4. Optional: Filter by location ---
    loc_filter = input("Enter location name to filter (or press Enter for all): ").strip()
    filtered_sensors = [s for s in sensors if loc_filter.lower() in s.location.lower()] if loc_filter else sensors

    # --- 5. Print results ---
    safe_count = 0
    unsafe_count = 0
    results = []

    for sensor in filtered_sensors:
        if sensor.is_safe:
            status = f"Sensor {sensor.sensor_id} at {sensor.location}: ✅ Safe"
            safe_count += 1
        else:
            status = f"Sensor {sensor.sensor_id} at {sensor.location}: ❌ Unsafe ({sensor.reason})"
            unsafe_count += 1
        print(status)
        results.append({
            "sensor_id": sensor.sensor_id,
            "location": sensor.location,
            "ph": sensor.ph,
            "turbidity": sensor.turbidity,
            "temperature": sensor.temperature,
            "is_safe": sensor.is_safe,
            "reason": sensor.reason
        })

    # --- 6. Print summary ---
    print(f"\nSummary: {safe_count} safe, {unsafe_count} unsafe")

    # --- 7. Save results to CSV ---
    results_df = pd.DataFrame(results)
    results_df.to_csv("results.csv", index=False)
    print("Results saved to results.csv")


if __name__ == "__main__":
    main()