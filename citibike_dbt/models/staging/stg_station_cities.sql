{{ config(materialized='table') }}

select distinct
    start_station_id as station_id,
    case
        when start_station_id like 'HB%' then 'Hoboken'
        when start_station_id like 'JC%' then 'Jersey City'
        when start_station_id like 'NY%' then 'New York'
        else 'Unknown'
    end as city
from {{ source('citibike', 'trips') }}
where start_station_id is not null
