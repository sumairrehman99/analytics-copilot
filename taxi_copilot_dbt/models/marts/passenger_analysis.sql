    {{ config(materialized='table') }}

select
    passenger_count,
    count(*) as trip_count,
    round(avg(total_amount),2) as avg_total_amount,
    round(avg(trip_distance),2) as avg_trip_distance,
    round(avg(trip_duration_minutes),2) as avg_trip_duration
from {{ ref('clean_taxi_trips') }}
group by passenger_count
order by passenger_count