from dagster import EnvVar, resource
from dagster_dbt import DbtCliResource

# Ensure the following absolute paths point to the Meltano and dbt projects.
meltano_dir = EnvVar("MELTANO_PROJECT_ROOT").get_value()

dbt_dir = EnvVar("DBT_PROJECT_ROOT").get_value()

# Meltano resources
meltano_tap = "tap-duckdb"
meltano_target = "target-bigquery"
meltano_args = ["meltano", "run", meltano_tap, meltano_target]

# Dbt resources
dbt_manifest_path = f"{dbt_dir}/target/manifest.json"
@resource
def dbt_bigquery():
    return DbtCliResource(
        project_dir=dbt_dir)
