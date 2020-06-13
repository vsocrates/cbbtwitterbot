import os
import json
import time
import tweepy

def lambda_handler(event, context):


  auth = tweepy.OAuthHandler(os.environ['CBB_API_KEY'], os.environ['CBB_API_SECRET_KEY'])
  auth.set_access_token(os.environ['CBB_ACCESS_TOKEN'], os.environ['CBB_ACCESS_TOKEN_SECRET'])
  api = tweepy.API(auth)

  # TODO: implement support for extended tweets (240 chars)
  for mention in tweepy.Cursor(api.mentions_timeline, include_rts = True).items():
    try:
      api.retweet(mention.id)
      time.sleep( 5 )
    except tweepy.TweepError as e:
      print(e)
    
