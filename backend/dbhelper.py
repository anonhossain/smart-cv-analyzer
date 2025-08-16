from copy import Error
from fastapi import HTTPException
import mysql.connector

# Your env.py file with host, user, password, database

class DBHelper:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="smart_resume_analyzer"
        )
        self.mycursor = self.conn.cursor(dictionary=True)

    # def register_user(self, first_name, last_name, username, phone, email, password, role):
    #     sql = """
    #     INSERT INTO users (first_name, last_name, username, phone, email, password, role)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s)
    #     """
    #     values = (first_name, last_name, username, phone, email, password, role)
    #     self.mycursor.execute(sql, values)
    #     self.conn.commit()
    #     return self.mycursor.lastrowid

    def register_user(self, first_name, last_name, username, phone, email, password,role):
        try:
            # Check if the username, email, or phone already exists
            self.mycursor.execute("SELECT * FROM users WHERE username=%s OR email=%s OR phone=%s",
                                  (username, email, phone))
            if self.mycursor.fetchone():
                return -1  # User already exists

            self.mycursor.execute(
    "INSERT INTO users (first_name, last_name, username, phone, email, password, `role`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    (first_name, last_name, username, phone, email, password, role)
)
            self.conn.commit()
            return self.mycursor.lastrowid  # Return the ID of the newly created user
        except mysql.connector.Error as e:
            print(f"Error during registration: {e}")
            return -1

    def search(self, identifier, password):
        # Searching by email, phone, or username
        self.mycursor.execute("""
        SELECT * FROM users WHERE (email = %s OR phone = %s OR username = %s) AND password = %s
        """, (identifier, identifier, identifier, password))

        data = self.mycursor.fetchall()
        return data
    
    def search(self, identifier, password):
        # Searching by email, phone, or username
        self.mycursor.execute("""
        SELECT * FROM users WHERE (email = %s OR phone = %s OR username = %s) AND password = %s
        """, (identifier, identifier, identifier, password))

        data = self.mycursor.fetchall()
        return data
    
    # Fetch all users
    def get_all_users(self):
        self.mycursor.execute("SELECT * FROM users")
        rows = self.mycursor.fetchall()
        return [dict(row) for row in rows]  # convert sqlite3.Row → dict
    
    def update_user(self, user_id: int, data: dict):
        query = """
        UPDATE users
        SET first_name=%s, last_name=%s, username=%s, phone=%s, email=%s, role=%s
        WHERE id=%s
        """
        values = (
            data["first_name"],
            data["last_name"],
            data["username"],
            data["phone"],
            data["email"],
            data["role"],
            user_id
        )
        try:
            self.mycursor.execute(query, values)
            self.conn.commit()
            return True
        except Error as e:
            print("DB update error:", e)
            return False