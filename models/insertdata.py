import os

import psycopg2
from psycopg2.extras import RealDictCursor

import datetime

from configdatabase import *
from models.extractdata import *

class insertdata:
    def getinsertconnection(self):

        #Define our connection string to heroku basic database
        if os.environ.get('ON_HEROKU'):
            conn_string = os.environ.get('DATABASE_URL')
        else :
            conn_string = connectionStringDatabase
        #connect
        try:
            conn = psycopg2.connect(conn_string)
            conn.autocommit = True
        except psycopg2.Error as e:
            print ("Unable to connect!")
            print (e.pgerror)
            print (e.diag.message_detail)
        else:
            print ("Connected!")

        return conn

    def insertrecommendation(self,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o ):

        connection = self.getinsertconnection()
        cursor = connection.cursor()
        query = 'INSERT INTO recommendations  (sessionid, airport,rec_name,type_userinput,googletype,type_convert,userDescription,place_id,recommender,address,lat ,lng ,details,created_unix, ymd) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s)'

        cursor.execute(query,(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o))
        connection.close()
        
        return

def __init__(self):
        print ("in init")
