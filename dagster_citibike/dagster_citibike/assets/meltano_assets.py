from dagster import asset
import subprocess
from dagster_citibike.resources import meltano_dir, meltano_args

@asset(group_name="citibike_meltano")
def citibike_ingestion_duckdb_bigquery():
    # Run Meltano ELT: DuckDB → BigQuery
    result = subprocess.run(
        meltano_args,
        cwd=meltano_dir,
        capture_output=True,
        text=True
    )
    print(result.stdout, result.stderr)