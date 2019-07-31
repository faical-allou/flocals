from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS

import requests
import psycopg2
import os
import collections
import datetime
import time
import sys
import math
import gc

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth

from models.extractdata import *
from models.insertdata import *

app = Flask(__name__)
CORS(app)

if os.environ.get('ON_HEROKU'):
        app.secret_key = os.environ.get("HERO_FLASK_SECRET_KEY", default=False)
        g_api_key = os.environ.get("HERO_G_API_KEY", default=False)
        
else :
    app.secret_key = FLASK_SECRET_KEY
    g_api_key = G_API_KEY


app.register_blueprint(google_auth.app)

extractdata = extractdata()
insertdata = insertdata()

@app.route('/')
def render_hello():
    return 'Hello, Flocals!'

@app.route('/api/v1/home/') 
def return_alltypes(): 
    activity_types = extractdata.getallacttypes() 
    return activity_types

@app.route('/api/v1/home/<airport>/') 
def return_alltypesbyairport(airport): 
    activity_types = extractdata.getacttypes(airport) 
    return activity_types

@app.route('/api/v1/home/<airport>/<type>/')
def return_activities(airport, type):
    activities = extractdata.getactivities(airport, type)
    return activities

@app.route('/api/v1/home/recommendations/<lang>/<id>/')
def return_recommendations(lang, id):
    recommendations = extractdata.getrecommendations(id)
    url = 'https://translation.googleapis.com/language/translate/v2?key=' + g_api_key 
    returnrec =[]
    for rec in json.loads(recommendations):
        format = {"key": g_api_key, "headers": {"Accept": 'application/json',"Content-Type": 'application/json',"charset":'utf-8'}}
        body = { "q": [rec['userdescription']], "target": lang }       
        r = requests.post(url, params=format, json=body)
        rjson = r.json()
        rec['userdescription_translated']= rjson['data']['translations'][0]['translatedText']
        returnrec.append(rec)
    return json.dumps(returnrec)


@app.route('/api/v1/home/newactivity/',methods=['GET', 'POST'])
def add_activities():
    json_request = request.get_json(force=True, silent=False, cache=True)
    s = json_request['sessionid']
    ap = json_request['airport']
    n = json_request['name']
    tu = json_request['type_user']
    tg = json_request['googletype']
    tc = json_request['type_convert']
    ud = json_request['userDescription']
    p = json_request['place_id']
    r = json_request['recommender']
    a = json_request['address']
    lt = json_request['details']['result']['geometry']['location']['lat']
    lg = json_request['details']['result']['geometry']['location']['lng'] 
    dt = json.dumps(json_request['details'])
    tx = time.time()
    now = datetime.datetime.now()
    ymd = str(now.year)+str(format(now.month,'02'))+str(format(now.day,'02'))
    
    insertdata.insertrecommendation(s,ap,n,tu,tg,tc,ud,p,r,a,lt,lg,dt,tx,ymd)

    return 'done'

@app.route('/api/v1/airport/<inputcode>/')
def return_airportcoord(inputcode):
    airportdata = extractdata.getairportcoord(inputcode)
    return airportdata

@app.route('/testDB/')
def testDB():
    accounts = extractdata.getaccounts()
    return accounts

@app.route('/login/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'You are not currently logged in.'


@app.route('/<path:filename>/', methods=['GET'])
def display_static():
    return send_from_directory(app.static_folder, filename)

@app.route('/js/<path:filename>/', methods=['GET'])
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
        app.run(host='0.0.0.0', port=port)