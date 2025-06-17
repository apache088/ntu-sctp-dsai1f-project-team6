{{ config(materialized='table') }}

WITH starts AS (
    SELECT DISTINCT
        start_station_id AS station_id,
        start_lat AS latitude,
        start_lng AS longitude,
        start_station_name AS station_name
    FROM {{ source('citibike', 'trips') }}
    WHERE start_station_id IS NOT NULL
      AND start_lat IS NOT NULL
      AND start_lng IS NOT NULL
),

ends AS (
    SELECT DISTINCT
        end_station_id AS station_id,
        end_lat AS latitude,
        end_lng AS longitude,
        end_station_name AS station_name
    FROM {{ source('citibike', 'trips') }}
    WHERE end_station_id IS NOT NULL
      AND end_lat IS NOT NULL
      AND end_lng IS NOT NULL
),

all_coords AS (
    SELECT * FROM starts
    UNION DISTINCT
    SELECT * FROM ends
)

SELECT
    station_id,
    AVG(latitude) AS latitude,
    AVG(longitude) AS longitude,
    MIN(station_name) AS station_name  -- taking the most consistent name
FROM all_coords
GROUP BY station_id
