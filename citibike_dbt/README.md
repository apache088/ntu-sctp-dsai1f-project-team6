# Citibike Trip Data Transformation

## Feature Engineering

Synopsis: This section explains how new features were created or selected to improve model performance.  

| S/N | Table | New Feature(s) | Implementation Logic | Key Benefit(s)
| --- | ----- | -------------- | -------------------- | ---------------------
| 1 | `fact_trip` | `duration_mins` | Computing difference between start and end times | Key metric used for analysis; no additional computation is required during analysis
| 2 | `fact_trip` | `distance_metres` | Using BigQuery’s functions (`ST_DISTANCE`, `ST_GEOPOINT`) | Can be used to estimate the trip distance
| 3 | `fact_trip` | `price_paid` | Referencing `price_plans` seed table to compute price paid per trip | Key metric to determine revenue impact by stations; no additional computation is required during analysis
| 4 | `dim_stations` | Every station as an unique record | Using CTE to combine all start and end stations into a temp table and group them by four columns to uniquely identify every station | Normalised data facilitates analysis at per station level
| 5 | `dim_stations` | `total_starts`, `total_ends` | Using a temp column to store roles of every station and counting how many times each station is used as the start station for trips, likewise for end station | Useful indicators to quickly identify most used or least used stations

## Model Development

Synopsis: This section documents the models built, algorithms used, and rationale for their selection.  

There are four models built (excluding the `price_plans` seed table which contains static/reference data): *`fact_trips`, `dim_stations`, `dim_membership_types`, `dim_bike_types`*.

All models are built based on the source dataset, with new features added as per described in the preceding section. Full implementation logic is shown in the following code snippets.  

As the source dataset does have incomplete data, several implementation techniques are applied to mitigate errors during execution of the data pipeline.

\
Defensive coding (applicable to all tables)  
- Explicit casting to mitigate inference differences between `dbt` and BigQuery  
- Using `COALESCE` function to mitigate errors due to missing/null values  
- Using common environment variables by implementing `python-dotenv`  

\
Data quality (applicable to `dim_stations` table)  
- Generating primary key based on four columns to mitigate incomplete source data which can give rise to downstream discrepancies (e.g., distance computation with null or zero results)  

\
*SQL code snippet for `fact_trips` table*
```sql
SELECT
    CAST(ride_id AS STRING) AS trip_id,
    CAST(started_at AS TIMESTAMP) AS started_at,
    CAST(ended_at AS TIMESTAMP) AS ended_at,
    CAST(TIMESTAMP_DIFF(CAST(ended_at AS TIMESTAMP), CAST(started_at AS TIMESTAMP), MINUTE) AS INT64) AS duration_mins,
    CAST(start_stations.station_key AS STRING) AS start_station_key,
    CAST(end_stations.station_key AS STRING) AS end_station_key,
    CAST(
        ST_DISTANCE(
            ST_GEOGPOINT(start_stations.longitude, start_stations.latitude),
            ST_GEOGPOINT(end_stations.longitude, end_stations.latitude),
            TRUE
        ) AS INT64
    ) AS distance_metres,
    CAST(membership_types.membership_type_id AS STRING) AS membership_type_id,
    CAST(bike_types.bike_type_id AS STRING) AS bike_type_id,
    CAST(price_plans.price_plan_id AS INT64) AS price_plan_id,
    CAST(
        ROUND(
            COALESCE(price_plans.unlock_fee, 0) +
            COALESCE(
                CASE
                    WHEN CAST(TIMESTAMP_DIFF(CAST(ended_at AS TIMESTAMP), CAST(started_at AS TIMESTAMP), MINUTE) AS INT64) > COALESCE(price_plans.included_mins, 0)
                    THEN (CAST(TIMESTAMP_DIFF(CAST(ended_at AS TIMESTAMP), CAST(started_at AS TIMESTAMP), MINUTE) AS INT64) - COALESCE(price_plans.included_mins, 0)) * COALESCE(price_plans.per_minute_pricing, 0)
                    ELSE 0
                END,
                0
            ),
        2
        ) AS FLOAT64
    ) AS price_paid
FROM
    {{ source(env_var('BIGQUERY_SOURCE_DATASET'), env_var('BIGQUERY_RAW_DATA_TABLE')) }} source_data
INNER JOIN {{ ref('dim_stations') }} start_stations
    ON COALESCE(source_data.start_station_id, '') = COALESCE(start_stations.station_id, '')
    AND COALESCE(source_data.start_station_name, '') = COALESCE(start_stations.station_name, '')
    AND COALESCE(CAST(source_data.start_lat AS FLOAT64), 0.0) = COALESCE(CAST(start_stations.latitude AS FLOAT64), 0.0)
    AND COALESCE(CAST(source_data.start_lng AS FLOAT64), 0.0) = COALESCE(CAST(start_stations.longitude AS FLOAT64), 0.0)
INNER JOIN {{ ref('dim_stations') }} end_stations
    ON COALESCE(source_data.end_station_id, '') = COALESCE(end_stations.station_id, '')
    AND COALESCE(source_data.end_station_name, '') = COALESCE(end_stations.station_name, '')
    AND COALESCE(CAST(source_data.end_lat AS FLOAT64), 0.0) = COALESCE(CAST(end_stations.latitude AS FLOAT64), 0.0)
    AND COALESCE(CAST(source_data.end_lng AS FLOAT64), 0.0) = COALESCE(CAST(end_stations.longitude AS FLOAT64), 0.0)
INNER JOIN {{ ref('dim_membership_types') }} membership_types
    ON COALESCE(source_data.member_casual, '') = COALESCE(membership_types.type, '')
INNER JOIN {{ ref('dim_bike_types') }} bike_types
    ON COALESCE(source_data.rideable_type, '') = COALESCE(bike_types.type, '')
INNER JOIN {{ ref('price_plans') }} price_plans
    ON COALESCE(source_data.member_casual, '') = COALESCE(price_plans.membership_type, '')
    AND COALESCE(source_data.rideable_type, '') = COALESCE(price_plans.bike_type, '')
    AND DATE(CAST(source_data.started_at AS TIMESTAMP)) BETWEEN price_plans.valid_from AND price_plans.valid_to
```

