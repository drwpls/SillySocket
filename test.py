import socket
from PIL import Image, ImageGrab
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging

logging.basicConfig(level=logging.DEBUG)
class ScreenShot_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ScreenShot')      
        #self.setFixedSize(1000, 500)
        self.resize(830, 410)

        self.Picture_box = QtWidgets.QLabel(self)
        #self.Picture_box.setFixedSize(800,400)
        self.Picture_box.move(0, 10)
        self.Picture_box.resize(400, 710)

        self.Pixmap = QtGui.QPixmap('example.png')
        myScaledPixmap = self.Pixmap.scaled(self.Picture_box.size(), QtGui.Qt.KeepAspectRatio) 
        self.Picture_box.setPixmap(myScaledPixmap)

        self.Picture_Layout = QtWidgets.QHBoxLayout(self)
        self.Picture_Layout.addWidget(self.Picture_box)

        self.TakeButton = QtWidgets.QPushButton('Take', self)
        self.TakeButton.move(720, 10)

        self.SaveButton = QtWidgets.QPushButton('Save', self)
        self.SaveButton.move(720, 50)
        
        #self.show()

def receive_screenshot(sock):
    img = open('received.png', 'wb')

    data = sock.recv(1024)
    while data and data.decode('utf8') != 'done':
        img.write(data)
        data = sock.recv(1024)
    
    img.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ScreenShot_Dialog()
    window.show()
    sys.exit(app.exec_())