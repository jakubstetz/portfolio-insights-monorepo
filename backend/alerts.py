"""
This file implements all of the functionality in order to manage stock price alerts through interaction with the PostgreSQL database.
"""

import database
import market
from datetime import datetime

def get(id):
  """
  Get stock price alert by id.
  """
  with database.connection.cursor() as cur:
    cur.execute('SELECT * FROM alerts WHERE alert_id = %s;', (id,))
    return cur.fetchone()

def create(alert):
  """
  Create a new stock price alert. Note that the alert id will be automatically created in the database using SERIAL.
  """
  with database.connection.cursor() as cur:
    alert = alert.dict()
    cur.execute('''
                INSERT INTO alerts (ticker, price, direction, expiration_date)
                VALUES (%(ticker)s, %(price)s, %(direction)s, %(expiration_date)s) RETURNING alert_id;
                ''', alert)
    return cur.fetchone()

def delete(id):
  """
  Delete a stock price alert by id.
  """
  with database.connection.cursor() as cur:
    cur.execute("DELETE FROM alerts WHERE alert_id = %s RETURNING alert_id;", (id,))
    return cur.fetchone()

def update(id):
  """
  Update a stock price alert by id.
  """

def evaluate():
  """
  Evaluate all alerts against stock prices to determine if alert should be triggered.
  """
  # Retrieve alerts from database
  with database.connection.cursor() as cur:
    cur.execute('SELECT alert_id, ticker, price, direction FROM alerts WHERE triggered = false;')
    alerts = cur.fetchall()

  # Evaluate alerts and trigger as appropriate
  checked = {} # Dictionary for caching checked alerts with associated price
  for id, ticker, price, direction in alerts: # Iterate through returned alerts
    # Retrieve stock price
    if ticker in checked: # Stock price has already been retreived
      stock_price = checked[ticker] # Retrieve cached stock price
    else: # Stock price has not yet been retreived
      stock_price = market.stock_price(ticker) # Retrieve current stock price using yfinance
      checked[ticker] = stock_price # Cache current stock price

    # Check alert price against actual stock price
    if (direction == 'below' and price > stock_price) or (direction == 'above' and price < stock_price):
      trigger(id)

def trigger(id):
  """
  Triggers an alert based on its id.
  """
  with database.connection.cursor() as cur:
    cur.execute('''
                UPDATE alerts
                SET triggered = true, triggered_time = %s
                WHERE alert_id = %s;
                ''', (datetime.now(), id))