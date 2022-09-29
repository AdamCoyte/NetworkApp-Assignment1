from concurrent.futures import ThreadPoolExecutor
from genericpath import isfile
import socket
from sqlite3 import connect
import time
import os

# Header to send how long the message is
HEADER = 8
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
    totalRequests = 0
    successfullRequests = 0
    while connected:
    # wait for message from client, use HEADER and FORMAT for receiving the message
        filename = conn.recv(HEADER).decode(FORMAT)
        print(f"[{addr}] {filename}")
        totalRequests += 1 
        if os.path.isfile(filename):
            conn.send("File Already Exists".encode(FORMAT))            
            connected = False
        else:
            conn.send("File {filename} [not] found at server.".encode(FORMAT))
            file = open(filename, 'wb') 
            data = conn.recv(HEADER).decode()
            print("This is data:")
            print(data)          
            while data:      
                file.write(data)    
                data = conn.recv(HEADER)
                print(data)
            conn.send("File data received:".encode(FORMAT))
            print(f"[RECEIVED]: {filename}")
            file.close()
            connected = False
            successfullRequests += 1

            
        


def start():
    server.listen()
    while True:
        # waiting for connection to server. saving information of connections
        # such as port and address of the client

        conn, addr = server.accept()
        
        # start the handling of threads
        with ThreadPoolExecutor(max_workers=10) as executer:
            result = executer.submit(handle_client, conn, addr)
        # thread = threading.Thread(target=handle_client, args=(conn, addr))
        # thread.start()

        # print amount of active connections (-1 because of this start thread)
        active_connection = "[ACTIVE CONNECTIONS:] {}"
        print(result.result())

print("[STARTING]... Server is Starting. Please Wait")
print(SERVER)
start()