{{ config(materialized='table') }}

with starts as (
    select distinct
        start_station_id as station_id,
        start_lat as latitude,
        start_lng as longitude
    from {{ source('citibike', 'trips') }}
    where start_station_id is not null
),
ends as (
    select distinct
        end_station_id as station_id,
        end_lat as latitude,
        end_lng as longitude
    from {{ source('citibike', 'trips') }}
    where end_station_id is not null
),
all_coords as (
    select * from starts
    union distinct
    select * from ends
)
select
    station_id,
    avg(latitude) as latitude,
    avg(longitude) as longitude
from all_coords
group by station_id
