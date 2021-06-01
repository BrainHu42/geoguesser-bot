import os
import dotenv
import requests
import pprint
from PIL import Image

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


img = Image.open('highres.jpg')
scale_factor = 4000000.0 / 5481727
# dimensions = (int(x * scale_factor) for x in img.size)
# img.resize(dimensions,Image.ANTIALIAS)
# img.save("temp.jpg",quality=95)
img.save('temp.jpg',optimize=True,quality=int(100*scale_factor)) 
