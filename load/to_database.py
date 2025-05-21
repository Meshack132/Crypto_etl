import sqlite3
import pandas as pd
from config.db_config import DB_PATH, TABLE_NAME

def create_database():
    """Creates SQLite database and table if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        coin_id TEXT,
        symbol TEXT,
        name TEXT,
        price_usd REAL,
        market_cap_usd REAL,
        volume_usd REAL,
        price_change_24h REAL,
        extracted_at TEXT,
        PRIMARY KEY (coin_id, extracted_at)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

def load_data(df):
    """
    Loads transformed data into SQLite database
    Args:
        df (pd.DataFrame): Transformed data to load
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        conn.close()
    except Exception as e:
        print(f"Error loading data to database: {e}")
        raise