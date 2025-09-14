import sqlite3 
import functools

def with_db_connection(func):
    """
    Opens a connection to 'users.db', passes it to the decorated function,
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

def transactional(func):
    """
    Wraps the function in a database transaction.
    Commits if successful, rolls back if there's an error.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Run the DB logic
            conn.commit()  # Commit changes
            return result
        except Exception as e:
            conn.rollback()  # Roll back on error
            print("Transaction failed. Changes rolled back.")
            raise e  # Re-raise the exception
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')