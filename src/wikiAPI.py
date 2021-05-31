import os
import requests
from wikidata.client import Client

client = Client()

def get_data(ID, tweet):
    entity = client.get(ID, load=True)
    description = str(entity.description.__repr__())[2:-1]
    image_prop = client.get('P18')
    image = entity[image_prop]
    response = requests.get(image.image_url, stream=True)
    if response.status_code == 200:
        tweet['image_url'] = image.image_url
        tweet['description'] = description
        with open('temp.jpg', 'wb') as image:
            for chunk in response:
                image.write(chunk)
    return response.status_code