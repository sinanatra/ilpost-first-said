import tweepy
import os

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'])
auth.set_access_token(os.environ['TWITTER_TOKEN'], os.environ['TWITTER_TOKEN_SECRET'])

# Create API object
api = tweepy.API(auth)

statusid = ''

def updateStatus (status, link):
    tweet = api.update_status(status)
    statusid = tweet.id_str
    # reply to tweet
    api.update_status('@ilpostdice ' + status +' appare in:  ' + link, statusid)
