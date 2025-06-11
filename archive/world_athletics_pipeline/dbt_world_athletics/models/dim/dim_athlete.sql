select
  {{ dbt_utils.generate_surrogate_key(['competitor', 'dob']) }} as athlete_id,
  competitor,
  dob,
  nationality,
  gender,
  dbt_valid_from as valid_from,
  dbt_valid_to as valid_to
from {{ ref('snapshot_dim_athlete') }}
where dbt_valid_to is null