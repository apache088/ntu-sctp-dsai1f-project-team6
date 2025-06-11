from dagster import define_asset_job
from .assets import *

dbt_advanced_pipeline = define_asset_job(
    name="dbt_advanced_pipeline",
    selection=[extract_load,
    dbt_debug,
    dbt_snapshots,
    dbt_staging_assets,
    dbt_dimension_assets,
    dbt_fact_assets,
    dbt_mart_assets])