import selectors    # working with multi-clients
import socket       # socket 

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui        # GUI

sel = selectors.DefaultSelector()           # Monitor will hand all of connections

def start_connect(_sock):
    _connect, _address = _sock.accept() # accpet connection from client
    _connect.setblocking(False)         # set sock not block
    _data = _address    
    _event = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(_connect, events = _event, data = _data)        # register this connect to sel, with wait-event are both read & write

def service_connect(_key, _mask):
    _sock = _key.fileobj
    _address = _key.data
    
    if _mask & selectors.EVENT_READ:
        recv_data = _sock.recv(1024)  # read data
        if recv_data and recv_data != 'Close':
            print('Message from ', _address, recv_data)
        else:
            print('closing connection to', _address)
            sel.unregister(_sock)
            _sock.close()
        
    if _mask & selectors.EVENT_WRITE:
        pass

def start_listening(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # USE TCP/IP Connection
    sock.bind((host, port)) 
    print('listening on', (host, port))
    sock.listen(10)          # accept 10 connections

    sel.register(sock, selectors.EVENT_READ, data=None)

    while True:
        event = sel.select(timeout = 0) # timeout = 0: wait until event appear
        for key, mask in event:
            if key.data == None:     # client start connects to server (key.data is None = not registered)
                start_connect(key.fileobj)
            else:                   # service connects
                service_connect(key, mask)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 65432
    start_listening(host, port)