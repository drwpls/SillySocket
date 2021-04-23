# Python GUI
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import logging

logging.basicConfig(level=logging.DEBUG)

class client_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer_update_GUI = QtCore.QTimer()
        #self.timer_update_GUI.start(500) # Update every 500ms

        # create windows title and its size
        self.setWindowTitle("Client")      
        self.setFixedSize(500, 500)

        # IP box
        self.IPTextBox = QtWidgets.QLineEdit("127.0.0.1", self)
        self.IPTextBox.setInputMask('000.000.000.000;_')
        self.IPTextBox.move(10,50)
        self.IPTextBox.setFixedWidth(200)

        # Port box
        self.PortTextBox =  QtWidgets.QLineEdit("65432", self)
        self.PortTextBox.setInputMask('00000;_')
        self.PortTextBox.move(self.IPTextBox.geometry().x() + self.IPTextBox.width(),50)
        self.PortTextBox.setFixedWidth(50)
    

        # Connect Button
        self.ConnectButton = QtWidgets.QPushButton("Connect!", self)
        self.ConnectButton.move(self.PortTextBox.geometry().x() + self.PortTextBox.width(), 50)
        
        # Connect status
        self.ConnectStatus = QtWidgets.QLabel("DISCONNECT!", self, alignment=QtCore.Qt.AlignCenter)
        self.ConnectStatus.move(10 + self.ConnectButton.geometry().x() + self.ConnectButton.width(), 50)
        self.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")

        buttonwidth = -10 + self.ConnectButton.geometry().x() + self.ConnectButton.width()

        # Process Running button
        self.ProcessRunningButton = QtWidgets.QPushButton("View running process", self)
        self.ProcessRunningButton.move(10, 100)
        self.ProcessRunningButton.setFixedWidth(buttonwidth)

        # App running
        self.AppRunningButton = QtWidgets.QPushButton("View running application", self)
        self.AppRunningButton.move(10, 140)
        self.AppRunningButton.setFixedWidth(buttonwidth)

        # Shutdown
        self.ShutdownButton = QtWidgets.QPushButton("Shut remote computer down", self)
        self.ShutdownButton.move(10, 180)
        self.ShutdownButton.setFixedWidth(buttonwidth)

        # ShotScreen
        self.ShotScreenButton = QtWidgets.QPushButton("Get Screen Shot", self)
        self.ShotScreenButton.move(10, 220)
        self.ShotScreenButton.setFixedWidth(buttonwidth)

        # KeyStroke
        self.KeyStrokeButton = QtWidgets.QPushButton("Get Key Stroke", self)
        self.KeyStrokeButton.move(10, 260)
        self.KeyStrokeButton.setFixedWidth(buttonwidth)

        # RegistryEdit
        self.RegistryEditButton = QtWidgets.QPushButton("Edit remote computer registry", self)
        self.RegistryEditButton.move(10, 300)
        self.RegistryEditButton.setFixedWidth(buttonwidth)

        # QuitButton
        self.QuitButton = QtWidgets.QPushButton("QUIT", self)
        self.QuitButton.move(buttonwidth + 20, 100)
        self.QuitButton.setFixedHeight(self.RegistryEditButton.geometry().y() + self.RegistryEditButton.height() - 100)

        #inputdebugger:
        self.Input = QtWidgets.QLineEdit(self)
        self.Input.move(10, 350)
        self.Input.setFixedWidth(buttonwidth)

        #outputdebugger
        self.OutputPanel = QtWidgets.QLabel('', self)
        self.OutputPanel.move(10, 380)
        self.OutputPanel.setFixedWidth(buttonwidth)
        self.OutputPanel.setFixedHeight(100)
        self.OutputPanel.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")

        #SentButton
        self.SentButton = QtWidgets.QPushButton('SEND', self)
        self.SentButton.move(buttonwidth + 20, 380)
        self.SentButton.setFixedHeight(100)

    @QtCore.Slot()
    def add_Click_Behavior(self, obj, func):
        obj.clicked.connect(func)

    def showError(self, error = 'NO CONNECTION', message = 'Please connect to server first'):
        msg = QtWidgets.QMessageBox()
        msg.setFixedWidth(200)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(error)
        msg.setInformativeText(message)
        msg.setWindowTitle(error)
        return msg

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = client_window()
    window.show()

    sys.exit(app.exec_())