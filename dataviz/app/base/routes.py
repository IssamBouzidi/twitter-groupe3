# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from dataviz.app.base import blueprint
from dataviz.app.base.util import verify_pass
from database.db_access import DatabaseManager as db

@blueprint.route('/')
def route_default():
    return render_template('index.html')

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

    return render_template('tweet.html', tweet_id=tweet.get('tweet_id'), 
            positive = float(tweet.get('sentiment')['confidence_scores']['positive'])*100,
            neutral = float(tweet.get('sentiment')['confidence_scores']['neutral'])*100,
            negative = float(tweet.get('sentiment')['confidence_scores']['negative'])*100,
            score = tweet.get('sentiment')['sentiment_score'],
            username=tweet.get('user_screenname'))

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
