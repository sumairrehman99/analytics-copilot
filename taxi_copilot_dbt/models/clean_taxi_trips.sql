{{ config(materialized='view') }}

with cleaned as (

    select
        cast(cast(vendorid as numeric) as integer) as vendorid,

        cast(tpep_pickup_datetime as timestamp) as pickup_datetime,
        cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime,

        cast(cast(passenger_count as numeric) as integer) as passenger_count,

        cast(trip_distance as numeric) as trip_distance,

        cast(cast(pulocationid as numeric) as integer) as pickup_location_id,
        cast(cast(dolocationid as numeric) as integer) as dropoff_location_id,
        cast(cast(payment_type as numeric) as integer) as payment_type,

        cast(fare_amount as numeric) as fare_amount,
        cast(extra as numeric) as extra,
        cast(mta_tax as numeric) as mta_tax,
        cast(tip_amount as numeric) as tip_amount,
        cast(tolls_amount as numeric) as tolls_amount,
        cast(total_amount as numeric) as total_amount,
        cast(congestion_surcharge as numeric) as congestion_surcharge,
        cast(airport_fee as numeric) as airport_fee,

        extract(hour from cast(tpep_pickup_datetime as timestamp)) as pickup_hour,
        extract(dow from cast(tpep_pickup_datetime as timestamp)) as pickup_day_of_week,
        extract(month from cast(tpep_pickup_datetime as timestamp)) as pickup_month,
        extract(year from cast(tpep_pickup_datetime as timestamp)) as pickup_year,

        extract(epoch from (
            cast(tpep_dropoff_datetime as timestamp)
            - cast(tpep_pickup_datetime as timestamp)
        )) / 60 as trip_duration_minutes

    from {{ source('raw', 'raw_taxi_trips') }}

)

select *
from cleaned
where fare_amount > 0
  and total_amount > 0
  and trip_distance > 0
  and passenger_count > 0
  and trip_duration_minutes > 0