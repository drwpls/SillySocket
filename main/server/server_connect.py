import selectors    # working with multi-clients
import socket       # socket 

class Server_Connection:
    def __init__(self, host, port):
        self.connect_status = 0
        self.sel = selectors.DefaultSelector()           # Monitor will hand all of connections    
        self.host = host
        self.port = port

    def start_listen(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # USE TCP/IP Connection
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sel.register(self.server_sock, selectors.EVENT_READ, data=None)
        self.server_sock.bind((self.host, self.port))  
        # accept 10 connections
        self.server_sock.listen(10) 
        self.connect_status = 1 # set to start listening flag, 1 is one socket (server_sock)
        print('listening on', (self.host, self.port))
        while self.connect_status:
            event = self.sel.select(timeout = 0) # timeout = 0: wait until event appear
            for key, mask in event:
                if key.data == None:     # client start connects to server (key.data is None = not registered)
                    self.start_connect(key.fileobj)
                else:                   # service connects
                    self.service_connect(key, mask)
    def stop_listen(self):
        s = self.sel.get_map()
        keys = [i for i in s]
        fileobjs = [s[i] for i in keys]

        # None tell except server_socket
        socks = [file_obj[0] for file_obj in fileobjs if file_obj[3] != None]

        # for short, but not use because of readability
        #_socks = [s[i][0] for i in s if s[i][3] != None]
        
        for sock in socks:
            print('Stop connection with ', sock.getpeername())
            sock.close()
            self.sel.unregister(sock)

        #self.server_sock.shutdown(socket.SHUT_RDWR)
        print ('1')
        self.connect_status = 0 # set to disconnected flag
        self.server_sock.close()
        self.sel.unregister(self.server_sock)
        
        print('stop_listen')


    def start_connect(self, _sock):
        _connect, _address = _sock.accept() # accpet connection from client
        _connect.setblocking(False)         # set sock not block
        _data = _address    
        _event = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(_connect, events = _event, data = _data)        # register this connect to sel, with wait-event are both read & write
        self.connect_status += 1
        print('Start connection with ', _address)

    def stop_connect(self, _sock):
        self.sel.unregister(_sock)
        self.connect_status -= 1
        _sock.close()

    def service_connect(self, _key, _mask):
        _sock = _key.fileobj
        _address = _key.data
        
        if _mask & selectors.EVENT_READ:
            try:
                recv_data = _sock.recv(1024)  # read data
            except ConnectionResetError:
                print('Forcibly closed by ', _address)
                self.stop_connect(_sock)
            else:
                if recv_data and recv_data != b'Close':
                    print('Message from ', _address, recv_data)
                else:
                    print('Closing connection to', _address)
                    self.stop_connect(_sock)  
            
        if _mask & selectors.EVENT_WRITE:
            pass

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 65432
    start_listen(host, port)