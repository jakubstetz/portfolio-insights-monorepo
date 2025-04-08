"""
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Activate the backend virtual environment by running the shell command: source venv/bin/activate
Start a server by running the shell command: fastapi dev server.py
"""

from fastapi import FastAPI
import alerts
import database
from yfinance_functions import stock_info
from pydantic import BaseModel
from datetime import datetime

app = FastAPI() # Initialize FastAPI server

class Alert(BaseModel): # Used for easier alert creation in alerts POST route
    ticker: str # 1-10 characters, enforced in database
    price: float
    direction: str # 'above' or 'below'
    one_time: bool
    expiration_date: datetime # ISO 8601 string will be automatically parsed

# ------------------------------------------------------------------------ #

##### Lifespan Events #####

# On startup, open database connection
@app.on_event("startup")
def startup():
    return database.init()

# On shutdown, commit database changes and close database connection
@app.on_event("shutdown")
def shutdown():
    return database.close()

# ------------------------------------------------------------------------ #

##### General #####

# Root endpoint
@app.get('/')
async def root():
    return 'Hello World'

# Endpoint to return basic stock information
@app.get("/info/{ticker}")
async def get_stock_info(ticker = 'SPY'):
    return stock_info(ticker)

# ------------------------------------------------------------------------ #

##### Manage Stock Price Alerts #####

# Endpoint to retrieve an alert by id
@app.get("/alerts")
def get_alert(id):
    alert = alerts.get(id)
    if not alert: return 'Error!' # Alert with the given id wasn't found
    else: return alert # Alert with the given id was found

# Endpoint to create a new alert
@app.post("/alerts")
def create_alert(alert: Alert):
    # Successful alert creation
    if alerts.create(alert):
        return 'Success! Alert created:'
    # Alert creation failed
    else: return 'Error!'


# Endpoint to delete an existing alert by id
@app.delete("/alerts")
def delete_alert(id):
    if alerts.delete(id):
        return f"Alert {id} deleted."
    else:
        return 'Error!' 

# Endpoint to return basic stock information - NOT IMPLEMENTED
@app.patch("/alerts")
def update_alert(id, ticker, price, direction, one_time, expiration_date): 
    return alerts.update(id)

'''
@app.get("/data")
async def historical_data_q(ticker = 'SPY'): # Endpoint to practice using query parameters
    if len(ticker) > 5: return 'Error! Invalid Ticker!'
    return ticker
'''