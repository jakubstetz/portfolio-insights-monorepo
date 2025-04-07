'''
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Activate the backend virtual environment by running the shell command: source venv/bin/activate
Start a server by running the shell command: fastapi dev server.py

'''

from fastapi import FastAPI
import alerts
import database
from yfinance_functions import stock_info

app = FastAPI() # Initialize FastAPI server

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

@app.get("/info/{ticker}")
async def get_stock_info(ticker = 'SPY'): # Endpoint to return basic stock information
    return stock_info(ticker)

# ------------------------------------------------------------------------ #

##### Manage Stock Price Alerts #####

# Endpoint to retrieve an alert by id
@app.get("/alerts")
def get_alert(id):
    return alerts.get(id)

# Endpoint to create a new alert
@app.post("/alerts")
def create_alert(ticker, price, direction, one_time, expiration_date):
    return alerts.create(ticker, price, direction, one_time, expiration_date)

# Endpoint to delete an existing alert by id
@app.delete("/alerts")
def delete_alert(id):
    return alerts.delete(id)

# Endpoint to return basic stock information
@app.patch("/alerts")
def update_alert(id, ticker, price, direction, one_time, expiration_date): 
    return alerts.update(id)

'''
@app.get("/data")
async def historical_data_q(ticker = 'SPY'): # Endpoint to practice using query parameters
    if len(ticker) > 5: return 'Error! Invalid Ticker!'
    return ticker
'''