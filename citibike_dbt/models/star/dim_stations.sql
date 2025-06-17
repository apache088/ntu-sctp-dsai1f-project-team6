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