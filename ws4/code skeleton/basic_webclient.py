# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 23:32:32 2014

This script implements the client application

@author: alpcan
"""

import requests
# import helper data reading functions
from pricetempreader import *

# communication basics
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://localhost/forfun", params=payload)
#r = requests.post("http://localhost/forfun", data=payload)

## If you are behind the university proxy
#proxies = {
#  "http": "http://wwwproxy.unimelb.edu.au:8000",
#  "https": "http://wwwproxy.unimelb.edu.au:8000",
#}

# requests.get("http://www.python.org", proxies=proxies)
## see below for more information
## http://docs.python-requests.org/en/latest/user/advanced/

# display info on console
print "Request made: %s \n" %r.url
print "Response recived: %s " %r.text





    
