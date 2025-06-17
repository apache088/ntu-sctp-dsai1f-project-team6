{{ config(materialized='table') }}

SELECT
  {{ dbt_utils.generate_surrogate_key(['member_casual']) }} AS membership_type_id,
  member_casual AS type
FROM {{ source('citibike', 'trips') }}
GROUP BY member_casual
