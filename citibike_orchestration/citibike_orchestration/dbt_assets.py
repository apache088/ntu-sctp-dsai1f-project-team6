from dagster_dbt import DbtCliResource, dbt_assets
from dagster import AssetExecutionContext
from pathlib import Path

# Set path to the dbt project (adjusted two levels up)
DBT_PROJECT_PATH = Path(__file__).resolve().parents[2] / "citibike_dbt"

# Define the dbt CLI resource
dbt_cli_resource = DbtCliResource(project_dir=str(DBT_PROJECT_PATH))

@dbt_assets(manifest=DBT_PROJECT_PATH / "target" / "manifest.json")
def dbt_citibike_models(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
