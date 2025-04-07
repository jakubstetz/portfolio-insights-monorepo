'''
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Activate the backend virtual environment by running the shell command: source venv/bin/activate
Start a server by running the shell command: fastapi dev server.py

'''

from fastapi import FastAPI
import alerts

app = FastAPI() # Initialize FastAPI server

@app.get('/') # Root endpoint
async def root():
    return 'Hello World'

@app.get("/info/{ticker}")
async def get_stock_info(ticker = 'SPY'): # Endpoint to return basic stock information
    return stock_info(ticker)

# ------------------------------------------------------------------------ #

##### Managing Alerts #####
@app.get("/alerts")
def get_alert(id): # Endpoint to retrieve an alert by id
    return alerts.get(id)

@app.post("/alerts")
def create_alert(ticker, price, direction, one_time, expiration_date): # Endpoint to create a new alert
    return alerts.create(ticker, price, direction, one_time, expiration_date)

@app.delete("/alerts")
def delete_alert(id): # Endpoint to delete an existing alert by id
    return alerts.delete(id)

@app.patch("/alerts")
def update_alert(id, ticker, price, direction, one_time, expiration_date): # Endpoint to return basic stock information
    return alerts.update(id)

'''
@app.get("/data")
async def historical_data_q(ticker = 'SPY'): # Endpoint to practice using query parameters
    if len(ticker) > 5: return 'Error! Invalid Ticker!'
    return ticker
'''