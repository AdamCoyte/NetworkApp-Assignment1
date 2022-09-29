import socket
from sqlite3 import connect
import threading
import time

# Header to send how long the message is
HEADER = 16
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
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DC_MESSAGE:
                connected = False
            
            print(f"[{addr}] {msg}")

            
        


def start():
    server.listen()
    while True:
        # waiting for connection to server. saving information of connections
        # such as port and address of the client

        conn, addr = server.accept()
        
        # start the handling of threads
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # print amount of active connections (-1 because of this start thread)
        active_connection = "[ACTIVE CONNECTIONS:] {}"
        print(active_connection.format(threading.active_count() -1))

print("[STARTING]... Server is Starting. Please Wait")
print(SERVER)
start()