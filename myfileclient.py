import socket
import sys
import os


HEADER = 1200
# set port
PORT = 5454     
# get host IP address of server
FORMAT = 'utf-8'


def download_file(file, ip, port):
    
    # setup the socket and connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    client.connect((ip,int(port)))
    
    # send the name of the file
    client.send(file.encode(FORMAT))

    # receive information based on previous requests
    RequestInfo = client.recv(HEADER)
    RequestInfo = RequestInfo.decode(FORMAT)
    print(RequestInfo) 
    
    ResponseCheck = str(RequestInfo)
    # we'll search the response to see if the server has the requested file
    if "[not]" in ResponseCheck.split(" "):
        info = client.recv(HEADER)
        print(info.decode(FORMAT))
    elif "successful" in ResponseCheck.split(" "):
        # the server found the file and we'll start downloading
        
        filename = open(file, 'wb')          
        fileData = client.recv(HEADER)
        print(f"Downloading file {file}")
        # start receiving data
        
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