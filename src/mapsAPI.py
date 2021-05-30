import os
import requests
import pprint
from random import randint
from src.wikiAPI import get_data

#Development
# dotenv.load_dotenv()

# ROOT = Path(__file__).resolve().parents[0]

def get_place():
    API_KEY = os.getenv("API_KEY")
    longitude = randint(-18000,18000) / 100.0
    latitude = randint(-9000,9000) / 100.0

    parameters = {
        "radius": "1000000",
        "lat": latitude,
        "lon": longitude,
        "rate": "3",
        "limit": "10",
        "apikey": API_KEY,
    }
    response = requests.get("https://api.opentripmap.com/0.1/en/places/radius", params=parameters)
    places = response.json()['features']
    
    #Pick place from choices
    for place in places:
        tweet = {}
        props = place['properties']
        # xid = props['xid']
        if 'wikidata' in props:
            wiki = props['wikidata']
            status = get_data(wiki,tweet)
            if status == 200:
                tweet['name'] = props['name']
                tweet['coordinates'] = place['geometry']['coordinates']
                tweet['types'] = props['kinds']
                return tweet

    return get_place()