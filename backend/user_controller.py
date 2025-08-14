from fastapi import HTTPException
from dbhelper import DBHelper

db = DBHelper()

class UserController:

    @staticmethod
    def register_user(first_name, last_name, username, phone, email, password, role):
        # Check if the username or email already exists
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s OR email = %s",
            (username, email)
        )
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")

        # Register the new user
        user_id = db.register_user(
            first_name, 
            last_name, 
            username, 
            phone, 
            email, 
            password, 
            role
        )

        if user_id:
            return {"message": "User registered successfully!"}
        else:
            raise HTTPException(status_code=500, detail="User registration failed")

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