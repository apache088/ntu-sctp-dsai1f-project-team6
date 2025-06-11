with raw_data_with_duplicates as (
    select 
        *,
        row_number() over (
            partition by
                competitor,
                dob,
                discipline,
                date,
                venue,
                venue_country,
                mark_numeric
            order by 
                result_score desc, -- Prefer higher scores
                rank asc          -- Prefer better rankings
        ) as raw_dup_flag
    from {{ source('meltano_world_athletics','public_raw_world_athletics')}}
),
raw_data as (
    select 
        * except(raw_dup_flag)
    from raw_data_with_duplicates
    where raw_dup_flag = 1  -- Keep only the first occurrence
),
cast_raw_data as (
    select 
        safe_cast(rank as int) as rank,
        safe_cast(wind as numeric) as wind,
        competitor,
        safe_cast(dob as date) as dob,
        nationality,
        safe_cast(position as int) as position,
        venue,
        safe_cast(date as date) as date,
        safe_cast(result_score as numeric) as result_score,
        discipline,
        type,
        sex as gender,
        age_cat,
        normalized_discipline,
        track_field,
        safe_cast(mark_numeric as numeric) as mark,
        venue_country,
        safe_cast(age_at_event AS numeric) as age_at_event,
        season
    from raw_data
),
add_columns as (
    select 
        * except(track_field,type),
        lower(track_field) as track_field,
        lower(track_field) = 'track' as is_track,
        lower(track_field) = 'field' as is_field,
        lower(track_field) = 'mixed' as is_mixed,
        lower(type) as type,
        case
            when lower(type) = 'combined-events' 
                then 'points'
            when lower(type) in ('hurdles','race-walks','relays','road-running','sprints')
                then 'seconds'
            when lower(type) in ('jumps','throws')
                then 'metres'
            else null 
        end as mark_unit
    from cast_raw_data
)
select * except(track_field) from add_columns
where age_at_event >= 15