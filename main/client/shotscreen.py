import socket
from PIL import Image, ImageGrab
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging
import io
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
        self.resize(850, 400)

        self.Picture_box = QtWidgets.QLabel(self)
        #self.Picture_box.setFixedSize(800,400)
        self.Picture_box.move(0, 10)
        self.Picture_box.resize(828, 393)

        self.Picture_Layout = QtWidgets.QHBoxLayout(self)
        self.Picture_Layout.addWidget(self.Picture_box)        

        self.TakeButton = QtWidgets.QPushButton('Take', self)
        self.TakeButton.move(720, 10)

        self.SaveButton = QtWidgets.QPushButton('Save', self)
        self.SaveButton.move(720, 50)

        self.TakeButton.clicked.connect(self.click_takebutton)
        self.SaveButton.clicked.connect(self.click_savebutton)
        self.click_takebutton()

    def click_takebutton(self):
        message = FEATURE_CODE['ShotScreen'] + 'take'
        message = message.encode('utf-8')
        self.sock.sendall(message)
        self.img = self.receive_screenshot()

        self.Pixmap = QtGui.QPixmap()
        if self.Pixmap.loadFromData(self.img, 'png'):
            myScaledPixmap = self.Pixmap.scaled(self.Picture_box.size(), QtGui.Qt.KeepAspectRatio) 
            self.Picture_box.setPixmap(myScaledPixmap)
        else:
            self.Picture_box.setText('Invalid Img')

    def receive_screenshot(self):
        img = io.BytesIO()
        data = self.sock.recv(512*1024)
        while data and data[-4:] != b'done':
            #logging.debug('data is {}'.format(data))
            img.write(data)
            data = self.sock.recv(512*1024)
        
        img.write(data[:-4])
        return img.getvalue()

    def click_savebutton(self):
        filename = self.get_save_filename()
        if filename:
            stream = open(filename, 'wb')
            stream.write(self.img)
            stream.close()

    def get_save_filename(self):
        file_filter = 'Image (*.png)'
        response = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a data file',
            filter=file_filter,
        )
        print(response)
        return response[0]

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ShotScreen_Dialog()
    window.show()
    sys.exit(app.exec_())