from dagster_dbt import dbt_assets, DbtCliResource
from dagster_citibike.resources import dbt_manifest_path

@dbt_assets(manifest=dbt_manifest_path)
def transform_bigquery_data(dbt: DbtCliResource):
    # Run dbt build
    yield from dbt.cli(["build"]).stream()  