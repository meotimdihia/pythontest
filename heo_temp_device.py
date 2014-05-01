#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from time import sleep

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host ='123.30.53.72'
port = 8222               # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.
#c, addr = s.accept()     # Establish connection with client.
#print 'Got connection from', addr

while True:

	c, addr = s.accept()     # Establish connection with client.
	print 'Got connection from', addr
	c.send('READ')
	print c.recv(1024)
	#  sleep(1)
	#  c.send('READ')
	# print c.recv(1024)
	sleep(3)
	c.close()                # Close the connection
