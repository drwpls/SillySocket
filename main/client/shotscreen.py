import socket
from PIL import Image, ImageGrab
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging

logging.basicConfig(level=logging.DEBUG)

FEATURE_CODE = {
    'PING' : '00',
    'ProcessRunning' : '01',
    'AppRunning' : '02',
    'Shutdown' : '03',
    'ShotScreen' : '04',
    'KeyStroke' : '05',
    'RegistryEdit' : '06',
}

class ShotScreen_Dialog(QtWidgets.QDialog):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.setWindowTitle('ScreenShot')      
        #self.setFixedSize(1000, 500)
        self.resize(830, 410)

        self.Picture_box = QtWidgets.QLabel(self)
        #self.Picture_box.setFixedSize(800,400)
        self.Picture_box.move(0, 10)
        self.Picture_box.resize(400, 710)

        self.Picture_Layout = QtWidgets.QHBoxLayout(self)
        self.Picture_Layout.addWidget(self.Picture_box)        

        self.TakeButton = QtWidgets.QPushButton('Take', self)
        self.TakeButton.move(720, 10)

        self.SaveButton = QtWidgets.QPushButton('Save', self)
        self.SaveButton.move(720, 50)

        self.TakeButton.clicked.connect(self.click_takebutton)
        self.click_takebutton()
        
    def click_takebutton(self):
        message = FEATURE_CODE['ShotScreen'] + 'take'
        message = message.encode('utf-8')
        self.sock.sendall(message)
        self.receive_screenshot()

        self.Pixmap = QtGui.QPixmap('received.png')
        myScaledPixmap = self.Pixmap.scaled(self.Picture_box.size(), QtGui.Qt.KeepAspectRatio) 
        self.Picture_box.setPixmap(myScaledPixmap)

    def receive_screenshot(self):
        img = open('received.png', 'wb')
        
        data = ''
        data = self.sock.recv(1024)
        while data and data[-4:] != b'done':
            #logging.debug('data is {}'.format(data))
            img.write(data)
            data = self.sock.recv(1024)
        
        img.write(data[:-4])
        img.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ShotScreen_Dialog()
    window.show()
    sys.exit(app.exec_())