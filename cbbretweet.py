import os
import json
import time
import tweepy

def lambda_handler(event, context):

  # these variables are stored in AWS lambda ENVIRONMENT VARIABLES
  auth = tweepy.OAuthHandler(os.environ['CBB_API_KEY'], os.environ['CBB_API_SECRET_KEY'])
  auth.set_access_token(os.environ['CBB_ACCESS_TOKEN'], os.environ['CBB_ACCESS_TOKEN_SECRET'])
  api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

  # get all my friends
  friend_ids = []
  for friend_id in tweepy.Cursor(api.friends_ids).items():
    friend_ids.append(friend_id)

  # TODO: implement support for extended tweets (240 chars)
  for mention in tweepy.Cursor(api.mentions_timeline, include_rts = True).items():
    try:
      # check whether this mention is in the whitelist of @YaleCBB friends
      if mention.user.id in friend_ids:
        api.retweet(mention.id)
        time.sleep( 5 )
    except tweepy.TweepError as e:
      print(e)
    
