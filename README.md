# NYC Taxi Analytics Copilot

An analytics application that lets users query NYC taxi trip data using natural language. Built with Snowflake, dbt, Python, FastAPI, Streamlit, and an LLM.

## Architecture

```text
NYC Taxi API
    ↓
Python ingestion
    ↓
Snowflake RAW
    ↓
dbt STAGING
    ↓
dbt MARTS
    ↓
FastAPI + LLM
    ↓
Streamlit dashboard
```

## Tech Stack

* **Python** — data ingestion and application logic
* **Snowflake** — cloud data warehouse
* **dbt** — SQL transformations, analytical models, and data quality tests
* **FastAPI** — API for natural-language analytics
* **Streamlit** — interactive user interface
* **Docker Compose** — containerized API and frontend
* **OpenAI API** — natural-language-to-SQL generation and result summaries

## Data Pipeline

1. Ingest NYC taxi trip records into Snowflake's `RAW` schema.
2. Transform and clean records in dbt's `STAGING` layer.
3. Build analytical models in the `MARTS` schema.
4. Use FastAPI to translate questions into SQL and query Snowflake.
5. Display query results, summaries, and visualizations in Streamlit.

## dbt Models

The analytical models include revenue trends, hourly demand, passenger analysis, payment analysis, pickup hotspots, route analysis, and tipping patterns.

dbt tests validate model data quality.

## Run Locally

### Prerequisites

* Docker Desktop
* Snowflake account and credentials
* OpenAI API key

### Configure environment variables

Create a `.env` file using `.env.example` as a template. Add your own Snowflake credentials and OpenAI API key.

Never commit `.env` or real credentials to Git.

### Start the application

```bash
docker compose up --build
```

Open:

* Streamlit: http://localhost:8501
* FastAPI documentation: http://localhost:8001/docs

## Project Goals

This project demonstrates cloud data warehousing, SQL transformation, data quality testing, API development, and natural-language analytics.
