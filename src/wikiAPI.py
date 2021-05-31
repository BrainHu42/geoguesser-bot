import os
import requests

from PIL import Image
from wikidata.client import Client

client = Client()

def get_data(ID, tweet):
    entity = client.get(ID, load=True)
    description = entity.description.__str__()

    #checks if description is in english
    count = 0
    for c in description:
        try: 
            c.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            count += 1
        if count > 2:
            return 400

    image_prop = client.get('P18')
    image = entity[image_prop]
    response = requests.get(image.image_url, stream=True)
    if response.status_code == 200:
        tweet['image_url'] = image.image_url
        tweet['description'] = description
            
        with open('temp.jpg', 'wb') as f:
            for chunk in response:
                f.write(chunk)

        if image.image_size > 4500000:
            img = Image.open('temp.jpg')
            scale_factor = 4500000.0 / image.image_size
            dimensions = (int(x * scale_factor) for x in image.image_resolution)
            img.resize(dimensions,Image.ANTIALIAS)
            img.save("temp.jpg",quality=95)

    return response.status_code