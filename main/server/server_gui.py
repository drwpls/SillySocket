import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class server_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer_update_GUI = QtCore.QTimer()
        
        # create windows title and its size
        self.setWindowTitle("Server")      
        self.setFixedSize(260, 170)

        # ListenBox
        self.ListenBox = QtWidgets.QPushButton("Start listening", self)
        self.ListenBox.move(10,10)
        self.ListenBox.setFixedSize(240, 150)
    
    @QtCore.Slot()
    def add_Click_Behavior(self, obj, func):
        obj.clicked.connect(func)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = server_window()
    window.show()
    sys.exit(app.exec_())