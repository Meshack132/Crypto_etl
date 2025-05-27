import sqlite3
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "crypto_data.db")

def create_database():
    # Ensure the directory exists
    os.makedirs(DB_DIR, exist_ok=True)

    # Then connect
    conn = sqlite3.connect(DB_PATH)
    return conn
