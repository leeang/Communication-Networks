# -*- coding: utf-8 -*-
"""
@author: Ang LI 631317 & Qingyun LIN 682834
"""

import socket
import sys
import time

# define server address (IP (localhost = 127.0.0.1) and port)
serverAddress = ('localhost', 8080)

# The port numbers in the range from 0 to 1023 are the well-known ports or system ports. They are used by system processes that provide widely used types of network services. On Unix-like operating systems (e.g. Mac OS X), a process must execute with superuser privileges (>>> sudo python server.py) to be able to bind a network socket to an IP address using one of the well-known ports. Hence, we decide to use 8080.

# define buffer size
bufsize = 140

# create a connectionless socket (SOCK_DGRAM)
mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind 'mysocket' to the defined server address
mysocket.bind(serverAddress)

while True:
    # get request (string) and client address
    request, clientAddress = mysocket.recvfrom(bufsize)

    # print the request message
    print 'Message received from client: ', request

    # generate a response with a timestamp
    response = 'Message received at ' + time.ctime()

    # send response message back to client address
    mysocket.sendto(response, clientAddress)

# close the socket
mysocket.close()
print 'socket closed'
