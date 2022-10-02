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


def download_file(file, ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(file.encode(FORMAT))
    
    RequestInfo = client.recv(HEADER)
    print(RequestInfo.decode(FORMAT))
    
    ResponseCheck = str(RequestInfo)
    if "[not]" in ResponseCheck.split(" "):
        info = client.recv(HEADER)
        print(info.decode(FORMAT))  
    elif RequestInfo:
        filename = open(file, 'wb')          
        fileData = client.recv(HEADER)
        print(f"Downloading file {file}")
        while fileData:
            filename.write(fileData)
            fileData = client.recv(HEADER)
        print("Download Complete")
        filename.close()
    else:
        print("No Connection Found")
    client.close()
    
def main(argv):
    ServerIP =  argv[1]
    # print(ServerIP)
    ServerPort = argv[2]
    # print(ServerPort)
    filename = str(argv[3])
    # print(filename)
    download_file(filename, ServerIP, ServerPort)

main(sys.argv)