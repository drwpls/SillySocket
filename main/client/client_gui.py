# Python GUI
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class client_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # create windows title and its size
        self.setWindowTitle("Client")      
        self.setFixedSize(500, 400)

        # IP box
        self.IPTextBox = QtWidgets.QLineEdit("Server IP", self)
        self.IPTextBox.move(10,50)
        self.IPTextBox.setFixedWidth(200)

        # Port box
        self.PortTextBox =  QtWidgets.QLineEdit("Port", self)
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


        #self.button.clicked.connect(self.magic)
    '''
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        '''

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = client_window()
    window.show()

    sys.exit(app.exec_())