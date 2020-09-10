###################################################
#@author: Diem Bui
#@Date: 08/09/2020
###################################################


import tweepy
import json
import requests
import pandas as pd
from datatweet.tweet import SentTweet




class TweetCollection:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.tweet_api = self._get_tweet_api()

    def _get_tweet_api(self):
        
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        return api
    
    

    def get_tweet_by_product(self, product_name):

        list_tweet = []
        keyword = "#" + product_name
        for tweet in self.tweet_api.search(q=keyword 
                                    #, lang="en"
                                    , include_entities=True
                                    , result_type='recent'
                                    , count =5):
            #print(tweet)
            '''
            print(f"user screen name: {tweet.user.screen_name}")
            print("user name: ",tweet.user.name)
            print("user location:", tweet.user.location)
            print("user description: ", tweet.user.description)
            print("tweet id:", tweet.id)
            print("entities: ",tweet.entities)
            print("text: ", tweet.text)
            print("created at: ", tweet.created_at)
            #print(tweet.direct_message)
            '''
            list_tweet.append(SentTweet(str(tweet.id)
                                    , tweet.text
                                    , tweet.user.name
                                    , tweet.user.screen_name
                                    , tweet.user.location
                                    ,  tweet.metadata['iso_language_code']
                                    , tweet.entities
                                    , tweet.created_at))
        return list_tweet


class TweetSentimentPrediction:

    def __init__(self, list_tweet, subscription_key, endpoint_url):
        self.list_tweet = list_tweet
        self.subcription_key = subscription_key
        self.endpoint_url = endpoint_url
    
    def get_header(self):
        return {"Ocp-Apim-Subscription-Key": self.subcription_key}



    def create_documents(self):
        
        list_document = []
        for tweet in self.list_tweet:
            list_document.append(tweet.to_json_azure())
        
        return {"documents": list_document}


    def predict(self):

        documents = self.create_documents()
        response = requests.post(self.endpoint_url, headers=self.get_header(), json=documents)
        return response.json()

    



    



"""
if __name__ == "__main__":
    print(resources.CONSUMER_SECRRET)
    #print(resources.CONSUMER_KEY)
"""