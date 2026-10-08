{{ config(materialized='table') }}

select
    date(pickup_datetime) as pickup_date,
    count(*) as trip_count,
    round(sum(total_amount), 2) as total_revenue,
    round(avg(total_amount), 2) as avg_total_amount,
    round(avg(tip_amount), 2) as avg_tip
from {{ ref('clean_taxi_trips') }}
group by date(pickup_datetime)
order by pickup_date