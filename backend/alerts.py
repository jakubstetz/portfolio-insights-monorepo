"""
Manage stock price alerts through interaction with the PostgreSQL database.
"""

import database
from datetime import datetime, timezone
from utils.logging import logger


def search(search_term):
    """
    Search stock price alerts by a search term.
    """
    logger.debug("Fetching alerts for search_term: %s", search_term)
    # Use wildcards (%) to match prefix, suffix, or substring
    ilike_argument = "%" + search_term + "%"
    with database.connection.cursor() as cur:
        cur.execute("SELECT * FROM alerts WHERE ticker ILIKE %s;", (ilike_argument,))
        # Extract column names from the result metadata
        keys = [column[0] for column in cur.description]
        all_alerts = cur.fetchall()
        logger.info("Retrieved %d alerts", len(all_alerts))
        # Format results as list of dictionaries for JSON compatibility
        return [dict(zip(keys, row)) for row in all_alerts]


def create(alert):
    """
    Create a new stock price alert. Note that the alert id will be automatically created in the database using SERIAL.
    """
    # Convert Pydantic model to plain dict and set 'expired' status
    alert = alert.dict()
    if alert["expiration_time"]:
        alert["expired"] = False
    else:
        alert["expired"] = None

    # Insert alert into the database
    with database.connection.cursor() as cur:
        cur.execute(
            """
                INSERT INTO alerts (ticker, price, direction, expired, expiration_time)
                VALUES (%(ticker)s, %(price)s, %(direction)s, %(expired)s, %(expiration_time)s) RETURNING alert_id;
                """,
            alert,
        )
        database.connection.commit()
        return cur.fetchone()[0]  # Return the newly created alert id


def delete(id):
    """
    Delete a stock price alert by id.
    """
    with database.connection.cursor() as cur:
        cur.execute("DELETE FROM alerts WHERE alert_id = %s RETURNING alert_id;", (id,))
        database.connection.commit()


def evaluate():
    """
    Evaluate all alerts against stock prices to determine if alert should be triggered.
    """
    # Fetch active, untriggered alerts from the database
    with database.connection.cursor() as cur:
        cur.execute(
            """
                SELECT alert_id, ticker, price, direction
                FROM alerts
                WHERE triggered = false AND expired = false;
                """
        )
        alerts = cur.fetchall()

    # Avoid redundant API calls by caching stock prices
    cache = {}
    for id, ticker, price, direction in alerts:
        # Get stock price (use cached value if available)
        if ticker in cache:
            stock_price = cache[ticker]
        else:
            stock_price = market.stock_price(ticker)
            cache[ticker] = stock_price

        # Trigger alert if stock price meets condition
        if (direction == "below" and price > stock_price) or (
            direction == "above" and price < stock_price
        ):
            trigger(id)


def trigger(id):
    """
    Triggers an alert based on its id.
    """
    with database.connection.cursor() as cur:
        cur.execute(
            """
                UPDATE alerts
                SET triggered = true, triggered_time = %s, expired = NULL, expiration_time = NULL
                WHERE alert_id = %s;
                """,
            (datetime.now(timezone.utc), id),
        )
        database.connection.commit()
