import os
import tweepy
import dotenv
import json
import collections
import pprint
dotenv.load_dotenv()
from wikidata.client import Client

# client = Client()

# entity = client.get('Q2006222',load=True)
# print(entity.data['sitelinks']['enwiki']['url'])
# pprint.pprint(entity.data)


consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
name = 'name_this_place'
for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=99999).items(1000):
    print(tweet.text)

# timeline = api.user_timeline(count=30, screen_name='name_this_place')

# with open('src/tweets.json') as file:
    # history = [json.loads(line) for line in file]

# new = [] 

# for entry in history:
#     for tweet in timeline:
#         text = tweet.text[:-24]
#         tweet_id = tweet.id_str
#         coords = tweet.coordinates['coordinates']
#         if str(entry['coordinates'][0]) == str(coords[0]) and str(entry['coordinates'][1]) == str(coords[1]):
#             entry['text'] = text
#             entry['tweet_id'] = tweet_id
#     # print("Tweet ID: "+tweet_id)
#     # print(text)
#     # print(coords)
#     # print()

# for entry in history:
#     temp = {}
#     coords = entry['coordinates']
#     temp['coordinates'] = coords
#     for key in entry:
#         if not key == 'coordinates':
#             temp[key] = entry[key]
#     new.append(temp)

# # print(new)
# with open('new.jsonl', 'a') as f:
#     for tweet in new:
#         json.dump(tweet, f)
#         f.write(os.linesep)