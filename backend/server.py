"""
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Activate the backend virtual environment by running the shell command:
source venv/bin/activate

Start the server by running the shell command:
fastapi dev server.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import alerts
import database
import market
from pydantic import BaseModel
from datetime import datetime

class Alert(BaseModel): # Used for easier alert creation in alerts POST route with automatic type validation
    ticker: str # 1-10 characters, enforced in database
    price: float
    direction: str # 'above' or 'below'
    expiration_time: datetime # ISO 8601 string will be automatically parsed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" SHOULD ONLY BE USED IN DEVELOPMENT, CHANGE TO FRONTEND ORIGIN IN PRODUCTION
)

#------------------------------------------------------------------------#

##### Lifespan Events #####

# On startup, open database connection
@app.on_event("startup")
def startup():
    return database.init()

# On shutdown, close database connection
@app.on_event("shutdown")
def shutdown():
    return database.close()

#------------------------------------------------------------------------#

##### General #####

# Root endpoint
@app.get('/')
async def root():
    return 'Hello World'

# Endpoint to return stock price history
@app.get("/stocks")
async def get_stock_info(ticker):
    try:
        return market.stock_info(ticker)
    except Exception:
        raise HTTPException(status_code=404, detail="Ticker not found")

# Flexible endpoint to conveniently test whatever functionality I want
@app.get("/test")
async def test():
    return alerts.evaluate()

#------------------------------------------------------------------------#

##### Manage Stock Price Alerts #####

# Endpoint to retrieve alerts matching a search_term
@app.get("/alerts")
async def get_alert(search_term):
    try:
        return alerts.get(search_term)
    except Exception:
        raise HTTPException(status_code=404, detail="No matching alerts found")

# Endpoint to create a new alert
@app.post("/alerts")
def create_alert(alert: Alert):
    insertion_id = alerts.create(alert)
    return f'Success! Alert created with id = {insertion_id}' if insertion_id else 'Error!'

# Endpoint to delete an existing alert by id
@app.delete("/alerts")
def delete_alert(id):
    return f"Alert {id} deleted." if alerts.delete(id) else 'Error!'