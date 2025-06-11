select
    {{ dbt_utils.generate_surrogate_key(['venue', 'venue_country']) }} as venue_id,
    venue,
    venue_country,
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
from {{ ref('snapshot_dim_venue') }}
where dbt_valid_to is null