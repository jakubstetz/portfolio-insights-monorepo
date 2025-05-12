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
def startup():
    logger.info("Opening database connection")
    return database.init()


# On shutdown, close database connection
@app.on_event("shutdown")
def shutdown():
    logger.info("Closing database connection")
    return database.close()


# ------------------------------------------------------------------------#

##### General #####


# Root
@app.get("/")
async def root():
    return "Hello World"


# Health check for uptime monitoring
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Health check for database and market connections
@app.get("/health/deep")
def health_check_deep():
    logger.info("Testing database connection...")
    db_ok = database.ping()
    logger.info("Testing market connection...")
    market_ok = market.ping()
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

##### yfinance Connections #####


# Endpoint to return stock price history
@app.get("/stocks")
async def get_stock_info(ticker, startDate, interval):
    try:
        return market.stock_info(ticker, startDate, interval)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Ticker not found")


@app.get("/check-alert")
async def check_alert(ticker, price: float, direction):
    try:
        market_response = market.is_valid_alert(ticker, price, direction)
        if not market_response["valid"]:
            raise HTTPException(status_code=400, detail=market_response["message"])
        return market_response
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Ticker not found")


# ------------------------------------------------------------------------#

##### Manage Stock Price Alerts #####


# Get alerts matching optional search_term
@app.get("/alerts", response_model=List[Dict])
async def search_alerts(search_term=""):
    try:
        return alerts.search(search_term)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Endpoint to create a new alert
@app.post("/alerts", status_code=status.HTTP_201_CREATED)
def create_alert(alert: Alert):
    try:
        alert_id = alerts.create(alert)
        return {"message": "Alert created successfully", "new_alert_id": alert_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Delete alert by ID (query parameter)
@app.delete("/alerts")
def delete_alert(id):
    try:
        alerts.delete(id)
        return {"message": "Alert deleted successfully", "deleted_alert_id": id}
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="Internal server error")
