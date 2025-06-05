{{config(materialized='table', alias='stg_world_athletics')}}

with add_columns as (
    select 
        *EXCEPT(track_field),
        lower(track_field) as track_field,
        case
            when lower(track_field) = 'track' then true
            else false
        end as is_track,
        case
            when lower(track_field) = 'field' then true
            else false
        end as is_field,
        case
            when lower(track_field) = 'mixed' then true
            else false
        end as is_mixed
    from {{ source('world_athletics','raw_world_athletics')}}
),
filtered as (

    select *
    from add_columns
    where age_at_event is null or age_at_event >= 16

)

select * from filtered