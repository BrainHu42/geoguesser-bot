import os
import requests
import json
import itertools
import tweepy

from pathlib import Path
from src.mapsAPI import get_place

ROOT = Path(__file__).resolve().parents[0]


def lambda_handler(event, context):
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    with open('tweets.json') as file:
        history = [json.loads(line)['name'] for line in itertools.islice(file,0,200)]
        tweet = get_place()
        while tweet['name'] in history:
            os.remove('temp.jpg')
            tweet = get_place()

    media = api.media_upload(filename="temp.jpg")
    text = "Try to guess the name of this location"
    post_result = api.update_status(status=text, media_ids=[media.media_id])
    os.remove('temp.jpg')

    with open('tweets.json', 'a') as file:
        json.dump(tweet, file)
        file.write(os.linesep)

    return {"statusCode": 200, "tweet": tweet}
