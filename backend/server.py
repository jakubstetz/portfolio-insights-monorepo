'''
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Activate the backend virtual environment by running the shell command: source venv/bin/activate
Start a server by running the shell command: fastapi dev server.py

'''

from fastapi import FastAPI
from yfinance_functions import stock_info

app = FastAPI() # Initialize FastAPI server

@app.get('/') # Root endpoint
async def root():
    return 'Hello World'

@app.get("/info/{ticker}")
async def get_stock_info(ticker = 'SPY'): # Endpoint to return basic stock information
    if len(ticker) > 5: return 'Error! Invalid Ticker!'
    return stock_info(ticker)

'''
@app.get("/data")
async def historical_data_q(ticker = 'SPY'): # Endpoint to practice using query parameters
    if len(ticker) > 5: return 'Error! Invalid Ticker!'
    return ticker
'''