from dagster import AssetExecutionContext, AssetKey, Config, EnvVar, resource
from dagster_dbt import DbtCliResource

# Ensure the following absolute paths point to the Meltano and dbt projects.
meltano_dir = EnvVar("MELTANO_PROJECT_ROOT").get_value()

dbt_dir = EnvVar("DBT_PROJECT_ROOT").get_value()

# States
class JobConfig(Config):
    """Job configuration that can be passed to an asset in the job."""
    # The AssetKey to identify the asset from which to read metadata from.
    asset_key: str

# ELT job should read from the real ingestion asset.
config_elt = JobConfig(asset_key="citibike_ingestion_duckdb_bigquery")
# DBT only job should read from the mock ingestion asset.
config_dbt = JobConfig(asset_key="citibike_mock_ingestion")

def check_ingestion_done(context: AssetExecutionContext, asset_key: str, meta_data_key: str):
    """
    Search using the meta_data_key in the metadata of the given asset's latest materialization to see if the ingestion has been completed.
    """
    ingestion_done = False
    latest_record = context.instance.get_latest_materialization_event(
        AssetKey(asset_key)
    )

    if not latest_record or not latest_record.dagster_event:
        pass
    else:
        status = latest_record.dagster_event.event_specific_data.materialization.metadata.get(meta_data_key)
        if status is not None:
            ingestion_done = status
    return ingestion_done

# Meltano resources
meltano_tap = "tap-duckdb"
meltano_target = "target-bigquery"
meltano_run = ["meltano", "run", meltano_tap, meltano_target]

# Dbt resources
dbt_manifest_path = f"{dbt_dir}/target/manifest.json"
@resource
def dbt_bigquery():
    return DbtCliResource(
        project_dir=dbt_dir)
