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

    def __init__(self
                , consumer_key
                , consumer_secret
                , access_token
                , access_token_secret):
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
                                    , count = 200
                                   ):

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

    def get_sentiment(self, response):
        """get sentiment score of tweet

        Args:
            documents (json): a json with structure: {"documents": []
                                                        "errors", []
                                                        ,"modelVersion" : []}
        Return a json object with structure:
            {sentiment": "positive"
            , "confidenceScores": 
            {
                "positive": 1.0,
                "neutral": 0.0,
                "negative": 0.0
            }}
        """
#        print(response)

        sentiment = {"sentiment_score" : response["sentiment"]
                    , "confidence_scores" : response["confidenceScores"]}
        return sentiment



    def create_documents(self):
        """
        ["documents": []
        , "documents" : []]
        """
        """
        list_document = []
        

        for tweet in self.list_tweet:
            list_document.append(tweet.to_json_azure())
        
        return {"documents": list_document}

        """

        list_documents = []
        documents = []
        start = 0
        end = 0
        c_tweet = len(self.list_tweet)

        if (c_tweet <= end):
            for tweet in self.list_tweet:
                documents.append(tweet.to_json_azure())
                list_documents.append({"documents" : documents})
        else: # number of tweet is greater 10
            while (end < c_tweet):
                
                start = end
                end += 10
                documents = []

                if (end > c_tweet):
                    end = c_tweet

                for tweet in self.list_tweet[start:end]:
                    documents.append(tweet.to_json_azure())

                list_documents.append({"documents" : documents})
    


                """
                if (end > c_tweet):
                    end = c_tweet   
                """
                
        
        return list_documents

        

    def predict(self):
        """
        return a List <SentTweet> with sentiment updated
        """
        # send 10 documents maixum to the Azure server
        list_documents = self.create_documents()
        list_repsonse = []
        for documents in list_documents:
            response = requests.post(self.endpoint_url
                                , headers=self.get_header()
                                , json=documents)
            jsresponse =  response.json()
            for value in jsresponse['documents']:
                list_repsonse.append(value)

        for tweet, resp in zip(self.list_tweet, list_repsonse):
            tweet.update_sentiment(self.get_sentiment(resp))
        
        return self.list_tweet

    



    



"""
if __name__ == "__main__":
    print(resources.CONSUMER_SECRRET)
    #print(resources.CONSUMER_KEY)
"""