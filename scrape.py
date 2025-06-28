import requests
import pandas as pd
from datetime import date

def get_data(url, headers, params):
      req = requests.get(url, headers=headers, params=params)
      req.raise_for_status()  # Check for response errors
      return req.json()

def scrape(ticker_list, expiry_list):
    data = []
    if (not ticker_list):
        print("No ticker(s) specified!")
        exit(-1)
    if (not expiry_list):
        print("No expiry date(s) specified!")
        exit(-1)

    for ticker in ticker_list:
        url = "https://finviz.com/api/options/" + ticker
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}  # May cause issues if not using Windows + Chrome - not tested
        ticker_expiries = get_data(url + "/expiries", headers, {})
        for expiry in expiry_list:
                if " - " in expiry:  # Range of dates
                        start = date.fromisoformat(expiry[0:10])
                        end = date.fromisoformat(expiry[13:])
                        if start > end:
                              print("Invalid date range!")
                              exit(-1)
                        for ticker_exp in ticker_expiries:
                              exp = date.fromisoformat(ticker_exp)
                              if start <= exp and exp <= end:
                                    data.append(get_data(url, headers, {"expiry" : ticker_exp}))
                elif expiry in ticker_expiries:  # Single dates
                      data.append(get_data(url, headers, {"expiry" : expiry}))
                else:
                      print("No " + ticker + " options expire on " + expiry + ".")
    dataframe = pd.DataFrame(data=data).transpose()
    print(dataframe)

# Usage: scraper(ticker: ["AAPL", "MSFT", ...], expiry: ["YYYY-MM-DD - YYYY-MM-DD", ...] | ["YYYY-MM-DD", "YYYY-MM-DD", ...])
# Returns list of dataframes, each corresponding to a unique ticker and expiry date
dataframes = scrape(["AAPL", "MSFT", "SIGMABOY"], ["2025-07-01 - 2025-07-10", "2025-07-03"])