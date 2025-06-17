from dagster import resource
from dagster_dbt import DbtCliResource

# Update the following absolute paths to point to the Meltano and dbt projects.
meltano_dir = "../../../citibike-ingestion"

dbt_dir = "/insert_path_to_project/ntu-sctp-dsai1f-project-team6/citibike_dbt"

# Meltano resources
meltano_tap = "tap-github"
meltano_target = "target-bigquery"
meltano_args = ["meltano", "run", meltano_tap, meltano_target]

# Dbt resources
dbt_manifest_path = f"{dbt_dir}/target/manifest.json"
@resource
def dbt_bigquery():
    return DbtCliResource(
        project_dir=dbt_dir)
