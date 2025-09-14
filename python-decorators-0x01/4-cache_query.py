import time
import sqlite3 
import functools

query_cache = {}

def with_db_connection(func):
    """
    Opens a connection to 'users.db', passes it to the function,
    and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Caches the result of SQL queries based on the query string
    to avoid redundant database calls.
    """
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("[CACHE] Returning cached result for query.")
            return query_cache[query]
        else:
            print("[DB] Executing query and caching result.")
            result = func(conn, query)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


users = fetch_users_with_cache(query="SELECT * FROM users")


users_again = fetch_users_with_cache(query="SELECT * FROM users")
