import os
import sys
import pymysql # Change this

# When running this module directly, Python's import path may not include
# the project's `app/src` directory so `backend` cannot be resolved.
# Add the `app/src` directory (three levels up from this file) to sys.path
# so `from backend.core.config import settings` works both when running
# as a script and when used as a package.
_ROOT_SRC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT_SRC not in sys.path:
    sys.path.insert(0, _ROOT_SRC)

from backend.core.config import settings

def init_db():
    try:
        # PyMySQL uses 'host', 'user', 'password' just like before
        conn = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}")
        cursor.execute(f"USE {settings.DB_NAME}")

        users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            phone VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(users_table_query)
        conn.commit()
        print("Database and tables verified successfully via PyMySQL.")
        cursor.close()
        conn.close()
    except Exception as err:
        # Print full error so user can see auth/plugin issues
        print(f"Failed to initialize database: {err}")

def get_db_connection():
    try:
        return pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor # Optional: returns rows as dicts
        )
    except Exception as err:
        print(f"Error: {err}")
        return None
    
# if __name__ == "__main__":
#     # First try to create the database and tables
#     init_db()

#     # Then try to obtain a connection to the configured database
#     conn = get_db_connection()
#     if conn is None:
#         print("Database connection test failed. See errors above for details.")
#     else:
#         print("Database connection test successful.")
#         try:
#             conn.close()
#         except Exception:
#             pass