import requests
import json
from pathlib import Path
import os
import sqlite3
import logging
import time

class CoinRate:
    def __init__(self,api_key,currency_from = "USD",currency_to = "ILS"):

        self.api_key = api_key
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={currency_from}&to_symbol={currency_to}&apikey={api_key}"
        self.response = requests.get(self.url)

    def get_data(self,days_prev = 5):

        #route for json file
        self.data_dir_json = Path.cwd() / "json_data"
        self.data_dir_json.mkdir(exist_ok=True)
        
        data = self.response.json()
        sorted_items = sorted(data["Time Series FX (Daily)"].items(), key = lambda x:x[0],reverse=True)
        data_desc = dict(sorted_items)
        data_dict = {}
        # return 'days_prev' days from data_desc
        for date_str in list(data_desc.keys())[:days_prev]:
            #close rates are in '4. close' key in json files
            data_dict[date_str] = round(float(data_desc[date_str]['4. close']), 2)
            with open (self.data_dir_json/f"{date_str}.json",'wt',encoding='utf-8') as f:
                json.dump(round(float(data_desc[date_str]['4. close']), 2),f,indent=2)
        return data_dict
    
    def save_as_db(self,name_db,table_name,columns_dict,data_dict):
        #create db if not exist
        self.db_path = Path.cwd() / name_db
        if self.db_path.exists():
            os.remove(self.db_path)
        self.db_path.touch(exist_ok=True)

        #create db
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        columns = ", ".join([f'{col} {dtype}' for col,dtype in columns_dict.items()])
        columns_sql = ", ".join(columns_dict.keys())
        placeholders = ", ".join(["?"] * len(columns_dict))

        col_names = list(columns_dict.keys())

        #create table if not exist
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            {columns},
            PRIMARY KEY ({list(columns_dict.keys())[0]})
            )
            """)
        
        if set(data_dict.keys()) == set(col_names):
            values_list = [tuple(data_dict[c] for c in col_names)]  # שורה אחת
        else:
            values_list = [(k, v) for k, v in data_dict.items()]    # הרבה שורות
           
        cursor.executemany(f"""
            INSERT INTO {table_name} ({columns_sql})
            VALUES ({placeholders})
            """, values_list)

        conn.commit()
        conn.close()
    
    def log_api(self) :

        #route for logs file
        self.data_dir_logs = Path.cwd() / "logs"
        self.data_dir_logs.mkdir(exist_ok=True)
        self.log_file = self.data_dir_logs / "log.log"
        self.log_file.touch(exist_ok=True)  
        url = self.url
        logging.basicConfig(
                            filename=self.log_file, 
                            level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s'
                            )

        try:
            start = time.time()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            response = self.response
            response.raise_for_status()
            duration = time.time() - start
            logging.info(f"API request successful - {url} - Duration: {duration:.2f}")

            log_dict = {
            "timestamp": timestamp,
            "level": "INFO",
            "status": "success",
            "duration": duration
            }

        except Exception as e:
            logging.error(f"API request failed: {e}")

            log_dict = {
            "timestamp": None,
            "level": "ERROR",
            "status": "failure",
            "duration": None
        }
        return log_dict


test = CoinRate("0XYM15TH4D8AIHSE","USD","ILS")
data = test.get_data(7)
result = test.save_as_db("data_coin_rates.db","value_rates",{"Date":"TEXT","close_value":"REAL"},data)
#get log
log_dict =  test.log_api()
log_db = test.save_as_db("logs.db","logs",{"timestamp":"REAL","level":"TEXT","status":"TEXT","duration":"REAL"},log_dict)