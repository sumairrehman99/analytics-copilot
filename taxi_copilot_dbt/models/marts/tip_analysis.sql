{{ config(materialized='table') }}

select
    pickup_hour,
    round(avg(tip_amount),2) as avg_tip,
    round(avg(total_amount),2) as avg_total_amount,
    round(avg(100.0 * tip_amount / nullif(total_amount,0)),2) as avg_tip_percent
from {{ ref('clean_taxi_trips') }}
group by pickup_hour
order by pickup_hour