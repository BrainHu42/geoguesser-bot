import os
import tweepy
from unidecode import unidecode

# def get_access_token():
#     consumer_key = os.getenv("CONSUMER_KEY")
#     consumer_secret = os.getenv("CONSUMER_SECRET")
#     access_token = os.getenv("ACCESS_TOKEN")
#     access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     api = tweepy.API(auth)
#     return api

def post_tweet(tweet, history):
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Reply to Replies after 8 hours
    name = 'name_this_place'
    past_tweet = history[3]
    tweet_id = past_tweet['tweet_id']
    answer = unidecode(past_tweet['name']).lower()
    address = past_tweet.get('address')

    count = 0
    for reply in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=99999).items(500):
        if hasattr(reply, 'in_reply_to_status_id_str'):
            if (reply.in_reply_to_status_id_str==tweet_id):
                text = unidecode(reply.text.replace('@name_this_place','')).lower()
                username = reply.user.screen_name
                if answer in text:
                    api.update_status(status="@"+username+" You got it exactly right!", in_reply_to_status_id=reply.id_str)

                elif address is not None:
                    for key in address:
                            if not(key=='country_code' and key=='postcode') and unidecode(address[key]).lower() in text:
                                api.update_status(status="@"+username+" You got the right "+key+"!", in_reply_to_status_id=reply.id_str)
                count += 1
                if count > 200:
                    break
    # Post answer
    text = "The correct answer is "+past_tweet['name']+". "
    if 'wikipedia' in past_tweet:
        text += past_tweet['wikipedia']
    api.update_status(text, in_reply_to_status_id=tweet_id)

    # Post new tweet
    media = api.media_upload(filename="temp.jpg")
    post_result = api.update_status(status=tweet['text'], media_ids=[media.media_id], long=tweet['coordinates'][0], lat=tweet['coordinates'][1], display_coordinates=True)
    tweet['tweet_id'] = post_result.id_str
    print('--------Posted to Twitter--------')
