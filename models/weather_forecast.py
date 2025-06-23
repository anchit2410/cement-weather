# from dotenv import load_dotenv        
# import os
# import pandas as pd
# import requests
# import time
# from requests.exceptions import RequestException
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from threading import Lock

# from constant import MAX_RETRIES, MAX_WORKERS, RETRY_DELAY

# dotenv_path = "env/local.env"
# load_dotenv(dotenv_path)
# APIUrl = os.getenv("API_Url") 

# # Rate limiting setup
# MAX_CALLS_PER_MINUTE = 600
# CALL_INTERVAL = 60 / MAX_CALLS_PER_MINUTE  # seconds between calls
# last_call_time = time.time()
# call_lock = Lock()

# def rate_limited_fetch_weather_data(latitude, longitude):
#     global last_call_time
#     with call_lock:
#         now = time.time()
#         elapsed = now - last_call_time
#         if elapsed < CALL_INTERVAL:
#             time.sleep(CALL_INTERVAL - elapsed)
#         last_call_time = time.time()

#     url = APIUrl
#     params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "daily": "rain_sum",
#         "timezone": "UTC",
#         "forecast_days": 16
#     }


#     for attempt in range(MAX_RETRIES):
#         try:
#             response = requests.get(url, params=params, timeout=30)
#             response.raise_for_status()
#             return response.json()
#         except RequestException as e:
#             print(f"Attempt {attempt+1} failed: {e}")
#             time.sleep(RETRY_DELAY)

#     print(f"Failed to fetch data for latitude {latitude} and longitude {longitude} after {MAX_RETRIES} attempts.")
#     return None

# def process_row(row):
#     data_json = rate_limited_fetch_weather_data(row['Lat'], row['Long'])
#     if data_json is None:
#         return []

#     daily_data = data_json.get('daily', {})
#     results = []
#     for date, rain in zip(daily_data.get('time', []), daily_data.get('rain_sum', [])):
#         results.append({
#             "date": date,
#             "rain_sum": rain,
#             "District Code": row['District Code'],
#             "Cluster": row['Cluster'],
#             "State RSM": row['State RSM'],
#             "RSM Name": row['RSM Name'],
#             "County/District": row['County/District'],
#             "Zone": row['Zone'],
#             "State Standard": row['State Standard'],
#             "Discount RSM": row['Discount RSM'],
#             "Lat": row['Lat'],
#             "Long": row['Long']
#         })
#     return results

# def execute_code(input_data):
#     df = input_data['Sheet1']

#     # Clean the data: convert to string, strip whitespace, and convert to float
#     df['Lat'] = df['Lat'].astype(str).str.strip().astype(float)
#     df['Long'] = df['Long'].astype(str).str.strip().astype(float)

#     results = []

#     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         future_to_row = {executor.submit(process_row, row): row for _, row in df.iterrows()}
#         for future in as_completed(future_to_row):
#             row_results = future.result()
#             results.extend(row_results)

#     # Convert list of results to a dictionary of lists
#     res = {key: [row[key] for row in results] for key in results[0].keys()}
#     return res

# # from datetime import datetime, timedelta
# # from dotenv import load_dotenv        
# # import os
# # import pandas as pd
# # import requests
# # import time
# # from requests.exceptions import RequestException
# # from concurrent.futures import ThreadPoolExecutor, as_completed
# # from threading import Lock

# # # Constants
# # MAX_RETRIES = 3
# # MAX_WORKERS = 10
# # RETRY_DELAY = 2  # seconds

# # # Load environment variables
# # dotenv_path = "env/local.env"
# # load_dotenv(dotenv_path)
# # APIUrl = os.getenv("API_Url") 
# # HistoricalAPIUrl = os.getenv("Historical_API_Url")

# # # Rate limiting setup
# # MAX_CALLS_PER_MINUTE = 600
# # CALL_INTERVAL = 60 / MAX_CALLS_PER_MINUTE
# # last_call_time = time.time()
# # call_lock = Lock()

# # # Calculate dynamic historical date range
# # current_date = datetime.utcnow().date()
# # end_date = current_date - timedelta(days=2)
# # start_date = datetime(2025, 6, 14).date()  # fixed start date

# # HISTORICAL_PARAMS = {
# #     "start_date": start_date.isoformat(),
# #     "end_date": end_date.isoformat(),
# #     "daily": "rain_sum",
# #     "timezone": "UTC"
# # }

# # def rate_limited_fetch_data(url, params):
# #     global last_call_time
# #     with call_lock:
# #         now = time.time()
# #         elapsed = now - last_call_time
# #         if elapsed < CALL_INTERVAL:
# #             time.sleep(CALL_INTERVAL - elapsed)
# #         last_call_time = time.time()

