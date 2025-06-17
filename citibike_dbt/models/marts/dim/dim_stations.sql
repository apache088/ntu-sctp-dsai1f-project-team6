{{ config(materialized='table') }}

with coords as (
    select
        station_id,
        latitude,
        longitude,
        station_name
    from {{ ref('stg_station_coords') }}
),
meta as (
    select
        station_id,
        city
    from {{ ref('stg_station_cities') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['coords.station_id', 'coords.latitude', 'coords.longitude']) }} as station_key,
    coords.station_id,
    coords.station_name,
    meta.city,
    coords.latitude,
    coords.longitude
from coords
inner join meta
    on coords.station_id = meta.station_id
