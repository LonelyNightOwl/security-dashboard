import os
import subprocess
import hashlib
import pickle
import sqlite3

# Hardcoded credentials (bad practice)
password = "admin123"
secret_key = "hardcoded_secret_key_123"

# SQL Injection vulnerability
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

# Command injection vulnerability
def run_command(user_input):
    os.system("ls " + user_input)
    subprocess.call("echo " + user_input, shell=True)

# Weak hashing
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

# Insecure deserialization
def load_data(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

# Insecure temp file
def write_temp():
    import tempfile
    f = tempfile.mktemp()
    return f