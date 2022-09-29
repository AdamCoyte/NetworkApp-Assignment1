from concurrent.futures import ThreadPoolExecutor
from genericpath import isfile
import socket
from sqlite3 import connect
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

# create a socket instance, specify IPv4 and TCP
# TCP is needed because send files require acknoledgements 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the address to the socket
server.bind(ADDR)
REQUESTNO = 0
REQUESTSUCCESS = 0


def handle_client(conn, addr):
    connected = True
    global REQUESTNO
    global REQUESTSUCCESS
    totalRequests = REQUESTNO
    successfullRequests = REQUESTSUCCESS
    filename = conn.recv(HEADER).decode(FORMAT)
    while connected:

    # wait for message from client, use HEADER and FORMAT for receiving the message
        conn.send("[CONNECTED]".encode(FORMAT))
        print(f"REQ <{totalRequests}>: File {filename} requested from {addr}")
        REQUESTNO += 1 
        if os.path.isfile(filename):
            # open file
            f = open(filename, 'rb')
            # read file and turn to string
            data = f.read(HEADER)
            while data:
                print("This is data")
                print(data)
                conn.send(data)
                data = f.read(HEADER)
                REQUESTSUCCESS += 1
                successfullRequests += 1
            f.close()
           

        else:
            conn.send("File {filename} [not] found at server.".encode(FORMAT))
            print(f"REQ <{totalRequests}>: [Not] Successful")
            print(f"REQ <{totalRequests}>File transfer complete")
            connected = False

        print(f"REQ <{totalRequests}>: Total successful requests so far = {successfullRequests}")





def start():
    server.listen()
    while True:
        # waiting for connection to server. saving information of connections
        # such as port and address of the client

        conn, addr = server.accept()
        
        # start the handling of threads
        with ThreadPoolExecutor(max_workers=10) as executer:
            result = executer.submit(handle_client, conn, addr)

        active_connection = "[ACTIVE CONNECTIONS:] {}"

print("[STARTING]... Server is Starting. Please Wait")
print(SERVER)
start()