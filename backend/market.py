"""
Started using AlgoTrading101's “yfinance Library – A Complete Guide” as a reference:
https://algotrading101.com/learn/yfinance-guide/

Official documentation:
https://yfinance-python.org/
"""

import yfinance as yf


def stock_info(ticker, period, interval):
    """
    Retrieve stock information.
    """
    ticker_object = yf.Ticker(ticker)
    info = ticker_object.fast_info
    hist = ticker_object.history(period=period, interval=interval)

    if hist.empty:
        raise ValueError("No historical data found")
    
    prices = [
        {"date": date.strftime("%Y-%m-%d"), "close": round(row["Close"], 2)}
        for date, row in hist.iterrows()
    ]

    return {
        "ticker": ticker.upper(),
        "price": info["lastPrice"],
        "currency": info.get("currency", "USD"),
        "prices": prices,
    }


def stock_price(ticker):
    """
    Retrieve current stock price.
    """
    return yf.Ticker(ticker).fast_info["lastPrice"]
