# -*- coding: utf-8 -*-
"""
Created on Tue Jul 08 09:56:49 2014

@author: alpcan
"""

import time
import cgi
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Main parameters
HOST_NAME = 'localhost' 
PORT_NUMBER = 80        

# Handler
class MyHandler(BaseHTTPRequestHandler):
    ''' HTTP request handler class extending BaseHTTPRequestHandler '''
    
    def info_messgage(self):
        ''' create information message based on the GET request'''
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES: ',
                'client_address=%s (%s) ' % (self.client_address,
                                            self.address_string()),
                'command=%s ' % self.command,
                'path=%s ' % self.path,
                'real path=%s  ' % parsed_path.path,
                'query=%s  ' % parsed_path.query,
                'request_version=%s  <br/>' % self.request_version,
                '',
                'SERVER VALUES:  ',
                'server_version=%s  ' % self.server_version,
                'sys_version=%s  ' % self.sys_version,
                'protocol_version=%s  <br/>' % self.protocol_version,
                '',
                'HEADERS RECEIVED: ',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s ' % (name, value.rstrip()))
        message_parts.append('')
        message = '<br/>'.join(message_parts)
        return message
    

    def do_GET(self):
        ''' responds to a GET request '''        
        
        #send response
        self.send_response(200)
        
        #send headers
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # send content
        self.wfile.write("<html><head><title>Test Website</title></head>")
        self.wfile.write("<body><p>This is a test python webserver.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then self.path equals "/foo/bar/".
        self.wfile.write("<p>You accessed path: ")
        self.wfile.write("http://localhost%s</p>" % self.path)

        # add the information message        
        msg=self.info_messgage()

        self.wfile.write("<p> %s" %msg)
        self.wfile.write("</p>")
        self.wfile.write("</body></html>")
        
        return
        
    def do_POST(self):
        ''' responds to a POST request '''       
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        return 
    

#################################################
##              Main

# create server
httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
# run server until user presses CTRL+C
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)