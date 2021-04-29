import socket
from PIL import Image, ImageGrab
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import logging
import io
import psutil
import win32process
import operator
import signal
import threading
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
        self.sock = sock     
        self.resize(400, 500)
        self.mainWidget = QtWidgets.QTableView(self)
        self.mainWidget.move(0, 0)
        self.mainWidget.setFixedSize(250, 500)
        self.mainWidget.setSortingEnabled(True)
        self.list_process_data = []

        self.ViewButton = QtWidgets.QPushButton('View Process', self)
        self.ViewButton.move(260, 10)
        self.ViewButton.setFixedWidth(120)
        
        self.KillButton = QtWidgets.QPushButton('Kill Process', self)
        self.KillButton.move(260, 40)
        self.KillButton.setFixedWidth(120)

        self.StartButton = QtWidgets.QPushButton('Start Process', self)
        self.StartButton.move(260, 70)
        self.StartButton.setFixedWidth(120)

        self.ClearButton = QtWidgets.QPushButton('Clear', self)
        self.ClearButton.move(260, 100)
        self.ClearButton.setFixedWidth(120)


        self.DirectModifyGr = QtWidgets.QGroupBox('Filter Process', self)
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


        self.ViewButton.clicked.connect(self.click_viewbutton)
        self.KillButton.clicked.connect(self.click_killprocess)
        self.StartButton.clicked.connect(self.click_startprocess)
        self.ClearButton.clicked.connect(self.click_clearprocess)
        self.filterButton.clicked.connect(self.click_filterbutton)
    def get_process_list(self):
        self.list_process_data = []
        self.list_process_data_backup = []
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                self.list_process_data.append([processName, processID])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    def set_data(self):
        header = ['Name', 'PID']
        model = TableModel(self, self.list_process_data, header)
        model.setHeaderData(0,QtCore.Qt.Horizontal, "Id", QtCore.Qt.DisplayRole)
        model.setHeaderData(1,QtCore.Qt.Horizontal, "Id")
        self.mainWidget.setModel(model)    

    
    def kill_proc_tree(self, pid, sig=signal.SIGTERM, include_parent=True,
                    timeout=None, on_terminate=None):
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
        for p in children:
            p.send_signal(sig)
        gone, alive = psutil.wait_procs(children, timeout=timeout,
                                        callback=on_terminate)
        return (gone, alive)

    def click_viewbutton(self):
        self.get_process_list()
        self.set_data()
        print(sys.getsizeof(self.list_process_data))

    def click_killprocess(self):
        index = self.mainWidget.selectedIndexes()
        if not index:
            print('No Process select')
        else:
            cell = index[0]
            row = cell.row()
            x = self.mainWidget.model().index(row, 1).data()
            logging.debug('Killing {}'.format(x))
            self.kill_proc_tree(pid = x)
            self.click_viewbutton()

    def click_startprocess(self):
        process, ok = QtWidgets.QInputDialog.getText(self, 'Start', 'Enter process/application name:')
        if ok:
            psutil.Popen(str(process))

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
            
            

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Process_Dialog(0)
    #print(window.list_process_data)
    window.show()
    sys.exit(app.exec_())
