SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['member_casual']) }} AS membership_type_id,
    CAST(member_casual AS STRING) AS type
FROM
    {{ source('citibike_ingestion', 'main_citibike_tripdata') }}
