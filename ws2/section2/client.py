# -*- coding: utf-8 -*-

import telnetlib

HOST = 'localhost'
PORT = 8080
# define address

tn = telnetlib.Telnet(HOST, PORT)
tn.interact()
