from dagster import AssetSelection, define_asset_job, Definitions, load_assets_from_modules, RunConfig
from dagster_citibike.resources import dbt_bigquery, config_elt, config_dbt
from dagster_citibike.assets import meltano_assets, dbt_assets


all_assets = load_assets_from_modules([meltano_assets,dbt_assets])

# Create jobs
# Job runs the full Citibike ELT with Meltano ingestion and dbt transformation (after ingest has succeeded).
job_elt = define_asset_job(
    name="citibike_elt",
    selection=AssetSelection.assets(meltano_assets.citibike_ingestion_duckdb_bigquery, dbt_assets.citibike_dbt_elt),
    config=RunConfig(ops={"citibike_dbt_elt": config_elt})
)

# Job runs just the Citibike dbt without waiting for a real ingestion.
job_dbt = define_asset_job(
    name="dbt_only",
    selection=AssetSelection.assets(dbt_assets.citibike_mock_ingestion, dbt_assets.citibike_dbt_elt),
    config=RunConfig(ops={"citibike_dbt_elt": config_dbt})
)

defs = Definitions(
    assets=all_assets,
    jobs=[job_elt, job_dbt],
    resources={
        "dbt": dbt_bigquery,
    },
)
