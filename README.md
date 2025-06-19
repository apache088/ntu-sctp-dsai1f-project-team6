# Citibike Trip Data Analysis: Identifying Failed Rides & Revenue Impact

## Project Overview
This data pipeline analyzes Jersey City's Citibike trip data (sourced from [Citibike's official tripdata](https://s3.amazonaws.com/tripdata/index.html)) to identify operational inefficiencies and quantify their financial impact. The project focuses on detecting **failed rides** - trips where users likely encountered technical issues (evidenced by identical start/end stations with abnormally short durations) - and calculates their effect on business revenue.

## Technical Architecture
The solution implements a Extract Load Transform (**ELT**) data stack:

1. **[Ingestion & Storage](./citibike-ingestion/README.md)**
   - Raw CSV tripdata loaded into DuckDB for initial processing
   - Meltano extracts from DuckDB for loading to BigQuery

1. **[Transformation](./citibike_dbt/README.md)**
   - dbt models structure the data into a Star Schema:
     - 1 fact table (`fact_trips`)
     - 4 dimension tables (`dim_stations`, `dim_bike_types`, `dim_membership_types`, `price_plans`)

1. **[Orchestration](./dagster_citibike/README.md)**
   - Dagster connects and automates ELT pipeline:
     - Triggers Meltano extracts/loads
     - Triggers dbt transformations

## Business Value
- **Analysis**
  - Failed ride detection algorithm (same-station trips < threshold duration)
  - Missed revenue calculations
- **Further actions for business consideration**
   - Identify operational issues costing revenue.
   - Identify problematic stations needing further investigation.
   - Improve customer experience by reducing failed rides.
   - Optimize bike redistribution strategies.
