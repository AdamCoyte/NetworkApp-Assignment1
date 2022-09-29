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


def send_file(file, ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(file.encode(FORMAT))
    file = open(file, 'wb')
    msg = client.recv(HEADER)
    print(msg)
    fileData = client.recv(HEADER)
    while fileData:
        file.write(fileData)
        print(fileData)
        fileData = client.recv(HEADER)
    print(f"[SERVER]: {msg}")
    file.close()
    client.send("File Transfer complete")
    
def main(argv):
    ServerIP =  argv[1]
    # print(ServerIP)
    ServerPort = argv[2]
    # print(ServerPort)
    filename = str(argv[3])
    # print(filename)
    send_file(filename, ServerIP, ServerPort)

main(sys.argv)