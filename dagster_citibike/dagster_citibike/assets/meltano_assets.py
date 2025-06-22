import os
from dagster import asset, AssetExecutionContext, Output
import subprocess
from dagster_citibike.resources import meltano_dir, meltano_run

@asset(group_name="citibike_meltano")
def citibike_ingestion_duckdb_bigquery(context: AssetExecutionContext):
    """
    Runs the Meltano ingestion part of the citibike elt.
    """
    meta_data_key = f"{context.run_id}_ingestion_done"
    context.log.info(f"[ELT][INGEST] Process PID: {os.getpid()} {meta_data_key=}.")

    ingestion_done = False
    # Run Meltano ELT: DuckDB → BigQuery
    result = subprocess.run(
        meltano_run,
        cwd=meltano_dir,
        capture_output=True,
        text=True
    )
    # Set state and log.
    if result.returncode != 0:
        context.log.error(f"[ELT][INGEST] {ingestion_done=} Meltano run failed with return code {result.returncode}.\nCmd: {result.args}")
    else:
        ingestion_done = True
        context.log.info(f"[ELT][INGEST] {ingestion_done=} Meltano run completed.")

    # Pass meltano log to Dagster.
    context.log.info(result.stdout)
    context.log.error(result.stderr)

    metadata={
        meta_data_key: ingestion_done,
        "run_id": context.run_id
    }
    context.log.info(f"[ELT][INGEST] DONE. {metadata=}.")

    return Output(
        value=ingestion_done,
        metadata=metadata
    )