\
*SQL code snippet for `dim_stations` table*
```sql
WITH stations AS (
    SELECT
        station_id,
        station_name,
        latitude,
        longitude,
        SUM(CASE WHEN station_role = 'start' THEN 1 ELSE 0 END) AS total_starts,
        SUM(CASE WHEN station_role = 'end' THEN 1 ELSE 0 END) AS total_ends
    FROM (
        SELECT
            start_station_id AS station_id,
            start_station_name AS station_name,
            start_lat AS latitude,
            start_lng AS longitude,
            'start' AS station_role
        FROM {{ source(env_var('BIGQUERY_SOURCE_DATASET'), env_var('BIGQUERY_RAW_DATA_TABLE')) }}
        UNION ALL
        SELECT
            end_station_id AS station_id,
            end_station_name AS station_name,
            end_lat AS latitude,
            end_lng AS longitude,
            'end' AS station_role
        FROM {{ source(env_var('BIGQUERY_SOURCE_DATASET'), env_var('BIGQUERY_RAW_DATA_TABLE')) }}
    ) t
    GROUP BY station_id, station_name, latitude, longitude
)
SELECT 
    {{ dbt_utils.generate_surrogate_key(['station_id', 'station_name', 'latitude', 'longitude']) }} station_key,
    CAST(station_id AS STRING) AS station_id,
    CAST(station_name AS STRING) AS station_name,
    CAST(latitude AS FLOAT64) AS latitude,
    CAST(longitude AS FLOAT64) AS longitude,
    CAST(total_starts AS INT64) AS total_starts,
    CAST(total_ends AS INT64) AS total_ends
FROM
    stations
```

\
*SQL code snippet for `dim_membership_types` table*
```sql
SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['member_casual']) }} AS membership_type_id,
    CAST(member_casual AS STRING) AS type
FROM
   {{ source(env_var('BIGQUERY_SOURCE_DATASET'), env_var('BIGQUERY_RAW_DATA_TABLE')) }}
```

\
*SQL code snippet for `dim_bike_types` table*
```sql
SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['rideable_type']) }} AS bike_type_id,
    CAST(rideable_type AS STRING) AS type
FROM
    {{ source(env_var('BIGQUERY_SOURCE_DATASET'), env_var('BIGQUERY_RAW_DATA_TABLE')) }}
```

## Model Evaluation & Results

Synopsis: This section presents validation methods and key results.  

Test functions provided by `dbt` and `dbt_expectations` are used to validate the data generated by the models. The following table summarises the functions used and associated test results. Total number of executed tests is 65.

