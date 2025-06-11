{% snapshot snapshot_dim_venue %}
{{
    config(
        target_schema='snapshots',
        unique_key="venue || '-' || venue_country",
        strategy='check',
        check_cols='all'
    )
}}

select distinct
    venue,
    venue_country
from {{ ref('stg_world_athletics') }}
group by venue, venue_country

{% endsnapshot %}