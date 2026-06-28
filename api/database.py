import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)



def get_schema():
    inspector = inspect(engine)
    schema = ''

    for table in inspector.get_table_names():
        if table in 'raw_taxi_trips':
            continue
        
        schema += f'\nTable: {table}\n' 
        
        columns = inspector.get_columns(table)
        for col in columns:
            schema += f"- {col['name']} ({col['type']})\n"

    return schema

def run_query(query: str):
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df.to_dict(orient="records")