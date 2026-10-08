import os
import pandas as pd
from dotenv import load_dotenv
from .snowflake import get_snowflake_connection

load_dotenv()


def get_schema():
    conn = get_snowflake_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT table_name
            FROM ANALYTICS_COPILOT.INFORMATION_SCHEMA.TABLES
            WHERE table_schema = 'MARTS'
            ORDER BY table_name
        """)

        tables = cursor.fetchall()

        schema = ""

        for (table_name,) in tables:
            schema += f"\nTable: {table_name}\n"

            cursor.execute(f"""
                SELECT column_name, data_type
                FROM ANALYTICS_COPILOT.INFORMATION_SCHEMA.COLUMNS
                WHERE table_schema = 'MARTS'
                  AND table_name = '{table_name}'
                ORDER BY ordinal_position
            """)

            columns = cursor.fetchall()

            for column_name, data_type in columns:
                schema += f"- {column_name} ({data_type})\n"

        return schema

    finally:
        conn.close()


def run_query(query: str):
    conn = get_snowflake_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=columns)

        return df.to_dict(orient="records")

    finally:
        conn.close()
