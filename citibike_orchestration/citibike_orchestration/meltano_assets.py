from dagster import asset
import pandas as pd
from pathlib import Path

@asset
def citibike_tripdata():
    # Compute absolute path to the CSV file
    current_dir = Path(__file__).resolve().parents[2]
    file_path = current_dir / "data" / "JC-202505-citibike-tripdata.csv"

    # Load CSV
    df = pd.read_csv(file_path)

    # Return the DataFrame as an asset
    return df
