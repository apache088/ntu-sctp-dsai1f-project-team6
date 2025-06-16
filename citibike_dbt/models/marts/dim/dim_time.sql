{{ config(materialized='table') }}

with raw as (
  select distinct
    date(started_at)                  as event_date,
    extract(year  from started_at)    as year,
    extract(month from started_at)    as month,
    extract(day   from started_at)    as day,
    extract(hour  from started_at)    as hour,
    extract(minute from started_at)   as minute
  from {{ source('citibike','trips') }}
)

select
  {{ dbt_utils.generate_surrogate_key(
       ['event_date','year','month','day','hour','minute']
     ) }}                         as time_sk,
  event_date,
  year,
  month,
  day,
  hour,
  minute
from raw
