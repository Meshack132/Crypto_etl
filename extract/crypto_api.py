import requests
from datetime import datetime
from config.db_config import API_URL, API_PARAMS

def extract_crypto_data():
    """
    Extracts cryptocurrency market data from CoinGecko API
    Returns:
        list: Raw JSON data of cryptocurrency market information
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    try:
        response = requests.get(API_URL, params=API_PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error extracting data from API: {e}")
        raise