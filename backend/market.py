"""
Development begun using AlgoTrading101 Blog's "yfinance Library – A Complete Guide" article as a reference:
https://algotrading101.com/learn/yfinance-guide/

Full yfinance documentation available here:
https://yfinance-python.org/
"""

import yfinance as yf

def stock_info(ticker):
  """
  Retrieve stock information.
  """
  info = yf.Ticker(ticker).fast_info
  return {
            "ticker": ticker.upper(),
            "price": info["lastPrice"],
            "currency": info.get("currency", "USD")
        }

def stock_price(ticker):
  """
  Retrieve current stock price.
  """
  return yf.Ticker(ticker).fast_info["lastPrice"]