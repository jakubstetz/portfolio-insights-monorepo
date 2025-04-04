'''
Development begun using the FastAPI "First Steps" tutorial.
Reference: https://fastapi.tiangolo.com/tutorial/first-steps/


'''

from fastapi import FastAPI

app = FastAPI() # Initialize FastAPI server

@app.get("/") # Root endpoint
async def root():
    return {"message": "Hello World"}

@app.get("/test_yfinance") # Endopoint to test yfinance functionality
async def root():
    return {"message": "This is an endpoint where we will test yfinance functionality."}