import os
import subprocess
import sqlite3

# Hardcoded credentials
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

def execute_user_command(cmd):
    """Unsafe command execution"""
    os.system("echo " + cmd)
    subprocess.call(cmd, shell=True)

def get_user_data(user_id):
    """SQL Injection vulnerability"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    cursor.execute(query)
    return cursor.fetchall()

def weak_hash(password):
    """Weak hashing"""
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

def deserialize_data(data):
    """Insecure deserialization"""
    import pickle
    return pickle.loads(data)