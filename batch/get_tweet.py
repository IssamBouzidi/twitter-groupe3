#coding:utf-8

import tweepy
import json
import smart_tweet_keys as stk

keys = stk.Settings()

auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


dico_tweet = []

for tweet in tweepy.Cursor(api.search,  q = "#XboxSeriesS", lang = "fr").items(150):
    if tweet.retweeted == False:
        temp = {}
        temp['Date'] = tweet.created_at.strftime("%Y-%d-%m")
        temp['Auteur'] = tweet.user.screen_name
        temp['Texte'] = tweet.text
        dico_tweet.append(temp)

with open('xbox_tweet.json', 'w') as json_file:
    json.dump(dico_tweet, json_file)