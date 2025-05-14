"""
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Activate the backend virtual environment by running the shell command:
source venv/bin/activate

Start the server by running the shell command:
fastapi dev server.py
"""

from utils.logging import logger

logger.info("Starting Portfolio Insights backend")
logger.info("Importing modules...")

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import httpx
import alerts
import database
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

logger.info("Modules loaded")


load_dotenv()
logger.info(f"Environment loaded:")
for key, value in os.environ.items():
    logger.info(f"   {key} = {value}")

cors_origins = os.getenv("CORS_ORIGINS").split(",")
go_api_url = os.getenv("GO_API_URL")


# Used in POST /alerts for automatic validation and parsing
class Alert(BaseModel):
    ticker: str  # 1-10 characters, enforced in database
    price: float
    direction: str  # 'above' or 'below'
    expiration_time: Optional[datetime]  # ISO 8601 string will be automatically parsed


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------#

##### Lifespan Events #####


# On startup, open database connection
@app.on_event("startup")
def startup() -> None:
    logger.info("Opening database connection")
    return database.init()


# On shutdown, close database connection
@app.on_event("shutdown")
def shutdown() -> None:
    logger.info("Closing database connection")
    return database.close()


# ------------------------------------------------------------------------#

##### General #####


# Root
@app.get("/")
async def root() -> str:
    return "Hello World"


# Health check for uptime monitoring
@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


# Health check for database and market connections
@app.get("/health/deep")
async def health_check_deep() -> Dict[str, str | bool]:

    logger.info("Testing database connection...")
    db_ok = database.ping()

    logger.info("Testing market connection...")
    endpoint = "/health"
    url = go_api_url + endpoint
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
        response.raise_for_status()
        market_ok = True
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error(f"Go microservice health check failed: {e}")
        market_ok = False

    return {
        "status": "ok" if db_ok and market_ok else "fail",
        "database connection": db_ok,
        "market connection": market_ok,
    }


# Temporary endpoint for manual testing
@app.get("/test")
async def test():
    return True


# ------------------------------------------------------------------------#

##### Market Connections #####


# Endpoint to return stock price history
@app.get("/stocks")
async def get_stock_info(
    ticker: str, startDate: str, interval: str
) -> List[Dict[str, str | float]]:
    endpoint = "/stocks"
    query = f"?ticker={ticker}&startDate={startDate}&interval={interval}"
    url = go_api_url + endpoint + query
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail="Error from Go service"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Ticker not found")


@app.get("/check-alert")
async def check_alert(
    ticker: str, price: float, direction: str
) -> Dict[str, str | bool]:
    endpoint = "/check-alert"
    query = f"?ticker={ticker}&price={price}&direction={direction}"
    url = go_api_url + endpoint + query
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json().get("message", "Error from Go service")
        except Exception:
            detail = "Error from Go service"
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=502, detail="Market service unavailable")


# ------------------------------------------------------------------------#

##### Manage Stock Price Alerts #####


# Get alerts matching optional search_term
@app.get("/alerts", response_model=List[Dict])
async def search_alerts(search_term: str = "") -> List[Dict]:
    try:
        return alerts.search(search_term)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Endpoint to create a new alert
@app.post("/alerts", status_code=status.HTTP_201_CREATED)
def create_alert(alert: Alert) -> Dict[str, str | int]:
    try:
        alert_id = alerts.create(alert)
        return {"message": "Alert created successfully", "new_alert_id": alert_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Delete alert by ID (query parameter)
@app.delete("/alerts")
def delete_alert(id: int) -> Dict[str, str | int]:
    try:
        alerts.delete(id)
        return {"message": "Alert deleted successfully", "deleted_alert_id": id}
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="Internal server error")
