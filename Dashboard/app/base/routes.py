# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from app import db, login_manager
from app.base import blueprint
from app.base.models import User
from app.base.util import verify_pass

@blueprint.route('/')
def route_default():
    return render_template('index.html')

@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## App pages
@blueprint.route('/tweet')
def tweet_page():
    tweet = db.get_tweet_by_id('1304045485242580992')
    u = tweet.get('user_screenname')
    return render_template('tweet.html', accuracy = 20)

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
