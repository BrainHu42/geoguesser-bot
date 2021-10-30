import os
import requests
import json
import itertools
import random

from pathlib import Path
from src.mapsAPI import get_place
from src.instaAPI import cross_post
from src.twitterAPI import post_tweet

ROOT = Path(__file__).resolve().parents[0]


def lambda_handler(event, context):
    # Check for Uniqueness
    with open(ROOT / 'tweets.json') as file:
        history = [json.loads(line) for line in itertools.islice(reversed(file.readlines()),0,200)]
        tweet = get_place(history)
        if tweet == "abort":
            return {"statusCode": 404, "tweet": "Aborted"}

    # Constructing Caption
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

    # Add hashtags
    text += " "+random.choice(['#geography', '#photography', '#interesting', '#picoftheday'])
    hashtags = {
        "mountain": "#mountain", "architecture": "#architecture",
        "natur": "#nature", "beach": "#beach",
        "monument": "#monument", "cultural": "#culture",
        "histor": "#history", "bridge": "#bridge",
        "lighthouses": "#lighthouse", "towers": "#tower",
        "skyscrapers": "#skyscraper", "museums": "#museum",
        "geological": "#geology", "islands": "#island",
    }

    for key in hashtags:
        if key in tweet['types']:
            text += " "+hashtags[key]

    tweet['text'] = text

    # Post on Instagram and Facebook
    cross_post(tweet)

    # Post on Twitter
    post_tweet(tweet,history)
    
    # Clean Up
    os.remove('/tmp/temp.jpg')
    del tweet['types']
    with open(ROOT / 'tweets.json', 'a') as file:
        json.dump(tweet, file)
        file.write(os.linesep)

    return {"statusCode": 200, "tweet": tweet}
