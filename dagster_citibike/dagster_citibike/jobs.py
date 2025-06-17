from dagster import define_asset_job, AssetSelection
from dagster_citibike.assets import dbt_assets

# Define a job that runs Meltano → dbt
elt_job = define_asset_job(
    name="elt_job",
    selection=AssetSelection.groups("meltano_github_json") 
    | AssetSelection.from_modules(dbt_assets)
)