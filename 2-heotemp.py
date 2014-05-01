#!/usr/bin/env python

import urllib
import urllib2
import json
import logging

token = 'HjXQxa5ItI' # Required

# logging
logging.basicConfig(filename='2-measure_env.log', format='%(asctime)s: %(levelname)s - %(message)s', level=logging.DEBUG)

def save_env_measure(humidity, temperature):
    url = 'http://sw.hongphucjsc.com/api/weathers'
    data = {
        'humidity': humidity,
        'temperature': temperature,
        'wind_speed': 0,
        'temp_mode': 1,
        'wind_mode': 1,
        'id_site': 1
    }

    header = {'hpswine_token': token}

    req = urllib2.Request(url, urllib.urlencode(data), header)
    try:
        res = urllib2.urlopen(req)

        if (res.getcode() == 200):
            result = res.read()
            result = json.loads(result)
            if (result['status'] == 1):
                print 'saved'
    except Exception, e:
        logging.error("Code: {0}, Reason: {1}".format(e.code, e.reason))


save_env_measure(60, 30)