# #     for attempt in range(MAX_RETRIES):
# #         try:
# #             response = requests.get(url, params=params, timeout=30)
# #             response.raise_for_status()
# #             return response.json()
# #         except RequestException as e:
# #             print(f"Attempt {attempt+1} failed: {e}")
# #             time.sleep(RETRY_DELAY)

# #     print(f"Failed to fetch data for params {params} after {MAX_RETRIES} attempts.")
# #     return None

# # def process_row(row):
# #     latitude = row['Lat']
# #     longitude = row['Long']

# #     forecast_params = {
# #         "latitude": latitude,
# #         "longitude": longitude,
# #         "daily": "rain_sum",
# #         "timezone": "UTC",
# #         "forecast_days": 16
# #     }

# #     historical_params = {
# #         **HISTORICAL_PARAMS,
# #         "latitude": latitude,
# #         "longitude": longitude
# #     }

# #     forecast_json = rate_limited_fetch_data(APIUrl, forecast_params)
# #     historical_json = rate_limited_fetch_data(HistoricalAPIUrl, historical_params)

# #     forecast_data = forecast_json.get('daily', {}) if forecast_json else {}
# #     historical_data = historical_json.get('daily', {}) if historical_json else {}

# #     forecast_dates = forecast_data.get('time', [])
# #     forecast_rain = forecast_data.get('rain_sum', [])
# #     historical_dates = historical_data.get('time', [])
# #     historical_rain = historical_data.get('rain_sum', [])

# #     results = []

# #     # Add forecast data
# #     for date, rain in zip(forecast_dates, forecast_rain):
# #         results.append({
# #             "date": date,
# #             "Forecast_rain_sum": rain,
# #             "Historical_rain_sum": None,
# #             "District Code": row['District Code'],
# #             "Cluster": row['Cluster'],
# #             "State RSM": row['State RSM'],
# #             "RSM Name": row['RSM Name'],
# #             "County/District": row['County/District'],
# #             "Zone": row['Zone'],
# #             "State Standard": row['State Standard'],
# #             "Discount RSM": row['Discount RSM'],
# #             "Lat": latitude,
# #             "Long": longitude
# #         })

# #     # Add historical-only data
# #     for date, rain in zip(historical_dates, historical_rain):
# #         if date not in forecast_dates:
# #             results.append({
# #                 "date": date,
# #                 "Forecast_rain_sum": None,
# #                 "Historical_rain_sum": rain,
# #                 "District Code": row['District Code'],
# #                 "Cluster": row['Cluster'],
# #                 "State RSM": row['State RSM'],
# #                 "RSM Name": row['RSM Name'],
# #                 "County/District": row['County/District'],
# #                 "Zone": row['Zone'],
# #                 "State Standard": row['State Standard'],
# #                 "Discount RSM": row['Discount RSM'],
# #                 "Lat": latitude,
# #                 "Long": longitude
# #             })

# #     return results

# # def execute_code(input_data):
# #     df = input_data['Sheet1']

# #     df['Lat'] = df['Lat'].astype(str).str.strip().astype(float)
# #     df['Long'] = df['Long'].astype(str).str.strip().astype(float)

# #     results = []

# #     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
# #         future_to_row = {executor.submit(process_row, row): row for _, row in df.iterrows()}
# #         for future in as_completed(future_to_row):
# #             row_results = future.result()
# #             results.extend(row_results)

# #     res = {key: [row[key] for row in results] for key in results[0].keys()}
# #     pd.DataFrame(res).to_csv("consolidated_weather_data.csv", index=False)
# #     print("✅ Weather data saved to consolidated_weather_data.csv")
# #     return res



# from dotenv import load_dotenv        
# import os
# import pandas as pd
# import requests
# import time
# from requests.exceptions import RequestException
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from threading import Lock

# from constant import MAX_RETRIES, MAX_WORKERS, RETRY_DELAY

# dotenv_path = "env/local.env"
# load_dotenv(dotenv_path)
# APIUrl = os.getenv("API_Url") 

# # Rate limiting setup
# MAX_CALLS_PER_MINUTE = 600
# CALL_INTERVAL = 60 / MAX_CALLS_PER_MINUTE  # seconds between calls
# last_call_time = time.time()
# call_lock = Lock()

# def rate_limited_fetch_weather_data(latitude, longitude):
#     global last_call_time
#     with call_lock:
#         now = time.time()
#         elapsed = now - last_call_time
#         if elapsed < CALL_INTERVAL:
#             time.sleep(CALL_INTERVAL - elapsed)
#         last_call_time = time.time()

