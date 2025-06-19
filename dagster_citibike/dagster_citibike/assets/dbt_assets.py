from dagster import AssetExecutionContext
from dagster_dbt import dbt_assets, DbtCliResource
from dagster_citibike.resources import dbt_manifest_path

@dbt_assets(manifest=dbt_manifest_path)
def citibike_dbt(context: AssetExecutionContext, dbt: DbtCliResource):
    # Run dbt build
    yield from dbt.cli(["build"], context=context).stream()