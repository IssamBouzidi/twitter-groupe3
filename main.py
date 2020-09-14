import sys
from configuration import resources
import database
import datatweet
import dataviz
from datatweet.tweet_manager import TweetCollection
from datatweet.tweet_manager import TweetSentimentPrediction
from datatweet.tweet import SentTweet
from flask_migrate import Migrate
from sys import exit
from os import environ
from dataviz.config import config_dict
from dataviz.app import create_app
from database.database_access import DatabaseManager

get_config_mode = environ.get('APPSEED_CONFIG_MODE', resources.APPSEED_CONFIG_MODE)

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid APPSEED_CONFIG_MODE environment variable entry.')

app = create_app(config_mode) 

if __name__ == "__main__":
    #print(resources.CONSUMER_SECRRET)
    product_name = "#XboxSeriesS"


    # test first 5 most recent tweets
    list_tweet = TweetCollection(resources.CONSUMER_KEY
    , resources.CONSUMER_SECRRET
    , resources.ACCESS_TOKEN
    , resources.ACCESS_TOKEN_SECRET).get_tweet_by_product(product_name)

    """
    for tweet in list_tweet:
        print(tweet.to_json())
        print("\n")
    """
    
    list_sent_tweet = TweetSentimentPrediction(list_tweet
            , resources.SUBSCRIPTION_KEY
            , resources.SENTIMENT_ENDPOINT_URL).predict()
            
    #print(list_response)
    list_json = []
    for tweet in list_sent_tweet:
        #print(tweet.to_json())
        list_json.append(tweet.to_json())



    mongo_instance = DatabaseManager(resources.MONGODB_USER
                                    , resources.MONGODB_PASSWORD
                                    , resources.MONGODB_SERVER)

    mongo_instance.add_many_tweets(list_json)

    app.run(host='localhost', port = 8080,use_reloader=False)
    