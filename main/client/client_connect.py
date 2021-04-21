import socket
import time
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = '1'
while data != 'close':
    print('Input message')
    data = str(input())
    message = data.encode('utf-8')
    s.sendall(message)
