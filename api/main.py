from fastapi import FastAPI
from api.database import run_query
from api.chart import recommend_chart

from pydantic import BaseModel
from api.copilot import generate_sql, summarize_results

app = FastAPI(title="NYC Taxi Analytics API")

class AskRequest(BaseModel):
    question: str
    history: list = []



@app.get("/health")
def health():
    return {"status": "ok"}

@app.post('/ask')
def ask(request: AskRequest):
    try:
        sql = generate_sql(request.question, request.history)

        
        results = run_query(sql)
        summary = summarize_results(request.question, sql, results)
        chart = recommend_chart(results)

        return {
            'question': request.question,
            'sql': sql.strip(),
            'results': results,
            'summary': summary,
            'chart': chart
        }
    except Exception as e:
        return {
            "error": "I generated SQL, but it failed when running against the database.",
            "sql": sql,
            "details": str(e),
            "suggestion": "Try rephrasing the question or asking about one of the available analytics tables."
        }


@app.get("/hourly-demand")
def hourly_demand():
    query = """
    SELECT *
    FROM hourly_demand
    ORDER BY pickup_hour;
    """
    return run_query(query)


@app.get("/daily-revenue")
def daily_revenue():
    query = """
    SELECT *
    FROM daily_revenue
    ORDER BY pickup_date;
    """
    return run_query(query)


@app.get("/payment-analysis")
def payment_analysis():
    query = """
    SELECT *
    FROM payment_analysis
    ORDER BY trips DESC;
    """
    return run_query(query)


@app.get("/top-routes")
def top_routes():
    query = """
    SELECT *
    FROM top_routes
    LIMIT 20;
    """
    return run_query(query)

@app.get('/get-schema')
def get_schema():
    return {
        'schema': '\n' + get_schema()
    }
    