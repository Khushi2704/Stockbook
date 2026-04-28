"""
User model and authentication operations
"""
from database.db import fetch_one, fetch_all, insert
from utils.helpers import hash_password, verify_password


class User:
    """User data model and operations"""
    
    @staticmethod
    def create(username, password):
        """Create a new user"""
        query = """
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """
        try:
            hashed_pwd = hash_password(password)
            user_id = insert(query, (username, hashed_pwd))
            return user_id
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user and return user object if valid"""
        query = "SELECT * FROM users WHERE username = ?"
        user = fetch_one(query, (username,))
        
        if not user:
            return None, "User not found"
        
        if not verify_password(password, user['password']):
            return None, "Invalid password"
        
        # Check if user is active
        if not user['is_active']:
            return None, "User account is inactive. Contact admin for activation."
        
        return user, "Login successful"
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT id, username, is_active, created_at FROM users WHERE id = ?"
        return fetch_one(query, (user_id,))
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        query = "SELECT id, username, is_active, created_at FROM users WHERE username = ?"
        return fetch_one(query, (username,))
    
    @staticmethod
    def get_all():
        """Get all users with their status"""
        query = "SELECT id, username, is_active, created_at FROM users ORDER BY created_at DESC"
        return fetch_all(query)
    
    @staticmethod
    def get_all_with_status():
        """Get all users with formatted status"""
        users = User.get_all()
        result = []
        for user in users:
            # Convert sqlite3.Row to dictionary
            user_dict = dict(user)
            user_dict['status'] = 'Active' if user_dict['is_active'] else 'Inactive'
            result.append(user_dict)
        return result
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        # First verify old password
        query = "SELECT password FROM users WHERE id = ?"
        user = fetch_one(query, (user_id,))
        
        if not user or not verify_password(old_password, user['password']):
            return False
        
        # Update to new password
        hashed_pwd = hash_password(new_password)
        query = "UPDATE users SET password = ? WHERE id = ?"
        from database.db import update
        update(query, (hashed_pwd, user_id))
        return True
    
    @staticmethod
    def exists(username):
        """Check if user exists"""
        query = "SELECT id FROM users WHERE username = ?"
        return fetch_one(query, (username,)) is not None
    
    @staticmethod
    def activate_user(user_id):
        """Activate a user account"""
        query = "UPDATE users SET is_active = 1 WHERE id = ?"
        from database.db import update
        return update(query, (user_id,)) > 0
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate a user account"""
        query = "UPDATE users SET is_active = 0 WHERE id = ?"
        from database.db import update
        return update(query, (user_id,)) > 0
    
    @staticmethod
    def is_active(user_id):
        """Check if user is active"""
        user = User.get_by_id(user_id)
        return user and user['is_active']
