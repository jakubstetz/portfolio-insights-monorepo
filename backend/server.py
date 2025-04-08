"""
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Activate the backend virtual environment by running the shell command:
source venv/bin/activate

Start the server by running the shell command:
fastapi dev server.py
"""

from fastapi import FastAPI
import alerts
import database
import market
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Alert(BaseModel): # Used for easier alert creation in alerts POST route with automatic type validation
    ticker: str # 1-10 characters, enforced in database
    price: float
    direction: str # 'above' or 'below'
    expiration_time: datetime # ISO 8601 string will be automatically parsed

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

# Endpoint to return basic stock information, mostly for testing
@app.get("/info/{ticker}")
async def get_stock_info(ticker = 'SPY'):
    return market.stock_info(ticker)

# Flexible endpoint to conveniently test whatever functionality I want
@app.get("/test")
async def test():
    return alerts.evaluate()

#------------------------------------------------------------------------#

##### Manage Stock Price Alerts #####

# Endpoint to retrieve an alert by id
@app.get("/alerts")
def get_alert(id):
    alert = alerts.get(id)
    return alert or 'Error!'

# Endpoint to create a new alert
@app.post("/alerts")
def create_alert(alert: Alert):
    insertion_id = alerts.create(alert)
    return f'Success! Alert created with id = {insertion_id}' if insertion_id else 'Error!'

# Endpoint to delete an existing alert by id
@app.delete("/alerts")
def delete_alert(id):
    return f"Alert {id} deleted." if alerts.delete(id) else 'Error!'