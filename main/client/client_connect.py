import socket
import sys
import time

def start_connecting(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5) 
    try:
        s.connect((HOST, PORT))
    except: # this is exception socket.error:
       print('Cant connect to host')
       sys.exit()
    
    data = '1'
    while not (data == 'Close' or not data):
        print('Input message')
        data = str(input())
        message = data.encode('utf-8')
        s.sendall(message)

if __name__ == '__main__':
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server
    start_connecting(HOST, PORT)
