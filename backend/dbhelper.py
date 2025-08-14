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

    def register_user(self, first_name, last_name, username, phone, email, password, role):
        sql = """
        INSERT INTO users (first_name, last_name, username, phone, email, password, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, username, phone, email, password, role)
        self.mycursor.execute(sql, values)
        self.conn.commit()
        return self.mycursor.lastrowid
