{% snapshot snapshot_dim_athlete %}
{{
    config(
        target_schema='snapshots',
        unique_key="competitor || '-' || dob",
        strategy='check',
        check_cols=['nationality', 'gender']
    )
}}

with ranked_athletes as (
    select 
        competitor,
        dob,
        nationality,
        gender,
        date,
        row_number() over (
            partition by competitor, dob 
            order by date desc
        ) as recency_rank
    from {{ ref('stg_world_athletics') }}
)

select 
    competitor,
    dob,
    nationality,
    gender
from ranked_athletes
where recency_rank = 1  -- Only take the most recent record for each athlete

{% endsnapshot %}
