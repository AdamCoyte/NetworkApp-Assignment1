from email.headerregistry import Address
import socket
import sys
import os

HEADER = 1024
# set port
PORT = 5454     
# get host IP address of server
SERVER = "192.168.0.127"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_MESSAGE = "!DISCONNECT"
SEPERATOR = "<SEPERATOR>"


def handle_response(conn, addr):
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


def send_file(file, ip, port):
    
    filesize = os.path.getsize(file)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    f = open(file, 'r')
    print("Sending. . .")

    data = f.read()
    client.send(file.encode(FORMAT))
    msg = client.recv(HEADER).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    f.close()
    client.close()

def main():
    ServerIP = SERVER #argv[1]
    ServerPort = PORT #argv[2]
    filename = "file.txt" #argv[3]
    send_file(filename, ServerIP, ServerPort)

main()