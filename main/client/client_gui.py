# Python GUI
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging
from enum import Enum, auto

logging.basicConfig(level=logging.DEBUG)

class client_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer_update_GUI = QtCore.QTimer()
        # self.timer_update_GUI.start(500) # Update every 500ms

        # create windows title and its size
        self.setWindowTitle("Client")
        self.setFixedSize(500, 500)

        # IP box
        self.IPTextBox = QtWidgets.QLineEdit("127.0.0.1", self)
        # self.IPTextBox.setInputMask('000.000.000.000')
        self.IPTextBox.move(10, 50)
        self.IPTextBox.setFixedWidth(200)

        # Port box
        self.PortTextBox = QtWidgets.QLineEdit("65432", self)
        self.validator = QtGui.QIntValidator(0, 65535, self)
        self.PortTextBox.setValidator(self.validator)

        self.PortTextBox.move(self.IPTextBox.geometry().x() + self.IPTextBox.width() + 5, 50)
        self.PortTextBox.setFixedWidth(50)

        # Connect Button
        self.ConnectButton = QtWidgets.QPushButton("Connect!", self)
        self.ConnectButton.move(self.PortTextBox.geometry().x() + self.PortTextBox.width() + 5, 50)

        # Connect status
        self.ConnectStatus = QtWidgets.QLabel("DISCONNECTED!", self, alignment=QtCore.Qt.AlignCenter)
        self.ConnectStatus.move(10 + self.ConnectButton.geometry().x() + self.ConnectButton.width(), 50)
        self.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")

        buttonwidth = -10 + self.ConnectButton.geometry().x() + self.ConnectButton.width()

        # Process Running button
        self.ProcessRunningButton = QtWidgets.QPushButton("View running processes", self)
        self.ProcessRunningButton.move(10, 100)
        self.ProcessRunningButton.setFixedWidth(buttonwidth)

        # App running
        self.AppRunningButton = QtWidgets.QPushButton("View running applications", self)
        self.AppRunningButton.move(10, 140)
        self.AppRunningButton.setFixedWidth(buttonwidth)

        # Shutdown
        self.ShutdownButton = QtWidgets.QPushButton("Shut down remote computer", self)
        self.ShutdownButton.move(10, 180)
        self.ShutdownButton.setFixedWidth(buttonwidth)

        # Screenshot
        self.ScreenshotButton = QtWidgets.QPushButton("Take screenshot", self)
        self.ScreenshotButton.move(10, 220)
        self.ScreenshotButton.setFixedWidth(buttonwidth)

        # Keystroke
        self.KeystrokeButton = QtWidgets.QPushButton("Get keystroke", self)
        self.KeystrokeButton.move(10, 260)
        self.KeystrokeButton.setFixedWidth(buttonwidth)

        # RegistryEdit
        self.RegistryEditButton = QtWidgets.QPushButton("Edit remote computer registry", self)
        self.RegistryEditButton.move(10, 300)
        self.RegistryEditButton.setFixedWidth(buttonwidth)

        # QuitButton
        self.QuitButton = QtWidgets.QPushButton("QUIT", self)
        self.QuitButton.move(buttonwidth + 20, 100)
        self.QuitButton.setFixedHeight(self.RegistryEditButton.geometry().y() + self.RegistryEditButton.height() - 100)

        # inputdebugger:
        self.Input = QtWidgets.QLineEdit(self)
        self.Input.move(10, 350)
        self.Input.setFixedWidth(buttonwidth)

        # outputdebugger
        self.OutputPanel = QtWidgets.QLabel('', self)
        self.OutputPanel.move(10, 390)
        self.OutputPanel.setFixedWidth(buttonwidth)
        self.OutputPanel.setFixedHeight(100)
        self.OutputPanel.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")

        # SendButton
        self.SendButton = QtWidgets.QPushButton('SEND', self)
        self.SendButton.move(buttonwidth + 20, 350)
        self.SendButton.setFixedHeight(140)

    @QtCore.Slot()
    def add_click_behavior(self, obj, func):
        obj.clicked.connect(func)

    def change_GUI_status(self, STATUS_CODE):
        if STATUS_CODE == self.Status_Code.CONNECTING:
            ConnectingString = ['Connecting', 'Connecting.', 'Connecting..', 'Connecting...']
            text = self.ConnectButton.text()
            index = 3
            if (text != 'Connect!'):
                index = ConnectingString.index(text)
            index = (index + 1) % 4
            self.ConnectButton.setText(ConnectingString[index])

        if STATUS_CODE == self.Status_Code.CONNECTED:
            self.ConnectButton.setText('Disconnect!')
            self.ConnectStatus.setText('CONNECTED!')
            self.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : green; }")

        if STATUS_CODE == self.Status_Code.DISCONNECT:
            self.ConnectButton.setText('Connect!')
            self.ConnectStatus.setText('DISCONNECTED!')
            self.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")

        if STATUS_CODE == self.Status_Code.TIMEOUT:
            self.ConnectButton.setText('Connect!')
            self.ConnectStatus.setText('TIMED OUT!')
            self.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : brown ; }")

    def showError(self, error='NO CONNECTIONS', message='Please connect to server first'):
        msg = QtWidgets.QMessageBox()
        msg.setFixedWidth(200)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(error)
        return msg

    class Status_Code(Enum):
        CONNECTED = auto(),
        DISCONNECT = auto(),
        CONNECTING = auto(),
        TIMEOUT = auto()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = client_window()
    window.show()

    sys.exit(app.exec_())
