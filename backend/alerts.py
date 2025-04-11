"""
This file implements all of the functionality in order to manage stock price alerts through interaction with the PostgreSQL database.
"""

import database
import market
from datetime import datetime, timezone

def search(search_term):
  """
  Search stock price alerts by a search term.
  """
  ilike_argument = '%' + search_term + '%' # Wildcards (%) used so that substring can be prefix or suffix, or contained within a string
  with database.connection.cursor() as cur:
    cur.execute('SELECT * FROM alerts WHERE ticker ILIKE %s;', (ilike_argument,))
    all_alerts = cur.fetchall()
    return all_alerts # Return corresponding alerts IS THIS GOOD FORM OR SHOULD THERE BE JSON

def create(alert):
  """
  Create a new stock price alert. Note that the alert id will be automatically created in the database using SERIAL.
  """
  with database.connection.cursor() as cur:
    alert = alert.dict()
    cur.execute('''
                INSERT INTO alerts (ticker, price, direction, expiration_time)
                VALUES (%(ticker)s, %(price)s, %(direction)s, %(expiration_time)s) RETURNING alert_id;
                ''', alert)
    database.connection.commit()
    return cur.fetchone()[0] # Return id for new alert

def delete(id):
  """
  Delete a stock price alert by id.
  """
  with database.connection.cursor() as cur:
    cur.execute("DELETE FROM alerts WHERE alert_id = %s RETURNING alert_id;", (id,))
    database.connection.commit()
    return cur.fetchone()[0] # Return id for deleted alert

def evaluate():
  """
  Evaluate all alerts against stock prices to determine if alert should be triggered.
  """
  # Retrieve alerts from database
  with database.connection.cursor() as cur:
    cur.execute('''
                SELECT alert_id, ticker, price, direction
                FROM alerts
                WHERE triggered = false AND expired = false;
                ''')
    alerts = cur.fetchall()

  # Evaluate alerts and trigger as appropriate
  cache = {}
  for id, ticker, price, direction in alerts:
    # Retrieve stock price
    if ticker in cache: stock_price = cache[ticker]
    else:
      stock_price = market.stock_price(ticker)
      cache[ticker] = stock_price

    # Trigger alert if stock price falls within price alert trigger condition
    if (direction == 'below' and price > stock_price) or (direction == 'above' and price < stock_price): trigger(id)

def trigger(id):
  """
  Triggers an alert based on its id.
  """
  with database.connection.cursor() as cur:
    cur.execute('''
                UPDATE alerts
                SET triggered = true, triggered_time = %s, expired = NULL, expiration_time = NULL
                WHERE alert_id = %s;
                ''', (datetime.now(timezone.utc), id))
    database.connection.commit()