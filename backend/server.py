'''
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/

Start a server by running the shell command: fastapi dev server.py

'''

from fastapi import FastAPI

app = FastAPI() # Initialize FastAPI server

@app.get('/') # Root endpoint
async def root():
    return 'Hello World'

@app.get("/data/{ticker}")
async def historical_data_p(ticker = 'SPY'): # Endpoint to practice using path parameters
    if len(ticker) > 5: return 'Error! Invalid Ticker!'
    return ticker

@app.get("/data")
async def historical_data_q(ticker = 'SPY'): # Same functionality as above; endpoint to practice using query parameters
    if len(ticker) > 5: return 'Error! Invalid Ticker!'
    return ticker