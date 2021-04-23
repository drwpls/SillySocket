import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging

logging.basicConfig(level=logging.DEBUG)

class Shutdown_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.timeout = 0

        self.setWindowTitle('Shutdown')      
        self.setFixedSize(220, 70)

        self.TimeoutDescription = QtWidgets.QLabel('Timeout in second:', self)
        self.TimeoutDescription.move(5, 5)

        self.TimeoutBox = QtWidgets.QLineEdit("", self)
        validator = QtGui.QIntValidator(0, 10000, self)
        self.TimeoutBox.setValidator(validator)
        self.TimeoutBox.move(10,30)
        self.TimeoutBox.setFixedWidth(100)

        self.ShutdownConfirmButton = QtWidgets.QPushButton('Shutdown', self)
        self.ShutdownConfirmButton.move(110, 30)

        self.ShutdownConfirmButton.setDefault(True)
        self.ShutdownConfirmButton.clicked.connect(self.click_shutdownconfirmbutton)
        #self.ShutdownConfirmButton.clicked.connect(self.accept)

    @QtCore.Slot()
    def click_shutdownconfirmbutton(self):
        logging.debug('Set return to Accepted')
        self.timeout = int('0' + self.TimeoutBox.text()) # Avoid blank input
        logging.debug(self.timeout)
        self.accept()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Shutdown_Dialog()
    window.show()
    sys.exit(app.exec_())
        