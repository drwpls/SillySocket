import client_gui
import client_connect
import sys
import threading
import shutdown
import logging

FEATURE_CODE = {
    'PING' : '00',
    'ProcessRunning' : '01',
    'AppRunning' : '02',
    'Shutdown' : '03',
    'ShotScreen' : '04',
    'KeyStroke' : '05',
    'RegistryEdit' : '06',
}

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
    if client_connection.connect_status != 1:
        # by default, showError will display NOCONNECTION error
        errmsg = window.showError()
        errmsg.exec_()
        return -1
    message = str(window.Input.text())
    client_connection.send_message(message)

def click_shutdownbutton(window):
    if client_connection.connect_status != 1:
        errmsg = window.showError()
        errmsg.exec_()
        return -1
    shutdown_dialog = shutdown.Shutdown_Dialog()
    dialog_result_code = shutdown_dialog.exec_()

    # debugging
    if dialog_result_code == shutdown_dialog.Accepted:
        # sent the command to server:
        client_connection.send_message(FEATURE_CODE['Shutdown'] + str(shutdown_dialog.timeout))
        logging.debug('Shutdown accepted!')
        logging.debug('Timeout is {}'.format(shutdown_dialog.timeout))
    # else, user cancel shutdown
    elif dialog_result_code == shutdown_dialog.Rejected:
        logging.debug('Shutdown rejected!')
    else:
        logging.debug('The result code is {}'.format(dialog_result_code))

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
        client_connection.send_message('00')

def onQuit():
    if client_connection.connect_status in [-1, 1]:
        client_connection.stop_connect()
    app.exit()
def connect_GUI_Feature(window):
    app.lastWindowClosed.connect(onQuit)
    window.timer_update_GUI.timeout.connect(lambda: UPDATE_GUI(window))
    window.add_Click_Behavior(window.ConnectButton,lambda: click_connectbutton(window))
    window.add_Click_Behavior(window.SentButton, lambda: click_sentbutton(window))
    window.add_Click_Behavior(window.ShutdownButton, lambda: click_shutdownbutton(window))

if __name__ == '__main__':
    app = client_gui.QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = client_gui.client_window()
    window.show()
    host_str = window.IPTextBox.text()
    #print(host_str)
    connect_GUI_Feature(window)
    sys.exit(app.exec_())