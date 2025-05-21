import pandas as pd
from datetime import datetime

def transform_data(raw_data):
    """
    Transforms raw API data into structured DataFrame
    Args:
        raw_data (list): Raw JSON data from API
    Returns:
        pd.DataFrame: Transformed and cleaned data
    """
    if not raw_data:
        raise ValueError("No data provided for transformation")
    
    try:
        df = pd.DataFrame(raw_data)
        
        # Select and rename columns
        columns_mapping = {
            "id": "coin_id",
            "symbol": "symbol",
            "name": "name",
            "current_price": "price_usd",
            "market_cap": "market_cap_usd",
            "total_volume": "volume_usd",
            "price_change_percentage_24h": "price_change_24h"
        }
        df = df[list(columns_mapping.keys())].rename(columns=columns_mapping)
        
        # Add extraction timestamp
        df["extracted_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        return df
    except Exception as e:
        print(f"Error transforming data: {e}")
        raise