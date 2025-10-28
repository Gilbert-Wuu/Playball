# %%
import json
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Get API key securely
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# %%
def get_weather(city, default_file="raw_weather.json"):
    """
    Get weather data from Weatherapi API
    :param city: city name
    :param default_file: when api calling fails, using default file
    :return: dictionary from json data
    """
    if not WEATHER_API_KEY:
        raise ValueError("Missing WEATHER_API_KEY in .env file.")
        
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"

    # Attempt to fetch data from the API
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
    else:
        # If the API request fails, read from the local JSON file
        with open(default_file, "r") as json_file:
            data = json.load(json_file)

    return data


# %%
def to_weather_df(data: dict):
    """
    Extract data from json and convert into pandas DataFrame
    :param data: Dictionary from weather json data
    :return: Weather info DataFrame
    """

    # Extract weather data, listing each day"s data separately
    weather_data = {
        "City": [data["location"]["name"]] * 3,
        "State": [data["location"]["region"]] * 3,
        "Date": [
            data["forecast"]["forecastday"][0]["date"],
            data["forecast"]["forecastday"][1]["date"],
            data["forecast"]["forecastday"][2]["date"]
        ],
        "Max Temp (F)": [
            data["forecast"]["forecastday"][0]["day"]["maxtemp_f"],
            data["forecast"]["forecastday"][1]["day"]["maxtemp_f"],
            data["forecast"]["forecastday"][2]["day"]["maxtemp_f"]
        ],
        "Min Temp (F)": [
            data["forecast"]["forecastday"][0]["day"]["mintemp_f"],
            data["forecast"]["forecastday"][1]["day"]["mintemp_f"],
            data["forecast"]["forecastday"][2]["day"]["mintemp_f"]
        ],
        "Avg Temp (F)": [
            data["forecast"]["forecastday"][0]["day"]["avgtemp_f"],
            data["forecast"]["forecastday"][1]["day"]["avgtemp_f"],
            data["forecast"]["forecastday"][2]["day"]["avgtemp_f"]
        ],
        "Max Wind (mph)": [
            data["forecast"]["forecastday"][0]["day"]["maxwind_mph"],
            data["forecast"]["forecastday"][1]["day"]["maxwind_mph"],
            data["forecast"]["forecastday"][2]["day"]["maxwind_mph"]
        ],
        "Total Precip (mm)": [
            data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],
            data["forecast"]["forecastday"][1]["day"]["totalprecip_mm"],
            data["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]
        ],
        "Total Snow (cm)": [
            data["forecast"]["forecastday"][0]["day"]["totalsnow_cm"],
            data["forecast"]["forecastday"][1]["day"]["totalsnow_cm"],
            data["forecast"]["forecastday"][2]["day"]["totalsnow_cm"]
        ],
        "Avg Visibility (miles)": [
            data["forecast"]["forecastday"][0]["day"]["avgvis_miles"],
            data["forecast"]["forecastday"][1]["day"]["avgvis_miles"],
            data["forecast"]["forecastday"][2]["day"]["avgvis_miles"]
        ],
        "Avg Humidity (%)": [
            data["forecast"]["forecastday"][0]["day"]["avghumidity"],
            data["forecast"]["forecastday"][1]["day"]["avghumidity"],
            data["forecast"]["forecastday"][2]["day"]["avghumidity"]
        ],
        "Chance of Rain (%)": [
            data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"],
            data["forecast"]["forecastday"][1]["day"]["daily_chance_of_rain"],
            data["forecast"]["forecastday"][2]["day"]["daily_chance_of_rain"]
        ],
        "Chance of Snow (%)": [
            data["forecast"]["forecastday"][0]["day"]["daily_chance_of_snow"],
            data["forecast"]["forecastday"][1]["day"]["daily_chance_of_snow"],
            data["forecast"]["forecastday"][2]["day"]["daily_chance_of_snow"]
        ],
        "Weather Condition": [
            data["forecast"]["forecastday"][0]["day"]["condition"]["text"],
            data["forecast"]["forecastday"][1]["day"]["condition"]["text"],
            data["forecast"]["forecastday"][2]["day"]["condition"]["text"]
        ],
        "UV Index": [
            data["forecast"]["forecastday"][0]["day"]["uv"],
            data["forecast"]["forecastday"][1]["day"]["uv"],
            data["forecast"]["forecastday"][2]["day"]["uv"]
        ]
    }

    # Create DataFrame and specify the order of the columns
    df = pd.DataFrame(weather_data, columns=[
        "Date",
        "City",
        "State",
        "Max Temp (F)",
        "Min Temp (F)",
        "Avg Temp (F)",
        "Weather Condition",
        "Chance of Rain (%)",
        "Chance of Snow (%)",
        "Max Wind (mph)",
        "Total Precip (mm)",
        "Total Snow (cm)",
        "Avg Humidity (%)",
        "Avg Visibility (miles)",
        "UV Index"
    ])

    return df.transpose()
