# -*- coding: utf-8 -*-

import time
import csv
import cgi
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import helper data reading functions

from pricetempreader import import_pricedata
from pricetempreader import get_time_index

import json

# Main parameters
HOST_NAME = 'localhost' 
PORT_NUMBER = 8080

class MyHandler(BaseHTTPRequestHandler):
    ''' HTTP request handler class extending BaseHTTPRequestHandler '''
     
    def myparse_getrequest(self):
        ''' GET request: parse the path and extract query '''
        query_string = urlparse.urlparse(self.path).query
        querydict=urlparse.parse_qs(query_string)

        # return path components in a list (ordered)
        # and query variables&values in a dictionary (unordered)
        return querydict

    def myparse_postrequest(self):
        ''' POST request: parse the form data posted '''
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )
        postdict = {}
        for field in form.keys():
            postdict[field] = form.getvalue(field)

        return postdict

    # respond to a GET request
    def do_GET(self):
        ''' responds to a GET request '''
        
        #send response
        self.send_response(200)
        self.end_headers()
        
        # querydict=self.myparse_getrequest()
        
        # replace this part with application logic ----------------
        # send back parsed request content for debugging
        # self.wfile.write(querydict)
        ####------------------------------------------------------

        return

    # respond to a POST request
    def do_POST(self):

        # Begin the response
        self.send_response(200)
        self.end_headers()

        postdict=self.myparse_postrequest()

        username = postdict['username']
        temperature = postdict['temperature']
        set_point = float(postdict['set_point'])
        localtime = postdict['localtime']

        if username and temperature and set_point and localtime :
            writer = csv.writer(file('client-information.csv', 'a+'))
            row = [username, temperature, set_point, localtime]
            writer.writerow(row)

        price = get_price()

        data = json.dumps({"price": price})
        
        # replace this part with application logic ----------------
        # send back parsed post content for debugging
        self.wfile.write(data)
        ####------------------------------------------------------

        return

def get_price():
    time_index = get_time_index()
    # divide 24*60 minutes into 48 slots (30 min / slot)
    # get_time_index() is defined in 'pricetempreader.py'

    # We want to simulate price change over 24h based on 'avg_pricelist' returned by import_pricedata() function
    # In 'GRAPH_5VIC1.csv', data start from 12:35.

    # csv   csv slot        time_index  real slot
    # 0     12:35~13:00     25          12:30:01~13:00:00
    # 1     13:05~13:30     26          13:00:01~13:30:00
    # 2     13:35~14:00     27          13:30:01~14:00:00
    # ...   ...
    # 22    23:35~0:00      47          23:30:01~00:00:00
    # 23    0:05~0:30       0           00:00:01~00:30:00
    # 24    0:35~1:00       1           00:30:01~01:00:00
    # ...   ...             ...
    # 46    11:35~12:00     23          11:30:01~12:00:00
    # 47    12:05~12:30     24          12:00:01~12:30:00

    # for instance
    # the price in 12:30:01~13:00:00 corresponds to avg_pricelist[0]
    # the price in 12:00:01~12:30:00 corresponds to avg_pricelist[47]

    index = (time_index + 23) % 48

    avg_pricelist = import_pricedata()

    price = avg_pricelist[index]

    price = round(price, 2)     # round and keep 2 decimals

    return price


#################################################
##              Main

httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
