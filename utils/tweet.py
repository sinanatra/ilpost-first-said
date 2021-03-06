import tweepy
import os
import time

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'])
auth.set_access_token(os.environ['TWITTER_TOKEN'], os.environ['TWITTER_TOKEN_SECRET'])

# Create API object
api = tweepy.API(auth)

statusid = ''

def updateStatus (status, link, title, finalsnippet):
    tweet = api.update_status(status)
    statusid = tweet.id_str
    # reply to tweet
    time.sleep(10)
    api.update_status('@ilpostdice "' + finalsnippet + '" appare in: ' + link, in_reply_to_status_id = statusid, card_uri = 'tombstone://card')
