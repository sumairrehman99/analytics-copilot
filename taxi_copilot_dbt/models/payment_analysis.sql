select
    pt.payment_description,
    count(*) as trips,
    round(avg(ctt.total_amount),2) as avg_total,
    round(avg(ctt.tip_amount),2) as avg_tip

from {{ ref('clean_taxi_trips') }} ctt

join {{ ref('payment_types') }} pt
on ctt.payment_type = pt.payment_type

group by pt.payment_description