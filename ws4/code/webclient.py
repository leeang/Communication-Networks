# -*- coding: utf-8 -*-

import requests

from pricetempreader import import_tempdata
from pricetempreader import get_time_index

import time

USERNAME = 'angli'
# username

def get_temperature(time_index):

    temperature = import_tempdata()
    # import_tempdata() has been slightly modified

    temperature = temperature[time_index]

    return temperature

def get_set_point(time_index, price):
    # ##
    #  arithmetic underlying get_set_point() function is explained in detail in the workshop report.
    # ##

    set_point = 20
    price_average = 36.87

    if price > price_average :
        set_point = set_point - 0.3 * (price - price_average)
    else:
        set_point = set_point - 0.1 * (price - price_average)

    if time_index <= 12 :
        # time_index 0~12 are aligned to 00:00 ~ 6:00
        set_point = set_point - (10 - 1.66 * abs(index - 6))

    set_point = round(set_point, 2)

    return set_point


#################################################
##              Main

set_point = 0
# initial set point

print USERNAME
# print username

while True:
    time_index = get_time_index()
    # divide 24*60 minutes into 48 slots (30 min / slot)
    # get_time_index() is defined in 'pricetempreader.py'
    
    temperature = get_temperature(time_index)

    localtime = time.strftime('%d %b %Y %X', time.localtime(time.time()))
    # local time represented in string like '04 Oct 2015 19:51:42'

    payload = {'username': USERNAME, 'temperature': temperature, 'set_point': set_point, 'localtime': localtime}
    # parameters posted to server

    r = requests.post("http://localhost:8080/client_api", data=payload)
    # post data and receive response
    r = r.json()
    # json decode
    price = r['price']

    set_point = get_set_point(time_index, price)
    #  arithmetic within get_set_point() function is explained in detail in the workshop report.

    print 'Temperature: ', temperature
    print 'Price: ', price
    print 'Set point: ', set_point

    time.sleep(3)
