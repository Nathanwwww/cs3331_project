import threading
import sys
import time
from socket import *
import queue

class ack(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
    
    def run(self):
        while True:
            self.sock.send('ack'.encode())
            time.sleep(1)

class recv_handler(threading.Thread):

    def __init__(self,sock,q):
        threading.Thread.__init__(self)
        self.sock = sock
        self.q = q
    def run(self):
        while 1:
            
            
            message = self.sock.recv(8192).decode()

            if message == '>':
                continue
            if message.split()[0] == '>p2p':
                source = message.split()[1]
                dest = message.split()[2]
                print("%s is connecting you" %source)
                dd = 'addr ' + message.split()[3] + ' ' + source + ' ' +  dest
                self.q.put(dd)

            if message.split()[0] == 'p2p':
                source = message.split()[1]
                dest = message.split()[2]
                print("%s is connecting you" %source)
                dd = 'addr ' + message.split()[3] + ' ' + source + ' ' +  dest
                self.q.put(dd)
                
            if message == "close":
                self.sock.close()
                print("you have logged out")
                break
            
            message.strip('>')
            print(message)

    def stop(self):
        self._is_running = False


class send_handler(threading.Thread):
    def __init__(self,sock,q,p_port):
        threading.Thread.__init__(self)
        self.sock = sock
        self.q = q
        self.p_port = p_port

    def run(self):
        while 1:
            cmd = input()
            
        

            if ':' in cmd:
                cmd = 'message' + ' ' + cmd.replace(':',' ')
            
            
            elif 'startprivate' in cmd: 
                cmd ='startprivate ' + cmd.split()[1] + ' ' + str(self.p_port)

            elif 'private' in cmd and len(cmd.split()) == 3:
                self.q.put(cmd)
                continue

            elif 'stopprivate' in cmd:
                self.q.put(cmd)
                continue
            

            msg = cmd.encode()
            self.sock.send(msg)
    
    def stop(self):
        self._is_running = False


class p2p_recv(threading.Thread):

    def __init__(self,sock,q,p_port):
        threading.Thread.__init__(self)
        self.sock = sock
        self.q = q
        self.p_port = p_port
    def run(self):

        while 1:
            s, addr = self.sock.accept()
            if s != None:
                break
        
        while 1:
            msg = s.recv(1024).decode()
            
            if self.q.empty() == False:
                db = self.q.get()
                if db.split()[0] == "stopprivate":
                    self.q.put(db)
                    break

            if msg.split()[0] == 'addr':
                self.q.put(msg)
            
            if msg.split()[0] == 'stopprivate':
                self.q.put(msg)
                break

            print(msg)

class p2p_send(threading.Thread):
    def __init__(self,q,p_port):
        threading.Thread.__init__(self)
        self.sock = None
        self.q = q
        self.origin = None
        self.chater = None
        self.p_port = p_port
    def run(self):
        
        source = ''
        dest = ''
        while True:

            if self.q.empty() == False:
                db = self.q.get()
                if db.split()[0] == "addr":
                    
                    addr = int(db.split()[1])
                    self.chater = db.split()[2]
                    self.origin = db.split()[3]
                    dest = db.split()[2]
                    source = db.split()[3]
                    s = socket(AF_INET, SOCK_STREAM)
                    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                    s.connect(('localhost', addr))
                    
                    self.sock = s
                    print("you have connected to %s" %self.chater)
                    break
        
        hello_msg = "addr " +  str(self.p_port) + ' ' + source + ' ' + dest 
        self.sock.send(hello_msg.encode())

        while True:
             if self.q.empty() == False:
                db = self.q.get()
                if db.split()[0] == "addr":
                    continue

                elif db.split()[0] == "private" and db.split()[1] == self.chater:
                    msg = self.origin + ': ' +  db.split()[2]
                    self.sock.send(msg.encode())
                
                elif db.split()[0] == "stopprivate" and db.split()[1] == self.chater:
                    #end connection
                    self.sock.send(("stopprivate "  + self.origin).encode())
                    self.sock.close()
                    print("connection closed,you have to log in again for new p2p")
                    self.q.put(db)
                    break

                else:
                    self.q.put(db)
                    




