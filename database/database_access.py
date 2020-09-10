from pymongo import MongoClient

class DatabaseManager:
    """Provide methods and connection to the MongoDb database
    """

    def __init__(self
                , mongo_user
                , mongo_password
                , mongo_server):
        
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password
        self.mongo_server = mongo_server
        self.__connection_string = self._get_connection_string()
        self.__client = MongoClient(self.__connection_string)

    def _get_connection_string(self):
        return str.format("mongodb+srv://{}:{}@{}/business?retryWrites=true&w=majority"
                        , self.mongo_user
                        , self.mongo_password
                        , self.mongo_server )

 
    def __get_collection(self, db_name, collection_name):
        """Generic method to connect to a give collection in a given database
        If the database or the collection don't exist, it will be created

        Args:
            db_name (str): name of the database
            collection_name (str): name of the collection

        Returns:
            collection: the collection
        """
        return self.__client.get_database(db_name).get_collection(collection_name)

    def add_one_tweet(self, tweet):
        """Insert a tweet in the tweets collection

        Args:
            tweet (json): the enhanced tweet json 

        Returns:
            bool : True if insertion succeed else False
        """
        result = self.__get_collection('smart_tweets', 'tweets').insert_one(tweet)
        return result.acknowledged
        
    def add_many_tweets(self, tweets):
        """add list of tweets

        Args:
            tweets (json[]): list of json

        Returns:
            bool: True if insertions fully succeed else false
        """
        result = True
        for tweet in tweets:
            result &= self.add_one_tweet(tweet)
        return result

    def get_tweet_by_id(self, id):
        """Get a tweet by id

        Args:
            id (str): id of the tweet

        Returns:
            json: the enhanced tweet
        """
        return self.__get_collection('smart_tweets', 'tweets').find_one({'_id': id})

    def get_tweets(self, filters):
        """get tweets by filter

        Args:
            filters (dictionnary): filters to apply for the select.
                                    ex : {'name':'XXXXX', 'sentiment':4}

        Returns:
            json[]: list of enhanced tweets
        """
        return self.__get_collection('smart_tweets', 'tweets').find(filters)

    def update_tweet_by_id(self, id, data):
        """Update a tweet by its id

        Args:
            id (str): id of the tweet
            data (dictionnary): list of key/value to update

        Returns:
            bool: True if one tweet updated else false
        """
        result = self.__get_collection('smart_tweets', 'tweets').update_one({'_id': id}, {"$set": data}, upsert=True)
        return result.modified_count == 1

    def update_tweets(self, filters, data):
        """update list of tweets matching with filters

        Args:
            filters (dictionnary): filters to apply for the select.
            data  (dictionnary): list of key/value to update

        Returns:
            int: number of tweets updated
        """
        result = self.__get_collection('smart_tweets', 'tweets').update_many(filters, data)
        return result.modified_count

    def delete_tweets(self, filters):
        """delete list of tweets matching with filters

        Args:
            filters (dictionnary): filters to apply for the select.

        Returns:
            int: number of tweets deleted
        """
        result = self.__get_collection('smart_tweets', 'tweets').delete_many(filters)
        return result.deleted_count

    def get_tweet_collection(self):
        """temporary method to get collection in order to manipulate collection without methods
            For additionnal methods, db_access should be updated, do not manipulate collection outside this manager

        Returns:
            [type]: [description]
        """
        return self.__get_collection('smart_tweets', 'tweets')