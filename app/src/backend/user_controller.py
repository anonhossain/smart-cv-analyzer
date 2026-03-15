from fastapi import HTTPException
from dbhelper import DBHelper

db = DBHelper()

class UserController:

    @staticmethod
    def register_user(user):
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s OR email = %s",
            (user.username, user.email)
        )
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")

        user_id = db.register_user(
            user.first_name, 
            user.last_name, 
            user.username, 
            user.phone, 
            user.email, 
            user.password, 
            user.role
        )

        if user_id:
            return {"message": "User registered successfully!"}
        else:
            raise HTTPException(status_code=500, detail="User registration failed")

    @staticmethod
    def login(username: str, password: str):
        data = db.search(username, password)

        print("DB search returned:", data)  # Debugging

        if not data:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email, phone number, or username/password"
            )

        user = None

        # Case 1: data is already a dict
        if isinstance(data, dict):
            user = data

        # Case 2: data is list of dicts
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            user = data[0]

        # Case 3: data is list of tuples/rows (e.g. raw SQL fetchall)
        elif isinstance(data, (list, tuple)) and len(data) > 0 and isinstance(data[0], (list, tuple)):
            row = data[0]
            return {
                "message": "Login successful",
                "user": {
                    "id": row[0],
                    "name": f"{row[1]} {row[2]}",
                    "role": row[7]
                }
            }

        else:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected data format from database: {type(data)}"
            )

        # Unified return for dict-style user
        return {
            "message": "Login successful",
            "user": {
                "id": user.get("id"),
                "name": f"{user.get('first_name', '')} {user.get('last_name', '')}",
                "role": user.get("role")
            }
        }

    def search(self, identifier, password):
        # Searching by email, phone, or username
        self.mycursor.execute("""
        SELECT * FROM users WHERE (email = %s OR phone = %s OR username = %s) AND password = %s
        """, (identifier, identifier, identifier, password))

        data = self.mycursor.fetchall()
        return data

    @staticmethod
    def get_users():
        """Fetch all users from the database."""
        db.mycursor.execute("SELECT * FROM users")
        users = db.mycursor.fetchall()
        return users

    @staticmethod
    def get_dashboard_info():
        """Fetch counts of users by role."""
        db.mycursor.execute("SELECT * FROM users")
        users = db.mycursor.fetchall()
        candidate = 0
        admin = 0
        hr = 0

        for user in users:
            role = user[7]  # Assuming the 8th column is the role
            if role == 'Candidate':
                candidate += 1
            elif role == 'Admin':
                admin += 1
            elif role == 'HR':
                hr += 1

        return {"candidate": candidate, "admin": admin, "hr": hr}
    
    @staticmethod
    def delete_user(user_id: int):
        db.mycursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        db.conn.commit()
        return {"message": "User deleted successfully!"}
    
    @staticmethod
    def update_user(user_id: int, user):
        # Check if the user exists
        cursor = db.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update user info
        update_query = """
            UPDATE users 
            SET first_name = %s, last_name = %s, username = %s, phone = %s, email = %s, role = %s
            WHERE id = %s
        """
        cursor.execute(
            update_query, 
            (user.first_name, user.last_name, user.username, user.phone, user.email, user.role, user_id)
        )
        db.conn.commit()

        return {
            "id": user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "role": user.role
        }