| S/N | Table | Column(s) | Test Function(s) | Test Count | Test Result
| --- | ----- | --------- | -------------- | -------------------- | ---------------------
| 1 | `fact_trips` | All columns | `dbt_expectations.expect_column_values_to_be_of_type` | 11 | Passed
| 2 | `fact_trips` | `trip_id` | `dbt` `unique`, `dbt` `not_null` | 2 | Passed
| 3 | `fact_trips` | `ended_at`, `started_at` | `dbt_expectations.expect_column_pair_values_A_to_be_greater_than_B` | 1 | Passed
| 4 | `fact_trips` | `duration_mins` | `dbt_expectations.expect_column_values_to_be_between`, `min_value: 0`, `strictly: true` | 1 | Passed
| 5 | `fact_trips` | `price_paid` | `dbt_expectations.expect_column_values_to_be_between`, `min_value: 0`, `strictly: false` | 1 | Passed
| 6 | `fact_trips` | `start_station_key` | `dbt` `relationships` with `dim_stations.station_key` | 1 | Passed
| 7 | `fact_trips` | `end_station_key` | `dbt` `relationships` with `dim_stations.station_key` | 1 | Passed
| 8 | `fact_trips` | `membership_type_id` | `dbt` `relationships` with `dim_membership_types.membership_type_id` | 1 | Passed
| 9 | `fact_trips` | `bike_type_id` | `dbt` `relationships` with `dim_bike_types.bike_type_id` | 1 | Passed
| 10 | `fact_trips` | `price_plan_id` | `dbt` `relationships` with `price_plans.price_plan_id` | 1 | Passed
| 11 | `dim_stations` | All columns | `dbt_expectations.expect_column_values_to_be_of_type` | 7 | Passed
| 12 | `dim_stations` | `station_key` | `dbt` `unique`, `dbt` `not_null` | 2 | Passed
| 13 | `dim_stations` | `total_starts` | `dbt_expectations.expect_column_values_to_be_between`, `min_value: 0`, `strictly: false` | 1 | Passed
| 14 | `dim_stations` | `total_ends` | `dbt_expectations.expect_column_values_to_be_between`, `min_value: 0`, `strictly: false` | 1 | Passed
| 15 | `dim_membership_types` | All columns | `dbt_expectations.expect_column_values_to_be_of_type` | 2 | Passed
| 16 | `dim_membership_types` | `membership_type_id` | `dbt` `unique`, `dbt` `not_null` | 2 | Passed
| 17 | `dim_membership_types` | `type` | `dbt_expectations.expect_column_values_to_be_in_set`, `value_set: ['casual', 'member']` | 1 | Passed
| 18 | `dim_bike_types` | All columns | `dbt_expectations.expect_column_values_to_be_of_type` | 2 | Passed
| 19 | `dim_bike_types` | `bike_type_id` | `dbt` `unique`, `dbt` `not_null` | 2 | Passed
| 20 | `dim_bike_types` | `type` | `dbt_expectations.expect_column_values_to_be_in_set`, `value_set: ['classic_bike', 'electric_bike']` | 1 | Passed
| 21 | `price_plans` | All columns | `dbt_expectations.expect_column_values_to_be_of_type` | 8 | Passed
| 22 | `price_plans` | All columns | `dbt` `not_null` | 8 | Passed
| 23 | `price_plans` | `price_plan_id` | `dbt` `unique` | 1 | Passed
| 24 | `price_plans` | `valid_to`, `valid_from` | `dbt_expectations.expect_column_pair_values_A_to_be_greater_than_B` | 1 | Passed
| 25 | `price_plans` | `membership_type` | `dbt_expectations.expect_column_values_to_be_in_set`, `value_set: ['casual', 'member']` | 1 | Passed
| 26 | `price_plans` | `bike_type` | `dbt_expectations.expect_column_values_to_be_in_set`, `value_set: ['classic_bike', 'electric_bike']` | 1 | Passed
| 27 | `price_plans` | `unlock_fee` | `dbt_expectations.expect_column_values_to_be_between`, `min_value: 0`, `strictly: false` | 1 | Passed
| 28 | `price_plans` | `per_minute_pricing` | `dbt_expectations.expect_column_values_to_be_between`, `min_value: 0`, `strictly: false` | 1 | Passed
| 29 | `price_plans` | `included_mins` | `dbt_expectations.expect_column_values_to_be_between`, `min_value: 0`, `strictly: false` | 1 | Passed