import requests
import json
import pandas as pd
from pathlib import Path
import os
from datetime import datetime, timedelta

#API_KEY = "X8X2LQ8OP5LLZNSH"
#url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=ILS&apikey={API_KEY}"

#respone = requests.get(url)

#data = response.json()


DAYS_PREV = 7
# נתיב לתיקייה הנוכחית של הסקריפט
DATA_DIR = Path(__file__).parent / "json_data"

#dictionary
data = {
  "Meta Data": {
    "1. Information": "Forex Daily Prices (open, high, low, close)",
    "2. From Symbol": "USD",
    "3. To Symbol": "ILS",
    "4. Output Size": "Compact",
    "5. Last Refreshed": "2026-03-20",
    "6. Time Zone": "UTC"
  },
  "Time Series FX (Daily)": {
    "2026-03-20": {
      "1. open": "3.10370",
      "2. high": "3.14340",
      "3. low": "3.09200",
      "4. close": "3.13130"
    },
    "2026-03-19": {
      "1. open": "3.12060",
      "2. high": "3.13350",
      "3. low": "3.09940",
      "4. close": "3.10370"
    },
    "2026-03-18": {
      "1. open": "3.11000",
      "2. high": "3.12500",
      "3. low": "3.09500",
      "4. close": "3.12060"
    }
  }


}

sorted_items = sorted(data["Time Series FX (Daily)"].items(), key = lambda x:x[0],reverse=True)

data_desc = dict(sorted_items)

# return DAYS_PREV days from data_desc
for date_str in list(data_desc.keys())[:DAYS_PREV]:
    print(date_str)
    with open (DATA_DIR/f"{date_str}.json",'wt',encoding='utf-8') as f:
        json.dump(data_desc[date_str],f,indent=2)


exit()




#print(json.dumps(data,indent = 2))

#df = pd.DataFrame(data['open'])

time_series = data_s["Time Series FX (Daily)"]


print(time_series)


exit()
