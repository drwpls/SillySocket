import client_gui
import client_connect
import sys
import threading
import time

client_connection = client_connect.Client_Connection()

def click_connectbutton(window):
    if (client_connection.connect_status == 0 or client_connection.connect_status == -2): # -2 = timeout
        client_connection.connect_status = -1  # Connecting status
        window.ConnectStatus.setText('DISCONNECT!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")
        host_str = str(window.IPTextBox.text())
        port_str = int(window.PortTextBox.text())   
        connection_thread = threading.Thread(target = client_connection.start_connect, args = (host_str, port_str))
        connection_thread.start()
        window.timer_update_GUI.start(500)
    elif (client_connection.connect_status == 1):
        client_connection.stop_connect()
        window.ConnectButton.setText('Connect!')
        window.ConnectStatus.setText('DISCONNECT!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")
        window.timer_update_GUI.stop()

def click_sentbutton(window):
    if not client_connection.connect_status:
        return -1
    message = str(window.Input.text())
    client_connection.send_message(message)

def UPDATE_GUI(window):
    if (client_connection.connect_status == -1): # Connecting-status
        # just change button text
        ConnectingString = ['Connecting', 'Connecting.', 'Connecting..', 'Connecting...']
        text = window.ConnectButton.text()
        index = 3
        if (text != 'Connect!'):
            index = ConnectingString.index(text)
        #index = ConnectingString.index(text)
        index = (index + 1) % 4
        window.ConnectButton.setText(ConnectingString[index])
    elif (client_connection.connect_status == -2):
        window.ConnectButton.setText('Connect!')
        window.ConnectStatus.setText('TIMEOUT!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : brown ; }")
    elif (client_connection.connect_status == 0):   # Disconnect-status\
        if (client_connection.lost_connect == True):
            client_connection.lost_connect = False
            server_address = str(client_connection.mainsock.getpeername()[0]) + ':' + str(client_connection.mainsock.getpeername()[1])
            errmsg = window.showError('Lost connection', ' from server: ' +  server_address)
            errmsg.exec_()
        window.ConnectButton.setText('Connect!')
        window.ConnectStatus.setText('DISCONNECT!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : red; }")
    elif (client_connection.connect_status == 1):               # in-connecting
        window.ConnectButton.setText('Disconnect!')
        window.ConnectStatus.setText('CONNECTED!')
        window.ConnectStatus.setStyleSheet("QLabel { border: 1.5px solid black;font-weight: bold; color : green; }")
        client_connection.send_message('0')

def onQuit():
    if client_connection.connect_status in [-1, 1]:
        client_connection.stop_connect()
    app.exit()
def connect_GUI_Feature(window):
    app.lastWindowClosed.connect(onQuit)
    window.add_Click_Behavior(window.ConnectButton,lambda: click_connectbutton(window))
    window.add_Click_Behavior(window.SentButton, lambda: click_sentbutton(window))
    window.timer_update_GUI.timeout.connect(lambda: UPDATE_GUI(window))

if __name__ == '__main__':
    app = client_gui.QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = client_gui.client_window()
    window.show()
    host_str = window.IPTextBox.text()
    #print(host_str)
    connect_GUI_Feature(window)
    sys.exit(app.exec_())