'''
Development begun using AlgoTrading101 Blog's "yfinance Library – A Complete Guide" article as a reference:
https://algotrading101.com/learn/yfinance-guide/

Full documentation available here:
https://yfinance-python.org/

'''

import yfinance as yf

# show actions (dividends, splits)
# apple.actions

# show dividends
# apple.dividends

# show splits
# apple.splits

# + other methods etc.

def historical_data(ticker):
  ticker_data = yf.Ticker(ticker)
  return ticker_data.info