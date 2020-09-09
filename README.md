
# twitter-groupe3
Réalisation du brief Smart tweet

Project structure


/resources.py: contains the key authentication of Azure API and Tweet API

/database
- db_access.py : python code files for database manipulation.
	Provide connection to the database with some methods:
	
	- add_one_tweet
	- add_many_tweets
	- get_tweet_by_id
	- get_tweets
	- update_tweet_by_id
	- update_tweets
	- delete_tweets
	
	**method call:**
    ```python
	from database.db_access import DatabaseManager as db

	db.getInstance().add_one_tweet({
        'name' : 'tweet1',
        'sentiment' : 2,
        'text' : 'random comment'
    })
    ```

/dataviz
- SQL code
- Python code for dashboard visulization

/datatweet
- Python code for tweet data management
- Python code for sentiment score retrieving
