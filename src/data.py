import pandas as pd
from sodapy import Socrata
from datetime import datetime

def getData(limit):
    client = Socrata("data.cityofnewyork.us", None)
    results = client.get("2yzn-sicd", limit = limit)
    results_df = pd.DataFrame.from_records(results)
    return results_df

def parseDate(dateStr):
    return datetime.strptime(dateStr.split(".")[0], "%Y-%m-%dT%H:%M:%S")

def preprocessDataRow(row):
    pickupDatetime = parseDate(row["pickup_datetime"])
    row["pickup_weekday"] = pickupDatetime.weekday()
    row["pickup_time"] = pickupDatetime.time()

    dropoffDatetime = parseDate(row["dropoff_datetime"])
    row["dropoff_weekday"] = dropoffDatetime.weekday()
    row["dropoff_time"] = dropoffDatetime.time()

    row.drop(labels = [
        "pickup_datetime",
        "dropoff_datetime",
        "vendor_id",
        "store_and_fwd_flag",
        "rate_code",
        "payment_type",
        "passenger_count",
        "mta_tax",
        "extra"
    ], errors = "ignore", inplace = True)

    return row

def preprocessData(data):
    data = data.apply(preprocessDataRow, axis = 1)
    
    data["dropoff_latitude"] = data["dropoff_latitude"].astype('float64')
    data["dropoff_longitude"] = data["dropoff_longitude"].astype('float64')
    data["pickup_latitude"] = data["pickup_latitude"].astype('float64')
    data["pickup_longitude"] = data["pickup_longitude"].astype('float64')
    
    data.drop(data[
        (data.dropoff_latitude == 0) | 
        (data.dropoff_longitude == 0) | 
        (data.pickup_latitude == 0) | 
        (data.pickup_longitude == 0)
    ].index, inplace=True)
    
    return data
    

def getPreprocessedData(limit):
    data = getData(limit)
    data = preprocessData(data)
    return data
