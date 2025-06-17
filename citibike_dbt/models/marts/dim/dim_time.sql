{{ config(materialized='table') }}

with raw_dates as (
    select distinct
        cast(started_at as date) as event_date
    from {{ source('citibike', 'trips') }}
)

select
    row_number() over (order by event_date) as time_sk,
    event_date,
    extract(year from event_date) as year,
    extract(month from event_date) as month,
    extract(day from event_date) as day,
    format_date('%A', event_date) as day_of_week,
    format_date('%B', event_date) as month_name
from raw_dates
