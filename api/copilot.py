import os
from openai import OpenAI
from dotenv import load_dotenv
from api.database import get_schema

import re

load_dotenv()

MODEL = 'gpt-4.1-mini'

open_ai_key = os.getenv('OPENAI_KEY')
if open_ai_key:
    print('KEY FOUND')
else:
    print('KEY NOT FOUND')

client = OpenAI(api_key=open_ai_key)




SYSTEM_PROMPT = f'''
You are an analytics SQL assistant for NYC taxi data.

Read the user's query and return the relevant data. The table schema is provided below:

{get_schema()}

Rules:
- Only write SELECT queries.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
- Prefer analytics tables over clean_taxi_trips.
- Return only SQL. No explanation

Business rules:

- Use hourly_demand for questions about pickup hours, demand, trip counts by hour, average fare by hour, or average distance by hour.
- Use daily_revenue for questions about revenue over time, busiest dates, daily trip counts, average daily tips, or total revenue.
- Use payment_analysis for payment type questions.
- Use top_routes for pickup/dropoff route pair questions.
- Use clean_taxi_trips only when the analytics tables do not contain enough detail.

Definitions:
- Demand = trip_count or count(*)
- Revenue = total_amount or total_revenue
- Tip rate = tip_amount / total_amount
- Trip duration = trip_duration_minutes
- Day of week uses pickup_day_of_week where 0 = Sunday and 6 = Saturday.

weekday_analysis:
Use for questions about busiest day of week, average fare by weekday, average tip by weekday.

tip_analysis:
Use for questions about tips by hour, average tip, tip percentage, and tipping behavior.

passenger_analysis:
Use for questions about passenger count, average fare by passenger count, and trip distance by passenger count.

route_analysis:
Contains average data for each route. Use for route-specific questions such as most expensive route

payment_description

Examples:
Credit Card
Cash
No Charge
Dispute

For percentage questions:
- Use 100.0 * numerator / denominator.

Question: What percentage of trips had a tip greater than 0?
SQL:
SELECT
  ROUND(100.0 * SUM(CASE WHEN tip_amount > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS percent_tipped
FROM clean_taxi_trips
LIMIT 100

Question: Which pickup hour has the highest average tip amount?
SQL:
SELECT
  pickup_hour,
  ROUND(AVG(tip_amount), 2) AS avg_tip
FROM clean_taxi_trips
GROUP BY pickup_hour
ORDER BY avg_tip DESC
LIMIT 10
'''

TABLE_GUIDE = {
    "hourly_demand": "Use for pickup hour, busiest hour, demand by hour, average fare by hour.",
    "daily_revenue": "Use for revenue over time, daily trip counts, busiest dates.",
    "payment_analysis": "Use for payment type comparisons.",
    "top_routes": "Use for pickup/dropoff route pairs.",
    "weekday_analysis": "Use for day-of-week trends.",
    "tip_analysis": "Use for tips by hour and tip percentage.",
    "passenger_analysis": "Use for passenger count questions.",
    "route_analysis": "Use for analysing route specific details. Contains details about each specific route"
}


def select_relevant_tables(question: str) -> str:
    q = question.lower()
    selected = []

    if "hour" in q or "time" in q:
        selected += ["hourly_demand", "tip_analysis"]

    if "day" in q or "week" in q or "weekday" in q:
        selected += ["weekday_analysis", "daily_revenue"]

    if "tip" in q:
        selected += ["tip_analysis", "payment_analysis"]

    if "passenger" in q or "group" in q:
        selected += ["passenger_analysis"]

    if "payment" in q:
        selected += ["payment_analysis"]

    if "route" in q or "pickup" in q or "dropoff" in q:
        selected += ["top_routes", "route_analysis"]

    if "revenue" in q or "fare" in q or "amount" in q:
        selected += ["daily_revenue", "clean_taxi_trips"]

    if not selected:
        selected = ["trip_summary", "clean_taxi_trips"]

    selected = list(dict.fromkeys(selected))

    return "\n".join([f"- {table}: {TABLE_GUIDE.get(table, '')}" for table in selected])

def generate_sql(question: str, history: list = []) -> str:
    relevant_tables = select_relevant_tables(question)
    
    history_text = "\n".join([f"User: {item.get('user')}\nAssistant: {item.get('assistant')}" for item in history])
    
    prompt = f'''{SYSTEM_PROMPT}

            These are the relevant tables.

            Relevant Tables: {relevant_tables}

            Other tables are okay to use if these are insufficient. 
            For individual trip questions, such as most expensive trip, longest trip, shortest trip, highest fare, or specific trip records, use clean_taxi_trips.
            Use public.clean_taxi_trips for individual trip-level questions.

            Ensure any columns you refer are actually present in the table you are referring.
            
            

            '''
    response = client.chat.completions.create(
        model = MODEL,
        messages=[
            {'role':'system', 'content': prompt},
            {'role':'user', 'content':f'''
            Conversation History:
            {history_text}

            Current Question:
            {question}

            Generate SQL for the current question
            '''}
        ]
    )

    sql = response.choices[0].message.content.strip()

    # In case sql is returned in markdown
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql

# Checks to see if the sql returned by the llm is safe to run. Must ensure it doesn't mess up any tables
# def sql_safety_check(sql: str) -> bool:
#     prohibited = ['insert', 'update', 'delete', 'drop', 'alter', 'create']

#     sql = sql.lower().strip()

#     if not sql.startswith('select'):
#         return False
    
#     # If contains any of the prohibited 
    
#     for word in prohibited:
#         if re.search(rf"\b{word}\b", sql):
#             return False
    
#     # Ensure a limit
#     if 'limit' not in sql:
#         sql += '\nLIMIT 100'
#         return True

#     return True

#     #  # Reject writable CTEs
#     # if re.search(r"with\s+.*\b(insert|update|delete)\b", sql):
#     #     return False

def summarize_results(question: str, sql: str, results: list) -> str:
    if not results:
        return 'No results were returned for this query.'
    
    sample_results = results

    response = client.chat.completions.create(
        model = MODEL,
        messages=[
            {
                'role':'system',
                'content':'You are an analytics assistant that explains sql results concisely'
            },
            {
                'role':'user',
                'content':f'''
                    Question:{question}
                    SQL:{sql}
                    Results:{sample_results}

                    Return a summary containing key insights.
                '''
            }
        ]
    )

    return response.choices[0].message.content.strip()

