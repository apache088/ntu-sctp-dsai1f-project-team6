{{ config(materialized='table') }}

with raw as (
  select distinct member_casual as membership_type
  from {{ source('citibike','trips') }}
  where member_casual is not null
)

select
  {{ dbt_utils.generate_surrogate_key(['membership_type']) }} as membership_type_id,
  membership_type as type
from raw
