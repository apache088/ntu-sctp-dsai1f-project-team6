# Citibike Trip Data ELT Orchestration

## Overview
This is a [Dagster](https://dagster.io/) project that automates the running of:
- Meltano ingestion
  - [Extraction](../citibike-ingestion/README.md#load-csv-file-into-duckdb) from DuckDB database.
  - [Uploading data](../citibike-ingestion/README.md#meltano-to-orchestrate-an-el-pipeline) to Google BigQuery as a table.
  - Implementation:
    - Uses a Python subprocess to run a meltano command.
- dbt transformation
  - Performs all the data transformation steps configured in dbt project.
  - Implementation:
    - Uses dbt CLI to run dbt build.

## Instructions for running this Dagster project
- Ensure all the [prerequisites](../README.md#prerequisites) have been done.
  - Use the **same VS Code terminal** for the following steps.
- Start at the root directory of this project.
- Go to Dagster project:
  - `cd dagster_citibike`
- Start Dagster UI:
  - `dagster dev`
  - Start the Dagster UI web server:
    - `dagster dev`
  - Open http://localhost:3000 on a browser for Dagster UI.
- On Dagster UI:
  - You can choose to materialize via jobs or individual assets.
  - It is recommended to materialize via jobs, which provide asset dependency checks to ensure proper materialization.
  - In the case of materilizing via individual assets:
    - Only the `citibike_ingestion_duckdb_bigquery` asset can be materialized on its own.
    - If both the `citibike_ingestion_duckdb_bigquery` asset and the `default` asset group (for dbt transformation) are selected to be materialized in the same run:
      - There is no guarantee that the ingestion will complete before the dbt data transformations are done.
      - Use the `citibike_elt` job instead for a full, ordered ELT process.

## Assets
- There are 3 assets in project.
- Each (except citibike_mock_ingestion) is meant to drive their respective ELT stages using their respective ELT projects with minimal configuration.
- The reason for this design is to maintain separation of logic between ELT steps and the automation (Dagster).
- This allows the intended operators of ELT projects (e.g. data scientists) and Dagster (data engineers) to work independently without interfering with each other.

### citibike_ingestion_duckdb_bigquery
- Automates the ingestion done at [citibike-ingestion](../citibike-ingestion).
- Defined at:
  - dagster_citibike/dagster_citibike/assets/[meltano_assets.py](dagster_citibike/assets/meltano_assets.py)

### citibike_dbt_elt
- Automates all the dbt steps done at [citibike_dbt](../citibike_dbt).
- Will run only if there has been a new ingestion.
  - A mock ingestion can be used to trigger the dbt run without a real ingestion.
- The selection of real or mock ingestion is made via resources.JobConfig during Job creation in [definitions.py](../dagster_citibike/dagster_citibike/definitions.py).
- Checks for a new ingestion for 5 minutes.
  - If none is found, this asset will terminate and dbt will not run.
- Defined at:
  - dagster_citibike/dagster_citibike/assets/[dbt_assets.py
](dagster_citibike/assets/dbt_assets.py)

### citibike_mock_ingestion
- A mock ingestion asset to trigger dbt run (downstream) without a real ingestion.
- The mock ingestion does nothing but sets some metadata so that the subsequent dbt asset in the same run thinks that an ingestion has occurred. 
- Defined at:
  - dagster_citibike/dagster_citibike/assets/[dbt_assets.py
](dagster_citibike/assets/dbt_assets.py)


## Jobs
- There are 2 jobs in this project.

### citibike_elt
- This runs the full Citibike ELT with Meltano ingestion and dbt transformations.
  - The dbt transformations are ordered to occur only after ingestion has succeeded.
- It uses the following assets:
  - `citibike_ingestion_duckdb_bigquery`
  - `citibike_dbt_elt`
- Defined at:
  - dagster_citibike/dagster_citibike/[definitions.py](../dagster_citibike/dagster_citibike/definitions.py)

### dbt_only
- This runs only the dbt transformations of the Citibike ELT.
- It achieves this by running a mock ingestion before the dbt transformations.
- It uses the following assets:
  - `citibike_mock_ingestion`
  - `citibike_dbt_elt`
- Defined at:
  - dagster_citibike/dagster_citibike/[definitions.py](../dagster_citibike/dagster_citibike/definitions.py)


## Potential issues
- If running any of the assets result in some configuration errors:
  - Try to run the specific ELT process manually via their own projects.
    - If this also results in an error:
      - Then it could be:
        - The ELT project requires some configuration to be set up.
        - Some general error, e.g. conda environment not activated, .env not properly loaded, etc.
        - The ELT project needs to be debugged.
      - After manual run succeeds, try running this asset again.
    - If fine, try running the assets again.
      - If error persists, it could be that this asset needs to be debugged.
- If some project paths or parameters could not be read:
  - Check that the `.env` file was correctly populated and loaded.
    - Paths must be absolute paths.
  - Dagster commands must be executed on the same VS Code terminal that activated conda environment and loaded `.env` parameters.
