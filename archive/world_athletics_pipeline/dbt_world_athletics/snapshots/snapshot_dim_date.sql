{% snapshot snapshot_dim_date %}
{{
    config(
        target_schema='snapshots',
        unique_key='date',
        strategy='check',
        check_cols=['season']
    )
}}

select
    cast(date as date) as date,
    cast(season as int) as season
from {{ ref('stg_world_athletics') }}
group by date, season

{% endsnapshot %}
