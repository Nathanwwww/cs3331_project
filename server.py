from socket import *
import sqlite3
from sqlite3 import Error
import os
import threading
import sys
import time
import queue

#initial user status table

onlineUser = {}
block_list = {}

def init_deb():
    with open('credentials.txt', 'rt') as f:    
        for line in f:
            onlineUser[line.strip().split()[0]] = {'status': False, 'addr' : None, 'LAT': None, 'msg': []}
        

def verify(msg,t_out):
    data = msg.split()
    #check input
    if len(data) != 3:
        return "wrong message"

    username = data[1]
    password = data[2]
    
    with open('credentials.txt', 'rt') as f:
        for line in f:
            if username == line.strip().split()[0]:
                if password == line.strip().split()[1]:
                    if onlineUser[username]['status'] == True:
                        return "online", None
                    else:
                        return "success" + " " + str(t_out), None
                else:
                    return "wrong password", username

        
    return "wrong u_name", None

    
class link(threading.Thread):
    
    def __init__(self,sock,addr,t_out,block,q):
        threading.Thread.__init__(self)
        self.sock = sock
        self.addr = addr
        self.t_out = t_out
        self.block = block
        self.username = None
        self.q = q
        self.b_user = []


    def run(self):
        print('Accept new connection from %s:%s...' % self.addr)
        count = 0

        while True:

#===================================================
            if self.q.empty() == False and self.username != None:
                db = self.q.get()
                
    
                if db.split()[0] == self.username and db.split()[1] not in self.b_user:
                    ms = db.split()[1] + ':' + db.split()[2]
                    self.sock.send(ms.encode())

                elif db.split()[0] == 'p2p' and db.split()[2] == self.username:
                    self.sock.send(db.encode())
                
                else:
                    self.q.put(db)
                
#===================================================
            
            try:
                data = self.sock.recv(1024)
            
            except timeout:
                #logout
                if self.username != None:
                    onlineUser[self.username]['status'] = False
                
                break
                
            data = data.decode()

            
            if data.split()[0] == "login":
                source = data.split()[1]
                if source in block_list:
                    if (time.time() - block_list[source]) < self.block:
                        msg = "block".encode()
                        break
                    else:
                        msg,u_name = verify(data,self.t_out)
                        msg = msg.encode()
                        count += 1
                else:
                    msg,u_name = verify(data,self.t_out)
                    msg = msg.encode()
                    count += 1
            
            elif data.split()[0] == 'ack':
                msg = '>'.encode()

            #connection confirm, user login correctly
            elif data.split()[0] == 'confirm':
                self.username = data.split()[1]
                onlineUser[self.username]['status'] = True
                onlineUser[self.username]['addr'] = self.addr
                onlineUser[self.username]['LAT'] = time.time()
                if self.username in block_list:
                    block_list.pop(self.username)

                for key in onlineUser:
                    if onlineUser[key]['status'] == True and key != self.username:
                        msg =  key + ' ' + self.username + ' ' + 'is_online'
                        self.q.put(msg)
                continue

            elif data.split()[0] == 'logout':
                onlineUser[self.username]['status'] = False
                
                for key in onlineUser:
                    if onlineUser[key]['status'] == True and key != self.username:
                        msg =  key + ' ' + self.username + ' ' + 'is_offline'
                        self.q.put(msg)
                break
            
            elif data.split()[0] == 'message':
                onlineUser[self.username]['LAT'] = time.time()
                chater = data.split()[1]
                print(data)
                #user test
                if chater not in onlineUser:
                    msg = 'user not exist'.encode()
                
                elif onlineUser[chater]['status'] == False:
                    msg = chater + ' ' + self.username + ' ' + data.split()[2]
                    self.q.put(msg)
                    continue
                
                elif onlineUser[chater]['status'] == True and onlineUser[chater]['addr'] != None:
                    #send msg to user
                    msg = chater + ' ' + self.username + ' ' + data.split()[2]
                    self.q.put(msg)
                    continue
                
            elif data.split()[0] == 'broadcast':
                onlineUser[self.username]['LAT'] = time.time()
                for key in onlineUser:
                    if onlineUser[key]['status'] == True and key != self.username:
                        msg =  key + ' ' + self.username + ' ' + data.split()[1] 
                        self.q.put(msg)
                continue

            elif data.split()[0] == 'block':
                onlineUser[self.username]['LAT'] = time.time()
                chater = data.split()[1]
                print(data)
                #user test
                if chater not in onlineUser:
                    msg = 'user not exist'.encode()
                elif chater == self.name:
                    msg = 'you cannot block yourself'.encode()
                else:
                    self.b_user.append(chater)
                    msg = ("you have blocked " + chater).encode()

            elif data.split()[0] == 'unblock':
                onlineUser[self.username]['LAT'] = time.time()
                chater = data.split()[1]
                print(data)
                #user test
                if chater not in self.b_user:
                    msg = 'user not in black list'.encode()
                
                else:
                    self.b_user.remove(chater)
                    msg = ("you have unblocked " + chater).encode()


            elif data.split()[0] == 'whoelse':
                onlineUser[self.username]['LAT'] = time.time()
                msg = ''
                for key in onlineUser:
                    if onlineUser[key]['status'] == True and key != self.username:
                        msg += key +'\n'

                msg = msg.encode()

            elif data.split()[0] == 'whoelsesince':
                onlineUser[self.username]['LAT'] = time.time()
                t = time.time() - int(data.split()[1])
                msg = ''
                for key in onlineUser:
                    if onlineUser[key]['LAT'] == None:
                        continue

                    elif onlineUser[key]['LAT'] >= t and key != self.username:
                        msg += key + '\n'
                
                msg = msg.encode()
            
            elif data.split()[0] == 'startprivate':
                
                onlineUser[self.username]['LAT'] = time.time()
                target = data.split()[1]
                port = data.split()[2]

                if onlineUser[target]['status'] == False:
                    msg = 'user is not online'.encode()
                elif target == self.username:
                    msg = 'cannot p2p yourself'.encode()
                else:
                    
                    mm = 'p2p ' + self.username + ' ' + target + ' ' + str(port)
                    self.q.put(mm)
                    msg = 'waiting for connection'.encode()
                    
                
            else:
                msg = 'invalid command'.encode()

            self.sock.send(msg)        

            if count >= 3:
                block_list[u_name] = time.time()
                break
            
            
        self.sock.send("close".encode())
        self.sock.close()
        print ('Connection from %s:%s closed.' % self.addr)


def main(argv):
    port = int(argv[1])
    block_duration = int(argv[2])
    t_out = int(argv[3])
    

    #create socket
    serversocket = socket(AF_INET,SOCK_STREAM)
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversocket.bind(('localhost',port))
    serversocket.listen(5)
    init_deb()
    q = queue.Queue()
    print("waiting for connection")


    while 1:
        sock, addr = serversocket.accept()

        sock.settimeout(t_out)

        #create socket
        t = link(sock,addr,t_out,block_duration,q) 
        t.start()
    

       
        

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("error: wrong parameters")
        sys.exit()
    main(sys.argv)

