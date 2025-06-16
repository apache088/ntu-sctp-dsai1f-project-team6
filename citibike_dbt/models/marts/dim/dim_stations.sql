{{ config(materialized='table') }}

with coords as (
    select * from {{ ref('stg_station_coords') }}
),
meta as (
    select distinct station_id, city
    from {{ ref('station_cities') }}  -- your station city source or model
)
select
    {{ dbt_utils.generate_surrogate_key(['m.station_id', 'c.latitude', 'c.longitude']) }} as station_key,
    m.station_id,
    m.city,
    c.latitude,
    c.longitude
from meta m
join coords c using (station_id)
