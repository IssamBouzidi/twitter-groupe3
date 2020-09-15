#coding:utf-8

import tweepy
import json
import smart_tweet_keys as stk

keys = stk.Settings()

auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

trends_paris = api.trends_place(615702) # WOEID de Paris.

# Indique le volume de tweets pour un hashtag donné.

for dictionnary in trends_paris:
    for trends in dictionnary['trends']:
        if trends['name'] == "#xboxseriess": 
            print(trends['tweet_volume'])

# Indique les sujets tendances pour la ville de Paris.

for dictionnary in trends_paris:
    for trends in dictionnary['trends']:
            print(trends['name'])