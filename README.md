# Citibike Trip Data Analysis: Identifying Failed Rides & Revenue Impact

## Project Overview
This data pipeline analyzes Jersey City's Citibike trip data (sourced from [Citibike's official tripdata](https://s3.amazonaws.com/tripdata/index.html)) to identify operational trends and quantify their financial impact. The project focuses on revenue affecting analysis such as usage trends, station popularity, and inferred **bike failure rates** - from trips where users likely encountered technical issues (evidenced by identical start/end stations with abnormally short durations).

## Usage
- To use this project, please follow the steps detailed in the [Technical Architecture](#technical-architecture) section.
- Additional materials for this project can be found at the [documents](./documents) directory.

## Technical Architecture

<img src="https://github.com/user-attachments/assets/f86ed486-b8c7-429c-a93b-fd89655e572e" width="75%" />


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
- **[Analysis](./Analysis/README.md)**
  - Analyse Usage Trends throughout the Day
     - Avg Trip Count per Day in 15 mins intervals, seperated by weekdays and weekends
  - Revenue Insights
     - Look into the Revenue and Trip Count Composition by Membership and Bike Type
  - Start and End Station Popularity
     - Look into heat maps of popular bike stations based on latitude, longitude, station names, and total count of start and end times
  - Anomaly Detection
     - Detect outliers based on duration_minutes and distance_metres

- **Further actions for business consideration**
   - Introduce Time-Based Pricing
      - Implement dynamic pricing (e.g., slightly higher fares during peak hours for casual users)
   - Time-Based Bike Redistribution
      - Ensure sufficient bike availability at key stations before peak commute hours on weekdays
   - Identify operational issues costing revenue.
   - Identify problematic stations needing further investigation.
   - Improve customer experience by reducing failed rides.
   - Optimize bike redistribution strategies.
