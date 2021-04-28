import socket
import os
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging

logging.basicConfig(level=logging.DEBUG)

FEATURE_CODE = {
    'PING': '00',
    'ProcessRunning': '01',
    'AppRunning': '02',
    'Shutdown': '03',
    'Screenshot': '04',
    'Keystroke': '05',
    'RegistryEdit': '06',
}


class Registry_Dialog(QtWidgets.QDialog):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

        self.setWindowTitle('Registry')
        self.setFixedSize(400, 400)

        self.RegFileAddr = QtWidgets.QLineEdit(self)
        self.RegFileAddr.move(10, 20)
        self.RegFileAddr.setFixedWidth(260)

        self.RegFileContent = QtWidgets.QTextEdit(self)
        self.RegFileContent.move(10, 50)
        self.RegFileContent.setFixedSize(260, 110)

        self.BrowseRegFile = QtWidgets.QPushButton('Browse...', self)
        self.BrowseRegFile.move(280, 20)

        self.SendContent = QtWidgets.QPushButton('Send file content', self)
        self.SendContent.move(280, 50)
        self.SendContent.setFixedSize(110, 110)

        self.DirectModifyGr = QtWidgets.QGroupBox('Directly modify registry', self)
        self.DirectModifyGr.move(10, 170)
        self.DirectModifyGr.setFixedSize(380, 220)

        self.OpComboBox = QtWidgets.QComboBox(self.DirectModifyGr)
        self.OpComboBox.move(10, 20)
        self.OpComboBox.addItems(['Create key', 'Delete key', 'Get value', 'Set value', 'Delete value'])
        self.OpComboBox.setFixedWidth(360)

        self.Addr = QtWidgets.QLineEdit(self.DirectModifyGr)
        self.Addr.move(10, 50)
        self.Addr.setFixedWidth(360)
        self.Addr.setPlaceholderText('Enter full address of the registry key')

        self.ValueName = QtWidgets.QLineEdit(self.DirectModifyGr)
        self.ValueName.move(10, 80)
        self.ValueName.setFixedWidth(110)
        self.ValueName.setPlaceholderText('Name of key')

        self.Value = QtWidgets.QLineEdit(self.DirectModifyGr)
        self.Value.move(130, 80)
        self.Value.setFixedWidth(110)
        self.Value.setPlaceholderText('Value of key')

        self.ValueTypeComboBox = QtWidgets.QComboBox(self.DirectModifyGr)
        self.ValueTypeComboBox.move(250, 80)
        self.ValueTypeComboBox.addItems(['String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String'])
        self.ValueTypeComboBox.setFixedWidth(120)

        self.ReturnMessageBox = QtWidgets.QTextEdit(self.DirectModifyGr)
        self.ReturnMessageBox.move(10, 110)
        self.ReturnMessageBox.setFixedSize(360, 75)

        self.DirectSend = QtWidgets.QPushButton('Send', self.DirectModifyGr)
        self.DirectSend.move(80, 190)

        self.DirectDel = QtWidgets.QPushButton('Delete', self.DirectModifyGr)
        self.DirectDel.move(220, 190)

        self.ValueName.hide()
        self.Value.hide()
        self.ValueTypeComboBox.hide()

        self.BrowseRegFile.clicked.connect(self.click_browsebutton)
        self.SendContent.clicked.connect(self.click_sendcontent)
        self.OpComboBox.activated.connect(self.change_OpComboBox)
        self.DirectSend.clicked.connect(self.click_senddirect)
        self.DirectDel.clicked.connect(self.click_deldirect)

    def click_browsebutton(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', 'Registry files (*.reg)')
        file_name = file[0]
        self.RegFileAddr.setText(file_name)
        data = open(file_name, 'r')
        self.RegFileContent.setText(data.read())

    def click_sendcontent(self):
        message = FEATURE_CODE['RegistryEdit'] + 'regf' + '~' + self.RegFileContent.toPlainText()
        message = message.encode('utf-8')
        self.sock.sendall(message)


    def change_OpComboBox(self):
        current_op = self.OpComboBox.currentText()
        if current_op == 'Create key':
            self.ValueName.hide()
            self.Value.hide()
            self.ValueTypeComboBox.hide()
        elif current_op == 'Delete key':
            self.ValueName.hide()
            self.Value.hide()
            self.ValueTypeComboBox.hide()
        elif current_op == 'Get value':
            self.ValueName.show()
            self.Value.hide()
            self.ValueTypeComboBox.hide()
        elif current_op == 'Set value':
            self.ValueName.show()
            self.Value.show()
            self.ValueTypeComboBox.show()
        elif current_op == 'Delete value':
            self.ValueName.show()
            self.Value.hide()
            self.ValueTypeComboBox.hide()

    def click_senddirect(self):
        message = FEATURE_CODE['RegistryEdit'] + 'send' + '~' \
            + self.OpComboBox.currentText() + '~' + self.Addr.text() + '~' \
            + self.ValueName.text() + '~' + self.Value.text() + '~' + self.ValueTypeComboBox.currentText()
        self.sock.sendall(message.encode('utf8'))

        s = self.sock.recv(1024).decode('utf8')
        print(s)
        self.ReturnMessageBox.append(s)

    def click_deldirect(self):
        self.ReturnMessageBox.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Registry_Dialog()
    window.show()
    sys.exit(app.exec_())
