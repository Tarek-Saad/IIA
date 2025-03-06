import os
from psycopg2 import pool
from src.config.config import POSTGRESS_URI

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    1,  # Minimum number of connections in the pool
    10,  # Maximum number of connections in the pool
    POSTGRESS_URI
)

# Check if the pool was created successfully
if connection_pool:
    print("Connection pool created successfully")

# Function to get a connection from the pool
def get_connection():
    return connection_pool.getconn()

# Function to return the connection to the pool
def return_connection(conn):
    connection_pool.putconn(conn)

# Function to close all connections in the pool
def close_all_connections():
    connection_pool.closeall()


# if __name__ == "__main__":
#     conn = get_connection()
#     print("Connected to the database.")
#     return_connection(conn)
