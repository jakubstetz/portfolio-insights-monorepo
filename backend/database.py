"""
Provides functions for opening and closing a PostgreSQL connection.

Used with FastAPI lifecycle events to open the connection on API startup and close it on shutdown,
instead of reconnecting on every request.

See: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
for connection string format.
"""

import os
import psycopg as postgres

# Initialize to satisfy module scope before first use
connection = None


def init():
    """
    Open a connection to our portfolio_insights database on API startup.
    """
    global connection
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    dbname = os.getenv("DATABASE_NAME")

    dsn = f"host={host} port={port} dbname={dbname}"
    connection = postgres.connect(dsn)


def close():
    """
    Close database connection on API shutdown.
    """
    global connection
    if connection:
        connection.close()
