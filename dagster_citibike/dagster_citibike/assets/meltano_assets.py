from dagster import asset
import subprocess
from dagster_citibike.resources import meltano_dir, meltano_args

@asset(
        group_name="meltano_github_json",
        # required_resource_keys={"meltano_elt"}
        )
def extract_github_to_json():
    # Run Meltano ELT: github → json
    result = subprocess.run(
        meltano_args,
        cwd=meltano_dir,
        capture_output=True,
        text=True
    )
