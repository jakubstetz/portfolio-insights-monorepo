"""
Provides functions for opening and closing a PostgreSQL connection.

Used with FastAPI lifecycle events to open the connection on API startup and close it on shutdown,
instead of reconnecting on every request.

See: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
for connection string format.
"""

import psycopg as postgres

# Initialize to satisfy module scope before first use
connection = None


def init():
    """
    Open a connection to our portfolio_insights database on API startup.
    """
    global connection
    connection = postgres.connect("host=localhost port=5432 dbname=portfolio_insights")


def close():
    """
    Close database connection on API shutdown.
    """
    global connection
    if connection:
        connection.close()
