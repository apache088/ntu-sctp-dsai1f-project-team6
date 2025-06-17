{{ config(materialized='table') }}

SELECT
  price_plan_id,
  membership_type,
  bike_type,
  unlock_fee,
  per_minute_pricing,
  included_mins,
  valid_from,
  valid_to
FROM {{ ref('price_plans') }}
