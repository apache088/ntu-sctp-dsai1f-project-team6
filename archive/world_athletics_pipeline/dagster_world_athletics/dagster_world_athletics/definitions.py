from dagster import Definitions, AssetSelection, ScheduleDefinition
from dagster_dbt import dbt_assets, DbtCliResource

from .resources import dbt_resource
from .assets import (
    extract_load,
    dbt_debug,
    dbt_staging_assets,
    dbt_snapshots,
    dbt_dimension_assets,
    dbt_fact_assets,
    dbt_mart_assets
)
from .jobs import dbt_advanced_pipeline

# If you have dbt assets defined via YAML
# (Optional - only needed if using @dbt_assets decorator)
# dbt_manifest_path = "../dbt/target/manifest.json"
# @dbt_assets(manifest=dbt_manifest_path)
# def my_dbt_assets(context, dbt: DbtCliResource):
#     yield from dbt.cli(["build"], context=context).stream()

defs = Definitions(
    assets=[
        extract_load,
        dbt_debug,
        dbt_staging_assets,
        dbt_snapshots,
        dbt_dimension_assets,
        dbt_fact_assets,
        dbt_mart_assets
        # my_dbt_assets  # Include if using @dbt_assets
    ],
    jobs=[dbt_advanced_pipeline],
    resources={
        "dbt": dbt_resource,
    },
    schedules=[
        ScheduleDefinition(
            job=dbt_advanced_pipeline,
            cron_schedule="0 3 * * *",  # Daily at 3 AM
            name="daily_refresh"
        )
    ]
)