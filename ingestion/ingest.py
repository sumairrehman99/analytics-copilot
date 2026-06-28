import os, time, requests, pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

API_URL = "https://data.cityofnewyork.us/resource/4b4i-vvec.json"
TOKEN = os.getenv("SOCRATA_APP_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

LIMIT = 50000
MAX_ROWS = 250000

headers = {"X-App-Token": TOKEN}

for offset in range(0, MAX_ROWS, LIMIT):
    print(f"Fetching offset {offset}")

    r = requests.get(
        API_URL,
        headers=headers,
        params={"$limit": LIMIT, "$offset": offset},
        timeout=90
    )
    r.raise_for_status()

    df = pd.DataFrame(r.json())

    df.to_sql(
        "raw_taxi_trips",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(f"Inserted {len(df)} rows")
    time.sleep(0.5)