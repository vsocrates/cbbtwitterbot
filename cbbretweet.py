import os
import json
import time
import tweepy
import boto3
from botocore.exceptions import ClientError

# TODO: NOT WORKING YET, add in integration to update since_id after check.
# We use since_id to make our retweeting more efficient, 
# as we only get the mentions newer that a specified tweet in time.
# However, the production code works without this as we just silently error 
# past already retweeted tweets

def lambda_handler(event, context):


  auth = tweepy.OAuthHandler(os.environ['CBB_API_KEY'], os.environ['CBB_API_SECRET_KEY'])
  auth.set_access_token(os.environ['CBB_ACCESS_TOKEN'], os.environ['CBB_ACCESS_TOKEN_SECRET'])
  api = tweepy.API(auth)

  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table("cbbtwitter")

  since_id = 0
  try:
    response = table.get_item(Key={'id_param': "since_id"})
  except ClientError as e:
    print(e.response['Error']['Message'])
  except KeyError as e:
    print(e.response)
  else:
    since_id = response['Item']

  # TODO: implement support for extended tweets (240 chars)
  for mention in tweepy.Cursor(api.mentions_timeline, include_rts = True, since_id=since_id).items():
    try:
      api.retweet(mention.id)
      time.sleep( 5 )
    except tweepy.TweepError as e:
      print(e)
    
