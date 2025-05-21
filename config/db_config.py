# Database configuration
DB_PATH = "data/crypto_prices.db"
TABLE_NAME = "crypto_market"

# API configuration
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
API_PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': False
}