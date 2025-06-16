{{ config(materialized='table') }}

select
  price_plan_id,
  membership_type,
  bike_type,
  unlock_fee,
  per_minute_pricing,
  included_mins
from {{ ref('price_plans') }}
