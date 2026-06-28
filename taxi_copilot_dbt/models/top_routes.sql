{{ config(materialized='table') }}

select
    pickup_location_id,
    dropoff_location_id,
    count(*) as trip_count,
    round(avg(total_amount), 2) as avg_total_amount,
    round(avg(trip_distance), 2) as avg_distance
from {{ ref('clean_taxi_trips') }}
group by pickup_location_id, dropoff_location_id
order by trip_count desc