import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class server_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # create windows title and its size
        self.setWindowTitle("Server")      
        self.setFixedSize(100, 100)

        # ListenBox
        self.ListenBox = QtWidgets.QPushButton("Start Listen", self)
        self.ListenBox.move(10,10)
        self.ListenBox.setFixedSize(80, 80)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = server_window()
    window.show()

    sys.exit(app.exec_())