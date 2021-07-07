import os
import requests
import json

from datetime import datetime


def get_access_token():
    access_token = os.getenv('INSTAGRAM_TOKEN')
    # refresh access token
    now = datetime.utcnow()
    if now.day == 1 and now.hour <= 1:
        parameters = {
            "grant_type": "ig_refresh_token",
            "access_token": access_token,
        }
        try:
            response = requests.get('https://graph.instagram.com/refresh_access_token',params=parameters)
        except:
            return access_token
        new_token = response.json()['access_token']
        os.environ['INSTAGRAM_TOKEN'] = new_token
        return new_token
    else:
        return access_token


def cross_post(tweet):
    ig_user_id = os.getenv('INSTAGRAM_ID')
    access_token = get_access_token()

    # Reply to Comments
    


    ig_create_url = 'https://graph.facebook.com/v10.0/{}/media'.format(ig_user_id)
    create_payload = {
        "image_url": tweet['image_url'],
        "caption": tweet['text'],
        "access_token": access_token,
    }
    response = requests.post(ig_create_url, data=create_payload)

    result = json.loads(response.text)
    print(result)
    if 'id' in result:
        creation_id = result['id']
        ig_post_url = 'https://graph.facebook.com/v10.0/{}/media_publish'.format(ig_user_id)
        post_payload = {
            "creation_id": creation_id,
            "access_token": access_token,
        }
        response = requests.post(ig_post_url, data=post_payload).json()
        print('--------Posted to Instagram--------')
        if 'id' in response:
            tweet['post_id'] = response['id']
