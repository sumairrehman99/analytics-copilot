select
    pickup_location_id,
    count(*) as trips
from {{ ref('clean_taxi_trips') }}
group by pickup_location_id
order by trips desc