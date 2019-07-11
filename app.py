from flask import Flask, jsonify, render_template, request, send_from_directory
import psycopg2
import os
import collections
import datetime
import sys
import math
import gc

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth

from models.extractdata import *

app = Flask(__name__)

if os.environ.get('ON_HEROKU'):
        app.secret_key = os.environ.get("HERO_FLASK_SECRET_KEY", default=False)
else :
    app.secret_key = FLASK_SECRET_KEY


app.register_blueprint(google_auth.app)

extractdata = extractdata()


@app.route('/')
def render_hello():
    return 'Hello, Flocals!'

@app.route('/home')
def render_home():
    activity_types = extractdata.getacttypes()
    return activity_types

@app.route('/home/<type>')
def render_activities(type):
    activities = extractdata.getactivities(type)
    return activities


@app.route('/testDB')
def testDB():
    accounts = extractdata.getaccounts()
    return accounts

@app.route('/login')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'You are not currently logged in.'


@app.route('/<path:filename>', methods=['GET'])
def display_static():
    return send_from_directory(app.static_folder, filename)

@app.route('/js/<path:filename>', methods=['GET'])
def load_js(filename):
    return send_from_directory('js', filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def pageNotFound(error):
    return "sorry problem"

@app.errorhandler(500)
def erroronpage(error):
    return "sorry problem"


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 80.
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('ON_HEROKU'):
        app.run(host='0.0.0.0', port=port)
    else :
        app.run(host='localhost', port=port)