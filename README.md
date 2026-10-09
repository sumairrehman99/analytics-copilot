# Analytics Copilot

Analytics Copilot is a natural-language analytics application built around NYC taxi trip data. It uses an LLM to turn questions into SQL, runs those queries against a Snowflake data warehouse, and returns results, summaries, and visualizations through a Streamlit interface.

The project combines data ingestion, warehouse modeling with dbt, and an API that connects the data layer to the application.

## Features

- Natural-language to SQL querying
- Python ingestion pipeline for public NYC taxi data
- Snowflake data warehouse with RAW, STAGING, and MARTS schemas
- dbt transformations, analytical models, and data quality tests
- FastAPI backend for query execution and result generation
- Streamlit frontend for interactive analytics
- Docker Compose setup for running the API and frontend together

## Architecture

```text
        NYC Taxi Public API
                 |
                 v
         Python Ingestion
                 |
                 v
          Snowflake RAW
                 |
                 v
          dbt STAGING
                 |
                 v
           dbt MARTS
                 |
                 v
          FastAPI Backend
                 |
          LLM SQL Generation
                 |
                 v
       Query Snowflake Models
                 |
                 v
       Results, Summaries,
        and Visualizations
                 |
                 v
        Streamlit Frontend
```

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Data Warehouse | Snowflake |
| Data Ingestion | Python |
| Data Modeling | dbt |
| Backend | FastAPI |
| Frontend | Streamlit |
| Natural Language Processing | OpenAI API |
| Containerization | Docker, Docker Compose |

## Data Pipeline and Modeling

The ingestion script loads public NYC taxi trip data into the RAW schema in Snowflake. dbt then cleans and transforms the data in the STAGING layer and builds analytical models in MARTS.

The mart models support analysis of revenue, hourly demand, passenger counts, payment types, pickup hotspots, routes, and tipping patterns. dbt tests help validate the resulting datasets.

## How It Works

1. Python retrieves public NYC taxi data and loads it into Snowflake.
2. dbt transforms the raw records and builds analytical models.
3. A user submits a question through Streamlit.
4. The LLM generates SQL based on the available analytical schema.
5. FastAPI executes the query against Snowflake.
6. The application returns the results, a natural-language summary, and a recommended visualization.

## Running Locally

### Prerequisites

- Docker Desktop
- A Snowflake account with access to the configured warehouse and schemas
- An OpenAI API key

### 1. Clone the repository

```bash
git clone -b snowflake-migration https://github.com/sumairrehman99/analytics-copilot.git
cd analytics-copilot
```

### 2. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Add your Snowflake credentials and OpenAI API key to `.env`. Use the variable names provided in `.env.example`.

Do not commit `.env` or share your credentials.

### 3. Start the application

```bash
docker compose up --build
```

Open the application:

- **Streamlit:** http://localhost:8501
- **FastAPI docs:** http://localhost:8001/docs

Stop the containers with `Ctrl+C`. To run them in the background, use `docker compose up --build -d`.

## Example Questions

- Which payment type has the highest average tip?
- How does trip demand vary by hour?
- Which pickup locations have the most trips?
- Which routes have the highest average fare?
- How does average tipping vary throughout the day?

## Future Improvements

- Automate and schedule recurring data ingestion
- Add CI/CD with GitHub Actions
- Deploy the application to AWS
- Improve query validation and error handling
- Add query history and saved reports

## What I Learned

This project gave me practical experience with Snowflake, dbt, data ingestion, SQL modeling, and data quality testing. It also helped me connect a warehouse to a working application using FastAPI, an LLM, and Streamlit, and package the services with Docker Compose.
