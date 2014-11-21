#!/usr/bin/env python

import urllib
import urllib2
import json
import logging
import time
import sys
import socket
import threading
import MySQLdb # uncomment this line to save data direct in database

IP = '127.0.0.1'
PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
TOKEN = 'HjXQxa5ItI'

DB_CONN = None
DB_HOST = '127.0.0.1'
DB_NAME = 'test'
DB_USER = 'root'
DB_PASS = 'mysqlduhang'


""" Function save temperature and humidity to server
"""

# logging
logging.basicConfig(filename='2-measure_env.log', format='%(asctime)s: %(levelname)s - %(message)s', level=logging.DEBUG)

""" Save data via API Web
"""
def save_env_measure(humidity, temperature):
    url = 'http://sw.hongphucjsc.com/api/weather'
    data = {
        'humidity': humidity,
        'temperature': temperature,
        'wind_speed': 0,
        'temp_mode': 1,
        'wind_mode': 1,
        'id_site': 1
    }

    header = {'hpswine_token': TOKEN}

    req = urllib2.Request(url, urllib.urlencode(data), header)
    try:
        res = urllib2.urlopen(req)

        if (res.getcode() == 200):
            result = res.read()
            result = json.loads(result)
            if (result['status'] == 1):
                return True
    except Exception, e:
        logging.error(e)
        print e

""" Save data to database directly , but required install MySQLdb
"""


def save_env_measure_mysql(humidity, temperature):
    global DB_CONN
    try:
        if not DB_CONN: 
            print 'Connecting to DB ...'
            DB_CONN = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
            print 'Connected';
        cur = DB_CONN.cursor()
        cur.execute("""INSERT INTO sw_weather 
                (humidity, temperature, wind_speed, measure_time,
                    created_at, updated_at, id_site) 
                VALUES ({0}, {1}, {2}, {3}, '{4}', '{5}', {6})
                """.format(
                        humidity, temperature, 0, int(round(time.time())), 
                        time.strftime("%Y-%m-%d %H:%I:%S"), time.strftime("%Y-%m-%d %H:%I:%S"), 1
                    )
        )
        DB_CONN.commit()
    except Exception, e:
        print e
        logging.error(e)
        return False

    return True



""" Receive data was sent from devices 
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)

while 1:
    try:
        conn, addr = s.accept()

        data = conn.recv(BUFFER_SIZE)

        data = data.split(' ');
        humidity = data[0].replace("%","")
        temperature = data[1].replace("%","")
        print 'humidity: ' + humidity + '%',
        print 'temperature: ' + temperature,

        if save_env_measure_mysql(humidity, temperature) : # send data to server
            print 'SAVED ' + time.strftime("%Y-%m-%d %H:%I:%S")
        else:
            print 'ERROR'
        if not data: break

        time.sleep(1)
        conn.close()
    except Exception, e:
        logging.error(e)