import socket







HEADER = 16
# set port
PORT = 5454     

# get host IP address of server
SERVER = "192.168.0.127"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_MESSAGE = "!DISCONNECT"  
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)