{% snapshot station_coords_snapshot %}
{{
    config(
      target_schema='citibike',
      unique_key='station_id',
      strategy='check',
      check_cols=['latitude', 'longitude']
    )
}}

select
    station_id,
    latitude,
    longitude
from {{ ref('stg_station_coords') }}

{% endsnapshot %}
