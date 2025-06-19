
-- Cast variables as their respective data types

with raw as (
    select
        cast(ride_id as STRING)             as trip_id,
        cast(rideable_type as STRING)       as bike_types,
        cast(member_casual as STRING)       as user_type,
        cast(started_at as timestamp)       as started_at,
        cast(ended_at as timestamp)         as ended_at,
        cast(start_station_name as STRING)  as start_station_name,
        cast(end_station_name as STRING)    as end_station_name,
        cast(start_station_id as STRING)    as start_station_id,
        cast(end_station_id as STRING)      as end_station_id,
        cast(start_lat as FLOAT64)          as start_lat,
        cast(start_lng as FLOAT64)          as start_lng,
        cast(end_lat as FLOAT64)            as end_lat,
        cast(end_lng as FLOAT64)            as end_lng,
        _sdc_received_at,
        _sdc_extracted_at,
        _sdc_deleted_at,
        _sdc_batched_at,
        _sdc_table_version,
        _sdc_sequence
from {{ source('citibike', 'main_citibike_tripdata') }}

-- Simple calculations to be used
select
*,
cast(timestamp_diff(ended_at, started_at, MINUTE) as INT64) as duration_mins
from raw