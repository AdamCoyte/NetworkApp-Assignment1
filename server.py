from ast import While
from concurrent.futures import ThreadPoolExecutor
from genericpath import isfile
import socket
from sqlite3 import connect
import time
import os

# Header to send how long the message is
HEADER = 1024
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


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
    # wait for message from client, use HEADER and FORMAT for receiving the message
        filename = conn.recv(HEADER).decode(FORMAT)
        print(filename)
        print("1")
        print(f"[RECEIVED]: {filename}")
        print(f"[{addr}] {filename}")
        conn.send("Server handled {} requests, {} were successful".encode(FORMAT))
        if os.path.isfile(filename):
            conn.send("File Already Exists".encode(FORMAT))
            connected = False
        else:
            conn.send("File {filename} [not] found at server.".encode(FORMAT))
            file = open(filename, 'w') 
            data = conn.recv(HEADER).decode(FORMAT)            
            while data:        
                file.write(data)
                conn.send("File data received:".encode(FORMAT))
                data.recv(HEADER).decode(FORMAT)
            file.close()
            connected = False
    
            
        


def start():
    server.listen()
    while True:
        # waiting for connection to server. saving information of connections
        # such as port and address of the client

        conn, addr = server.accept()
        
        # start the handling of threads
        executer = ThreadPoolExecutor(max_workers=10)
        result = executer.submit(handle_client, conn, addr)
        # thread = threading.Thread(target=handle_client, args=(conn, addr))
        # thread.start()

        # print amount of active connections (-1 because of this start thread)
        active_connection = "[ACTIVE CONNECTIONS:] {}"
        print(result.result())

print("[STARTING]... Server is Starting. Please Wait")
print(SERVER)
start()