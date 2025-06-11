-- models/staging/stg_bike_trips.sql
WITH dedup_source_data AS (
  SELECT *
  FROM (
    SELECT
      ride_id,
      rideable_type,
      -- Cast to TIMESTAMP
      TIMESTAMP(started_at) AS started_at,
      TIMESTAMP(ended_at) AS ended_at,
      start_station_name,
      start_station_id,
      end_station_name,
      end_station_id,
      -- Cast to FLOAT64 for Haversine math
      CAST(start_lat AS FLOAT64) AS start_lat,
      CAST(start_lng AS FLOAT64) AS start_lng,
      CAST(end_lat AS FLOAT64) AS end_lat,
      CAST(end_lng AS FLOAT64) AS end_lng,
      member_casual,
      ROW_NUMBER() OVER (PARTITION BY ride_id ORDER BY _sdc_received_at DESC) AS row_num
    FROM {{ source('citibike_trip', 'main_raw_citibike_trip') }}
  )
  WHERE row_num = 1
)

SELECT
  ride_id,
  rideable_type,
  started_at,
  ended_at,
  start_station_name,
  start_station_id,
  end_station_name,
  end_station_id,
  start_lat,
  start_lng,
  end_lat,
  end_lng,
  member_casual,
  
-- Haversine formula to calculate distance in meters
-- Earth radius in meters: 6371000
  -- Haversine distance in meters
  6371000 * 2 * ASIN(
    SQRT(
      POWER(SIN(((end_lat - start_lat) * 3.141592653589793 / 180) / 2), 2) +
      COS(start_lat * 3.141592653589793 / 180) * COS(end_lat * 3.141592653589793 / 180) *
      POWER(SIN(((end_lng - start_lng) * 3.141592653589793 / 180) / 2), 2)
    )
  ) AS distance_meters,
  
-- Calculate duration in seconds
TIMESTAMP_DIFF(ended_at, started_at, SECOND) AS duration_seconds,
  
  -- Add metadata columns
  CURRENT_TIMESTAMP AS dbt_loaded_at
FROM dedup_source_data