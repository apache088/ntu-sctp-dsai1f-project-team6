import time, os
from multiprocessing import Manager
from dagster import asset, AssetExecutionContext, Output
from dagster_dbt import dbt_assets
from dagster_citibike.resources import dbt_manifest_path, check_ingestion_done, JobConfig

@asset(group_name="citibike_dbt")
def citibike_mock_ingestion(context: AssetExecutionContext):
    """
    Mock ingestion asset to trigger dbt run without a real ingestion.
    """
    meta_data_key = f"{context.run_id}_ingestion_done"
    context.log.info(f"[MOCK][INGEST] Process PID: {os.getpid()} {meta_data_key=}.")

    ingestion_done = True
    metadata={
        meta_data_key: ingestion_done,
        "run_id": context.run_id
    }
    context.log.info(f"[MOCK][INGEST] DONE. {metadata=}.")

    return Output(
        value=True,
        metadata=metadata
    )

@dbt_assets(manifest=dbt_manifest_path, required_resource_keys={"dbt"})
def citibike_dbt_elt(context: AssetExecutionContext, config: JobConfig):
    """
    Runs dbt data transformation part of the citibike elt.
    Will run only if there has been a new ingestion.
    A mock ingestion can be used to trigger the dbt run without a real ingestion.
    The selection of real or mock ingestion is made via JobConfig during Job creation.
    Checks for new ingestion for 5 minutes.
    If none is found, dbt will not run.
    """
    meta_data_key = f"{context.run_id}_ingestion_done"
    asset_key = config.asset_key
    context.log.info(f"[ELT][DBT] Process PID: {os.getpid()} {asset_key=} {meta_data_key=}.")

    ingestion_done = check_ingestion_done(context, asset_key, meta_data_key)
    wait_total = 0
    wait_s = 10
    while (not ingestion_done and wait_total < 300):
        context.log.info(f"[ELT][DBT] {ingestion_done=} Waiting for a new ingestion to complete...")
        # Wait for some seconds before checking again
        wait_total += wait_s
        time.sleep(wait_s)
        ingestion_done = check_ingestion_done(context, asset_key, meta_data_key)
    
    # Exit if waited for >= 5 min.    
    if wait_total >= 300:
        context.log.info(f"[ELT][DBT] {ingestion_done=} Time out: No new ingestion found, skipping dbt build.")
        return
    
    context.log.info(f"[ELT][DBT] {ingestion_done=} New ingestion found, running dbt build...")

    # Run dbt build
    dbt = context.resources.dbt
    yield from dbt.cli(["build"], context=context).stream()
    context.log.info(f"[ELT][DBT] DONE. dbt build completed.")
