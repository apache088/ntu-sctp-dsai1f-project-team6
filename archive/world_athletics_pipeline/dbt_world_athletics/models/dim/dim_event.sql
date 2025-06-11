select
    {{ dbt_utils.generate_surrogate_key(['discipline','age_cat']) }} as event_id,
    normalized_discipline,
    discipline,
    type,
    is_track,
    is_field,
    is_mixed,
    age_cat,
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
from {{ ref('snapshot_dim_event') }}
where dbt_valid_to is null
