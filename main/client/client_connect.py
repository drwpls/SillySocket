import socket
import sys
import time
class Client_Connection:
    def __init__(self):
        self.timeout = 1800
        self.connect_status = 0
        self.host = '0.0.0.0'
        self.port = 0 
        self.mainsock = 0
        self.err = None

    def start_connect(self, host, port):
        
        self.host = host
        self.port = port
        self.mainsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.mainsock.connect((self.host, self.port))

        except ConnectionRefusedError as e: # this is exception socket.error:
            print('Cant connect to host', e)
            self.connect_status = 0
            return
        else:
            self.connect_status = 1
            print('Connected to server ', self.mainsock.getpeername())
        
        # begin transfer data: (for commandline debugger)
        '''
        data = '1'
        while not (data == 'Close' or not data):
            print('Input message')
            data = str(input())
            message = data.encode('utf-8')
            s.sendall(message)
            '''
        
        # keep thread running
        data = '1'
        while not (data == 'Close' or not data) and self.connect_status:
            pass
    
    def send_message(self, message):
        message = message.encode('utf-8')
        try:
            self.mainsock.sendall(message)
        except ConnectionAbortedError:
            print('Lost connection from ', self.mainsock.getpeername())
            self.connect_status = 0
        except ConnectionResetError:
            print('Lost connection from ', self.mainsock.getpeername())
            self.connect_status = 0
    def stop_connect(self):
        print('Closed connection to ', self.mainsock.getpeername())
        endmessage = 'Close'
        self.send_message(endmessage)
        self.connect_status = 0

if __name__ == '__main__':
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server
    client_connection = Client_Connection()
    client_connection.start_connect(HOST, PORT)
