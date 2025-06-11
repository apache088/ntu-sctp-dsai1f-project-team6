from dagster import resource
# from dagster_dbt import DbtCliResource , DbtProject
# from pathlib import Path

from dagster_dbt import DbtCliResource

@resource
def dbt_resource():
    return DbtCliResource(
        project_dir="/home/aswerty123/projects/dsai_1f/module_2/ntu-sctp-dsai1f-project-team6/world_athletics_pipeline/dbt_world_athletics",
        profiles_dir="/home/aswerty123/projects/dsai_1f/module_2/ntu-sctp-dsai1f-project-team6/world_athletics_pipeline/dbt_world_athletics",
        target='dev'
    )

# dbt_world_athletics_project = DbtProject(
#     project_dir=Path(__file__).joinpath("..", "..", "..","dbt_world_athletics").resolve(),
#     packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
# )

# @resource
# def dbt_resource():
#     return DbtCliResource(project_dir=dbt_world_athletics_project)
#     # return DbtCliResource.configured({
#     #     "project_dir": "/home/aswerty123/projects/dsai_1f/module_2/ntu-sctp-dsai1f-project-team6/world_athletics_pipeline/dbt_world_athletics",
#     #     "profiles_dir": "/home/aswerty123/projects/dsai_1f/module_2/ntu-sctp-dsai1f-project-team6/world_athletics_pipeline/dbt_world_athletics",
#     #     "target": "dev"
#     # })