{% snapshot snapshot_dim_event %}
{{
    config(
        target_schema='snapshots',
        unique_key="discipline || '-' || age_cat",
        strategy='check',
        check_cols=['normalized_discipline', 'type', 'is_track', 'is_field', 'is_mixed','age_cat']
    )
}}

select 
    discipline,
    normalized_discipline,
    type,
    is_track,
    is_field,
    is_mixed,
    age_cat
from {{ ref('stg_world_athletics') }}
group by discipline, normalized_discipline, type, is_track, is_field, is_mixed, age_cat

{% endsnapshot %}