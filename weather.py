from datetime import date, timedelta
from openmeteopy import OpenMeteo
from openmeteopy.hourly import HourlyForecast
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions


def get_weather_data():
    """
    Fetches weather data for a specific location using Open Meteo API.

    Returns:
        pd.DataFrame: A DataFrame containing the weather data.
    """
    # Latitude and Longitude for the location
    latitude = 33.89
    longitude = -6.31

    hourly = HourlyForecast()

    # Date range for the forecast
    start_date = date.today()
    end_date = date.today() + timedelta(days=7)

    # Create an options object with the specified parameters
    options = ForecastOptions(latitude, longitude, start_date, end_date)

    # Create a manager object with the desired forecast type (hourly or daily)
    mgr = OpenMeteo(options, hourly.all())

    # Download data and return as a DataFrame
    meteo = mgr.get_pandas()
    meteo.to_csv("weather.csv")  # Save to CSV for later use
    return meteo



