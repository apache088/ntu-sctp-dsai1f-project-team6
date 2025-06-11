from pathlib import Path
from dagster import AssetExecutionContext, asset, Output
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject
import subprocess

DBT_PROJECT_DIR = Path(__file__).parent.parent.parent / "dbt_world_athletics"  # Adjust this

# Initialize DbtProject
dbt_project = DbtProject(
    project_dir=str(DBT_PROJECT_DIR),
    profiles_dir=str(DBT_PROJECT_DIR),
    target="dev"
)

# 1. Meltano Extraction
@asset(group_name="extract_load")
def extract_load(context: AssetExecutionContext):
    result = subprocess.run(
        ["meltano", "elt", "tap-postgres", "target-bigquery"],
        cwd="/home/aswerty123/projects/dsai_1f/module_2/ntu-sctp-dsai1f-project-team6/world_athletics_pipeline/meltano_world_athletics",
        capture_output=True,
        text=True
    )
    return Output(result.stdout)

# 2. dbt Debug (optional, before running dbt builds)
# @asset(required_resource_keys={"dbt"}, group_name="transform", deps=[extract_load])
# def dbt_debug(context: AssetExecutionContext):
#     return context.resources.dbt.cli(["debug"], context=context).wait()

@dbt_assets(manifest=dbt_project.manifest_path, deps=[extract_load])
def dbt_debug(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["debug"], context=context).stream()
# # Initialize DbtProject
# dbt_project = DbtProject(
#     project_dir="path_to_your_dbt_project",  # Update this path
#     profiles_dir="path_to_your_dbt_profiles",  # Update this path
#     target="dev"  # Or your target name
# )

# 3. dbt tag:stg
@dbt_assets(manifest=dbt_project.manifest_path, select="tag:stg")
def dbt_staging_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run", "-s", "tag:stg"], context=context).stream()

# 4. dbt snapshot (optional, separate from dbt_assets)
@asset(required_resource_keys={"dbt"}, group_name="transform", deps=[dbt_staging_assets])
def dbt_snapshots(context: AssetExecutionContext):
    return context.resources.dbt.cli(["snapshot"], context=context).wait()

# 5. dbt tag:dim
@dbt_assets(manifest=dbt_project.manifest_path, select="tag:dim")
def dbt_dimension_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run", "-s", "tag:dim"], context=context).stream()

# 6. dbt tag:fct
@dbt_assets(manifest=dbt_project.manifest_path, select="tag:fct")
def dbt_fact_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run", "-s", "tag:fct"], context=context).stream()

# 7. dbt tag:marts
@dbt_assets(manifest=dbt_project.manifest_path, select="tag:marts")
def dbt_mart_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run", "-s", "tag:marts"], context=context).stream()