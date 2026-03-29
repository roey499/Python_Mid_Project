# CoinRate - FX Data Pipeline

## Overview
This project retrieves foreign exchange (Forex) data from the Alpha Vantage API, stores it as JSON files, saves it into an SQLite database, and logs API request activity.

---

## Features
- Fetch FX daily exchange rates for a given currency pair  
- Store data as JSON files by date  
- Dynamically insert data into an SQLite database  
- Log API request status (success or failure)  

---

## Project Structure
```
project/
│
├── json_data/        # JSON files with FX data
├── logs/             # Log files
├── *.db              # SQLite database files
└── main.py           # Main execution file
```

---

## Usage

### 1. Initialize the class
```python
coin = CoinRate(api_key, "USD", "ILS")
```

---

### 2. Fetch data and save as JSON
```python
data = coin.get_data(days_prev=5)
```

Example output:
```python
{
    "2026-03-27": 3.65,
    "2026-03-26": 3.60
}
```

This also creates JSON files inside the `json_data/` directory.

---

### 3. Save data to SQLite
```python
columns = {
    "date": "TEXT",
    "close": "REAL"
}

coin.save_as_db("rates.db", "fx_rates", columns, data)
```

---

### 4. Log API request
```python
log = coin.log_api()
```

Example output:
```python
{
    "timestamp": "2026-03-29 14:30:12",
    "level": "INFO",
    "status": "success",
    "duration": 0.45
}
```

A log file will also be created at:
```
logs/log.log
```

---

## Database Structure

### FX Table Example
| date       | close |
|------------|-------|
| 2026-03-27 | 3.65  |
| 2026-03-26 | 3.60  |

---

### Logs Table Example
| timestamp           | level | status  | duration |
|--------------------|-------|---------|----------|
| 2026-03-29 14:30   | INFO  | success | 0.45     |

---

## Notes
- The database file is recreated on each run (previous data is deleted)  
- A valid Alpha Vantage API key is required  
- In case of API failure, logs will record an error status  

---

## Requirements
```bash
pip install requests pandas seaborn matplotlib
```

### Standard Library Modules
The following modules are part of Python's standard library and do not require installation:
- json
- pathlib
- os
- sqlite3
- logging
- time

## Author
Roey Maor

