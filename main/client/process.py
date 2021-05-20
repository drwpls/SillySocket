import socket
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging
import io
import psutil
import operator
import signal
from FEATURE_CODE import FEATURE_CODE

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        else:
            return QtCore.QAbstractTableModel.headerData(self, col, orientation, role)
    def sort(self, col, order):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))

class Process_Dialog(QtWidgets.QDialog):
    def __init__(self, sock):
        super().__init__()
        self.setWindowTitle('Process')
        self.FEATURE_CODE = FEATURE_CODE['ProcessRunning']
        self.sock = sock     
        self.resize(400, 500)

        self.mainWidget = QtWidgets.QTableView(self)
        self.mainWidget.move(0, 0)
        self.mainWidget.setFixedSize(250, 500)
        self.mainWidget.setSortingEnabled(True)
        self.list_process_data = []

        self.ViewButton = QtWidgets.QPushButton('View', self)
        self.ViewButton.move(260, 10)
        self.ViewButton.setFixedWidth(120)
        
        self.KillButton = QtWidgets.QPushButton('Kill', self)
        self.KillButton.move(260, 40)
        self.KillButton.setFixedWidth(120)

        self.StartButton = QtWidgets.QPushButton('Start', self)
        self.StartButton.move(260, 70)
        self.StartButton.setFixedWidth(120)

        self.ClearButton = QtWidgets.QPushButton('Clear', self)
        self.ClearButton.move(260, 100)
        self.ClearButton.setFixedWidth(120)

        self.DirectModifyGr = QtWidgets.QGroupBox('Filter', self)
        self.DirectModifyGr.move(260, 180)
        self.DirectModifyGr.setFixedSize(140, 220)

        self.Label1 = QtWidgets.QLabel('Filter by:', self.DirectModifyGr)
        self.Label1.move(0, 20)

        self.ValueTypeComboBox = QtWidgets.QComboBox(self.DirectModifyGr)
        self.ValueTypeComboBox.move(0, 40)
        self.ValueTypeComboBox.addItems(['Name', 'PID'])
        self.ValueTypeComboBox.setFixedWidth(120)

        self.Label2 = QtWidgets.QLabel('Value:', self.DirectModifyGr)
        self.Label2.move(0, 70)

        self.filterTextbox = QtWidgets.QLineEdit('', self.DirectModifyGr)
        self.filterTextbox.move(0, 90)
        self.filterTextbox.setFixedWidth(120)

        self.filterButton = QtWidgets.QPushButton('Filter!', self.DirectModifyGr)
        self.filterButton.move(0, 130)
        self.filterButton.setFixedWidth(120)

        self.clearFilterButton = QtWidgets.QPushButton('Clear Filter', self.DirectModifyGr)
        self.clearFilterButton.move(0, 160)
        self.filterTextbox.setFixedWidth(120)

        self.ViewButton.clicked.connect(self.click_viewbutton)
        self.KillButton.clicked.connect(self.click_killprocess)
        self.StartButton.clicked.connect(self.click_startprocess)
        self.ClearButton.clicked.connect(self.click_clearprocess)
        self.filterButton.clicked.connect(self.click_filterbutton)
        self.clearFilterButton.clicked.connect(self.click_clearfilterbutton)

    def receive_list(self):
        message = ''
        data = self.sock.recv(512*1024).decode('utf-8')
        while data and data[-4:] != 'done':
            #logging.debug('data is {}'.format(data))
            message = message + str(data)
            data = self.sock.recv(512*1024).decode('utf-8')
        message = message + str(data[:-4])
        message = message.split('|')
        message = message[:-1]
        process_list = []
        for mess in message:
            name, pid = mess.split(',')
            pid = int(pid)
            process_list.append([name, pid])
        del message
        return process_list

    def get_process_list(self):
        self.list_process_data = []
        self.list_process_data_backup = []
        message = FEATURE_CODE['ProcessRunning'] + 'get__'
        self.sock.sendall(message.encode('utf-8'))
        self.list_process_data = self.receive_list()

    def set_data(self):
        header = ['Name', 'PID']
        model = TableModel(self, self.list_process_data, header)
        self.mainWidget.setModel(model)    
        self.mainWidget.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.mainWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def click_viewbutton(self):
        self.get_process_list()
        self.set_data()
        logging.debug('set done')

    def click_killprocess(self):
        index = self.mainWidget.selectedIndexes()
        if not index:
            logging.debug('No Process select')
        else:
            cell = index[0]
            row = cell.row()
            x = self.mainWidget.model().index(row, 1).data()
            message = FEATURE_CODE['ProcessRunning'] + 'kill_' + str(x)
            self.sock.sendall(message.encode('utf-8'))
            #self.click_viewbutton()

    def click_startprocess(self):
        process, ok = QtWidgets.QInputDialog.getText(self, 'Start', 'Enter process/application name:')
        if ok:
            message = FEATURE_CODE['ProcessRunning'] + 'start' + str(process)
            self.sock.sendall(message.encode('utf-8'))

    def click_clearprocess(self):
        self.mainWidget.model().deleteLater()

    def click_filterbutton(self):
        option = self.ValueTypeComboBox.currentText()
        value = self.filterTextbox.text()
        self.list_process_data_backup = self.list_process_data
        newlist = []
        if option == 'Name':
            for name, pid in self.list_process_data:
                if value in name:
                    newlist.append([name, pid])
        if option == 'PID':
            for name, pid in self.list_process_data:
                if value in str(pid):
                    newlist.append([name, pid]) 
        if not newlist:
            errbox = QtWidgets.QMessageBox(self)
            errbox.setText('not found')
            errbox.exec_()
        else:
            self.list_process_data = newlist 
            self.set_data()
                    
    def click_clearfilterbutton(self):
        self.list_process_data = self.list_process_data_backup 
        self.set_data()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Process_Dialog(0)
    #print(window.list_process_data)
    window.show()
    sys.exit(app.exec_())
