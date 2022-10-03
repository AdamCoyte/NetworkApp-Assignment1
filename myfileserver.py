from concurrent.futures import ThreadPoolExecutor
from genericpath import isfile
from threading import Lock
import socket
import time
import os

# Header to send how long the message is
HEADER = 1200
# set port
PORT = 5454
# get host IP address of server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8' 
REQUESTNO = 0
REQUESTSUCCESS = 0


# this function handles using the lock and keeping track of the amount of total and successful requests
def count_request(bool, lock, conn):
    global REQUESTNO
    global REQUESTSUCCESS
    
    # make sure to acquire the lock since we'll be changing global variables
    lock.acquire()
    REQUESTNO += 1
    if bool == True:
        REQUESTSUCCESS += 1
        requestAmount = "Server handled {} requests, {} requests were successful".format(REQUESTNO, REQUESTSUCCESS)
        print(requestAmount)
        conn.send(requestAmount.encode(FORMAT))
        # release the lock
        lock.release()
        return 0
    elif bool == False:
        requestAmount = "Server handled {} requests, {} requests were successful".format(REQUESTNO, REQUESTSUCCESS)
        conn.send(requestAmount.encode(FORMAT))
        # release the lock
        lock.release()
        return 0


def handle_client(conn, addr, lock):
    # set a boolean to keep track of the state of our connection
    connected = True
    global REQUESTNO
    global REQUESTSUCCESS
    
    # receive the filename
    filename = conn.recv(HEADER).decode(FORMAT)
    requestInfo = "REQ <{}>: File {} requested from {}".format(REQUESTNO,filename,addr)    
    print(requestInfo)
    
    while connected:
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
            # file was not found
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
    # setup to listen for connections
    server.listen()
    #create a lock. We need this since we use multithreading and are using global variables
    lock = Lock()
    with ThreadPoolExecutor(max_workers=10) as executer:
        while True:
            # create lock
            conn, addr = server.accept()
            # send off worker to handle client            
            result = executer.submit(handle_client, conn, addr, lock)
    

print("[STARTING]... Server is Starting. Please Wait")
print(SERVER)
# start the server
start()