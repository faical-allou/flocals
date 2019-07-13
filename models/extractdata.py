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

    def getacttypes(self ):

        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * fROM activity_types"
        cursor.execute(query)

        result = json.dumps(cursor.fetchall(), indent=2)

        connection.close()

        return result

    def getactivities(self, type ):

        connection = self.getconnection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT a.id, a.name, a.act_type, l.name,l.city  fROM activities a join locations l on a.loc_short = l.shortname  where act_type = %s"
        cursor.execute(query,(type,))

        result = json.dumps(cursor.fetchall(), indent=2)

        connection.close()

        return result

def __init__(self):
        print ("in init")
