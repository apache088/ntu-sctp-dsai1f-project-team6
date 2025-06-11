select
    -- {{ dbt_utils.generate_surrogate_key(['stg.competitor', 'stg.dob', 'stg.discipline', 'stg.age_cat', 'stg.date', 'stg.venue', 'stg.venue_country']) }} as performance_id,
    {{ dbt_utils.generate_surrogate_key([
        'a.athlete_id', 
        'e.event_id', 
        'd.date_id', 
        'v.venue_id',
        ]) }} as performance_id,
    a.athlete_id,
    e.event_id,
    d.date_id,
    v.venue_id,
    stg.rank,
    stg.mark,
    stg.wind,
    stg.position,
    stg.result_score,
    stg.age_at_event
from {{ ref('stg_world_athletics') }} stg
join {{ ref('dim_athlete') }} a
    on stg.competitor = a.competitor and stg.dob = a.dob
join {{ ref('dim_event') }} e
    on stg.normalized_discipline = e.normalized_discipline
join {{ ref('dim_venue') }} v
    on stg.venue = v.venue and stg.venue_country = v.venue_country
join {{ ref('dim_date') }} d
    on stg.date = d.date