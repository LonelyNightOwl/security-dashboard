import hashlib
import os
from pathlib import Path

def secure_hash(password, salt=None):
    """Secure password hashing using SHA256"""
    if salt is None:
        salt = os.urandom(32)
    return hashlib.sha256((password.encode() + salt)).hexdigest()

def read_file_safely(filepath):
    """Safe file reading with validation"""
    safe_path = Path(filepath).resolve()
    if not safe_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(safe_path, 'r') as f:
        return f.read()

def get_user_from_db(user_id):
    """Parameterized query - safe from SQL injection"""
    import sqlite3
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Using ? placeholders prevents SQL injection
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()

def validate_input(user_input, max_length=100):
    """Input validation and sanitization"""
    if not isinstance(user_input, str):
        raise TypeError("Input must be string")
    if len(user_input) > max_length:
        raise ValueError(f"Input exceeds max length of {max_length}")
    return user_input.strip()