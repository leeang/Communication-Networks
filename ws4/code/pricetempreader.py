# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 13:42:46 2014

@author: alpcan
"""

import csv
import numpy as np
import json

import datetime

def import_pricedata():
    ''' Imports wholesale electricity price from the AEMO file
        'GRAPH_5VIC1.csv' which should be in the same folder.
        returns the 30 min average prices as an array.
        
        This array should be aligned with the temperature data!
    '''
    
    filename='GRAPH_5VIC1.csv'
    prices=[]
    with open(filename,'rb') as f:
        content=csv.reader(f)
        content.next() # skip first row 
        for row in content:
            prices.append(float(row[3])) # retail price
    
    # convert to numpy array
    pricearray=np.array(prices)

    # calculate moving average of prices
    # to get 30mins out of 5 min data
    avg_prices=np.zeros(48)
    for i in range(48):
        avg_prices[i]=np.mean(pricearray[i*6:(i+1)*6])
    
    # back to list from numpy array for convenience
    avg_pricelist=avg_prices.tolist()
    
    return avg_pricelist


# imports RRP data from AEMO file
def import_tempdata():
    ''' Imports air temperature data from BOM file for Melbourne
        'IDV60901.94868.json' which should be in the same folder.
        returns the 30 min temperatures as an array.
        
        This array should be aligned with the AEMO price data!
    '''
    
    filename='IDV60901.94868.json'
    with open(filename,'rb') as f:
        content=json.load(f)
    
    # only interested in air temp
    subset=content['observations']['data']
    tempset=[item['air_temp'] for item in subset]

    # We want to simulate temperature change over 24h based on the data stored in 'IDV60901.94868.json'
    # We select the dataset whose 'sort_oder' is in the range from 75 to 28

    # sort order    local time              real time
    # 75            2014-07-12 00:00:00     00:00:00~00:29:59
    # 74            2014-07-12 00:30:00     00:30:00~00:59:59
    # ...           ...
    # 29            2014-07-12 23:00:00     23:00:00~23:29:59
    # 28            2014-07-12 23:30:00     23:30:00~23:59:59
    
    # sort_order=28:75 AEMO price data
    temperature=tempset[28:75+1]

    # output in reverse order
    temperature=temperature[::-1]

    # Eventually, we get 48 temperatures on 12th July, 2014 which are enough to simulate the temperature change over 24h.

    return temperature


# divide 24*60 minutes into 48 slots (30 min / slot)
def get_time_index():
    now = datetime.datetime.now()
    # the time stamp of now

    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # the time stamp of 00:00:00 on the same day

    minutes = (now - midnight).seconds / 60
    # how many minutes since midnight

    time_index = minutes / 30
    # divide 24*60 minutes into 48 slots (30 min / slot)

    return time_index


def print_price_list():
    avg_pricelist = import_pricedata()

    price_list = [0] * 48

    for i in range(48):
        index = (i + 23) % 48
        price_list[i] = avg_pricelist[index]
    print price_list
