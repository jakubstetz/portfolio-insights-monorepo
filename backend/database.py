'''
This file provides functions for opening and closing a database connection. The purpose of this file is to allow for easy use of FastAPI lifestyle events to open a database connection on API startup and close the connection on API shutdown rather than opening and closing a database connectiaon with every API request.

Go to the following link for information about the PostgreSQL connection string, which is the single argument that's used in the connect() calls below:
https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
'''

import psycopg as postgres

def database_init():
  # Open a connection to our portfolio_insights database
  database_connection = postgres.connect('host=localhost port=5432 dbname=portfolio_insights')
  
  # Open a cursor to perform database operations
  alerts_database = database_connection.cursor()

def database_close():
  # Make the changes to the database persistent
  database_connection.commit()