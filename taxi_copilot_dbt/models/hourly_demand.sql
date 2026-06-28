{{ config(materialized='table') }}

select
    pickup_hour,
    count(*) as trip_count,
    round(avg(fare_amount), 2) as avg_fare,
    round(avg(trip_distance), 2) as avg_trip_distance,
    round(avg(trip_duration_minutes), 2) as avg_trip_duration
from {{ ref('clean_taxi_trips') }}
group by pickup_hour
order by pickup_hour