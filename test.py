# Python GUI
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class client_window(QtWidgets.QMainWindow):
    def showTime(self):
        text = QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.ConnectStatus.setText(text)
    def __init__(self):
        super().__init__()

        #help(QTimer)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        #self.timer_update_GUI = 
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
        self.ConnectStatus = QtWidgets.QLabel("DISCONNECT", self, alignment=QtCore.Qt.AlignCenter)
        self.ConnectStatus.move(10 + self.ConnectButton.geometry().x() + self.ConnectButton.width(), 50)
        self.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")

        buttonwidth = -10 + self.ConnectButton.geometry().x() + self.ConnectButton.width()

        # Process Running button
        self.ProcessRunning = QtWidgets.QPushButton("View running process", self)
        self.ProcessRunning.move(10, 100)
        self.ProcessRunning.setFixedWidth(buttonwidth)

        # App running
        self.AppRunning = QtWidgets.QPushButton("View running application", self)
        self.AppRunning.move(10, 140)
        self.AppRunning.setFixedWidth(buttonwidth)

        # Shutdown
        self.Shutdown = QtWidgets.QPushButton("Shut remote computer down", self)
        self.Shutdown.move(10, 180)
        self.Shutdown.setFixedWidth(buttonwidth)

        # ShotScreen
        self.ShotScreen = QtWidgets.QPushButton("Get Screen Shot", self)
        self.ShotScreen.move(10, 220)
        self.ShotScreen.setFixedWidth(buttonwidth)

        # KeyStroke
        self.KeyStroke = QtWidgets.QPushButton("Get Key Stroke", self)
        self.KeyStroke.move(10, 260)
        self.KeyStroke.setFixedWidth(buttonwidth)

        # RegistryEdit
        self.RegistryEdit = QtWidgets.QPushButton("Edit remote computer registry", self)
        self.RegistryEdit.move(10, 300)
        self.RegistryEdit.setFixedWidth(buttonwidth)

        # QuitButton
        self.QuitButton = QtWidgets.QPushButton("QUIT", self)
        self.QuitButton.move(buttonwidth + 20, 100)
        self.QuitButton.setFixedHeight(self.RegistryEdit.geometry().y() + self.RegistryEdit.height() - 100)


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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = client_window()
    window.show()

    sys.exit(app.exec_())