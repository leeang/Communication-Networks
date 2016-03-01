# -*- coding: utf-8 -*-
"""
Created on Tue Jul 08 09:56:49 2014

@author: alpcan
"""

import time
import csv
import cgi
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import helper data reading functions
from pricetempreader import *

# Main parameters
HOST_NAME = 'localhost' 
PORT_NUMBER = 80        


class MyHandler(BaseHTTPRequestHandler):
    ''' HTTP request handler class extending BaseHTTPRequestHandler '''
     
    def myparse_getrequest(self):  
        ''' GET request: parse the path and extract query  '''
        parsed_path = urlparse.urlparse(self.path)
        pathlist=parsed_path.path.split('/')[1:]
        querylist=parsed_path.query.split('&')
        querydict={}
        for item in querylist:
            keyvalpair=item.split('=')
            querydict[keyvalpair[0]]=keyvalpair[1]
            
        # return path components in a list (ordered)
        # and query variables&values in a dictionary (unordered)
        return pathlist, querydict
    
    def myparse_postrequest(self):
        ''' POST request: parse the form data posted  '''
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        postdict={}
        for field in form.keys():
            postdict[field]=form.getvalue(field)

        return postdict

    # respond to a GET request
    def do_GET(self):
        ''' responds to a GET request '''   
        
        #send response
        self.send_response(200)
        self.end_headers()
        
        pathlist,querydict=self.myparse_getrequest()
        
        # replace this part with application logic ----------------
        # send back parsed request content for debugging
        self.wfile.write(pathlist)
        self.wfile.write(querydict)
        ####------------------------------------------------------

        return
        
    # respond to a POST request
    def do_POST(self):

        # Begin the response
        self.send_response(200)
        self.end_headers()

        postdict=self.myparse_postrequest()        
        
        # replace this part with application logic ----------------
        # send back parsed post content for debugging       
        self.wfile.write(postdict)
        ####------------------------------------------------------

        
        return

def ServerApp():
    ''' this function implements the server application logic '''
    pass




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