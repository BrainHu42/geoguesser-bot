import os
import dotenv
import requests
import pprint
from random import randint

#Development
dotenv.load_dotenv()

# ROOT = Path(__file__).resolve().parents[0]

def get_place():
    API_KEY = os.getenv("API_KEY")
    longitude = -74
    latitude = 40

    parameters = {
        "radius": "1000000",
        "lat": latitude,
        "lon": longitude,
        "rate": "3h",
        "limit": "10",
        "apikey": API_KEY,
    }
    response = requests.get("https://api.opentripmap.com/0.1/en/places/radius", params=parameters)
    places = response.json()['features']
    pprint.pprint(places)

get_place()