"""
This file implements all of the functionality in order to manage stock price alerts through interaction with the PostgreSQL database.
"""

import database

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
    cur.execute('''
                INSERT INTO alerts (ticker, price, direction, one_time, creation_date, expiration_date)
                VALUES (%s, %s, %s, %s, NOW(), %s);
                ''', (alert.ticker, alert.price, alert.direction, alert.one_time, alert.expiration_date))
  return True

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