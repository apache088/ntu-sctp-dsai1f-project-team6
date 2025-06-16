{{ config(materialized='table') }}

with raw as (
  select distinct rideable_type as bike_type
  from {{ source('citibike','trips') }}
  where rideable_type is not null
)

select
  {{ dbt_utils.generate_surrogate_key(['bike_type']) }} as bike_type_id,
  bike_type as type
from raw
