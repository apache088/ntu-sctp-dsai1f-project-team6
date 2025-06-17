{{ config(materialized='table') }}

SELECT
  source_data.ride_id AS trip_id,
  source_data.started_at,
  source_data.ended_at,
  TIMESTAMP_DIFF(source_data.ended_at, source_data.started_at, MINUTE) AS duration_mins,

  -- Foreign keys
  start_stations.station_key AS start_station_key,
  end_stations.station_key AS end_station_key,
  membership_types.membership_type_id,
  bike_types.bike_type_id,
  price_plans.price_plan_id,

  -- Coordinates
  start_stations.latitude AS start_lat,
  start_stations.longitude AS start_lng,
  end_stations.latitude AS end_lat,
  end_stations.longitude AS end_lng,

  -- Distance in meters using Haversine formula
  6371000 * 2 * ASIN(SQRT(
    POWER(SIN((end_stations.latitude - start_stations.latitude) * (ACOS(-1) / 180) / 2), 2) +
    COS(start_stations.latitude * (ACOS(-1) / 180)) *
    COS(end_stations.latitude * (ACOS(-1) / 180)) *
    POWER(SIN((end_stations.longitude - start_stations.longitude) * (ACOS(-1) / 180) / 2), 2)
  )) AS distance_m,

  -- Fare paid calculation
  ROUND(
    COALESCE(price_plans.unlock_fee, 0) +
    GREATEST(TIMESTAMP_DIFF(source_data.ended_at, source_data.started_at, MINUTE) - COALESCE(price_plans.included_mins, 0), 0)
    * COALESCE(price_plans.per_minute_pricing, 0),
    2
  ) AS price_paid

FROM {{ source('citibike', 'trips') }} AS source_data

-- Join start station
INNER JOIN {{ ref('dim_stations') }} AS start_stations
  ON source_data.start_station_id = start_stations.station_id
  AND source_data.start_station_name = start_stations.station_name

-- Join end station
INNER JOIN {{ ref('dim_stations') }} AS end_stations
  ON source_data.end_station_id = end_stations.station_id
  AND source_data.end_station_name = end_stations.station_name

-- Join membership type
INNER JOIN {{ ref('dim_membership_types') }} AS membership_types
  ON source_data.member_casual = membership_types.type

-- Join bike type
INNER JOIN {{ ref('dim_bike_types') }} AS bike_types
  ON source_data.rideable_type = bike_types.type

-- Join price plan
INNER JOIN {{ ref('dim_price_plans') }} AS price_plans
  ON source_data.member_casual = price_plans.membership_type
  AND source_data.rideable_type = price_plans.bike_type
  AND DATE(source_data.started_at) BETWEEN price_plans.valid_from AND price_plans.valid_to

-- Filter out incomplete trip records
WHERE
  source_data.start_station_id IS NOT NULL
  AND source_data.end_station_id IS NOT NULL
  AND start_stations.latitude IS NOT NULL
  AND start_stations.longitude IS NOT NULL
  AND end_stations.latitude IS NOT NULL
  AND end_stations.longitude IS NOT NULL
