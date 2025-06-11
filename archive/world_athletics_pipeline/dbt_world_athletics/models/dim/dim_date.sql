select
    {{ dbt_utils.generate_surrogate_key(['date']) }} as date_id,
    date,
    season as year,
    extract(month from date) as month,
    extract(day from date) as day,
    extract(quarter from date) as quarter,
    extract(dayofweek from date) as day_of_week,
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to
from {{ ref('snapshot_dim_date') }}
where dbt_valid_to is null