import socket
from PIL import Image, ImageGrab

def receive_screenshot(sock):
    img = open('received.png', 'wb')

    data = sock.recv(1024)
    while data and data.decode('utf8') != 'done':
        img.write(data)
        data = sock.recv(1024)
    
    img.close()