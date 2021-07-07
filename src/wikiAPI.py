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
        if count > 0:
            return 400

    image_prop = client.get('P18')
    image = entity[image_prop]
    response = requests.get(image.image_url, stream=True)
    print(response.headers, response.status_code)
    if response.status_code == 200:
        tweet['image_url'] = image.image_url
        tweet['description'] = description
        if 'sitelinks' in entity.data and 'enwiki' in entity.data['sitelinks']:
            tweet['wikipedia'] = entity.data['sitelinks']['enwiki']['url']
            print(entity.data['sitelinks'])
            
        with open('temp.jpg', 'wb') as f:
            for chunk in response:
                f.write(chunk)

        if image.image_size > 4500000:
            img = Image.open('temp.jpg')
            scale_factor = 3600000.0 / image.image_size
            img.save('temp.jpg',optimize=True,quality=int(100*scale_factor)) 

    return response.status_code