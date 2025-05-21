import sqlite3
import pandas as pd
from config.db_config import DB_PATH, TABLE_NAME
import argparse

def view_database(limit=10):
    """
    View contents of the SQLite database using pandas display
    Args:
        limit (int): Number of records to display
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Get table info
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n=== Database Tables ===")
        for table in tables:
            print(f"- {table[0]}")
        
        # Display data
        print(f"\n=== Contents of {TABLE_NAME} (latest {limit} records) ===")
        query = f"SELECT * FROM {TABLE_NAME} ORDER BY extracted_at DESC LIMIT ?"
        df = pd.read_sql_query(query, conn, params=(limit,))
        
        if not df.empty:
            # Configure pandas display
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            pd.set_option('display.max_colwidth', 20)
            
            # Display the dataframe
            print(df)
            
            # Show stats
            print("\n=== Summary ===")
            print(f"Total records: {pd.read_sql(f'SELECT COUNT(*) FROM {TABLE_NAME}', conn).iloc[0,0]}")
            print(f"Date range: {pd.read_sql(f'SELECT MIN(extracted_at) FROM {TABLE_NAME}', conn).iloc[0,0]} to "
                  f"{pd.read_sql(f'SELECT MAX(extracted_at) FROM {TABLE_NAME}', conn).iloc[0,0]}")
            print(f"Unique coins: {pd.read_sql(f'SELECT COUNT(DISTINCT coin_id) FROM {TABLE_NAME}', conn).iloc[0,0]}")
        else:
            print("No data found in the table.")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='View Crypto ETL Database')
    parser.add_argument('--limit', type=int, default=10,
                       help='Number of recent records to display')
    args = parser.parse_args()
    view_database(args.limit)