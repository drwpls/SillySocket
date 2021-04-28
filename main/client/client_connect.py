import socket
import sys
import time
import logging
from enum import Enum, auto
# for debugging
logging.basicConfig(level=logging.DEBUG)

class Client_Connection:
    def __init__(self):
        self.connect_status = self.Status_Code.DISCONNECT
        self.host = '0.0.0.0'
        self.port = 0 
        self.mainsock = 0
        self.lost_connect = False

    def start_connect(self, host, port, DEBUGGING = False):
        self.host = host
        self.port = port
        self.mainsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.mainsock.connect((self.host, self.port))
        except (ConnectionRefusedError, TimeoutError) as e: # this is exception socket.error:
            logging.debug('Cannot connect to host {}'.format(e))
            self.connect_status =  self.Status_Code.TIMEOUT   # Timout-status
            return
        else:
            logging.debug('Connected to server {}'.format(self.mainsock.getpeername()))
            self.connect_status =  self.Status_Code.CONNECTED
        
        # begin transfer data: (for commandline debugger)
        if DEBUGGING == True:
            data = '1'
            while not (data == 'Close' or not data):
                print('Input message')
                data = str(input())
                message = data.encode('utf-8')
                self.mainsock.sendall(message)
        else:
            # keep thread running
            data = '1'
            while not (data == 'Close' or not data) and self.connect_status ==  self.Status_Code.CONNECTED:
                pass
    
    def send_message(self, message):
        message = message.encode('utf-8')
        try:
            self.mainsock.sendall(message)
        except: # ConnectionAbortedError and ConnectionResetError
            logging.debug('Lost connection from {}'.format(self.mainsock.getpeername()))
            self.connect_status =  self.Status_Code.DISCONNECT
            self.lost_connect = True

    def stop_connect(self):
        logging.debug('Closed connection to {}'.format(self.mainsock.getpeername()))
        endmessage = 'Close'
        self.send_message(endmessage)
        self.connect_status =  self.Status_Code.DISCONNECT

    class Status_Code(Enum):
        CONNECTED = auto(),
        DISCONNECT = auto(),
        CONNECTING = auto(),
        TIMEOUT = auto()

if __name__ == '__main__':
    HOST = '192.168.1.11'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server
    client_connection = Client_Connection()
    client_connection.start_connect(HOST, PORT, True)