#     url = APIUrl
#     params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "daily": "rain_sum",
#         "timezone": "UTC",
#         "forecast_days": 16
#     }


#     for attempt in range(MAX_RETRIES):
#         try:
#             response = requests.get(url, params=params, timeout=30)
#             response.raise_for_status()
#             return response.json()
#         except RequestException as e:
#             print(f"Attempt {attempt+1} failed: {e}")
#             time.sleep(RETRY_DELAY)

#     print(f"Failed to fetch data for latitude {latitude} and longitude {longitude} after {MAX_RETRIES} attempts.")
#     return None

# def process_row(row):
#     data_json = rate_limited_fetch_weather_data(row['Lat'], row['Long'])
#     if data_json is None:
#         return []

#     daily_data = data_json.get('daily', {})
#     results = []
#     for date, rain in zip(daily_data.get('time', []), daily_data.get('rain_sum', [])):
#         results.append({
#             "date": date,
#             "rain_sum": rain,
#             "District Code": row['District Code'],
#             "Cluster": row['Cluster'],
#             "State RSM": row['State RSM'],
#             "RSM Name": row['RSM Name'],
#             "County/District": row['County/District'],
#             "Zone": row['Zone'],
#             "State Standard": row['State Standard'],
#             "Discount RSM": row['Discount RSM'],
#             "Lat": row['Lat'],
#             "Long": row['Long']
#         })
#     return results

# def execute_code(input_data):
#     df = input_data['Sheet1']

#     # Clean the data: convert to string, strip whitespace, and convert to float
#     df['Lat'] = df['Lat'].astype(str).str.strip().astype(float)
#     df['Long'] = df['Long'].astype(str).str.strip().astype(float)

#     results = []

#     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         future_to_row = {executor.submit(process_row, row): row for _, row in df.iterrows()}
#         for future in as_completed(future_to_row):
#             row_results = future.result()
#             results.extend(row_results)

#     # Convert list of results to a dictionary of lists
#     res = {key: [row[key] for row in results] for key in results[0].keys()}
#     return res





# from dotenv import load_dotenv        
# import os
# import pandas as pd
# import requests
# import time
# from requests.exceptions import RequestException
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from threading import Lock

# from constant import MAX_RETRIES, MAX_WORKERS, RETRY_DELAY

# dotenv_path = "env/local.env"
# load_dotenv(dotenv_path)
# APIUrl = os.getenv("API_Url") 

# # Rate limiting setup
# MAX_CALLS_PER_MINUTE = 600
# CALL_INTERVAL = 60 / MAX_CALLS_PER_MINUTE  # seconds between calls
# last_call_time = time.time()
# call_lock = Lock()

# def rate_limited_fetch_weather_data(latitude, longitude):
#     global last_call_time
#     with call_lock:
#         now = time.time()
#         elapsed = now - last_call_time
#         if elapsed < CALL_INTERVAL:
#             time.sleep(CALL_INTERVAL - elapsed)
#         last_call_time = time.time()

#     url = APIUrl
#     params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "daily": "rain_sum",
#         "timezone": "UTC",
#         "forecast_days": 16
#     }


#     for attempt in range(MAX_RETRIES):
#         try:
#             response = requests.get(url, params=params, timeout=30)
#             response.raise_for_status()
#             return response.json()
#         except RequestException as e:
#             print(f"Attempt {attempt+1} failed: {e}")
#             time.sleep(RETRY_DELAY)

#     print(f"Failed to fetch data for latitude {latitude} and longitude {longitude} after {MAX_RETRIES} attempts.")
#     return None

# def process_row(row):
#     data_json = rate_limited_fetch_weather_data(row['Lat'], row['Long'])
#     if data_json is None:
#         return []

#     daily_data = data_json.get('daily', {})
#     results = []
#     for date, rain in zip(daily_data.get('time', []), daily_data.get('rain_sum', [])):
#         results.append({
#             "date": date,
#             "rain_sum": rain,
#             "District Code": row['District Code'],
#             "Cluster": row['Cluster'],
#             "State RSM": row['State RSM'],
#             "RSM Name": row['RSM Name'],
#             "County/District": row['County/District'],
#             "Zone": row['Zone'],
#             "State Standard": row['State Standard'],
#             "Discount RSM": row['Discount RSM'],
#             "Lat": row['Lat'],
#             "Long": row['Long']
#         })
#     return results

# def execute_code(input_data):
#     df = input_data['Sheet1']

