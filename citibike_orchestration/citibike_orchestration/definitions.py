# # citibike_orchestration/definitions.py

# from dagster import job, ScheduleDefinition, Definitions
# from dagster_meltano import meltano_resource, meltano_run_op
# from dagster_dbt import dbt_cli_resource, dbt_run_op

# @job(
#     name="etl_then_transform",
#     resource_defs={
#         "meltano": meltano_resource,   # lets us call meltano_run_op
#         "dbt":    dbt_cli_resource,    # lets us call dbt_run_op
#     },
# )
# def etl_then_transform():
#     # 1) Run your Meltano EL step (reads your meltano.yml)
#     meltano_run_op("tap-duckdb target-bigquery")()

#     # 2) Then run your dbt models (reads dbt_project.yml & profiles.yml)
#     dbt_run_op()()

# # Schedule it daily at midnight
# etl_schedule = ScheduleDefinition(
#     job=etl_then_transform,
#     cron_schedule="0 0 * * *",
# )

# defs = Definitions(
#     jobs=[etl_then_transform],
#     schedules=[etl_schedule],
# )

import os, subprocess
from dagster import job, op, ScheduleDefinition, Definitions

# helper to compute absolute path
ROOT = os.path.dirname(os.path.dirname(__file__))

@op
def meltano_elt():
    meltano_dir = os.path.join(ROOT, "..", "meltano_citibike_ingest")
    subprocess.check_call(
      ["meltano", "elt", "tap-duckdb", "target-bigquery", "--environment", "dev"],
      cwd=meltano_dir
    )

@op
def dbt_run():
    dbt_dir = os.path.join(ROOT, "..", "citibike_dbt")
    for cmd in [["dbt","deps"], ["dbt","seed"], ["dbt","run"], ["dbt","test"]]:
        subprocess.check_call(cmd, cwd=dbt_dir)

@job
def etl_then_transform():
    # enforce sequential execution
    meltano_elt()
    dbt_run()

etl_schedule = ScheduleDefinition(
    job=etl_then_transform,
    cron_schedule="0 0 * * *",
)

defs = Definitions(
    jobs=[etl_then_transform],
    schedules=[etl_schedule],
)
