{{ config(materialized='table') }}

select
    pickup_day_of_week,
    count(*) as trip_count,
    round(avg(total_amount),2) as avg_total_amount,
    round(avg(tip_amount),2) as avg_tip,
    round(avg(trip_duration_minutes),2) as avg_trip_duration
from {{ ref('clean_taxi_trips') }}
group by pickup_day_of_week
order by pickup_day_of_week