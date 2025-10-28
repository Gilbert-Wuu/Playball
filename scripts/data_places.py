# %%
import json
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# %%
def get_places(text_query, default_file="raw_places.json"):
    """
    Get places data from Google Map API
    :param text_query  : query string to the Google Map
    :param default_file: when api calling fails, using default file
    :return: dictionary from json data
    """
    if not GOOGLE_PLACES_API_KEY:
        raise ValueError("Missing GOOGLE_PLACES_API_KEY in .env file.")
        
    url = f"https://places.googleapis.com/v1/places:searchText?key={api_key}"

    res = requests.post(
        url=url,
        headers={
            "X-Goog-FieldMask": "places.displayName,"
                                "places.businessStatus,"
                                "places.formattedAddress,"
                                "places.types,"
                                "places.regularOpeningHours,"
                                "places.rating,"
                                "places.nationalPhoneNumber,"
                                "places.priceLevel"
        },
        data={
            "textQuery": text_query
        }
    )

    if res.status_code == 200:
        data = json.loads(res.content)
    else:
        with open(default_file) as f:
            data = json.loads(f.read())

    return data


# %%
def to_place_df(data: dict, save_csv=False):
    """
    Extract data from json and convert into pandas DataFrame
    :param data: Dictionary from places json data
    :param save_csv: If true, save the dataframe to csv file
    :return: Places info DataFrame
    """
    df = pd.DataFrame(data["places"])
    df["displayName"] = df["displayName"].map(lambda x: x["text"])
    df["openNow"] = df["regularOpeningHours"].map(lambda x: x["openNow"] if not pd.isna(x) else "")
    df["periods"] = df["regularOpeningHours"].map(lambda x: x["periods"][0] if not pd.isna(x) else "")

    if save_csv:
        df.to_csv("project/places.csv", index=False)

    return df
