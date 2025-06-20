{{ config(materialized='table') }}

-- 1. Grab every station_id seen in trips (start OR end)
with station_ids as (
  select distinct start_station_id as station_id
  from {{ source('citibike','trips') }}
  where start_station_id is not null

  union distinct

  select distinct end_station_id
  from {{ source('citibike','trips') }}
  where end_station_id is not null
),

-- 2. Bring in coords & names if you have them
coords as (
  select
    station_id,
    latitude,
    longitude,
    station_name
  from {{ ref('stg_station_coords') }}
),

-- 3. Bring in city metadata if you have it
meta as (
  select
    station_id,
    city
  from {{ ref('stg_station_cities') }}
),

-- 4. Count trips starting at each station
summary_start as (
  select
    start_station_id   as station_id,
    count(*)           as total_starts
  from {{ source('citibike','trips') }}
  group by start_station_id
),

-- 5. Count trips ending at each station
summary_end as (
  select
    end_station_id     as station_id,
    count(*)           as total_ends
  from {{ source('citibike','trips') }}
  group by end_station_id
)

-- 6. Assemble everything
select
  -- you can key off just station_id if you like,
  -- or continue using lat/long for your surrogate key
  {{ dbt_utils.generate_surrogate_key([
       'station_ids.station_id',
       'coords.latitude',
       'coords.longitude'
     ]) }} as station_key,

  station_ids.station_id,
  coords.station_name,
  meta.city,
  coords.latitude,
  coords.longitude,

  coalesce(summary_start.total_starts, 0) as total_starts,
  coalesce(summary_end.total_ends,   0) as total_ends

from station_ids

left join coords
  on station_ids.station_id = coords.station_id

left join meta
  on station_ids.station_id = meta.station_id

left join summary_start
  on station_ids.station_id = summary_start.station_id

left join summary_end
  on station_ids.station_id = summary_end.station_id
