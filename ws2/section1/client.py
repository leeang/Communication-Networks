# -*- coding: utf-8 -*-
"""
@author: Ang LI 631317 & Qingyun LIN 682834
"""

import socket
import sys

# define server address (IP (localhost = 127.0.0.1) and port)
serverAddress = ('localhost', 8080)

# The port numbers in the range from 0 to 1023 are the well-known ports or system ports. They are used by system processes that provide widely used types of network services. On Unix-like operating systems (e.g. Mac OS X), a process must execute with superuser privileges (>>> sudo python client.py) to be able to bind a network socket to an IP address using one of the well-known ports. Hence, we decide to use 8080.

# define buffer size
bufsize = 140

# creat a connectionless socket (SOCK_DGRAM)
mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# timeout after 5 seconds
mysocket.settimeout(5)

while True:
    # get keyborad inputs
    message =  raw_input("Please input the message or enter 'exit' to terminate the program.\n")
    # remove leading and trailing whitespace characters
    message = message.strip()

    # if the message is longer than 140 characters, ask for a new message.
    if len(message) > 140:
        print 'too long message'
        continue

    if message == 'exit':
        break

    try:
        # send the mesaage to a certain address
        mysocket.sendto(message, serverAddress)
        # get server response
        response, address = mysocket.recvfrom(bufsize)
        print 'Server response: ', response
    # if error occurs, show the error information.
    except socket.error as msg:
        print 'Error:', msg

# close the socket
mysocket.close()
print 'socket closed'

# terminate the program
sys.exit()
