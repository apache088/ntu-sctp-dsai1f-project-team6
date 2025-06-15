SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['rideable_type']) }} AS bike_type_id,
    CAST(rideable_type AS STRING) AS type
FROM
    {{ source('citibike_ingestion', 'main_citibike_tripdata') }}
