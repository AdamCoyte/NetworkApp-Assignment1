from concurrent.futures import ThreadPoolExecutor
from ctypes import resize
from genericpath import isfile
from itertools import count
import multiprocessing
from sqlite3 import connect
from threading import Lock
import socket
import time
import os

# Header to send how long the message is
HEADER = 64
# set port
PORT = 5454

# get host IP address of server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8' 
DC_MESSAGE = "!DISCONNECT"


REQUESTNO = 0
REQUESTSUCCESS = 0

def count_request(bool, lock, conn):
    global REQUESTNO
    global REQUESTSUCCESS
    with lock:
        REQUESTNO += 1
        if bool == True:
            REQUESTSUCCESS += 1
            requestAmount = "Server handled {} requests, {} requests were successful".format(REQUESTNO, REQUESTSUCCESS)
            conn.send(requestAmount.encode(FORMAT))
        else:
            requestAmount = "Server handled {} requests, {} requests were successful".format(REQUESTNO, REQUESTSUCCESS)
            conn.send(requestAmount.encode(FORMAT))

def handle_client(conn, addr, lock):
    connected = True
    global REQUESTNO
    global REQUESTSUCCESS
    filename = conn.recv(HEADER).decode(FORMAT)
    requestInfo = "REQ <{}>: File {} requested from {}".format(REQUESTNO,filename,addr)    
    print(requestInfo)  

    while connected:
    # wait for message from client, use HEADER and FORMAT for receiving the message
        if os.path.isfile(filename):
            count_request(True, lock, conn)
            # open file
            f = open(filename, 'rb')
            # read file
            
            
            data = f.read(HEADER)
            
            while (data):
                conn.send(data)
                data = f.read(HEADER)    
            print(f"REQ <{REQUESTNO}>: File transfer complete")
            f.close()
            connected = False
        else:
            conn.send(f"File {filename} [not] found at server.".encode(FORMAT))
            count_request(False, lock, conn)
            print(f"REQ <{REQUESTNO}>: [Not] Successful")
            connected = False
            
        print(f"REQ <{REQUESTNO}>: Total successful requests so far = {REQUESTSUCCESS}")
    conn.close()
        

def start():
    # create a socket instance, specify IPv4 and TCP
    # TCP is needed because send files require acknoledgements 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the address to the socket
    server.bind(ADDR)  
    server.listen()
    with ThreadPoolExecutor(max_workers=10) as executer:
        while True:
            # create lock
            conn, addr = server.accept()
            print(conn)
            with conn:
                # start the handling of threads     
                lock = Lock()
                result = executer.submit(handle_client, conn, addr, lock)
                print(result)

print("[STARTING]... Server is Starting. Please Wait")
print(SERVER)
start()