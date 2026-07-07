# Analytics Copilot

Analytics Copilot is an AI-powered analytics application that enables users to query structured data using natural language. The application converts English questions into SQL using an LLM, executes the generated queries against a PostgreSQL data warehouse, and returns both tabular results and visualizations through a web interface.

---

## Features

- Natural language to SQL
- PostgreSQL analytics warehouse
- ETL pipeline for public API data
- dbt data transformations
- FastAPI backend
- Interactive Streamlit frontend
- Dockerized application

---

## Architecture

```text
           Public API
                │
                ▼
          Python ETL Pipeline
                │
                ▼
           PostgreSQL
                │
             dbt Models
                │
                ▼
          Analytics Warehouse
                │
                ▼
         FastAPI Backend
                │
         LLM SQL Generation
                │
                ▼
        Execute SQL Queries
                │
                ▼
      Results & Visualizations
                │
                ▼
        Streamlit Frontend
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Database | PostgreSQL |
| Data Modeling | dbt |
| Backend | FastAPI |
| Frontend | Streamlit |
| AI | OpenAI LLM |
| Containerization | Docker |

---

## How It Works

1. Public datasets are ingested into PostgreSQL.
2. dbt transforms raw data into analytics-ready models.
3. Users ask questions in natural language.
4. The LLM converts the question into SQL.
5. SQL is executed against PostgreSQL.
6. Results are summarized and visualized.
7. Streamlit displays the response.

---

## Running Locally

Clone the repository

```bash
git clone https://github.com/sumairrehman99/analytics-copilot.git

cd analytics-copilot
```

Run

```bash
docker compose up --build
```

Frontend

```
http://localhost:8501
```

API Docs

```
http://localhost:8000/docs
```

---

## Example Questions

- Which regions had the highest sales last month?
- Show monthly trends by product category.
- Which customers generated the most revenue?
- Compare this month's metrics with last month.
- What are the top performing products?

---



## Future Improvements

- User authentication
- Query history
- Role-based access
- Scheduled reports
- Dashboard sharing
- AWS deployment
- GitHub Actions CI/CD
- Support for multiple databases

---

## Lessons Learned

This project was built to gain experience with:

- ETL pipelines
- Data modeling with dbt
- SQL generation using LLMs
- FastAPI
- Docker
- PostgreSQL
- Backend API development
- Analytics engineering

---

## Screenshots

*(Add screenshots after completing the UI.)*
