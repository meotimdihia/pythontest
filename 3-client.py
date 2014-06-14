#!/usr/bin/env python

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "50% 24"

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)

        data = s.recv(BUFFER_SIZE)

        print "received data:", data
    except Exception, e:
        print e

    s.close()
    
    time.sleep(1)