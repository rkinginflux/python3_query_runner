from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from influxdb_client_3 import InfluxDBClient3
from fastapi.staticfiles import StaticFiles
import pandas as pd

# InfluxDB Client Configuration
INFLUXDB_HOST = "http://192.168.xxx.xx:8181"
TOKEN = "123456789abcdefghijklmnopqr"
DATABASE = "my_database"

# Initialize FastAPI app
app = FastAPI()

# Serve static files (styles.css)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates Configuration
templates = Jinja2Templates(directory="templates")

def query_influxdb(sql_query: str):
    """Execute SQL query against InfluxDB v3 using the official client."""
    try:
        # Corrected InfluxDBClient3 instantiation
        client = InfluxDBClient3(host=INFLUXDB_HOST, token=TOKEN, database=DATABASE)

        # Execute the query and return a Pandas DataFrame
        df = client.query(sql_query, language="sql", mode="pandas")

        return df
    except Exception as e:
        return str(e)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": None})

@app.post("/query", response_class=HTMLResponse)
async def run_query(request: Request, sql_query: str = Form(...)):
    data = query_influxdb(sql_query)

    # Pass None if DataFrame is empty
    data_to_pass = data if isinstance(data, pd.DataFrame) and not data.empty else None

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data_to_pass,
            "error": data if isinstance(data, str) else None,
            "sql_query": sql_query,  # Pass the user-entered query back to the template
        },
    )
