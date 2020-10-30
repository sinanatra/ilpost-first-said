import tweepy
import os
import time

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'])
auth.set_access_token(os.environ['TWITTER_TOKEN'], os.environ['TWITTER_TOKEN_SECRET'])

auth1 = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY1'], os.environ['TWITTER_API_SECRET1'])
auth1.set_access_token(os.environ['TWITTER_TOKEN1'], os.environ['TWITTER_TOKEN_SECRET1'])

# Create API object
api = tweepy.API(auth)
api1 = tweepy.API(auth1)

statusid = ''

def updateStatus (status, link):
    tweet = api.update_status(status)
    statusid = tweet.id_str
    # reply to tweet
    time.sleep(10)
    cleanLink = link.replace('https://www.', '')
    print(cleanLink)
    api.update_status(status + ' appare in:  ' + cleanLink , statusid)
