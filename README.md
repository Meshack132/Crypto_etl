# Crypto Price Tracker ETL Pipeline

A simple but powerful Python pipeline that collects cryptocurrency market data and stores it for analysis.

## What This Does

Every time you run this:
1. **Pulls** the top 10 cryptocurrencies from CoinGecko
2. **Cleans** the data to keep only what matters
3. **Stores** it in a local database with a timestamp

Perfect for tracking price trends over time.

---

## Quick Start

### 1. Get the code
```bash
git clone https://github.com/Meshack132/Crypto_etl.git
cd Crypto_etl
```

### 2. Install requirements
```bash
pip install pandas requests
```

### 3. Run it
```bash
python crypto_price_etl.py
```
You'll see:
```
Extracting crypto data...
Transforming data...
Loading data into DB...
Done.
```

---

## Working With the Data

Your data gets saved in `crypto_prices.db`. Here's how to access it:

### View recent entries
```bash
sqlite3 crypto_prices.db "SELECT * FROM crypto_market ORDER BY extracted_at DESC LIMIT 5;"
```

### See all coins tracked
```bash
sqlite3 crypto_prices.db "SELECT DISTINCT name FROM crypto_market;"
```

---

## Database Structure

Table: `crypto_market`

| Column               | Contains                          |
|----------------------|-----------------------------------|
| id                   | CoinGecko's internal ID           |
| symbol               | Short code like BTC or ETH        |
| name                 | Full name (Bitcoin, Ethereum)     |
| current_price        | Price in USD right now            |
| market_cap           | Total value in USD                |
| total_volume         | 24hr trading volume              |
| price_change_24h     | Percentage change since yesterday |
| extracted_at         | When we recorded this data        |

---

## Where To Take This Next

Some ways to extend this:

- **Automate it** to run every hour (ask me about cron jobs)
- **Add visualizations** with matplotlib or Streamlit
- **Track more coins** by adjusting the API parameters
- **Compare currencies** by adding EUR/ZAR conversions

---

## About Me

I'm Meshack, a developer passionate about Coding and learning 

- GitHub: [@Meshack132](https://github.com/Meshack132)
- LinkedIn: [Let's connect](https://www.linkedin.com/in/meshackmthimkhulu)

---

Free to use under the MIT License. If you build something cool with this, let me know!

---