#     # Clean the data: convert to string, strip whitespace, and convert to float
#     df['Lat'] = df['Lat'].astype(str).str.strip().astype(float)
#     df['Long'] = df['Long'].astype(str).str.strip().astype(float)

#     results = []

#     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         future_to_row = {executor.submit(process_row, row): row for _, row in df.iterrows()}
#         for future in as_completed(future_to_row):
#             row_results = future.result()
#             results.extend(row_results)

#     # Convert list of results to a dictionary of lists
#     res = {key: [row[key] for row in results] for key in results[0].keys()}
#     return res

from datetime import datetime, timedelta
from dotenv import load_dotenv        
import os
import pandas as pd
import requests
import time
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Constants
MAX_RETRIES = 3
MAX_WORKERS = 10
RETRY_DELAY = 2  # seconds

# Load environment variables
dotenv_path = "env/local.env"
load_dotenv(dotenv_path)
APIUrl = os.getenv("API_Url") 
HistoricalAPIUrl = os.getenv("Historical_API_Url")

# Rate limiting setup
MAX_CALLS_PER_MINUTE = 600
CALL_INTERVAL = 60 / MAX_CALLS_PER_MINUTE
last_call_time = time.time()
call_lock = Lock()

# Calculate dynamic historical date range
current_date = datetime.utcnow().date()
end_date = current_date
start_date = datetime(2025, 6, 14).date()  # fixed start date

HISTORICAL_PARAMS = {
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    "daily": "precipitation_sum",
    "timezone": "UTC"
}

def rate_limited_fetch_data(url, params):
    global last_call_time
    with call_lock:
        now = time.time()
        elapsed = now - last_call_time
        if elapsed < CALL_INTERVAL:
            time.sleep(CALL_INTERVAL - elapsed)
        last_call_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(RETRY_DELAY)

    print(f"Failed to fetch data for params {params} after {MAX_RETRIES} attempts.")
    return None

def process_row(row):
    latitude = row['Lat']
    longitude = row['Long']

    forecast_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "precipitation_sum",
        "timezone": "UTC",
        "forecast_days": 16
    }

    historical_params = {
        **HISTORICAL_PARAMS,
        "latitude": latitude,
        "longitude": longitude
    }

    forecast_json = rate_limited_fetch_data(APIUrl, forecast_params)
    historical_json = rate_limited_fetch_data(HistoricalAPIUrl, historical_params)

    forecast_data = forecast_json.get('daily', {}) if forecast_json else {}
    historical_data = historical_json.get('daily', {}) if historical_json else {}

    forecast_dates = forecast_data.get('time', [])
    forecast_rain = forecast_data.get('precipitation_sum', [])
    historical_dates = historical_data.get('time', [])
    historical_rain = historical_data.get('precipitation_sum', [])

    results = []

    

    # Add historical-only data
    for date, rain in zip(historical_dates, historical_rain):
        if date not in forecast_dates:
            results.append({
                "date": date,
                "rain_sum": None,
                "Historical_rain_sum": rain,
                "District Code": row['District Code'],
                "Cluster": row['Cluster'],
                "State RSM": row['State RSM'],
                "RSM Name": row['RSM Name'],
                "County/District": row['County/District'],
                "Zone": row['Zone'],
                "State Standard": row['State Standard'],
                "Discount RSM": row['Discount RSM'],
                "Lat": latitude,
                "Long": longitude
            })
    
    # Add forecast data
    for date, rain in zip(forecast_dates, forecast_rain):
        results.append({
            "date": date,
            "rain_sum": rain,
            "Historical_rain_sum": None,
            "District Code": row['District Code'],
            "Cluster": row['Cluster'],
            "State RSM": row['State RSM'],
            "RSM Name": row['RSM Name'],
            "County/District": row['County/District'],
            "Zone": row['Zone'],
            "State Standard": row['State Standard'],
            "Discount RSM": row['Discount RSM'],
            "Lat": latitude,
            "Long": longitude
        })
        

    return results

def execute_code(input_data):
    df = input_data['Sheet1']

    df['Lat'] = df['Lat'].astype(str).str.strip().astype(float)
    df['Long'] = df['Long'].astype(str).str.strip().astype(float)

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_row = {executor.submit(process_row, row): row for _, row in df.iterrows()}
        for future in as_completed(future_to_row):
            row_results = future.result()
            results.extend(row_results)

    res = {key: [row[key] for row in results] for key in results[0].keys()}
    # pd.DataFrame(res).to_csv("consolidated_weather_data.csv", index=False)
    print("✅ Weather data saved to consolidated_weather_data.csv")
    return res
