import os

import psycopg2
from psycopg2.extras import RealDictCursor

import simplejson as json
import collections
import datetime
from itertools import groupby
from operator import itemgetter
from configdatabase import *

class extractdata:
    def getconnection(self):

        #Define our connection string to heroku basic database
        if os.environ.get('ON_HEROKU'):
            conn_string = os.environ.get('DATABASE_URL')
        else :
            conn_string = connectionStringDatabase
        #connect
        try:
            conn = psycopg2.connect(conn_string)
        except psycopg2.Error as e:
            print ("Unable to connect!")
            print (e.pgerror)
            print (e.diag.message_detail)
        else:
            print ("Connected!")

        return conn

    def getaccounts(self ):

        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * fROM account"
        cursor.execute(query)

        result = json.dumps(cursor.fetchall(), indent=2)

        connection.close()

        return result

    def getallacttypes(self ):
        
        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = \
        "SELECT type_convert FROM recommendations\
        GROUP BY type_convert"
        cursor.execute(query)
        result = json.dumps(cursor.fetchall(), indent=2)
        connection.close()


        return result

    def getacttypes(self, airport_ ):
        
        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = \
        "WITH cte_location as (SELECT latitude, longitude FROM airports where lower(iata) = lower(%s)) \
        SELECT type_convert FROM recommendations as r CROSS JOIN cte_location as l \
        WHERE gcd(r.lat, r.lng, l.latitude, l.longitude)<100 \
        GROUP BY type_convert"
        cursor.execute(query, (airport_,))
        result = json.dumps(cursor.fetchall(), indent=2)
        connection.close()


        return result

    def getactivities(self, airport_, type_ ):

        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "WITH cte_location as (SELECT latitude, longitude FROM airports where lower(iata) = lower(%s))\
                SELECT place_id, rec_name, lat, lng, count(1) as nb_rec \
                FROM recommendations as r CROSS JOIN cte_location as l\
                WHERE lower(r.type_convert) = lower(%s) AND gcd(r.lat, r.lng, l.latitude, l.longitude)<100 \
                GROUP BY place_id,rec_name, lat, lng order by count(1) DESC"
        cursor.execute(query,(airport_, type_,))
        result = json.dumps(cursor.fetchall(), indent=2)
        connection.close()

        return result

    def getrecommendations(self, id_ ):
        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT place_id, rec_name, recommender,lang, userDescription fROM recommendations where place_id = %s "
        cursor.execute(query,(id_,))
        result = json.dumps(cursor.fetchall(), indent=2)
        connection.close()

        return result

    def getairportcoord(self, inputcode ):

        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT name,city, latitude,longitude  fROM airports  where lower(iata) = lower(%s)"
        cursor.execute(query,(inputcode,))
        result = json.dumps(cursor.fetchone(), indent=2)
        connection.close()

        return result


def __init__(self):
        print ("in init")
