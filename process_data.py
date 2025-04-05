import pandas as pd
import numpy as np
from datetime import date, timedelta
import holidays

canadian_holidays = holidays.Canada(prov="AB")  # "AB" for Alberta

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"
    
def is_solar(data):
    """
    Wrapper function to determine if the solar radiation is zero or not.
    """
    data["Is Solar"] = 1
    data["Zero_Volume"] = np.where(
        (data["Hour"].between(1, 7)) | (data["Hour"].between(20, 23)), 1, 0
    )
    return data

def process_data_generation(date):
    data = pd.read_csv("weather.csv")
    data["time"] = pd.to_datetime(data["time"])
    data.rename(columns={
    "time": "Date",
    "relativehumidity_2m": "Humidity Inst. (%)",
    "apparent_temperature": "Air Temp. Inst. (Ã\x82Â°C)",
    "windspeed_10m": "Wind Speed 10 m Syno. (km/h)",
    "winddirection_10m": "Wind Dir. 10 m Syno. (Ã\x82Â°)",
    "precipitation": "Precip. (mm)",
    "shortwave_radiation": "Incoming Solar Rad. (W/m2)",
    }, inplace=True)

    columns = [
        "Date",
        "Air Temp. Inst. (Ã\x82Â°C)",
        "Humidity Inst. (%)",
        "Wind Speed 10 m Syno. (km/h)",
        "Wind Dir. 10 m Syno. (Ã\x82Â°)",
        "Precip. (mm)",
        "Incoming Solar Rad. (W/m2)"
    ]
    

    data = data[data["Date"] == pd.to_datetime(date)]

    columns_to_drop = [column for column in data.columns if column not in columns]
    data.drop(columns=columns_to_drop, axis=1, inplace=True)

    data["Wind Speed 10 m Avg. (km/h)"] = data["Wind Speed 10 m Syno. (km/h)"].rolling(window=24, min_periods=1).mean()

    data["Wind Dir. 10 m Avg. (Ã\x82Â°)"] = data["Wind Dir. 10 m Syno. (Ã\x82Â°)"].rolling(window=24, min_periods=1).mean()

    data["Year"]  = data["Date"].dt.year
    data["Month"]  = data["Date"].dt.month
    data["Day"]  = data["Date"].dt.day
    data["Hour"]  = data["Date"].dt.hour

    # Cyclical encoding for month and hour
    data["Month_sin"] = np.sin(2 * np.pi * data["Month"] / 12)
    data["Month_cos"] = np.cos(2 * np.pi * data["Month"] / 12)
    data["Hour_sin"] = np.sin(2 * np.pi * data["Hour"] / 24)
    data["Hour_cos"] = np.cos(2 * np.pi * data["Hour"] / 24)

    data["Season_Summer"] = np.where(data["Month"].isin([6, 7, 8]), True, False)
    data["Season_Winter"] = np.where(data["Month"].isin([12, 1, 2]), True, False)
    data["Season_Spring"] = np.where(data["Month"].isin([3, 4, 5]), True, False)

    

    data['is_weekend'] = data['Date'].dt.weekday >= 5
    data['is_public_holiday'] = data['Date'].isin(canadian_holidays)

    data.drop("Date", axis=1, inplace=True)  # Drop the original date column

    

    # data["is_solar"] = 0
    data["Zero_Volume"] = 0
    data["Is Solar"] = 0

    data.sort_index(inplace=True)  # Ensure the data is sorted by
    print(data.columns.tolist())
    
    return data


def process_data_load(date):
    data = pd.read_csv("weather.csv")
    data["time"] = pd.to_datetime(data["time"])
    data.rename(columns={
    "time": "Date",
    "relativehumidity_2m": "Humidity Inst. (%)",
    "apparent_temperature": "Air Temp. Inst. (Â°C)",
    "windspeed_10m": "Wind Speed 10 m Syno. (km/h)",
    "winddirection_10m": "Wind Dir. 10 m Syno. (Â°)",
    "precipitation": "Precip. (mm)",
    "shortwave_radiation": "Incoming Solar Rad. (W/m2)",
    }, inplace=True)

    columns = [
        "Date",
        "Air Temp. Inst. (Â°C)",
        "Humidity Inst. (%)",
        "Wind Speed 10 m Syno. (km/h)",
        "Wind Dir. 10 m Syno. (Â°)",
        "Precip. (mm)",
        "Incoming Solar Rad. (W/m2)"
    ]
    

    data = data[data["Date"] == pd.to_datetime(date)]

    columns_to_drop = [column for column in data.columns if column not in columns]
    data.drop(columns=columns_to_drop, axis=1, inplace=True)

    data["Wind Speed 10 m Avg. (km/h)"] = data["Wind Speed 10 m Syno. (km/h)"].rolling(window=24, min_periods=1).mean()

    data["Wind Dir. 10 m Avg. (Â°)"] = data["Wind Dir. 10 m Syno. (Â°)"].rolling(window=24, min_periods=1).mean()




    data["Year"]  = data["Date"].dt.year
    data["Month"]  = data["Date"].dt.month
    data["Day"]  = data["Date"].dt.day
    data["Hour"]  = data["Date"].dt.hour

    # Cyclical encoding for month and hour
    data["Month_sin"] = np.sin(2 * np.pi * data["Month"] / 12)
    data["Month_cos"] = np.cos(2 * np.pi * data["Month"] / 12)
    data["Hour_sin"] = np.sin(2 * np.pi * data["Hour"] / 24)
    data["Hour_cos"] = np.cos(2 * np.pi * data["Hour"] / 24)

    data["Season_Summer"] = np.where(data["Month"].isin([6, 7, 8]), True, False)
    data["Season_Winter"] = np.where(data["Month"].isin([12, 1, 2]), True, False)
    data["Season_Spring"] = np.where(data["Month"].isin([3, 4, 5]), True, False)
    
    
    

    data['is_weekend'] = data['Date'].dt.weekday >= 5
    data['is_public_holiday'] = data['Date'].isin(canadian_holidays)

    data.drop("Date", axis=1, inplace=True)  # Drop the original date column

    

    # data["is_solar"] = 0
    data["Zero_Volume"] = 0

    data.sort_index(inplace=True)  # Ensure the data is sorted by 
    
    return data