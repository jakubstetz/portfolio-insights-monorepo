"""
Started using AlgoTrading101's “yfinance Library – A Complete Guide” as a reference:
https://algotrading101.com/learn/yfinance-guide/

Official documentation:
https://yfinance-python.org/
"""

import yfinance as yf


def ping():
    """
    Health check function for verifying API connectivity with stock market via yfinance.
    """
    try:
        data = yf.Ticker("SPY").fast_info
        return "lastPrice" in data and data["lastPrice"] is not None
    except:
        return False


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


def is_valid_alert(ticker, price, direction):
    """
    Check proposed alert against market to see if it's valid.
    """
    try:
        stock = yf.Ticker(ticker).fast_info
        current_price = stock.get("lastPrice")
        if current_price is None:
            raise ValueError("Missing current price.")
    except Exception:
        return {"valid": False, "message": "Ticker not found or data unavailable."}

    if direction == "above" and current_price > price:
        return {
            "valid": False,
            "message": f"Current price is ${current_price:.2f}, already above ${price:.2f}.",
        }
    if direction == "below" and current_price < price:
        return {
            "valid": False,
            "message": f"Current price is ${current_price:.2f}, already below ${price:.2f}.",
        }

    return {"valid": True, "message": "Valid alert"}
