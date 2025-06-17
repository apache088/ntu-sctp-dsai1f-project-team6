from dagster import asset
import subprocess
from dagster_citibike.resources import meltano_dir, meltano_args

@asset(group_name="meltano_citibike")
def extract_citibike_duckdb_bigquery():
    # Run Meltano ELT: duckDB → BigQuery
    result = subprocess.run(
        meltano_args,
        cwd=meltano_dir,
        capture_output=True,
        text=True
    )
