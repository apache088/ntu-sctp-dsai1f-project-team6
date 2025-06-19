from dagster import Definitions, job, ScheduleDefinition
from .dbt_assets    import dbt_citibike_models, dbt_cli_resource
from .meltano_assets import citibike_tripdata

@job
def elt_pipeline():
    citibike_tripdata()
    dbt_citibike_models()

elt_schedule = ScheduleDefinition(
    job=elt_pipeline,
    cron_schedule="0 2 * * *",  # every day @ 02:00
)

defs = Definitions(
    assets=[citibike_tripdata, dbt_citibike_models],
    resources={"dbt": dbt_cli_resource},
    jobs=[elt_pipeline],
    schedules=[elt_schedule],
)
