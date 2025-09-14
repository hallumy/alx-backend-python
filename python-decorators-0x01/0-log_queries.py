import sqlite3
import functools

def log_queries(func):
    """
    Decorator that logs the SQL query before executing the function.

    Args:
        func (function): The function that takes a SQL query as input.

    Returns:
        function: A wrapper function that logs the query and then calls the original function.
    """
    @functools.wraps(func)
    def wrapper(query):
        print("[LOG] SQL Query:", query)  
        return func(query)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
