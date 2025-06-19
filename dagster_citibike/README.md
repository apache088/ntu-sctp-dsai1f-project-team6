# Citibike Trip Data ELT Orchestration

## Overview
This is a [Dagster](https://dagster.io/) project that automates the running of:
- Meltano ingestion
  - Extraction from DuckDB database.
  - Uploading data to Google BigQuery as a table.
  - Implementation:
    - Uses a Python subprocess to run a meltano command.
- dbt transformation
  - Performs all the data transformation steps configured in dbt project.
  - Implementation:
    - Uses dbt CLI to run dbt build.

## Instructions for running this Dagster project
- Prerequisites:
  - If `.env` at project root has not yet been created:
    - Create a `.env` file at project root.
    - Use the `env.txt` there as a template.
    - Fill in all the paths with absolute paths.
    - You may also edit the dataset and table names as required.
  - Create the conda environment required from this project using the provided `environment.yml` at project root:
    - `conda env create -f environment`
- Start VS Code
  - Do **all** the following CLI commands in the same **VS Code CLI**.
  - Start at the root directory of this project.
- Activate Conda environment:
  - `conda activate dsai_project`
- Load parameters from .env file:
  - `python load_env.py`
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
