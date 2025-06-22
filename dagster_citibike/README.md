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
  - First materialize the `citibike_meltano` asset
    - This must complete before dbt transformation can be done. 
  - Materialize the `default` asset group for dbt transformation.

## Assets
- There are 2 assets in project.
- Each is meant to drive their respective ELT stages using their respective ELT projects with minimal configuration.
- The reason for this design is to maintain separation of logic between ELT steps and the automation (Dagster).
- This allows the intended operators of ELT projects (e.g. data scientists) and Dagster (data engineers) to work independently without interfering with each other.

### citibike_ingestion_duckdb_bigquery
- Automates the ingestion done at [citibike-ingestion](../citibike-ingestion).
- Defined at:
  - dagster_citibike/dagster_citibike/assets/[meltano_assets.py](dagster_citibike/assets/meltano_assets.py)

### citibike_dbt
- Automates all the dbt steps done at [citibike_dbt](../citibike_dbt).
- If there are new material to ingest, ensure that `citibike_ingestion_duckdb_bigquery` completes before running this.
- Defined at:
  - dagster_citibike/dagster_citibike/assets/[dbt_assets.py
](dagster_citibike/assets/dbt_assets.py
)

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
