import os
import time
import requests
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv


load_dotenv()

API_URL = "https://data.cityofnewyork.us/resource/4b4i-vvec.json"
TOKEN = os.getenv("SOCRATA_APP_TOKEN")

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE"),
)

LIMIT = 10_000

headers = {"X-App-Token": TOKEN}

print("Fetching taxi data...")

r = requests.get(
    API_URL,
    headers=headers,
    params={"$limit": LIMIT},
    timeout=90
)

r.raise_for_status()

df = pd.DataFrame(r.json())

print(f"Fetched {len(df)} rows")

# Convert column names to uppercase to match Snowflake
df.columns = [col.upper() for col in df.columns]

# Convert numeric fields
numeric_columns = [
    "VENDORID",
    "PASSENGER_COUNT",
    "TRIP_DISTANCE",
    "RATECODEID",
    "PULOCATIONID",
    "DOLOCATIONID",
    "PAYMENT_TYPE",
    "FARE_AMOUNT",
    "EXTRA",
    "MTA_TAX",
    "TIP_AMOUNT",
    "TOLLS_AMOUNT",
    "IMPROVEMENT_SURCHARGE",
    "TOTAL_AMOUNT",
    "CONGESTION_SURCHARGE",
    "AIRPORT_FEE",
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Insert using Snowflake's pandas helper
from snowflake.connector.pandas_tools import write_pandas

success, chunks, rows, output = write_pandas(
    conn,
    df,
    "TAXI_TRIPS",
    database="ANALYTICS_COPILOT",
    schema="RAW",
    auto_create_table=False,
)

print(f"Loaded {rows} rows into Snowflake")

conn.close()