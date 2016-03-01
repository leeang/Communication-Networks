# -*- coding: utf-8 -*-

import socket
import select
import sys

HOST = 'localhost'
PORT = 8080
# define address

# The port numbers in the range from 0 to 1023 are the well-known ports or system ports. They are used by system processes that provide widely used types of network services. On Unix-like operating systems (e.g. Mac OS X), a process must execute with superuser privileges (>>> sudo python server.py) to be able to bind a network socket to an IP address using one of the well-known ports. Hence, we decide to use 8080.

bufsize = 1024
# define buffer size

socketList = []
addressList = []
# declare socket list and address list

# server initialization
def serverInit():
    global socketServer
    # set socketServer a global variable
    
    try:
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'server established'
        # create a connection-oriented socket (SOCK_STREAM)
    except:
        print 'cannot initialize server'
        sys.exit()

    socketServer.setblocking(0)
    # Set non-blocking mode of the socket. (Initially all sockets are in blocking mode.)

    try:
        socketServer.bind((HOST, PORT))
        print 'address bound'
    except:
        print 'cannot bind the host and port'
        sys.exit()

    socketServer.listen(5)
    print 'listening port', PORT

    socketList.append(socketServer)
    addressList.append("%s:%s" % (HOST, PORT))
    # append to socket list and address list

# broadcast message except the originating user
def broadcast(socketExcept, message):
    for s in socketList:
        if s != socketServer and s != socketExcept:
        # exclude the originating user and the server
            try:
            # try to send the message to current socket
                s.send(message)
            except socket.error, err:
                print err

# accept incoming connections
def acceptClient(s):
    clientsocket, address = s.accept()
    # aspect new connection and assign a new socket

    socketList.append(clientsocket)
    addressList.append("%s:%s" % address)
    # append to socket list and address list

    print "Client (%s:%s) connected" % address
    # 'client connected' notification

    clientsocket.send("Welcome, Client (%s:%s).\nPlease enter your message.\n" % address)
    # send the welcome message to the new user

    broadcast(clientsocket, "Client (%s:%s) connected\n" % address)
    # announce the arrival of new user

# check users for incoming messages
def checkUsers(s):
    try:
    # try to receive message from clients to check on-line status
        message = s.recv(bufsize)
        message = message.strip()
        # remove leading and trailing whitespace characters
        if message:
            s.send('"%s" received by the server\n' % message)
            # send an acknowledgment response to the originating user
            peername = "Client (%s:%s)" % s.getpeername()
            # get address (IP and port)
            broadcast(s, peername + ' said: ' +  message + '\n')
            # broadcast incoming messages to all users except from the originating one
    except:
    # if trial fails, close the socket and remove it from the list
        s.close()
        # close the socket

        index = socketList.index(s)
        # get index number of this socket in the socket list
        del socketList[index]
        # delete this socket from socket list
        addressString = addressList.pop(index)
        # get the address string from address list and delete
        
        print "Client (%s)" % addressString, 'left'
        # 'client left' notification

        broadcast(None, "Client (%s)" % addressString + ' left\n')
        # announce the departure of user

### ### ### Main ### ### ###

serverInit()
# server initialization

while True:
    rlist, wlist, xlist = select.select(socketList, [], [])
    # Reference: https://docs.python.org/2/howto/sockets.html#non-blocking-sockets
    # Reference: http://www.ibm.com/developerworks/linux/tutorials/l-pysocks/#N103D1

    for s in rlist:
        if s == socketServer:
            acceptClient(s)
            # accept incoming connections
        else:
            checkUsers(s)
            # check users for incoming messages

socketServer.close()
