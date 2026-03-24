# database.py
import sqlite3
import hashlib

class Database:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_users_table()

    def create_users_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def user_exists(self, username=None, email=None):
        cursor = self.conn.cursor()
        if username:
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        elif email:
            cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        return cursor.fetchone() is not None

    def create_user(self, username, password, email):
        try:
            hashed_password = self.hash_password(password)
            with self.conn:
                self.conn.execute(
                    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (username, hashed_password, email)
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = self.hash_password(password)
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        return cursor.fetchone()
        
    def get_all_users(self):
        """Fetch all users from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, email FROM users")
        return cursor.fetchall()

db = Database()
created = db.create_user("admin", "admin123", "admin@example.com")
if created:
    print("✅ Admin user created.")
else:
    print("⚠️ Admin user already exists or username/email is taken.")