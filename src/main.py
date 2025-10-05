import pandas as pd
from src.load_data import load_sensor_data
from src.clean_data import clean_sensor_data
from src.evaluate import WaterQualityEvaluator

def main():
    # 1. Load
    df = load_sensor_data("data/sensor_data.csv")
    
    # 2. Clean
    df = clean_sensor_data(df)
    
    # 3. Evaluate
    evaluator = WaterQualityEvaluator()
    df["is_safe"] = df.apply(evaluator.is_safe, axis=1)
    
    # 4. Print results
    for _, row in df.iterrows():
        status = "✅ Safe" if row["is_safe"] else "❌ Unsafe"
        print(f"Sensor {row['sensor_id']} at {row['location']}: {status}")

if __name__ == "__main__":
    main()
