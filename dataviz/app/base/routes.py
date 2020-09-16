# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from dataviz.app.base import blueprint
from dataviz.app.base.util import verify_pass
from database.db_access import DatabaseManager as db
from bson.json_util import dumps

@blueprint.route('/')
def route_default():
    positive = db.getInstance().get_top_positive_tweets({})
    negative = db.getInstance().get_top_negative_tweets({})
    json_positive = dumps(positive)
    json_negative = dumps(negative)
    total_tweets = db.getInstance().get_number_of_tweets()
    number_positive = db.getInstance().get_number_of_tweets_by_range("positive")
    number_neutral = db.getInstance().get_number_of_tweets_by_range("neutral")
    number_negative = db.getInstance().get_number_of_tweets_by_range("negative")
    listetags = db.getInstance().get_top_hashtags(20)


    return render_template('index.html', 
        positive_tweets = json_positive, 
        negative_tweets = json_negative,         
        count_tweets = total_tweets,
        count_positive = number_positive,
        count_negative = number_negative,
        count_neutral = number_neutral,
        hash = listetags
        )

@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## App pages
@blueprint.route('/tweet', methods=['GET'])
def tweet_page():
    tweet_id = request.args.get('id', default = '-1', type = str)
    tweet = db.getInstance().get_tweet_by_id(tweet_id)

    if tweet == None:
        return render_template('tweet-not-found.html'), 404

    json_data = dumps(tweet)
    return render_template('tweet.html', tweet_id=tweet.get('tweet_id'), username=tweet.get('user_screenname'), tweet= json_data)

@blueprint.route('/dataset')
def tweets_page():
    tweets = db.getInstance().get_tweets({})
    json_data = dumps(tweets)

    return render_template('datasetv2.html', tweets = json_data)

## Errors

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
