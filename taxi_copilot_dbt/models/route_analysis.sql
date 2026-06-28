{{ config(materialized='table') }}


select (concat(ctt.pickup_location_id , ' to ',  ctt.dropoff_location_id)) as route , avg(ctt.fare_amount) as avg_fare_amount, avg(ctt.tip_amount) as avg_tip_amount,
avg(ctt.tolls_amount ) as avg_toll_amount, avg(ctt.congestion_surcharge) as avg_surcharge, avg(ctt.pickup_hour ) as avg_pickup_hour,
avg(ctt.pickup_day_of_week ) as avg_pickup_dow, avg(ctt.pickup_month) as avg_pickup_month, avg(trip_duration_minutes) as avg_trip_duration
from {{ ref('clean_taxi_trips') }} ctt
group by ctt.pickup_location_id , ctt.dropoff_location_id   