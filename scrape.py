import requests
import pandas as pd

def scrape(ticker, expiry):
    url = "https://finviz.com/api/options/" + ticker
    params = {"expiry": expiry}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    req = requests.get(url, headers=headers, params=params)
    req.raise_for_status() # Check for response errors
    dataframe = pd.DataFrame.from_dict(req.json()["options"])
    print(dataframe)

# Usage: scraper(ticker: AAPL, expiry: YYYY-MM-DD)
scrape("AAPL", "2025-06-27")