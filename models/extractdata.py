import os
import psycopg2
import simplejson
import collections
import datetime
import numpy as np
import math
from itertools import groupby
from operator import itemgetter
from configdatabase import connectionStringDatabase

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

    def getpopularitytableredirects(self, filtertype, city ):

        connection = self.getconnection()
        cursor = connection.cursor()
        if filtertype == 'o':
            query = "SELECT origincitycode, destinationcitycode, concat(origincitycode, '-',destinationcitycode), seats FROM ptbexits_popular \
            WHERE origincitycode = '"+city+"' and destinationcitycode > 'AAA' \
            ORDER BY seats DESC LIMIT 10"
            cursor.execute(query)
        else:
            query = "SELECT origincitycode, destinationcitycode, concat(origincitycode, '-',destinationcitycode), seats FROM ptbexits_popular \
            WHERE origincitycode > 'AAA' and destinationcitycode = '"+city+"' \
            ORDER BY seats DESC LIMIT 10"
            cursor.execute(query)

        rows = [('a','b','c', 1)]
        rowarray_list = []

        while len(rows) > 0:

            rows = cursor.fetchmany(500)
            # Convert query to row arrays
            for row in rows:
                rows_to_convert = (row[0], row[1], row[2], row[3])
                t = list(rows_to_convert)
                rowarray_list.append(t)

        connection.close()
        #normalize the table (adding 1 to the sum to return 0 when empty)
        if len(rowarray_list) == 10:
            max_popular = max(max(row[3] for row in rowarray_list),1)
        else :
            max_popular = 99999

        for k in range(0,len(rowarray_list)):
            rowarray_list[k][3] = round(rowarray_list[k][3]*100/max_popular)

        return rowarray_list

 
def __init__(self):
        print ("in init")
