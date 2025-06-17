{% snapshot fact_trips_snapshot %}
{{ 
  config(
    target_schema='snapshots',
    unique_key='trip_id',
    strategy='check',
    check_cols=[
      'distance_m',
      'price_paid',
      'start_lat',
      'start_lng',
      'end_lat',
      'end_lng'
    ]
  ) 
}}

SELECT * FROM {{ ref('fact_trips') }}

{% endsnapshot %}
