#/usr/bin/env python

import pymysql
import dbconfig
import datetime

class DBHelper(object):
    def connect(self,database="crimemap"):
        return pymysql.connect(host="104.128.235.71",
                               user=dbconfig.user,
                               passwd=dbconfig.password,
                               db=database)

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "SELECT description from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_input(self,data):
        connection = self.connect()
        try:
            query = "INSERT into crimes(description) values (%s)"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()

    def add_crime(self, category, date, latitude, longitude, description):
        connection = self.connect()
        try:
            query = "INSERT into crimes(category, date, latitude, longitude, description) " \
                    "values (%s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(query,(category, date, latitude, longitude, description))
                connection.commit()
        finally:
            connection.close()

    def get_all_crimes(self):
        connection = self.connect()
        try:
            query = "select latitude, longitude, date, category, description from crimes"
            with connection.cursor() as cursor:
                cursor.execute(query)
            named_crimes = []
            for crime in cursor:
                named_crime = {
                    "latitude": crime[0],
                    "longitude": crime[1],
                    "date": datetime.datetime.strftime(crime[2],'%Y-%m-%d'),
                    'category': crime[3],
                    'description': crime[4]
                }
                named_crimes.append(named_crime)
            return named_crimes
        finally:
            connection.close()