SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['rideable_type']) }} AS bike_type_id,
    CAST(rideable_type AS STRING) AS type
FROM
    {{ source(env_var('BIGQUERY_SOURCE_DATASET'), env_var('BIGQUERY_RAW_DATA_TABLE')) }}
