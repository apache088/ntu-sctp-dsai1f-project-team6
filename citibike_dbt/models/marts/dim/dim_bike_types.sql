{{ config(materialized='table') }}

SELECT
  {{ dbt_utils.generate_surrogate_key(['rideable_type']) }} AS bike_type_id,
  rideable_type AS type
FROM {{ source('citibike', 'trips') }}
GROUP BY rideable_type
