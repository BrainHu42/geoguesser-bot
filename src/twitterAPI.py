import os
import requests
import json
import itertools
import tweepy
import random

from pathlib import Path
from src.mapsAPI import get_place
from src.instaAPI import cross_post

ROOT = Path(__file__).resolve().parents[0]


def lambda_handler(event, context):
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    with open(ROOT / 'tweets.json') as file:
        history = [json.loads(line)['name'] for line in itertools.islice(file,0,200)]
        tweet = get_place()
        while tweet['name'] in history:
            os.remove('temp.jpg')
            tweet = get_place()

    media = api.media_upload(filename="temp.jpg")
    synonym1 = random.choice(['location', 'place'])
    synonym2 = random.choice(['image','photograph', 'photo', 'picture'])
    messages = [f"Try to guess the name of this {synonym1}.", f"Where was this {synonym2} taken?", 
                f"What {synonym1} is this {synonym2} depicting?", f"What is the name of this {synonym1}?", 
                f"What {synonym1} is shown in this image?", f"Try to name this {synonym1}."]
    
    text = random.choice(messages)
    if len(tweet['description']) > 0:
        if ' ' in tweet['description'] and tweet['description'].split(' ')[0].endswith('est'):
            text += " Hint: Its the " + tweet['description']+'.'
        elif tweet['description'][0] in ['a','e','i','o','u']:
            text += " Hint: Its an " + tweet['description']+'.'
        else:
            text += " Hint: Its a " + tweet['description']+'.'
    tweet['text'] = text

    cross_post(tweet)
    
    post_result = api.update_status(status=text, media_ids=[media.media_id], long=tweet['coordinates'][0], lat=tweet['coordinates'][1])
    os.remove('temp.jpg')
    print('--------Posted to Twitter--------')

    with open(ROOT / 'tweets.json', 'a') as file:
        json.dump(tweet, file)
        file.write(os.linesep)

    return {"statusCode": 200, "tweet": tweet}
