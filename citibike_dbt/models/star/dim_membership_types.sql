SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['member_casual']) }} AS membership_type_id,
    CAST(member_casual AS STRING) AS type
FROM
   {{ source(env_var('BIGQUERY_SOURCE_DATASET'), env_var('BIGQUERY_RAW_DATA_TABLE')) }}
