from ast import arg
import socket
import sys
import os


HEADER = 64
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
    # open file
    f = open(file, 'rb')
    client.send(file.encode(FORMAT))
    client.recv(HEADER).decode(FORMAT)
    # read file and turn to string
    data = f.read(HEADER)
    while data:
        print("This is data")
        print(data)
        client.send(data)
        data = f.read(HEADER)
   
    f.close()
    msg = client.recv(HEADER).decode(FORMAT)
    print(f"[SERVER]: {msg}")

def main(argv):
    ServerIP =  argv[1]
    # print(ServerIP)
    ServerPort = argv[2]
    # print(ServerPort)
    filename = str(argv[3])
    # print(filename)
    send_file(filename, ServerIP, ServerPort)

main(sys.argv)