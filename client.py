from socket import *
import os
import time
import sys
import threading
from queue import Queue
import threading
from handlers import *


def login(sock):
    username = input("Username:")
    password = input("Password:")

    msg = ("login " + username + ' ' + password).encode()
    sock.send(msg)

    while 1:
        data = sock.recv(1024)
        data = data.decode()
        
        if data == "close":
            return None

        elif data == "block":
            print("You have been blocked")
            return None
        
        elif data == "wrong message":
            print("wrong input,please try agin later")
            return None
        
        elif data == "wrong u_name":
            print("User name does not exist")
            username = input("Username:")
            password = input("Password:")

            msg = ("login " + username + ' ' + password).encode()
            sock.send(msg)
            continue
        
        elif data == "wrong password":
            print("Invalid password. Please try again")
            password = input("Password:")

            msg = ("login " + username + ' ' + password).encode()
            sock.send(msg)
            continue
        
        elif data == "online":
            print("User has log in already")
            return None

        elif data.split()[0] == "success":
            return data + " " + username 


def main(argv):
    #create connection between server and client
    server_IP = argv[1]
    server_port = int(argv[2])
    
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.connect((server_IP, server_port))

    #create p2p socket
    p = socket(AF_INET,SOCK_STREAM)
    p.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    p.bind(('', 0))
    p.listen(5)
    p_port = p.getsockname()[1]

    #login
    verify_msg = login(s) 

    #login success
    if verify_msg != None:
        username = verify_msg.split()[2]
        
        msg = "confirm " + username
        s.send(msg.encode())
        print("Welcome\nPlease enter commands as format\n")
        #connection success
        q = Queue()

        send_thread = send_handler(s,q,p_port)
        send_thread.start()

        recv_thread = recv_handler(s,q)
        recv_thread.start() 

        p2p_1 = p2p_recv(p,q,p_port)
        p2p_2 = p2p_send(q,p_port)

        p2p_1.start()
        p2p_2.start()

        c = ack(s)
        c.start()

        send_thread.join()
        recv_thread.join()
        p2p_1.join()
        p2p_2.join()

        
    else:
        #connection Fail
        print("connection denied")
        s.close() 

   

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("error: wrong paramaters")
        sys.exit()
    main(sys.argv)