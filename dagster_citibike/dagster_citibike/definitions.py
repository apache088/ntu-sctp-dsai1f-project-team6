from dagster import Definitions, load_assets_from_modules
from dagster_citibike.resources import dbt_bigquery
from dagster_citibike.assets import meltano_assets, dbt_assets


all_assets = load_assets_from_modules([meltano_assets,dbt_assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "dbt": dbt_bigquery,
    }
)
