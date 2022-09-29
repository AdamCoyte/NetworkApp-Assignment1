from email.headerregistry import Address
import socket
import sys
import os

HEADER = 16
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
    f = open(file, 'rb')
    print("Sending. . .")
    l = f.read(1024)
    while(l):
        client.send(l)
        l = f.read(1024)
    f.close()
    print("Finished Sending")
    client.close()

def main(argv):
    ServerIP = argv[1]
    ServerPort = argv[2]
    filename = argv[3]
    send_file(filename, ServerIP, ServerPort)

main(SERVER, PORT, "README")