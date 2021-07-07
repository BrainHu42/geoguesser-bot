import os
import requests
from random import randint
from src.wikiAPI import get_data

#Development
# dotenv.load_dotenv()

# ROOT = Path(__file__).resolve().parents[0]

def get_place(history):
    API_KEY = os.getenv("API_KEY")
    coords = [entry['coordinates'] for entry in history]
    # print(coords)

    # Ration API request limit
    for count in range(420):
        xid = str(randint(0,13623032)) # Get random entity in database
        response = requests.get('https://api.opentripmap.com/0.1/en/places/xid/'+xid+'?apikey='+API_KEY)
        place = response.json()
        # Popular and Interesting Locations from wikidata that we haven't already posted
        if ('rate' in place and '3' in place['rate']) and 'wikidata' in place and 'interesting_places' in place['kinds']:
            print(place)
            tweet = {}
            if 'point' in place:
                tweet['coordinates'] = [place['point']['lon'], place['point']['lat']]
                # Ignore if already posted
                if tweet['coordinates'] in coords:
                    continue
            
            wiki = place['wikidata']
            status = get_data(wiki,tweet)
            print(status)
            if status == 200:
                tweet['name'] = place['name']
                tweet['types'] = place['kinds']
                if 'address' in place:
                    tweet['address'] = place['address']
                return tweet 

    return get_place(history)