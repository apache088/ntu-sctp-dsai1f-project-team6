{{ config(materialized='table') }}

with trips_main as (
    select
        ride_id as trip_id,
        started_at,
        ended_at,
        timestamp_diff(ended_at, started_at, minute) as duration_mins,
        start_station_id,
        end_station_id,
        member_casual as membership_type,
        rideable_type as bike_type
    from {{ source('citibike', 'trips') }}
),

plans as (
    select * from {{ ref('dim_price_plans') }}
),

trips_pricing as (
    select
        t.*,
        p.price_plan_id,
        p.unlock_fee,
        p.per_minute_pricing,
        p.included_mins
    from trips_main t
    join plans p
      on t.membership_type = p.membership_type
     and t.bike_type = p.bike_type
)

select
    trip_id,
    started_at,
    ended_at,
    duration_mins,
    start_station_id,
    end_station_id,
    price_plan_id,
    unlock_fee,
    per_minute_pricing,
    included_mins,
    (unlock_fee + greatest(duration_mins - included_mins, 0) * per_minute_pricing) as price_paid
from trips_pricing
where start_station_id is not null
  and end_station_id is not null
