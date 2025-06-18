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
    {{ source('citibike_ingestion', 'main_citibike_tripdata') }} source_data
INNER JOIN {{ ref('dim_stations') }} start_stations
    ON COALESCE(source_data.start_station_id, '') = COALESCE(start_stations.station_id, '')
    AND COALESCE(source_data.start_station_name, '') = COALESCE(start_stations.station_name, '')
    AND COALESCE(CAST(source_data.start_lat AS FLOAT64), 0) = COALESCE(start_stations.latitude, 0)
    AND COALESCE(CAST(source_data.start_lng AS FLOAT64), 0) = COALESCE(start_stations.longitude, 0)
INNER JOIN {{ ref('dim_stations') }} end_stations
    ON COALESCE(source_data.end_station_id, '') = COALESCE(end_stations.station_id, '')
    AND COALESCE(source_data.end_station_name, '') = COALESCE(end_stations.station_name, '')
    AND COALESCE(CAST(source_data.end_lat AS FLOAT64), 0) = COALESCE(end_stations.latitude, 0)
    AND COALESCE(CAST(source_data.end_lng AS FLOAT64), 0) = COALESCE(end_stations.longitude, 0)
INNER JOIN {{ ref('dim_membership_types') }} membership_types
    ON COALESCE(source_data.member_casual, '') = COALESCE(membership_types.type, '')
INNER JOIN {{ ref('dim_bike_types') }} bike_types
    ON COALESCE(source_data.rideable_type, '') = COALESCE(bike_types.type, '')
INNER JOIN {{ ref('price_plans') }} price_plans
    ON COALESCE(source_data.member_casual, '') = COALESCE(price_plans.membership_type, '')
    AND COALESCE(source_data.rideable_type, '') = COALESCE(price_plans.bike_type, '')
    AND DATE(CAST(source_data.started_at AS TIMESTAMP)) BETWEEN price_plans.valid_from AND price_plans.valid_to