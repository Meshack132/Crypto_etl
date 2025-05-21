import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config.db_config import DB_PATH, TABLE_NAME
import argparse

def get_db_connection():
    """Create and return a database connection"""
    return sqlite3.connect(DB_PATH)

def get_latest_data(limit=10):
    """
    Get the most recent data entries
    Args:
        limit (int): Number of records to return
    Returns:
        pd.DataFrame: DataFrame containing the latest records
    """
    conn = get_db_connection()
    query = f"""
    SELECT * FROM {TABLE_NAME}
    ORDER BY extracted_at DESC
    LIMIT ?
    """
    df = pd.read_sql(query, conn, params=(limit,))
    conn.close()
    return df

def get_coin_history(coin_id, days=7):
    """
    Get historical data for a specific coin
    Args:
        coin_id (str): The coin identifier (e.g., 'bitcoin')
        days (int): Number of days of history to retrieve
    Returns:
        pd.DataFrame: Historical data for the coin
    """
    conn = get_db_connection()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    query = f"""
    SELECT * FROM {TABLE_NAME}
    WHERE coin_id = ? AND extracted_at >= ?
    ORDER BY extracted_at
    """
    df = pd.read_sql(query, conn, params=(coin_id, cutoff_date))
    conn.close()
    return df

def display_summary_stats():
    """Display summary statistics of the collected data"""
    conn = get_db_connection()
    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql(query, conn)
    conn.close()
    
    if df.empty:
        print("No data available in the database.")
        return
    
    print("\n=== Summary Statistics ===")
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['extracted_at'].min()} to {df['extracted_at'].max()}")
    print(f"Coins tracked: {df['coin_id'].nunique()}")
    
    # Latest price stats
    latest = df.sort_values('extracted_at', ascending=False).drop_duplicates('coin_id')
    print("\n=== Latest Prices ===")
    print(latest[['coin_id', 'symbol', 'price_usd', 'price_change_24h']].to_string(index=False))

def plot_coin_history(coin_id, days=7):
    """
    Plot price history for a specific coin
    Args:
        coin_id (str): The coin identifier
        days (int): Number of days to plot
    """
    df = get_coin_history(coin_id, days)
    
    if df.empty:
        print(f"No data available for {coin_id} in the last {days} days.")
        return
    
    plt.figure(figsize=(12, 6))
    plt.plot(pd.to_datetime(df['extracted_at']), df['price_usd'], marker='o')
    plt.title(f'{coin_id.capitalize()} Price History (Last {days} Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def interactive_viewer():
    """Interactive command-line viewer"""
    while True:
        print("\n=== Crypto Data Viewer ===")
        print("1. View latest data")
        print("2. View coin history")
        print("3. Show summary statistics")
        print("4. Plot coin price history")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            limit = input("How many records to show? (default 10): ") or 10
            print(get_latest_data(int(limit)).to_string(index=False))
            
        elif choice == '2':
            coin_id = input("Enter coin ID (e.g., 'bitcoin'): ")
            days = input("How many days of history? (default 7): ") or 7
            print(get_coin_history(coin_id, int(days)).to_string(index=False))
            
        elif choice == '3':
            display_summary_stats()
            
        elif choice == '4':
            coin_id = input("Enter coin ID to plot (e.g., 'bitcoin'): ")
            days = input("How many days to plot? (default 7): ") or 7
            plot_coin_history(coin_id, int(days))
            
        elif choice == '5':
            break
            
        else:
            print("Invalid choice. Please try again.")

def main():
    parser = argparse.ArgumentParser(description='Crypto ETL Data Viewer')
    parser.add_argument('--latest', type=int, nargs='?', const=10, 
                       help='Show latest N records (default: 10)')
    parser.add_argument('--history', type=str, 
                       help='Show history for specific coin ID')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days of history to show')
    parser.add_argument('--plot', type=str, 
                       help='Plot history for specific coin ID')
    parser.add_argument('--stats', action='store_true',
                       help='Show summary statistics')
    parser.add_argument('--interactive', action='store_true',
                       help='Launch interactive viewer')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_viewer()
    elif args.latest:
        print(get_latest_data(args.latest).to_string(index=False))
    elif args.history:
        print(get_coin_history(args.history, args.days).to_string(index=False))
    elif args.plot:
        plot_coin_history(args.plot, args.days)
    elif args.stats:
        display_summary_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()